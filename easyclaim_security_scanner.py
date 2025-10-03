#!/usr/bin/env python3
"""
Комплексный сканер безопасности для доменов easyclaim.ru
Сканирует все основные домены и поддомены системы EasyClaim
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Импортируем наш расширенный сканер
from enhanced_security_scanner import EnhancedSecurityScanner

class EasyClaimSecurityAnalyzer:
    def __init__(self):
        self.domains = [
            'https://easyclaim.ru',
            'https://www.easyclaim.ru',
            'https://app.easyclaim.ru',
            'https://api.easyclaim.ru'
        ]
        
        self.results = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'scanner_version': '2.0',
                'domains_scanned': [],
                'total_domains': len(self.domains)
            },
            'domain_results': {},
            'summary': {
                'total_vulnerabilities': 0,
                'critical_issues': 0,
                'high_issues': 0,
                'medium_issues': 0,
                'low_issues': 0,
                'domains_with_issues': 0
            }
        }
        
    def log(self, message, level="INFO"):
        """Логирование"""
        timestamp = time.strftime("%H:%M:%S")
        colors = {
            "INFO": "📄",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🔴"
        }
        icon = colors.get(level, "📄")
        print(f"[{timestamp}] {icon} {level}: {message}")
        
    def scan_domain(self, domain_url):
        """Сканирование одного домена"""
        self.log(f"🔍 Начинаем сканирование {domain_url}", "INFO")
        
        scanner = EnhancedSecurityScanner(domain_url, delay=1.0)
        
        try:
            scanner.run_comprehensive_scan()
            results = scanner.results
            
            # Добавляем домен в список найденных
            self.results['scan_info']['domains_scanned'].append(domain_url)
            
            # Сохраняем результаты домена
            self.results['domain_results'][domain_url] = results
            
            # Подсчитываем уязвимости
            domain_vulnerabilities = self.count_vulnerabilities(results)
            
            self.log(f"✅ Сканирование {domain_url} завершено", "SUCCESS")
            self.log(f"📊 Найдено уязвимостей: {domain_vulnerabilities['total']}", "INFO")
            
            return domain_vulnerabilities
            
        except Exception as e:
            self.log(f"❌ Ошибка сканирования {domain_url}: {e}", "ERROR")
            self.results['domain_results'][domain_url] = {'error': str(e)}
            return {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            
    def count_vulnerabilities(self, results):
        """Подсчет уязвимостей в результатах"""
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        # Подсчитываем проблемы по категориям
        for category, items in results.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'severity' in item:
                        sev = item['severity']
                        if sev in severity_counts:
                            severity_counts[sev] += 1
            elif isinstance(items, dict):
                if 'severity' in items:
                    sev = items['severity']
                    if sev in severity_counts:
                        severity_counts[sev] += 1
                        
        return {
            'total': sum(severity_counts.values()),
            'critical': severity_counts['CRITICAL'],
            'high': severity_counts['HIGH'],
            'medium': severity_counts['MEDIUM'],
            'low': severity_counts['LOW']
        }
        
    def scan_all_domains(self):
        """Сканирование всех доменов"""
        self.log("🚀 Запуск комплексного сканирования безопасности EasyClaim", "INFO")
        print("=" * 80)
        print("🔐 СИСТЕМА КОМПЛЕКСНОГО АНАЛИЗА БЕЗОПАСНОСТИ EasyClaim.ru")
        print("=" * 80)
        print(f"📅 Дата сканирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Доменов для сканирования: {len(self.domains)}")
        print(f"🌐 Домены:")
        for i, domain in enumerate(self.domains, 1):
            print(f"   {i}. {domain}")
        print("=" * 80)
        
        start_time = time.time()
        
        for i, domain in enumerate(self.domains, 1):
            self.log(f"📊 Прогресс: {i}/{len(self.domains)} - {domain}", "INFO")
            
            vulnerabilities = self.scan_domain(domain)
            
            # Обновляем общую статистику
            self.results['summary']['total_vulnerabilities'] += vulnerabilities['total']
            self.results['summary']['critical_issues'] += vulnerabilities['critical']
            self.results['summary']['high_issues'] += vulnerabilities['high']
            self.results['summary']['medium_issues'] += vulnerabilities['medium']
            self.results['summary']['low_issues'] += vulnerabilities['low']
            
            if vulnerabilities['total'] > 0:
                self.results['summary']['domains_with_issues'] += 1
                
            # Пауза между доменами
            if i < len(self.domains):
                self.log(f"⏸️  Пауза между сканированиями (5 сек)...", "INFO")
                time.sleep(5)
                
        end_time = time.time()
        total_duration = end_time - start_time
        
        self.log(f"✅ Комплексное сканирование завершено за {total_duration:.2f} секунд", "SUCCESS")
        
    def generate_markdown_report(self):
        """Генерация отчета в формате Markdown"""
        report_content = self._create_markdown_report()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'easyclaim_security_report_{timestamp}.md'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        self.log(f"📄 Markdown отчет сохранен: {filename}", "SUCCESS")
        return filename
        
    def _create_markdown_report(self):
        """Создание содержимого Markdown отчета"""
        content = f"""# 🔐 Отчет по анализу безопасности EasyClaim.ru

