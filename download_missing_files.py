#!/usr/bin/env python3
"""
Скрипт для скачивания недостающих файлов WordPress
"""

import requests
import os
from urllib.parse import urljoin

BASE_URL = "https://agentdom.100200.ru"

# Список недостающих файлов
MISSING_FILES = [
    "/wp-includes/css/dist/block-library/style.min.css",
    "/wp-includes/js/wp-emoji-release.min.js",
    "/wp-includes/js/jquery/jquery.min.js",
    "/wp-includes/js/jquery/jquery-migrate.min.js",
]

def download_file(url, local_path):
    """Скачивает файл"""
    try:
        print(f"Скачиваю: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Создаем папку если не существует
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Сохраняем файл
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Сохранено: {local_path}")
        return True
        
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return False

def download_missing_files():
    """Скачивает все недостающие файлы"""
    print("Скачиваю недостающие файлы WordPress...")
    
    success_count = 0
    
    for file_path in MISSING_FILES:
        url = urljoin(BASE_URL, file_path)
        local_path = f"complete_local_site{file_path}"
        
        if download_file(url, local_path):
            success_count += 1
    
    print(f"Скачано файлов: {success_count}/{len(MISSING_FILES)}")

if __name__ == "__main__":
    download_missing_files()
