#!/usr/bin/env python3
"""
Скрипт для исправления всех ссылок в HTML файлах
"""

import os
import re
from pathlib import Path

def fix_html_links(file_path):
    """Исправляет ссылки в HTML файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем все ссылки на agentdom.100200.ru
        content = re.sub(r'https://agentdom\.100200\.ru', '', content)
        content = re.sub(r'http://agentdom\.100200\.ru', '', content)
        
        # Исправляем конкретные пути
        replacements = [
            # CSS файлы
            (r'/wp-content/themes/theme/assets/css/wp-content_themes_theme_assets_css_main\.css', '/wp-content/themes/theme/assets/css/main.css'),
            (r'/wp-content/themes/theme/assets/js/wp-content_themes_theme_assets_js_main\.js', '/wp-content/themes/theme/assets/js/main.js'),
            (r'/wp-content/themes/theme/assets/js/wp-content_themes_theme_assets_js_script\.js', '/wp-content/themes/theme/assets/js/script.js'),
            
            # Изображения
            (r'/wp-content/uploads/2023/03/', '/uploads/'),
            (r'/wp-content/uploads/2023/05/', '/uploads/'),
            (r'/template/realt/wp-content/uploads/', '/uploads/'),
            
            # Другие пути
            (r'/template/realt/', '/'),
        ]
        
        for old_pattern, new_pattern in replacements:
            content = re.sub(old_pattern, new_pattern, content)
        
        # Сохраняем исправленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Исправлен файл: {file_path}")
        return True
        
    except Exception as e:
        print(f"Ошибка при исправлении {file_path}: {e}")
        return False

def fix_all_html_files(directory):
    """Исправляет все HTML файлы в директории"""
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Найдено HTML файлов: {len(html_files)}")
    
    success_count = 0
    for html_file in html_files:
        if fix_html_links(html_file):
            success_count += 1
    
    print(f"Исправлено файлов: {success_count}/{len(html_files)}")

if __name__ == "__main__":
    print("Исправление ссылок в HTML файлах...")
    fix_all_html_files("complete_local_site")
    print("Готово!")
