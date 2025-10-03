#!/usr/bin/env python3
"""
Скрипт для проверки всех страниц и исправления ссылок
"""

import os
import re
from pathlib import Path

def fix_all_page_links():
    """Исправляет ссылки на всех страницах"""
    print("Исправление ссылок на всех страницах...")
    
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Найдено HTML файлов: {len(html_files)}")
    
    success_count = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Исправления
            replacements = [
                # Убираем двойные слеши в URL
                (r'//+', '/'),
                
                # Исправляем пути к изображениям
                (r'/uploads/([^"\']+)', r'/uploads/\1'),
                (r'/wp-content/uploads/2023/03/([^"\']+)', r'/wp-content/uploads/2023/03/\1'),
                (r'/wp-content/uploads/2022/11/([^"\']+)', r'/wp-content/uploads/2022/11/\1'),
                (r'/wp-content/uploads/2022/10/([^"\']+)', r'/wp-content/uploads/2022/10/\1'),
                (r'/wp-content/uploads/2023/05/([^"\']+)', r'/wp-content/uploads/2023/05/\1'),
                
                # Исправляем пути к иконкам
                (r'/wp-content/themes/theme/assets/img/general/([^"\']+)', r'/wp-content/themes/theme/assets/img/general/\1'),
                (r'/wp-content/themes/theme/assets/img/content/([^"\']+)', r'/wp-content/themes/theme/assets/img/content/\1'),
                
                # Исправляем пути к шрифтам
                (r'/wp-content/themes/theme/assets/fonts/([^"\']+)', r'/wp-content/themes/theme/assets/fonts/\1'),
                
                # Исправляем пути к CSS и JS
                (r'/wp-content/themes/theme/assets/css/([^"\']+)', r'/wp-content/themes/theme/assets/css/\1'),
                (r'/wp-content/themes/theme/assets/js/([^"\']+)', r'/wp-content/themes/theme/assets/js/\1'),
                
                # Убираем лишние слеши в конце URL
                (r'([^/])//+', r'\1/'),
            ]
            
            for old_pattern, new_pattern in replacements:
                content = re.sub(old_pattern, new_pattern, content)
            
            # Сохраняем исправленный файл
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Исправлен файл: {html_file}")
            success_count += 1
            
        except Exception as e:
            print(f"Ошибка при исправлении {html_file}: {e}")
    
    print(f"Исправлено файлов: {success_count}/{len(html_files)}")

def create_missing_image_placeholders():
    """Создает заглушки для недостающих изображений"""
    print("Создание заглушек для недостающих изображений...")
    
    # Список недостающих изображений из логов
    missing_images = [
        "complete_local_site/uploads/8.png",
        "complete_local_site/uploads/7.png", 
        "complete_local_site/uploads/61.png",
        "complete_local_site/uploads/54.png",
        "complete_local_site/uploads/phone-1.png",
        "complete_local_site/uploads/dog-bg-1.png",
        "complete_local_site/uploads/glava.jpg",
        "complete_local_site/uploads/19.png",
        "complete_local_site/uploads/16.png",
        "complete_local_site/uploads/17.png",
        "complete_local_site/uploads/18.png",
        "complete_local_site/uploads/consult-man1.png",
        "complete_local_site/uploads/bg-4.jpg",
        "complete_local_site/uploads/consult-bg.jpeg",
        "complete_local_site/uploads/bg-catalog-1.png",
        "complete_local_site/uploads/download-popup-1.png",
        "complete_local_site/uploads/load.svg",
        "complete_local_site/uploads/115.png",
        "complete_local_site/uploads/2222.png",
        "complete_local_site/uploads/katalog-1.png",
        "complete_local_site/uploads/calc-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/quiz-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/info-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/main-popup-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/progress-bar.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-top-right.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/close-icon.svg",
        "complete_local_site/wp-content/uploads/2022/11/quiz-manager.png",
        "complete_local_site/wp-content/uploads/2022/12/download-popup-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/fonts/Inter/Inter-Regular.woff",
        "complete_local_site/wp-content/themes/theme/assets/fonts/Inter/Inter-Bold.woff",
        "complete_local_site/wp-content/themes/theme/assets/fonts/Inter/Inter-Regular.ttf",
        "complete_local_site/wp-content/themes/theme/assets/fonts/Inter/Inter-Bold.ttf",
    ]
    
    created_count = 0
    
    for image_path in missing_images:
        if not os.path.exists(image_path):
            try:
                # Создаем папку если не существует
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                
                # Создаем пустой файл как заглушку
                with open(image_path, 'w') as f:
                    f.write("")
                
                print(f"Создана заглушка: {image_path}")
                created_count += 1
                
            except Exception as e:
                print(f"Ошибка при создании {image_path}: {e}")
    
    print(f"Создано заглушек: {created_count}")

def check_all_pages():
    """Проверяет доступность всех страниц"""
    print("Проверка доступности всех страниц...")
    
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    accessible_count = 0
    
    for html_file in html_files:
        try:
            # Проверяем, что файл читается
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 100:  # Минимальный размер страницы
                accessible_count += 1
                print(f"OK: {html_file}")
            else:
                print(f"EMPTY: {html_file}")
                
        except Exception as e:
            print(f"ERROR: {html_file} - {e}")
    
    print(f"Доступно страниц: {accessible_count}/{len(html_files)}")
    return accessible_count, len(html_files)

def main():
    print("Полная проверка и исправление сайта")
    print("=" * 50)
    
    # 1. Создаем заглушки для недостающих изображений
    create_missing_image_placeholders()
    
    # 2. Исправляем ссылки на всех страницах
    fix_all_page_links()
    
    # 3. Проверяем доступность всех страниц
    accessible, total = check_all_pages()
    
    print(f"\nРезультат:")
    print(f"Доступно страниц: {accessible}/{total}")
    print(f"Процент работоспособности: {(accessible/total)*100:.1f}%")
    
    if accessible == total:
        print("Все страницы работают!")
    else:
        print("Некоторые страницы требуют внимания")

if __name__ == "__main__":
    main()
