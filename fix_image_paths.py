#!/usr/bin/env python3
"""
Скрипт для исправления путей к изображениям
"""

import os
import shutil
import re

def fix_image_paths():
    """Исправляет пути к изображениям"""
    
    # Создаем правильную структуру папок
    directories = [
        "complete_local_site/wp-content/uploads/2022/10",
        "complete_local_site/wp-content/uploads/2022/11", 
        "complete_local_site/wp-content/uploads/2023/02",
        "complete_local_site/wp-content/uploads/2023/03",
        "complete_local_site/wp-content/uploads/2023/05",
        "complete_local_site/wp-content/themes/theme/assets/img/general",
        "complete_local_site/wp-content/themes/theme/assets/img/content",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Создана папка: {directory}")
    
    # Перемещаем изображения в правильные папки
    uploads_dir = "complete_local_site/uploads"
    
    # Словарь соответствий старых имен новым
    image_mappings = {
        # 2022/10
        "wp-content_uploads_2022_10_about-company-certificate-1.jpg": "complete_local_site/wp-content/uploads/2022/10/about-company-certificate-1.jpg",
        "wp-content_uploads_2022_10_img-review-1.jpg": "complete_local_site/wp-content/uploads/2022/10/img-review-1.jpg",
        "wp-content_uploads_2022_10_phone-review-1.jpg": "complete_local_site/wp-content/uploads/2022/10/phone-review-1.jpg",
        "wp-content_uploads_2022_10_phone-review-link-1.png": "complete_local_site/wp-content/uploads/2022/10/phone-review-link-1.png",
        "wp-content_uploads_2022_10_phone-review-link-2.png": "complete_local_site/wp-content/uploads/2022/10/phone-review-link-2.png",
        "wp-content_uploads_2022_10_video-review-1.jpg": "complete_local_site/wp-content/uploads/2022/10/video-review-1.jpg",
        
        # 2022/11
        "wp-content_uploads_2022_11_facebook.png": "complete_local_site/wp-content/uploads/2022/11/facebook.png",
        "wp-content_uploads_2022_11_instagram.png": "complete_local_site/wp-content/uploads/2022/11/instagram.png",
        "wp-content_uploads_2022_11_vk.png": "complete_local_site/wp-content/uploads/2022/11/vk.png",
        "wp-content_uploads_2022_11_whats-app-1.png": "complete_local_site/wp-content/uploads/2022/11/whats-app-1.png",
        "wp-content_uploads_2022_11_whats-app.png": "complete_local_site/wp-content/uploads/2022/11/whats-app.png",
        "wp-content_uploads_2022_11_telegram.png": "complete_local_site/wp-content/uploads/2022/11/telegram.png",
        "wp-content_uploads_2022_11_download-2.png": "complete_local_site/wp-content/uploads/2022/11/download-2.png",
        "wp-content_uploads_2022_11_arrow-top-right.svg": "complete_local_site/wp-content/uploads/2022/11/arrow-top-right.svg",
        
        # 2023/03
        "wp-content_uploads_2023_03_115.png": "complete_local_site/wp-content/uploads/2023/03/115.png",
        "wp-content_uploads_2023_03_116.png": "complete_local_site/wp-content/uploads/2023/03/116.png",
        "wp-content_uploads_2023_03_117.png": "complete_local_site/wp-content/uploads/2023/03/117.png",
        "wp-content_uploads_2023_03_forma45.png": "complete_local_site/wp-content/uploads/2023/03/forma45.png",
        "wp-content_uploads_2023_03_forma46.png": "complete_local_site/wp-content/uploads/2023/03/forma46.png",
        "wp-content_uploads_2023_03_forma47.png": "complete_local_site/wp-content/uploads/2023/03/forma47.png",
        "wp-content_uploads_2023_03_forma48.png": "complete_local_site/wp-content/uploads/2023/03/forma48.png",
        
        # 2023/05
        "wp-content_uploads_2023_05_118.png": "complete_local_site/wp-content/uploads/2023/05/118.png",
        "wp-content_uploads_2023_05_12.svg": "complete_local_site/wp-content/uploads/2023/05/12.svg",
        "wp-content_uploads_2023_05_16.png": "complete_local_site/wp-content/uploads/2023/05/16.png",
        "wp-content_uploads_2023_05_17.png": "complete_local_site/wp-content/uploads/2023/05/17.png",
        "wp-content_uploads_2023_05_18.png": "complete_local_site/wp-content/uploads/2023/05/18.png",
        "wp-content_uploads_2023_05_19.png": "complete_local_site/wp-content/uploads/2023/05/19.png",
        "wp-content_uploads_2023_05_211.png": "complete_local_site/wp-content/uploads/2023/05/211.png",
        "wp-content_uploads_2023_05_38.png": "complete_local_site/wp-content/uploads/2023/05/38.png",
        "wp-content_uploads_2023_05_43.png": "complete_local_site/wp-content/uploads/2023/05/43.png",
        "wp-content_uploads_2023_05_catalog-21.png": "complete_local_site/wp-content/uploads/2023/05/catalog-21.png",
        "wp-content_uploads_2023_05_consult-man1.png": "complete_local_site/wp-content/uploads/2023/05/consult-man1.png",
        "wp-content_uploads_2023_05_dog-bg-1.png": "complete_local_site/wp-content/uploads/2023/05/dog-bg-1.png",
        "wp-content_uploads_2023_05_download-popup-1.png": "complete_local_site/wp-content/uploads/2023/05/download-popup-1.png",
        "wp-content_uploads_2023_05_glava.jpg": "complete_local_site/wp-content/uploads/2023/05/glava.jpg",
        "wp-content_uploads_2023_05_katalog-1.png": "complete_local_site/wp-content/uploads/2023/05/katalog-1.png",
        "wp-content_uploads_2023_05_load.svg": "complete_local_site/wp-content/uploads/2023/05/load.svg",
        
        # 2024/06
        "wp-content_uploads_2024_06_1.jpg": "complete_local_site/wp-content/uploads/2024/06/1.jpg",
        
        # SVG иконки
        "wp-content_themes_theme_assets_img_general_arrow-bottom.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-bottom.svg",
        "wp-content_themes_theme_assets_img_general_arrow-top.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/arrow-top.svg",
        "wp-content_themes_theme_assets_img_general_check-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/check-icon.svg",
        "wp-content_themes_theme_assets_img_general_hit-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/hit-icon.svg",
        "wp-content_themes_theme_assets_img_general_new-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/new-icon.svg",
        "wp-content_themes_theme_assets_img_general_pdf-circle.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/pdf-circle.svg",
        "wp-content_themes_theme_assets_img_general_plus-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/plus-icon.svg",
        "wp-content_themes_theme_assets_img_general_sale-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/sale-icon.svg",
        "wp-content_themes_theme_assets_img_general_slider-next.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/slider-next.svg",
        "wp-content_themes_theme_assets_img_general_slider-prev.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/slider-prev.svg",
        "wp-content_themes_theme_assets_img_general_video-icon.svg": "complete_local_site/wp-content/themes/theme/assets/img/general/video-icon.svg",
    }
    
    # Перемещаем файлы
    moved_count = 0
    for old_name, new_path in image_mappings.items():
        old_path = os.path.join(uploads_dir, old_name)
        if os.path.exists(old_path):
            try:
                # Создаем папку назначения если не существует
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(old_path, new_path)
                print(f"Перемещен: {old_name} -> {new_path}")
                moved_count += 1
            except Exception as e:
                print(f"Ошибка при перемещении {old_name}: {e}")
        else:
            print(f"Не найден: {old_name}")
    
    print(f"Перемещено файлов: {moved_count}")
    
    # Создаем недостающие изображения (заглушки)
    missing_images = [
        "complete_local_site/uploads/quiz-final.png",
        "complete_local_site/uploads/step-1.jpg",
        "complete_local_site/uploads/step-2.jpg", 
        "complete_local_site/uploads/step-3.png",
        "complete_local_site/uploads/forma58.png",
        "complete_local_site/uploads/forma59.png",
        "complete_local_site/uploads/forma57.png",
        "complete_local_site/uploads/akcii-11.jpg",
        "complete_local_site/uploads/dom-13.png",
        "complete_local_site/uploads/bg-11.jpg",
        "complete_local_site/uploads/consult-bg.jpg",
        "complete_local_site/wp-content/uploads/2022/11/bez.jpg",
        "complete_local_site/wp-content/uploads/2022/11/kosmetich.jpg",
        "complete_local_site/wp-content/uploads/2022/11/evro.jpg",
        "complete_local_site/wp-content/uploads/2022/11/1624270380_dizajnerskij-remont.jpg",
        "complete_local_site/wp-content/uploads/2022/11/quiz-present.png",
        "complete_local_site/wp-content/uploads/2023/02/akcii-2.png",
        "complete_local_site/wp-content/themes/theme/assets/img/general/whats-app.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/viber.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/telegram.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/@.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/general/locker.svg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/work-steps-bd-dark.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/work-steps-bd-light.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/reviews-bg.jpg",
        "complete_local_site/wp-content/themes/theme/assets/img/content/phone-review-bg.png",
    ]
    
    for missing_path in missing_images:
        os.makedirs(os.path.dirname(missing_path), exist_ok=True)
        # Создаем пустой файл как заглушку
        with open(missing_path, 'w') as f:
            f.write("")
        print(f"Создана заглушка: {missing_path}")

if __name__ == "__main__":
    print("Исправление путей к изображениям...")
    fix_image_paths()
    print("Готово!")
