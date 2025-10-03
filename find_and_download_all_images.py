#!/usr/bin/env python3
"""
Скрипт для поиска всех ссылок на изображения в HTML и CSS файлах
и скачивания недостающих файлов
"""

import requests
import os
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

BASE_URL = "https://agentdom.100200.ru"

# Заголовки для запросов
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

def download_image(url, local_path):
    """Скачивает изображение"""
    try:
        print(f"Скачиваю: {url}")
        
        response = requests.get(url, headers=HEADERS, timeout=30)
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

def extract_images_from_html(html_content, current_url):
    """Извлекает все ссылки на изображения из HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = set()
    
    # 1. Ищем все img теги
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src and not src.startswith('data:'):
            full_url = urljoin(current_url, src)
            images.add(full_url)
    
    # 2. Ищем фоновые изображения в style атрибутах
    for element in soup.find_all(style=True):
        style = element['style']
        bg_matches = re.findall(r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', style)
        for bg_url in bg_matches:
            if not bg_url.startswith('data:'):
                full_url = urljoin(current_url, bg_url)
                images.add(full_url)
    
    # 3. Ищем в CSS файлах, подключенных к странице
    for link in soup.find_all('link', rel='stylesheet', href=True):
        css_url = urljoin(current_url, link['href'])
        try:
            css_response = requests.get(css_url, headers=HEADERS, timeout=10)
            if css_response.status_code == 200:
                css_content = css_response.text
                css_images = re.findall(r'url\(["\']?([^"\']+)["\']?\)', css_content)
                for css_img in css_images:
                    if not css_img.startswith('data:') and not css_img.startswith('#'):
                        full_url = urljoin(css_url, css_img)
                        images.add(full_url)
        except Exception as e:
            print(f"Ошибка при загрузке CSS {css_url}: {e}")
    
    # 4. Ищем в inline стилях
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            inline_images = re.findall(r'url\(["\']?([^"\']+)["\']?\)', style_tag.string)
            for inline_img in inline_images:
                if not inline_img.startswith('data:'):
                    full_url = urljoin(current_url, inline_img)
                    images.add(full_url)
    
    return images

def get_local_path(image_url):
    """Определяет локальный путь для изображения"""
    parsed = urlparse(image_url)
    path = parsed.path
    
    # Убираем слеш в начале
    if path.startswith('/'):
        path = path[1:]
    
    return f"complete_local_site/{path}"

def scan_all_files_for_images():
    """Сканирует все HTML и CSS файлы для поиска изображений"""
    print("Сканирование всех файлов для поиска изображений...")
    
    all_images = set()
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Найдено HTML файлов: {len(html_files)}")
    
    # Сканируем каждый HTML файл
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Определяем URL страницы
            relative_path = html_file.replace('complete_local_site', '').replace('\\', '/')
            if relative_path.startswith('/'):
                relative_path = relative_path[1:]
            
            if relative_path == 'index.html':
                page_url = BASE_URL + '/'
            elif relative_path.endswith('/index.html'):
                page_url = BASE_URL + '/' + relative_path[:-10] + '/'
            else:
                page_url = BASE_URL + '/' + relative_path
            
            # Извлекаем изображения
            images = extract_images_from_html(content, page_url)
            all_images.update(images)
            
            print(f"Обработан: {html_file} - найдено изображений: {len(images)}")
            
        except Exception as e:
            print(f"Ошибка при обработке {html_file}: {e}")
    
    # Также сканируем CSS файлы напрямую
    css_files = []
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.join(root, file))
    
    print(f"Найдено CSS файлов: {len(css_files)}")
    
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Извлекаем изображения из CSS
            css_images = re.findall(r'url\(["\']?([^"\']+)["\']?\)', css_content)
            for css_img in css_images:
                if not css_img.startswith('data:') and not css_img.startswith('#'):
                    # Определяем базовый URL для CSS файла
                    css_relative_path = css_file.replace('complete_local_site', '').replace('\\', '/')
                    if css_relative_path.startswith('/'):
                        css_relative_path = css_relative_path[1:]
                    
                    css_base_url = BASE_URL + '/' + css_relative_path
                    full_url = urljoin(css_base_url, css_img)
                    all_images.add(full_url)
            
            print(f"Обработан CSS: {css_file}")
            
        except Exception as e:
            print(f"Ошибка при обработке CSS {css_file}: {e}")
    
    print(f"Всего найдено уникальных изображений: {len(all_images)}")
    return all_images

def download_missing_images(all_images):
    """Скачивает все недостающие изображения"""
    print("Скачивание недостающих изображений...")
    
    success_count = 0
    missing_count = 0
    
    for image_url in all_images:
        local_path = get_local_path(image_url)
        
        # Проверяем, существует ли файл
        if not os.path.exists(local_path):
            missing_count += 1
            if download_image(image_url, local_path):
                success_count += 1
            time.sleep(0.5)  # Пауза между запросами
        else:
            print(f"Уже существует: {local_path}")
    
    print(f"Недостающих изображений: {missing_count}")
    print(f"Успешно скачано: {success_count}")
    return success_count

def create_missing_directories():
    """Создает недостающие директории"""
    directories = [
        "complete_local_site/wp-content/themes/theme/assets/fonts/Inter",
        "complete_local_site/wp-content/uploads/2022/12",
        "complete_local_site/wp-content/themes/theme/assets/img/content",
        "complete_local_site/uploads",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Создана папка: {directory}")

def main():
    print("Полный поиск и скачивание всех изображений")
    print("=" * 60)
    
    # 1. Создаем недостающие папки
    create_missing_directories()
    
    # 2. Сканируем все файлы для поиска изображений
    all_images = scan_all_files_for_images()
    
    # 3. Скачиваем недостающие изображения
    downloaded_count = download_missing_images(all_images)
    
    print(f"\nРезультат:")
    print(f"Найдено изображений: {len(all_images)}")
    print(f"Скачано новых: {downloaded_count}")
    print("Готово!")

if __name__ == "__main__":
    main()
