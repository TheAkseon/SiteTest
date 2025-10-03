#!/usr/bin/env python3
"""
Скрипт для скачивания всех страниц сайта agentdom.100200.ru
и создания полноценного локального сайта
"""

import requests
import os
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

# Базовый URL сайта
BASE_URL = "https://agentdom.100200.ru"

# Список всех страниц для скачивания
PAGES_TO_DOWNLOAD = [
    # Основные разделы
    "/",
    "/services/",
    "/pomoshh-v-pokupke/",
    "/pomoshh-v-prodazhe/",
    "/yuridicheskoe-soprovozhdenie/",
    "/srochnyj-vykup/",
    "/portfolios/",
    "/catalog/",
    "/o-kompanii-nedvizhimost/",
    "/blog/",
    "/contacts/",
    
    # Конкретные объекты недвижимости
    "/catalog/3-komnata/uteplitel-v-plitah-minvata-tehnonik-8/",
    "/catalog/2-komnata/2-komnatnaya-kvartira-na-ulicze-gagarina-11/",
    "/catalog/2-komnata/3-komnatnaya-kvartira-na-ulicze-popova-23/",
    "/catalog/1-komnata/1-komnatnaya-kvartirana-ulicze-gagarina-11/",
    
    # Портфолио новостроек
    "/portfolios/krylia/dom-v-sovremennom-stile-v-kieve-345-m2-4/",
    "/portfolios/zilart/zhk-zilart/",
    "/portfolios/bauman/zhk-bauman-house/",
    
    # Страница благодарности
    "/spasibo/",
]

