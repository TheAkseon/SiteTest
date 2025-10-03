#!/usr/bin/env python3
"""
Финальная проверка всех ссылок и изображений
"""

import os
import re
from pathlib import Path

def check_all_image_links():
    """Проверяет все ссылки на изображения в HTML файлах"""
    print("Проверка всех ссылок на изображения...")
    
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    missing_images = []
    found_images = []
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ищем все ссылки на изображения
            img_patterns = [
                r'src="([^"]+\.(?:png|jpg|jpeg|gif|svg|webp))"',
                r"src='([^']+\.(?:png|jpg|jpeg|gif|svg|webp))'",
                r'url\(["\']?([^"\']+\.(?:png|jpg|jpeg|gif|svg|webp))["\']?\)',
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # Очищаем путь от параметров
                    clean_path = match.split('?')[0].split('#')[0]
                    
                    # Определяем локальный путь
                    if clean_path.startswith('/'):
                        local_path = f"complete_local_site{clean_path}"
                    else:
                        local_path = f"complete_local_site/{clean_path}"
                    
                    if os.path.exists(local_path):
                        found_images.append(local_path)
                    else:
                        missing_images.append((html_file, clean_path, local_path))
            
        except Exception as e:
            print(f"Ошибка при обработке {html_file}: {e}")
    
    print(f"Найдено изображений: {len(found_images)}")
    print(f"Недостающих изображений: {len(missing_images)}")
    
    if missing_images:
        print("\nНедостающие изображения:")
        for html_file, clean_path, local_path in missing_images[:10]:  # Показываем первые 10
            print(f"  {clean_path} -> {local_path}")
        if len(missing_images) > 10:
            print(f"  ... и еще {len(missing_images) - 10}")
    
    return len(missing_images) == 0

def check_all_page_links():
    """Проверяет все внутренние ссылки между страницами"""
    print("Проверка внутренних ссылок...")
    
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    broken_links = []
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ищем все внутренние ссылки
            link_patterns = [
                r'href="([^"]+)"',
                r"href='([^']+)'",
            ]
            
            for pattern in link_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # Пропускаем внешние ссылки
                    if match.startswith('http') or match.startswith('mailto:') or match.startswith('tel:'):
                        continue
                    
                    # Очищаем путь
                    clean_path = match.split('?')[0].split('#')[0]
                    
                    if clean_path.startswith('/'):
                        clean_path = clean_path[1:]
                    
                    # Определяем локальный путь
                    if clean_path == '' or clean_path.endswith('/'):
                        local_path = f"complete_local_site/{clean_path}index.html"
                    else:
                        local_path = f"complete_local_site/{clean_path}"
                    
                    if not os.path.exists(local_path):
                        broken_links.append((html_file, match, local_path))
            
        except Exception as e:
            print(f"Ошибка при обработке {html_file}: {e}")
    
    print(f"Найдено внутренних ссылок")
    print(f"Недостающих страниц: {len(broken_links)}")
    
    if broken_links:
        print("\nНедостающие страницы:")
        for html_file, link, local_path in broken_links[:10]:  # Показываем первые 10
            print(f"  {link} -> {local_path}")
        if len(broken_links) > 10:
            print(f"  ... и еще {len(broken_links) - 10}")
    
    return len(broken_links) == 0

def create_final_report():
    """Создает финальный отчет о состоянии сайта"""
    print("Создание финального отчета...")
    
    # Подсчитываем файлы
    html_count = 0
    css_count = 0
    js_count = 0
    image_count = 0
    
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_count += 1
            elif file.endswith('.css'):
                css_count += 1
            elif file.endswith('.js'):
                js_count += 1
            elif file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                image_count += 1
    
    report = f"""
ФИНАЛЬНЫЙ ОТЧЕТ О СОСТОЯНИИ САЙТА
=====================================

Файлы:
- HTML страниц: {html_count}
- CSS файлов: {css_count}
- JS файлов: {js_count}
- Изображений: {image_count}

Проверки:
- Изображения: {'OK' if check_all_image_links() else 'ЕСТЬ ПРОБЛЕМЫ'}
- Внутренние ссылки: {'OK' if check_all_page_links() else 'ЕСТЬ ПРОБЛЕМЫ'}

Структура сайта:
complete_local_site/
├── index.html (главная)
├── services/ (услуги)
├── catalog/ (каталог)
├── portfolios/ (портфолио)
├── blog/ (блог)
├── contacts/ (контакты)
├── uploads/ (изображения)
└── wp-content/ (стили и скрипты)

Для запуска сайта:
python start_server.py

Сайт будет доступен по адресу: http://localhost:8000
"""
    
    with open("complete_local_site/SITE_REPORT.txt", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Отчет сохранен в complete_local_site/SITE_REPORT.txt")

def main():
    print("Финальная проверка сайта")
    print("=" * 30)
    
    # Проверяем изображения
    images_ok = check_all_image_links()
    
    # Проверяем внутренние ссылки
    links_ok = check_all_page_links()
    
    # Создаем отчет
    create_final_report()
    
    print(f"\nРезультат:")
    print(f"Изображения: {'OK' if images_ok else 'ЕСТЬ ПРОБЛЕМЫ'}")
    print(f"Ссылки: {'OK' if links_ok else 'ЕСТЬ ПРОБЛЕМЫ'}")
    
    if images_ok and links_ok:
        print("Сайт готов к использованию!")
    else:
        print("Требуется дополнительная настройка")

if __name__ == "__main__":
    main()