## 📋 Сводка сканирования

| Параметр | Значение |
|----------|----------|
| **Дата сканирования** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **Версия сканера** | 2.0 |
| **Доменов просканировано** | {len(self.results['domain_results'])}/{len(self.domains)} |
| **Общее количество уязвимостей** | {self.results['summary']['total_vulnerabilities']} |
| **Доменов с уязвимостями** | {self.results['summary']['domains_with_issues']} |

## 🚨 Статистика по критичности

| Уровень риска | Количество | Цвет индикатор |
|---------------|------------|---------------|
| 🔴 **Критические** | {self.results['summary']['critical_issues']} | Требуют немедленного исправления |
| 🟠 **Высокие** | {self.results['summary']['high_issues']} | Приоритетные для исправления |
| 🟡 **Средние** | {self.results['summary']['medium_issues']} | Рекомендуется исправить |
| 🔵 **Низкие** | {self.results['summary']['low_issues']} | Можно исправить в плановом порядке |

## 🌐 Результаты по доменам

"""
        
        for domain_url in self.domains:
            domain_results = self.results['domain_results'].get(domain_url, {})
            
            if 'error' in domain_results:
                content += f"""### ❌ {domain_url} - ОШИБКА СКАНИРОВАНИЯ

```
{domain_results['error']}
```

"""
                continue
                
            vulnerabilites = self.count_vulnerabilities(domain_results)
            
            # Информация о домене
            basic_info = domain_results.get('basic_info', {})
            
            content += f"""### 🌍 {domain_url}

| Параметр | Значение |
|----------|----------|
| **Статус** | {basic_info.get('status_code', 'Не определен')} |
| **Сервер** | {basic_info.get('server', 'Не определен')} |
| **IP адрес** | {basic_info.get('ip_address', 'Не определен')} |
| **Заголовок сайта** | {basic_info.get('title', 'Не определен')} |
| **Общее количество проблем** | {vulnerabilites['total']} |

#### 🚨 Найденные уязвимости

