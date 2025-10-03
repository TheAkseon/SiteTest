#!/usr/bin/env python3
"""
Главный скрипт для анализа безопасности и извлечения шаблонов
Объединяет функционал сканера уязвимостей и извлечения шаблонов
"""

import argparse
import sys
import time
from pathlib import Path

# Импортируем наши модули
from vulnerability_scanner import VulnerabilityScanner
from template_extractor import TemplateExtractor

class SecurityAnalyzer:
    def __init__(self, base_url, delay=1.0):
        self.base_url = base_url
        self.delay = delay
        self.scanner = VulnerabilityScanner(base_url, delay)
        self.extractor = TemplateExtractor(base_url)
        
    def log(self, message, level="INFO"):
        """Логирование"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_full_analysis(self):
        """Запуск полного анализа безопасности"""
        self.log("🔍 Начинаем полный анализ безопасности")
        
        # Этап 1: Сканирование уязвимостей
        self.log("Этап 1: Сканирование уязвимостей")
        self.scanner.run_full_scan()
        
        # Этап 2: Извлечение шаблонов
        self.log("Этап 2: Извлечение шаблонов")
        extracted_files = self.extractor.run_extraction()
        
        # Этап 3: Анализ результатов
        self.log("Этап 3: Анализ результатов")
        self.analyze_results()
        
        return {
            'vulnerabilities': self.scanner.results,
            'extracted_files': extracted_files
        }
        
    def analyze_results(self):
        """Анализ результатов сканирования"""
        self.log("Анализ результатов...")
        
        vulnerabilities = self.scanner.results
        
        # Подсчет критичности
        critical_count = len(vulnerabilities['path_traversal']) + len(vulnerabilities['directory_listing'])
        high_count = len(vulnerabilities['admin_panels']) + len(vulnerabilities['sensitive_files'])
        medium_count = len(vulnerabilities['template_files'])
        
        print("\n" + "="*60)
        print("АНАЛИЗ БЕЗОПАСНОСТИ")
        print("="*60)
        
        print(f"🔴 КРИТИЧЕСКИЕ: {critical_count}")
        print(f"🟠 ВЫСОКИЕ: {high_count}")
        print(f"🟡 СРЕДНИЕ: {medium_count}")
        
        # Рекомендации по безопасности
        print("\n🛡️ РЕКОМЕНДАЦИИ ПО БЕЗОПАСНОСТИ:")
        
        if critical_count > 0:
            print("  ⚠️  НЕМЕДЛЕННО устраните критические уязвимости!")
            print("     - Отключите directory listing")
            print("     - Исправьте path traversal уязвимости")
            
        if high_count > 0:
            print("  🔒 Ограничьте доступ к административным панелям")
            print("     - Используйте сильные пароли")
            print("     - Настройте двухфакторную аутентификацию")
            
        if medium_count > 0:
            print("  📁 Проверьте доступность файлов шаблонов")
            print("     - Убедитесь, что они не содержат чувствительной информации")
            
        # Общие рекомендации
        print("\n📋 ОБЩИЕ РЕКОМЕНДАЦИИ:")
        print("  - Регулярно обновляйте CMS и плагины")
        print("  - Используйте HTTPS для всех соединений")
        print("  - Настройте WAF (Web Application Firewall)")
        print("  - Проводите регулярные аудиты безопасности")
        print("  - Создавайте резервные копии")
        
    def save_complete_report(self, results, filename='security_report.json'):
        """Сохранение полного отчета"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'target_url': self.base_url,
            'vulnerabilities': results['vulnerabilities'],
            'extracted_files': results['extracted_files'],
            'summary': {
                'total_vulnerabilities': sum(len(v) for v in results['vulnerabilities'].values() if isinstance(v, list)),
                'total_files_extracted': len(results['extracted_files']),
                'critical_issues': len(results['vulnerabilities']['path_traversal']) + len(results['vulnerabilities']['directory_listing'])
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        self.log(f"Полный отчет сохранен в {filename}")

def main():
    parser = argparse.ArgumentParser(
        description='Комплексный анализ безопасности сайта',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Базовое сканирование
  python security_analyzer.py --url https://100200.ru

  # Сканирование с задержкой
  python security_analyzer.py --url https://100200.ru --delay 2.0

  # Только сканирование уязвимостей
  python security_analyzer.py --url https://100200.ru --scan-only

  # Только извлечение шаблонов
  python security_analyzer.py --url https://100200.ru --extract-only

⚠️  ВНИМАНИЕ: Используйте только на собственных сайтах!
        """
    )
    
    parser.add_argument('--url', default='https://100200.ru', 
                       help='URL для анализа (по умолчанию: https://100200.ru)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Задержка между запросами в секундах (по умолчанию: 1.0)')
    parser.add_argument('--scan-only', action='store_true',
                       help='Выполнить только сканирование уязвимостей')
    parser.add_argument('--extract-only', action='store_true',
                       help='Выполнить только извлечение шаблонов')
    parser.add_argument('--output', default='security_report.json',
                       help='Файл для сохранения отчета (по умолчанию: security_report.json)')
    
    args = parser.parse_args()
    
    print("🔐 Комплексный анализатор безопасности сайта")
    print("⚠️  ВНИМАНИЕ: Используйте только на собственных сайтах!")
    print(f"🎯 Цель: {args.url}")
    print(f"⏱️  Задержка: {args.delay} сек")
    print("-" * 60)
    
    analyzer = SecurityAnalyzer(args.url, args.delay)
    
    try:
        if args.scan_only:
            print("🔍 Режим: только сканирование уязвимостей")
            analyzer.scanner.run_full_scan()
            analyzer.scanner.print_summary()
            analyzer.scanner.save_results('vulnerability_scan.json')
            
        elif args.extract_only:
            print("📁 Режим: только извлечение шаблонов")
            extracted_files = analyzer.extractor.run_extraction()
            analyzer.extractor.print_summary(extracted_files)
            
        else:
            print("🔐 Режим: полный анализ безопасности")
            results = analyzer.run_full_analysis()
            analyzer.save_complete_report(results, args.output)
            
    except KeyboardInterrupt:
        print("\n❌ Анализ прерван пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
        
    print("\n✅ Анализ завершен успешно!")

if __name__ == "__main__":
    main()
