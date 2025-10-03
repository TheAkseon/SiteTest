#!/usr/bin/env python3
"""
Скрипт для докачивания всех недостающих изображений и проверки страниц
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
        print(f"Скачиваю изображение: {url}")
        
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

def extract_missing_images_from_html(html_content, current_url):
    """Извлекает все ссылки на изображения из HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = set()
    
    # Ищем все изображения
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src and not src.startswith('data:'):
            full_url = urljoin(current_url, src)
            images.add(full_url)
    
    # Ищем фоновые изображения в стилях
    for element in soup.find_all(style=True):
        style = element['style']
        bg_matches = re.findall(r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', style)
        for bg_url in bg_matches:
            full_url = urljoin(current_url, bg_url)
            images.add(full_url)
    
    # Ищем в CSS файлах
    for link in soup.find_all('link', rel='stylesheet', href=True):
        css_url = urljoin(current_url, link['href'])
        try:
            css_response = requests.get(css_url, headers=HEADERS, timeout=10)
            if css_response.status_code == 200:
                css_content = css_response.text
                css_images = re.findall(r'url\(["\']?([^"\']+)["\']?\)', css_content)
                for css_img in css_images:
                    if not css_img.startswith('data:'):
                        full_url = urljoin(css_url, css_img)
                        images.add(full_url)
        except:
            pass
    
    return images

def get_local_image_path(image_url):
    """Определяет локальный путь для изображения"""
    parsed = urlparse(image_url)
    path = parsed.path
    
    # Убираем слеш в начале
    if path.startswith('/'):
        path = path[1:]
    
    return f"complete_local_site/{path}"

def download_missing_images():
    """Скачивает все недостающие изображения"""
    print("Поиск и скачивание недостающих изображений...")
    
    # Список известных недостающих изображений из логов
    missing_images = [
        # Из логов сервера
        "https://agentdom.100200.ru/wp-content/uploads/2022/11/evro.jpg",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/img/content/quiz-bg.jpg",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/img/content/info-bg.jpg",
        "https://agentdom.100200.ru/wp-content/uploads/2022/11/quiz-manager.png",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/img/general/progress-bar.svg",
        "https://agentdom.100200.ru/uploads/8.png",
        "https://agentdom.100200.ru/uploads/7.png",
        "https://agentdom.100200.ru/uploads/61.png",
        "https://agentdom.100200.ru/uploads/54.png",
        "https://agentdom.100200.ru/uploads/phone-1.png",
        "https://agentdom.100200.ru/uploads/dog-bg-1.png",
        "https://agentdom.100200.ru/uploads/glava.jpg",
        "https://agentdom.100200.ru/uploads/19.png",
        "https://agentdom.100200.ru/uploads/16.png",
        "https://agentdom.100200.ru/uploads/17.png",
        "https://agentdom.100200.ru/uploads/18.png",
        "https://agentdom.100200.ru/uploads/consult-man1.png",
        "https://agentdom.100200.ru/uploads/bg-4.jpg",
        "https://agentdom.100200.ru/uploads/consult-bg.jpeg",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/fonts/Inter/Inter-Regular.woff",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/fonts/Inter/Inter-Bold.woff",
        "https://agentdom.100200.ru/uploads/bg-catalog-1.png",
        "https://agentdom.100200.ru/wp-content/uploads/2022/12/download-popup-bg.jpg",
        "https://agentdom.100200.ru/uploads/download-popup-1.png",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/fonts/Inter/Inter-Regular.ttf",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/fonts/Inter/Inter-Bold.ttf",
        "https://agentdom.100200.ru/uploads/load.svg",
        "https://agentdom.100200.ru/uploads/115.png",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/img/content/main-popup-bg.jpg",
        "https://agentdom.100200.ru/uploads/2222.png",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/img/general/arrow-top-right.svg",
        "https://agentdom.100200.ru/wp-content/themes/theme/assets/img/general/close-icon.svg",
        "https://agentdom.100200.ru/uploads/katalog-1.png",
        "https://agentdom.100200.ru/uploads/calc-bg.jpg",
    ]
    
    success_count = 0
    
    for image_url in missing_images:
        local_path = get_local_image_path(image_url)
        
        # Проверяем, существует ли файл
        if not os.path.exists(local_path):
            if download_image(image_url, local_path):
                success_count += 1
        else:
            print(f"Уже существует: {local_path}")
        
        time.sleep(0.5)  # Пауза между запросами
    
    print(f"Скачано новых изображений: {success_count}")
    return success_count

def scan_all_pages_for_images():
    """Сканирует все HTML страницы и извлекает ссылки на изображения"""
    print("Сканирование всех страниц для поиска изображений...")
    
    all_images = set()
    html_files = []
    
    # Находим все HTML файлы
    for root, dirs, files in os.walk("complete_local_site"):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Найдено HTML файлов: {len(html_files)}")
    
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
            images = extract_missing_images_from_html(content, page_url)
            all_images.update(images)
            
        except Exception as e:
            print(f"Ошибка при обработке {html_file}: {e}")
    
    print(f"Найдено уникальных изображений: {len(all_images)}")
    
    # Скачиваем все найденные изображения
    success_count = 0
    for image_url in all_images:
        local_path = get_local_image_path(image_url)
        
        if not os.path.exists(local_path):
            if download_image(image_url, local_path):
                success_count += 1
        
        time.sleep(0.3)  # Пауза между запросами
    
    print(f"Скачано изображений из HTML: {success_count}")
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
    print("Полное скачивание всех недостающих изображений")
    print("=" * 60)
    
    # Создаем недостающие папки
    create_missing_directories()
    
    # Скачиваем известные недостающие изображения
    count1 = download_missing_images()
    
    # Сканируем все страницы и скачиваем найденные изображения
    count2 = scan_all_pages_for_images()
    
    total = count1 + count2
    print(f"\nВсего скачано новых изображений: {total}")
    print("Готово!")

if __name__ == "__main__":
    main()
