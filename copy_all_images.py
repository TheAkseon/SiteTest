#!/usr/bin/env python3
"""
Скрипт для копирования всех существующих изображений в правильные места
"""

import os
import shutil
import re

def copy_all_existing_images():
    """Копирует все существующие изображения в правильные места"""
    print("Копирование всех существующих изображений...")
    
    # Находим все изображения в папке uploads
    uploads_dir = "complete_local_site/uploads"
    wp_uploads_dir = "complete_local_site/wp-content/uploads"
    
    copied_count = 0
    
    if os.path.exists(uploads_dir):
        for root, dirs, files in os.walk(uploads_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    source_path = os.path.join(root, file)
                    
                    # Определяем правильное место назначения
                    relative_path = os.path.relpath(source_path, uploads_dir)
                    
                    # Копируем в корень uploads
                    dest_path = f"complete_local_site/uploads/{file}"
                    if not os.path.exists(dest_path):
                        shutil.copy2(source_path, dest_path)
                        print(f"Скопирован: {file}")
                        copied_count += 1
                    
                    # Копируем в wp-content/uploads
                    wp_dest_path = f"{wp_uploads_dir}/{file}"
                    if not os.path.exists(wp_dest_path):
                        os.makedirs(os.path.dirname(wp_dest_path), exist_ok=True)
                        shutil.copy2(source_path, wp_dest_path)
                        print(f"Скопирован в WP: {file}")
                        copied_count += 1
    
    print(f"Скопировано файлов: {copied_count}")

def create_missing_directories():
    """Создает все необходимые директории"""
    directories = [
        "complete_local_site/wp-content/uploads/2022/10",
        "complete_local_site/wp-content/uploads/2022/11",
        "complete_local_site/wp-content/uploads/2022/12",
        "complete_local_site/wp-content/uploads/2023/02",
        "complete_local_site/wp-content/uploads/2023/03",
        "complete_local_site/wp-content/uploads/2023/05",
        "complete_local_site/wp-content/themes/theme/assets/img/general",
        "complete_local_site/wp-content/themes/theme/assets/img/content",
        "complete_local_site/wp-content/themes/theme/assets/fonts/Inter",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Создана папка: {directory}")

def copy_images_to_correct_locations():
    """Копирует изображения в правильные места согласно их именам"""
    print("Копирование изображений в правильные места...")
    
    # Словарь соответствий: имя файла -> правильное место
    image_mappings = {
        # Основные изображения
        "115.png": "complete_local_site/wp-content/uploads/2023/03/115.png",
        "116.png": "complete_local_site/wp-content/uploads/2023/03/116.png",
        "117.png": "complete_local_site/wp-content/uploads/2023/03/117.png",
        "118.png": "complete_local_site/wp-content/uploads/2023/05/118.png",
        "211.png": "complete_local_site/wp-content/uploads/2023/05/211.png",
        "38.png": "complete_local_site/wp-content/uploads/2023/05/38.png",
        "43.png": "complete_local_site/wp-content/uploads/2023/05/43.png",
        "12.svg": "complete_local_site/wp-content/uploads/2023/05/12.svg",
        
        # Формы
        "forma45.png": "complete_local_site/wp-content/uploads/2023/03/forma45.png",
        "forma46.png": "complete_local_site/wp-content/uploads/2023/03/forma46.png",
        "forma47.png": "complete_local_site/wp-content/uploads/2023/03/forma47.png",
        "forma48.png": "complete_local_site/wp-content/uploads/2023/03/forma48.png",
        "forma57.png": "complete_local_site/uploads/forma57.png",
        "forma58.png": "complete_local_site/uploads/forma58.png",
        "forma59.png": "complete_local_site/uploads/forma59.png",
        
        # Другие изображения
        "glava.jpg": "complete_local_site/wp-content/uploads/2023/05/glava.jpg",
        "consult-man1.png": "complete_local_site/wp-content/uploads/2023/05/consult-man1.png",
        "dog-bg-1.png": "complete_local_site/wp-content/uploads/2023/05/dog-bg-1.png",
        "katalog-1.png": "complete_local_site/wp-content/uploads/2023/05/katalog-1.png",
        "download-popup-1.png": "complete_local_site/wp-content/uploads/2023/05/download-popup-1.png",
        "load.svg": "complete_local_site/wp-content/uploads/2023/05/load.svg",
        "catalog-21.png": "complete_local_site/wp-content/uploads/2023/05/catalog-21.png",
        
        # Иконки
        "arrow-top-right.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-top-right.svg",
        "arrow-bottom.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-bottom.svg",
        "arrow-top.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-top.svg",
        "check-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/check-icon.svg",
        "hit-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/hit-icon.svg",
        "new-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/new-icon.svg",
        "pdf-circle.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/pdf-circle.svg",
        "plus-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/plus-icon.svg",
        "sale-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/sale-icon.svg",
        "slider-next.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/slider-next.svg",
        "slider-prev.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/slider-prev.svg",
        "video-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/video-icon.svg",
        "whats-app.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/whats-app.svg",
        "viber.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/viber.svg",
        "telegram.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/telegram.svg",
        "@.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/@.svg",
        "locker.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/locker.svg",
        
        # Социальные сети
        "facebook.png": "complete_local_site/wp-content/uploads/2022/11/facebook.png",
        "instagram.png": "complete_local_site/wp-content/uploads/2022/11/instagram.png",
        "vk.png": "complete_local_site/wp-content/uploads/2022/11/vk.png",
        "whats-app-1.png": "complete_local_site/wp-content/uploads/2022/11/whats-app-1.png",
        "whats-app.png": "complete_local_site/wp-content/uploads/2022/11/whats-app.png",
        "telegram.png": "complete_local_site/wp-content/uploads/2022/11/telegram.png",
        "download-2.png": "complete_local_site/wp-content/uploads/2022/11/download-2.png",
        
        # Отзывы
        "about-company-certificate-1.jpg": "complete_local_site/wp-content/uploads/2022/10/about-company-certificate-1.jpg",
        "img-review-1.jpg": "complete_local_site/wp-content/uploads/2022/10/img-review-1.jpg",
        "phone-review-1.jpg": "complete_local_site/wp-content/uploads/2022/10/phone-review-1.jpg",
        "phone-review-link-1.png": "complete_local_site/wp-content/uploads/2022/10/phone-review-link-1.png",
        "phone-review-link-2.png": "complete_local_site/wp-content/uploads/2022/10/phone-review-link-2.png",
        "video-review-1.jpg": "complete_local_site/wp-content/uploads/2022/10/video-review-1.jpg",
    }
    
    copied_count = 0
    
    for filename, dest_path in image_mappings.items():
        # Ищем файл в разных местах
        source_paths = [
            f"complete_local_site/uploads/{filename}",
            f"complete_local_site/wp-content/uploads/2023/03/{filename}",
            f"complete_local_site/wp-content/uploads/2023/05/{filename}",
            f"complete_local_site/wp-content/uploads/2022/11/{filename}",
            f"complete_local_site/wp-content/uploads/2022/10/{filename}",
        ]
        
        source_found = None
        for source_path in source_paths:
            if os.path.exists(source_path):
                source_found = source_path
                break
        
        if source_found and not os.path.exists(dest_path):
            try:
                # Создаем папку назначения если не существует
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Копируем файл
                shutil.copy2(source_found, dest_path)
                print(f"Скопирован: {filename} -> {dest_path}")
                copied_count += 1
                
            except Exception as e:
                print(f"Ошибка при копировании {filename}: {e}")
    
    print(f"Скопировано файлов: {copied_count}")

def main():
    print("Копирование всех изображений в правильные места")
    print("=" * 50)
    
    # 1. Создаем все необходимые папки
    create_missing_directories()
    
    # 2. Копируем все существующие изображения
    copy_all_existing_images()
    
    # 3. Копируем изображения в правильные места
    copy_images_to_correct_locations()
    
    print("\nГотово! Все изображения скопированы в правильные места.")

if __name__ == "__main__":
    main()