"""
            
            if vulnerabilites['total'] == 0:
                content += "✅ **Проблем безопасности не найдено**\n"
            else:
                if vulnerabilites['critical'] > 0:
                    content += f"🔴 **Критические**: {vulnerabilites['critical']}\n"
                if vulnerabilites['high'] > 0:
                    content += f"🟠 **Высокие**: {vulnerabilites['high']}\n"
                if vulnerabilites['medium'] > 0:
                    content += f"🟡 **Средние**: {vulnerabilites['medium']}\n"
                if vulnerabilites['low'] > 0:
                    content += f"🔵 **Низкие**: {vulnerabilites['low']}\n"
            
            content += "\n#### 📊 Детальные результаты\n\n"

            # SQL Injection
            sql_injections = domain_results.get('sql_injection', [])
            if sql_injections:
                content += "##### 🔍 SQL Injection\n\n"
                for injection in sql_injections[:3]:  # Показываем первые 3
                    content += f"- **URL**: `{injection['url']}`\n"
                    content += f"  - Payload: `{injection['payload'][:50]}...`\n"
                    content += f"  - Детектирован паттерн: `{injection['error_pattern']}`\n\n"
                
            # XSS
            xss_vulns = domain_results.get('xss_vulnerabilities', [])
            if xss_vulns:
                content += "##### ⚡ XSS уязвимости\n\n"
                for xss in xss_vulns[:3]:
                    content += f"- **URL**: `{xss['url']}`\n"
                    content += f"  - Параметр: `{xss['parameter']}`\n"
                    content += f"  - Payload: `{xss['payload'][:50]}...`\n\n"
                    
            # Directory Listing
            dir_listing = domain_results.get('directory_listing', [])
            if dir_listing:
                content += "##### 📁 Directory Listing\n\n"
                for listing in dir_listing[:3]:
                    content += f"- **URL**: `{listing['url']}`\n"
                    content += f"  - Размер контента: {listing['content_length']} байт\n\n"
                    
            # Sensitive Files
            sensitive_files = domain_results.get('sensitive_files', [])
            if sensitive_files:
                content += "##### 🔐 Чувствительные файлы\n\n"
                for file_info in sensitive_files[:3]:
                    content += f"- **URL**: `{file_info['url']}`\n"
                    content += f"  - Размер: {file_info['content_length']} байт\n"
                    content += f"  - Содержит чувствительные данные: {'Да' if file_info.get('has_sensitive_data') else 'Нет'}\n\n"
                    
            # Admin Panels
            admin_panels = domain_results.get('admin_panels', [])
            if admin_panels:
                content += "##### 👑 Административные панели\n\n"
                for panel in admin_panels:
                    content += f"- **URL**: `{panel['url']}`\n"
                    content += f"  - Статус: {panel['status_code']}\n"
                    content += f"  - Заголовок: {panel.get('title', 'Не определен')}\n"
                    content += f"  - Логин форма: {'Да' if panel.get('has_login_form') else 'Нет'}\n\n"
                    
            # Security Headers
            headers = domain_results.get('headers_security', {})
            if headers:
                content += "##### 🛡️ Заголовки безопасности\n\n"
                missing_headers = headers.get('missing_headers', [])
                if missing_headers:
                    content += "**Отсутствующие заголовки:**\n"
                    for header in missing_headers:
                        content += f"- `{header}`\n"
                    content += "\n"
                else:
                    content += "✅ Все основные заголовки безопасности присутны\n\n"
                    
            # API Endpoints
            api_endpoints = domain_results.get('exposed_endpoints', [])
            if api_endpoints:
                content += "##### 🔌 API Endpoints\n\n"
                for endpoint in api_endpoints[:3]:
                    content += f"- **URL**: `{endpoint['url']}`\n"
                    content += f"  - Статус: {endpoint['status_code']}\n"
                    content += f"  - Content-Type: `{endpoint['content_type']}`\n"
                    content += f"  - Методы: {', '.join(endpoint.get('methods_tested', []))}\n\n"
                    
            # Configuration Issues
            config_issues = domain_results.get('configuration_issues', [])
            if config_issues:
                content += "##### ⚙️ Проблемы конфигурации\n\n"
                for issue in config_issues[:3]:
                    content += f"- **Тип**: {issue['type']}\n"
                    content += f"  - Проблема: {issue.get('issue', 'Не указано')}\n"
                    content += f"  - Текущее значение: `{issue.get('current_value', 'Не указано')}`\n\n"
                    
            content += "---\n\n"
        
        # Рекомендации
        content += """## 🛡️ Рекомендации по улучшению безопасности

### Приоритет 1 - Критические проблемы
"""
        
        if self.results['summary']['critical_issues'] > 0:
            content += """1. **Немедленно исправить критические уязвимости**
   - Патрулировать все найденные критические проблемы
   - Приостановить работу затронутых сервисов до исправления
   - Провести дополнительное тестирование после исправлений

2. **SQL Injection (если обнаружено)**
   - Использовать подготовленные запросы (prepared statements)
   - Валидировать и санитизировать все пользовательские входы
   - Внедрить принцип наименьших привилегий для БД

3. **Проблемы с аутентификацией**
   - Восстановить доступ к административным панелям
   - Установить комплексные пароли
   - Внедрить многофакторную аутентификацию

"""
        else:
            content += "- ✅ Критических уязвимостей не обнаружено\n\n"

        content += """### Приоритет 2 - Высокие риски

1. **Защита административных панелей**
   - Ограничить доступ по IP адресам
   - Внедрить strong authentication
   - Настроить мониторинг попыток доступа

2. **Защита чувствительных файлов**
   - Удалить или защитить конфигурационные файлы
   - Скрыть бэкапы от веб-доступа
   - Обеспечить доступ только через SSH/SFTP

