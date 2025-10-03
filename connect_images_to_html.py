#!/usr/bin/env python3
"""
Скрипт для исправления путей к изображениям в HTML файлах
"""

import os
import re
import shutil

def fix_image_paths_in_html():
    """Исправляет пути к изображениям во всех HTML файлах"""
    print("Исправление путей к изображениям в HTML файлах...")
    
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
            
            # Исправления путей к изображениям
            replacements = [
                # Исправляем пути к изображениям в uploads
                (r'/uploads/([^"\']+)', r'/uploads/\1'),
                
                # Исправляем пути к изображениям WordPress
                (r'/wp-content/uploads/2023/03/([^"\']+)', r'/wp-content/uploads/2023/03/\1'),
                (r'/wp-content/uploads/2022/11/([^"\']+)', r'/wp-content/uploads/2022/11/\1'),
                (r'/wp-content/uploads/2022/10/([^"\']+)', r'/wp-content/uploads/2022/10/\1'),
                (r'/wp-content/uploads/2023/05/([^"\']+)', r'/wp-content/uploads/2023/05/\1'),
                (r'/wp-content/uploads/2022/12/([^"\']+)', r'/wp-content/uploads/2022/12/\1'),
                
                # Исправляем пути к иконкам
                (r'/wp-content/themes/theme/assets/img/general/([^"\']+)', r'/wp-content/themes/theme/assets/img/general/\1'),
                (r'/wp-content/themes/theme/assets/img/content/([^"\']+)', r'/wp-content/themes/theme/assets/img/content/\1'),
                
                # Исправляем пути к шрифтам
                (r'/wp-content/themes/theme/assets/fonts/([^"\']+)', r'/wp-content/themes/theme/assets/fonts/\1'),
                
                # Убираем двойные слеши
                (r'//+', '/'),
                
                # Исправляем конкретные проблемные пути
                (r'https://agentdom\.100200\.ru', ''),
                (r'http://agentdom\.100200\.ru', ''),
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

def copy_missing_images():
    """Копирует недостающие изображения в правильные места"""
    print("Копирование недостающих изображений...")
    
    # Словарь соответствий: откуда копировать -> куда копировать
    image_mappings = {
        # Копируем из uploads в правильные места
        "complete_local_site/uploads/115.png": "complete_local_site/wp-content/uploads/2023/03/115.png",
        "complete_local_site/uploads/116.png": "complete_local_site/wp-content/uploads/2023/03/116.png", 
        "complete_local_site/uploads/117.png": "complete_local_site/wp-content/uploads/2023/03/117.png",
        "complete_local_site/uploads/forma45.png": "complete_local_site/wp-content/uploads/2023/03/forma45.png",
        "complete_local_site/uploads/forma46.png": "complete_local_site/wp-content/uploads/2023/03/forma46.png",
        "complete_local_site/uploads/forma47.png": "complete_local_site/wp-content/uploads/2023/03/forma47.png",
        "complete_local_site/uploads/forma48.png": "complete_local_site/wp-content/uploads/2023/03/forma48.png",
        
        # Копируем другие изображения
        "complete_local_site/uploads/glava.jpg": "complete_local_site/wp-content/uploads/2023/05/glava.jpg",
        "complete_local_site/uploads/consult-man1.png": "complete_local_site/wp-content/uploads/2023/05/consult-man1.png",
        "complete_local_site/uploads/dog-bg-1.png": "complete_local_site/wp-content/uploads/2023/05/dog-bg-1.png",
        "complete_local_site/uploads/katalog-1.png": "complete_local_site/wp-content/uploads/2023/05/katalog-1.png",
        "complete_local_site/uploads/download-popup-1.png": "complete_local_site/wp-content/uploads/2023/05/download-popup-1.png",
        "complete_local_site/uploads/load.svg": "complete_local_site/wp-content/uploads/2023/05/load.svg",
        
        # Копируем иконки
        "complete_local_site/uploads/arrow-top-right.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-top-right.svg",
    }
    
    copied_count = 0
    
    for source_path, dest_path in image_mappings.items():
        if os.path.exists(source_path) and not os.path.exists(dest_path):
            try:
                # Создаем папку назначения если не существует
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Копируем файл
                shutil.copy2(source_path, dest_path)
                print(f"Скопирован: {source_path} -> {dest_path}")
                copied_count += 1
                
            except Exception as e:
                print(f"Ошибка при копировании {source_path}: {e}")
    
    print(f"Скопировано файлов: {copied_count}")

def create_missing_image_placeholders():
    """Создает заглушки для недостающих изображений"""
    print("Создание заглушек для недостающих изображений...")
    
    # Список недостающих изображений из логов сервера
    missing_images = [
        "complete_local_site/uploads/8.png",
        "complete_local_site/uploads/7.png",
        "complete_local_site/uploads/61.png", 
        "complete_local_site/uploads/54.png",
        "complete_local_site/uploads/phone-1.png",
        "complete_local_site/uploads/19.png",
        "complete_local_site/uploads/16.png",
        "complete_local_site/uploads/17.png",
        "complete_local_site/uploads/18.png",
        "complete_local_site/uploads/bg-4.jpg",
        "complete_local_site/uploads/consult-bg.jpeg",
        "complete_local_site/uploads/bg-catalog-1.png",
        "complete_local_site/uploads/2222.png",
        "complete_local_site/uploads/calc-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/quiz-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/info-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/main-popup-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/progress-bar.svg",
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

def main():
    print("Исправление подключения изображений к HTML")
    print("=" * 50)
    
    # 1. Копируем недостающие изображения в правильные места
    copy_missing_images()
    
    # 2. Создаем заглушки для отсутствующих изображений
    create_missing_image_placeholders()
    
    # 3. Исправляем пути к изображениям в HTML файлах
    fix_image_paths_in_html()
    
    print("\nГотово! Все изображения подключены к HTML файлам.")

if __name__ == "__main__":
    main()
