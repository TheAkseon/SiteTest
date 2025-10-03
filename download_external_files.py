#!/usr/bin/env python3
"""
Скрипт для скачивания внешних CSS и JS файлов
"""

import requests
import os
from urllib.parse import urlparse

# Внешние файлы для скачивания
EXTERNAL_FILES = [
    {
        "url": "https://cdn.jsdelivr.net/npm/@fancyapps/ui/dist/fancybox.css",
        "local": "complete_local_site/wp-content/themes/theme/assets/css/fancybox.css"
    },
    {
        "url": "https://fonts.googleapis.com/css?family=Raleway:100,200,300,400,500,600,700,800,900,100i,200i,300i,400i,500i,600i,700i,800i,900i,100ii,200ii,300ii,400ii,500ii,600ii,700ii,800ii,900ii&display=swap&subset=all",
        "local": "complete_local_site/wp-content/themes/theme/assets/css/google-fonts.css"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.umd.js",
        "local": "complete_local_site/wp-content/themes/theme/assets/js/fancybox.umd.js"
    }
]

def download_external_file(url, local_path):
    """Скачивает внешний файл"""
    try:
        print(f"Скачиваю: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Создаем папку если не существует
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Определяем режим записи (текст или бинарный)
        mode = 'wb' if url.endswith('.js') or url.endswith('.css') else 'w'
        encoding = None if mode == 'wb' else 'utf-8'
        
        # Сохраняем файл
        with open(local_path, mode, encoding=encoding) as f:
            if mode == 'wb':
                f.write(response.content)
            else:
                f.write(response.text)
        
        print(f"Сохранено: {local_path}")
        return True
        
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return False

def download_external_files():
    """Скачивает все внешние файлы"""
    print("Скачиваю внешние CSS и JS файлы...")
    
    success_count = 0
    
    for file_info in EXTERNAL_FILES:
        if download_external_file(file_info["url"], file_info["local"]):
            success_count += 1
    
    print(f"Скачано внешних файлов: {success_count}/{len(EXTERNAL_FILES)}")

if __name__ == "__main__":
    download_external_files()