3. **Directory listing**
   - Отключить отображение содержимого каталогов
   - Добавить index файлы в пустые директории
   - Настроить запрет .htaccess

### Приоритет 3 - Средние риски

1. **Заголовки безопасности**
   ```apache
   # Apache .htaccess
   Header always set X-Content-Type-Options nosniff
   Header always set X-Frame-Options DENY
   Header always set X-XSS-Protection "1; mode=block"
   Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
   Header always set Content-Security-Policy "default-src 'self'"
   ```

2. **Загрузка файлов**
   - Валидировать типы и содержимое файлов
   - Хранить файлы вне веб-директории
   - Переименовывать загруженные файлы
   - Сканировать на вирусы

### Приоритет 4 - Рекомендации

1. **Настройка SSL/TLS**
   - Перейти на HTTPS для всех доменов
   - Настроить HSTS заголовок
   - Обновить сертификаты до актуальных версий

2. **Мониторинг**
   - Внедрить систему мониторинга безопасности
   - Настроить логирование и алерты
   - Регулярно проводить сканирования

3. **Backup стратегия**
   - Создать резервные копии перед исправлениями
   - Внедрить автоматический бэкап
   - Протестировать процедуры восстановления

## 📊 Техническая информация

### Используемые технологии (по доменам)

"""
        
        for domain_url in self.domains:
            domain_results = self.results['domain_results'].get(domain_url, {})
            tech_info = domain_results.get('technology_identification', {})
            
            if tech_info:
                content += f"#### {domain_url}\n\n"
                for category, technologies in tech_info.items():
                    if technologies:
                        content += f"- **{category}**: {', '.join(technologies)}\n"
                content += "\n"

        content += f"""## 📝 Информация о сканировании

- **Дата создания отчета**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Версия сканера**: 2.0
- **Автоматически сгенерированный отчет**

---
*Этот отчет создан с помощью расширенного сканера безопасности. Для получения дополнительной информации или проведения повторного сканирования обратитесь к администратору безопасности.*

"""
        
        return content
        
    def save_json_results(self, filename='easyclaim_security_results.json'):
        """Сохранение результатов в JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        self.log(f"📄 JSON результаты сохранены: {filename}", "SUCCESS")
        return filename

def main():
    print("🔐 EasyClaim.ru - Комплексный анализ безопасности")
    print("⚠️  ВНИМАНИЕ: Сканирование проводится только для целей тестирования собственной безопасности!")
    print("=" * 80)
    
    analyzer = EasyClaimSecurityAnalyzer()
    
    try:
        # Запускаем сканирование всех доменов
        analyzer.scan_all_domains()
        
        # Сохраняем результаты
        json_file = analyzer.save_json_results()
        
        # Генерируем Markdown отчет
        md_file = analyzer.generate_markdown_report()
        
        # Выводим итоговую сводку
        analyzer.log("📊 СКАНИРОВАНИЕ ЗАВЕРШЕНО", "SUCCESS")
        print("\n" + "="*80)
        print("🎯 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
        print("="*80)
        
        print(f"✅ Доменов просканировано: {len(analyzer.results['domain_results'])}/{len(analyzer.domains)}")
        print(f"📊 Всего найдено проблем: {analyzer.results['summary']['total_vulnerabilities']}")
        print(f"🔴 Критических: {analyzer.results['summary']['critical_issues']}")
        print(f"🟠 Высоких: {analyzer.results['summary']['high_issues']}")
        print(f"🟡 Средних: {analyzer.results['summary']['medium_issues']}")
        print(f"🔵 Низких: {analyzer.results['summary']['low_issues']}")
        print(f"🌐 Доменов с проблемами: {analyzer.results['summary']['domains_with_issues']}")
        
        print(f"\n📄 Файлы отчета:")
        print(f"   📊 JSON данные: {json_file}")
        print(f"   📝 Markdown отчет: {md_file}")
        
        if analyzer.results['summary']['total_vulnerabilities'] == 0:
            print(f"\n🎉 ОТЛИЧНО! Серьезных проблем безопасности не найдено!")
        else:
            print(f"\n⚠️  Найдены проблемы безопасности - требуются меры по их устранению")
            
    except KeyboardInterrupt:
        print("\n❌ Сканирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