# Заголовки для запросов
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def create_directory_structure():
    """Создает структуру папок для локального сайта"""
    directories = [
        "local_site",
        "local_site/services",
        "local_site/pomoshh-v-pokupke",
        "local_site/pomoshh-v-prodazhe", 
        "local_site/yuridicheskoe-soprovozhdenie",
        "local_site/srochnyj-vykup",
        "local_site/portfolios",
        "local_site/portfolios/krylia",
        "local_site/portfolios/zilart",
        "local_site/portfolios/bauman",
        "local_site/catalog",
        "local_site/catalog/1-komnata",
        "local_site/catalog/2-komnata", 
        "local_site/catalog/3-komnata",
        "local_site/o-kompanii-nedvizhimost",
        "local_site/blog",
        "local_site/contacts",
        "local_site/spasibo",
        "local_site/uploads",
        "local_site/wp-content",
        "local_site/wp-content/themes",
        "local_site/wp-content/themes/theme",
        "local_site/wp-content/themes/theme/assets",
        "local_site/wp-content/themes/theme/assets/css",
        "local_site/wp-content/themes/theme/assets/js",
        "local_site/wp-content/themes/theme/assets/img",
        "local_site/wp-content/uploads",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Создана папка: {directory}")

def download_page(url, local_path):
    """Скачивает страницу и сохраняет локально"""
    try:
        print(f"📥 Скачиваю: {url}")
        
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # Создаем папку если не существует
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Сохраняем HTML
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✓ Сохранено: {local_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при скачивании {url}: {e}")
        return False

def fix_local_links(html_content):
    """Исправляет ссылки для локального использования"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Заменяем все ссылки на agentdom.100200.ru на локальные
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'agentdom.100200.ru' in href:
            # Извлекаем путь после домена
            parsed = urlparse(href)
            new_href = parsed.path
            if parsed.query:
                new_href += '?' + parsed.query
            link['href'] = new_href
    
    # Заменяем все ссылки на изображения
    for img in soup.find_all('img', src=True):
        src = img['src']
        if 'agentdom.100200.ru' in src:
            parsed = urlparse(src)
            new_src = parsed.path
            img['src'] = new_src
    
    # Заменяем ссылки в CSS
    for link in soup.find_all('link', href=True):
        href = link['href']
        if 'agentdom.100200.ru' in href:
            parsed = urlparse(href)
            new_href = parsed.path
            link['href'] = new_href
    
    # Заменяем ссылки в скриптах
    for script in soup.find_all('script', src=True):
        src = script['src']
        if 'agentdom.100200.ru' in src:
            parsed = urlparse(src)
            new_src = parsed.path
            script['src'] = new_src
    
    return str(soup)

def download_all_pages():
    """Скачивает все страницы сайта"""
    print("🚀 Начинаю скачивание всех страниц...")
    
    # Создаем структуру папок
    create_directory_structure()
    
    success_count = 0
    total_count = len(PAGES_TO_DOWNLOAD)
    
    for page_path in PAGES_TO_DOWNLOAD:
        url = urljoin(BASE_URL, page_path)
        
        # Определяем локальный путь
        if page_path == "/":
            local_path = "local_site/index.html"
        else:
            # Убираем слеш в начале и добавляем index.html
            clean_path = page_path.lstrip('/')
            if clean_path.endswith('/'):
                clean_path = clean_path.rstrip('/')
            local_path = f"local_site/{clean_path}/index.html"
        
        # Скачиваем страницу
        if download_page(url, local_path):
            success_count += 1
            
            # Исправляем ссылки в скачанной странице
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fixed_content = fix_local_links(content)
                
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✓ Исправлены ссылки в: {local_path}")
                
            except Exception as e:
                print(f"❌ Ошибка при исправлении ссылок в {local_path}: {e}")
        
        # Пауза между запросами
        time.sleep(1)
    
    print(f"\n🎉 Скачивание завершено!")
    print(f"✅ Успешно скачано: {success_count}/{total_count} страниц")
    
    if success_count == total_count:
        print("🎯 Все страницы скачаны успешно!")
    else:
        print("⚠️ Некоторые страницы не удалось скачать")

def copy_existing_files():
    """Копирует уже существующие файлы в новую структуру"""
    import shutil
    
    print("📁 Копирую существующие файлы...")
    
    # Копируем CSS файлы
    if os.path.exists("agentdom_template/wp-content_themes_theme_assets_css_main.css"):
        shutil.copy2(
            "agentdom_template/wp-content_themes_theme_assets_css_main.css",
            "local_site/wp-content/themes/theme/assets/css/main.css"
        )
        print("✓ Скопирован main.css")
    
    # Копируем JS файлы
    if os.path.exists("agentdom_template/wp-content_themes_theme_assets_js_main.js"):
        shutil.copy2(
            "agentdom_template/wp-content_themes_theme_assets_js_main.js",
            "local_site/wp-content/themes/theme/assets/js/main.js"
        )
        print("✓ Скопирован main.js")
    
    if os.path.exists("agentdom_template/wp-content_themes_theme_assets_js_script.js"):
        shutil.copy2(
            "agentdom_template/wp-content_themes_theme_assets_js_script.js",
            "local_site/wp-content/themes/theme/assets/js/script.js"
        )
        print("✓ Скопирован script.js")
    
    # Копируем изображения
    image_files = [
        f for f in os.listdir("agentdom_template") 
        if f.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))
    ]
    
    for image_file in image_files:
        shutil.copy2(
            f"agentdom_template/{image_file}",
            f"local_site/uploads/{image_file}"
        )
        print(f"✓ Скопировано изображение: {image_file}")

if __name__ == "__main__":
    print("Скачивание полного сайта agentdom.100200.ru")
    print("=" * 50)
    
    # Скачиваем все страницы
    download_all_pages()
    
    # Копируем существующие файлы
    copy_existing_files()
    
    print("\nГотово! Локальный сайт создан в папке 'local_site'")
    print("Структура:")
    print("   local_site/")
    print("   ├── index.html (главная)")
    print("   ├── services/index.html")
    print("   ├── catalog/index.html")
    print("   ├── portfolios/index.html")
    print("   ├── uploads/ (изображения)")
    print("   └── wp-content/ (стили и скрипты)")
