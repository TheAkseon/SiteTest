#!/usr/bin/env python3
"""
Скрипт для замены внешних ссылок на локальные файлы
"""

import os
import re

def replace_external_links(file_path):
    """Заменяет внешние ссылки на локальные"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Замены внешних ссылок на локальные
        replacements = [
            # Fancybox CSS
            (r'https://cdn\.jsdelivr\.net/npm/@fancyapps/ui/dist/fancybox\.css\?ver=6\.8\.2', '/wp-content/themes/theme/assets/css/fancybox.css'),
            
            # Google Fonts CSS
            (r'https://fonts\.googleapis\.com/css\?family=Raleway%3A100%2C200%2C300%2C400%2C500%2C600%2C700%2C800%2C900%2C100i%2C200i%2C300i%2C400i%2C500i%2C600i%2C700i%2C800i%2C900i%2C100ii%2C200ii%2C300ii%2C400ii%2C500ii%2C600ii%2C700ii%2C800ii%2C900ii&amp;display=swap&amp;subset=all&amp;ver=3\.2\.5', '/wp-content/themes/theme/assets/css/google-fonts.css'),
            
            # Fancybox JS
            (r'https://cdn\.jsdelivr\.net/npm/@fancyapps/ui@4\.0/dist/fancybox\.umd\.js\?ver=1\.0\.0', '/wp-content/themes/theme/assets/js/fancybox.umd.js'),
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
        if replace_external_links(html_file):
            success_count += 1
    
    print(f"Исправлено файлов: {success_count}/{len(html_files)}")

if __name__ == "__main__":
    print("Замена внешних ссылок на локальные файлы...")
    fix_all_html_files("complete_local_site")
    print("Готово!")
