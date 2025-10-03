#!/usr/bin/env python3
"""
Полный скрипт для скачивания всего сайта agentdom.100200.ru
Анализирует каждую страницу и скачивает все найденные ссылки рекурсивно
"""

import requests
import os
import time
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
import re
from collections import deque
import hashlib

# Базовый URL сайта
BASE_URL = "https://agentdom.100200.ru"
BASE_DOMAIN = "agentdom.100200.ru"

# Заголовки для запросов
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

class SiteDownloader:
    def __init__(self):
        self.downloaded_urls = set()
        self.failed_urls = set()
        self.url_queue = deque()
        self.local_site_dir = "complete_local_site"
        
    def create_directory_structure(self):
        """Создает базовую структуру папок"""
        directories = [
            self.local_site_dir,
            f"{self.local_site_dir}/uploads",
            f"{self.local_site_dir}/wp-content",
            f"{self.local_site_dir}/wp-content/themes",
            f"{self.local_site_dir}/wp-content/themes/theme",
            f"{self.local_site_dir}/wp-content/themes/theme/assets",
            f"{self.local_site_dir}/wp-content/themes/theme/assets/css",
            f"{self.local_site_dir}/wp-content/themes/theme/assets/js",
            f"{self.local_site_dir}/wp-content/themes/theme/assets/img",
            f"{self.local_site_dir}/wp-content/uploads",
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Создана папка: {directory}")
    
    def normalize_url(self, url):
        """Нормализует URL"""
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = BASE_URL + url
        
        # Убираем якоря и параметры для уникальности
        parsed = urlparse(url)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        return clean_url
    
    def is_valid_page_url(self, url):
        """Проверяет, является ли URL валидной страницей для скачивания"""
        parsed = urlparse(url)
        
        # Проверяем домен
        if parsed.netloc != BASE_DOMAIN:
            return False
        
        # Исключаем файлы
        excluded_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js', '.ico', '.zip', '.rar']
        if any(url.lower().endswith(ext) for ext in excluded_extensions):
            return False
        
        # Исключаем служебные страницы WordPress
        excluded_paths = [
            '/wp-admin/',
            '/wp-includes/',
            '/wp-content/uploads/',
            '/xmlrpc.php',
            '/feed/',
            '/sitemap',
            '/robots.txt',
            '/favicon.ico'
        ]
        
        if any(path in url for path in excluded_paths):
            return False
        
        return True
    
    def extract_links_from_page(self, html_content, current_url):
        """Извлекает все ссылки со страницы"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        # Ищем все ссылки
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            normalized_url = self.normalize_url(full_url)
            
            if self.is_valid_page_url(normalized_url):
                links.add(normalized_url)
        
        # Ищем ссылки в формах
        for form in soup.find_all('form', action=True):
            action = form['action']
            full_url = urljoin(current_url, action)
            normalized_url = self.normalize_url(full_url)
            
            if self.is_valid_page_url(normalized_url):
                links.add(normalized_url)
        
        return links
    
    def get_local_path(self, url):
        """Определяет локальный путь для URL"""
        parsed = urlparse(url)
        path = parsed.path
        
        # Убираем слеш в начале
        if path.startswith('/'):
            path = path[1:]
        
        # Если путь пустой, это главная страница
        if not path or path == '':
            return f"{self.local_site_dir}/index.html"
        
        # Если путь заканчивается слешем, добавляем index.html
        if path.endswith('/'):
            return f"{self.local_site_dir}/{path}index.html"
        
        # Если это файл с расширением, оставляем как есть
        if '.' in path.split('/')[-1]:
            return f"{self.local_site_dir}/{path}"
        
        # Иначе добавляем index.html
        return f"{self.local_site_dir}/{path}/index.html"
    
    def download_page(self, url):
        """Скачивает страницу"""
        try:
            print(f"Скачиваю: {url}")
            
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            # Определяем локальный путь
            local_path = self.get_local_path(url)
            
            # Создаем папку если не существует
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Сохраняем HTML
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Сохранено: {local_path}")
            return response.text, True
            
        except Exception as e:
            print(f"Ошибка при скачивании {url}: {e}")
            return None, False
    
    def fix_local_links(self, html_content):
        """Исправляет ссылки для локального использования"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Заменяем все ссылки на agentdom.100200.ru на локальные
        for link in soup.find_all('a', href=True):
            href = link['href']
            if BASE_DOMAIN in href:
                parsed = urlparse(href)
                new_href = parsed.path
                if parsed.query:
                    new_href += '?' + parsed.query
                link['href'] = new_href
        
        # Заменяем все ссылки на изображения
        for img in soup.find_all('img', src=True):
            src = img['src']
            if BASE_DOMAIN in src:
                parsed = urlparse(src)
                new_src = parsed.path
                img['src'] = new_src
        
        # Заменяем ссылки в CSS
        for link in soup.find_all('link', href=True):
            href = link['href']
            if BASE_DOMAIN in href:
                parsed = urlparse(href)
                new_href = parsed.path
                link['href'] = new_href
        
        # Заменяем ссылки в скриптах
        for script in soup.find_all('script', src=True):
            src = script['src']
            if BASE_DOMAIN in src:
                parsed = urlparse(src)
                new_src = parsed.path
                script['src'] = new_src
        
        # Заменяем action в формах
        for form in soup.find_all('form', action=True):
            action = form['action']
            if BASE_DOMAIN in action:
                parsed = urlparse(action)
                new_action = parsed.path
                form['action'] = new_action
        
        return str(soup)
    
    def copy_existing_files(self):
        """Копирует уже существующие файлы"""
        import shutil
        
        print("Копирую существующие файлы...")
        
        # Копируем CSS файлы
        css_files = [
            "agentdom_template/wp-content_themes_theme_assets_css_main.css",
            "agentdom_template/wp-content_themes_theme_assets_css_style.min.css"
        ]
        
        for css_file in css_files:
            if os.path.exists(css_file):
                filename = os.path.basename(css_file)
                shutil.copy2(css_file, f"{self.local_site_dir}/wp-content/themes/theme/assets/css/{filename}")
                print(f"Скопирован CSS: {filename}")
        
        # Копируем JS файлы
        js_files = [
            "agentdom_template/wp-content_themes_theme_assets_js_main.js",
            "agentdom_template/wp-content_themes_theme_assets_js_script.js"
        ]
        
        for js_file in js_files:
            if os.path.exists(js_file):
                filename = os.path.basename(js_file)
                shutil.copy2(js_file, f"{self.local_site_dir}/wp-content/themes/theme/assets/js/{filename}")
                print(f"Скопирован JS: {filename}")
        
        # Копируем изображения
        image_files = [
            f for f in os.listdir("agentdom_template") 
            if f.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))
        ]
        
        for image_file in image_files:
            shutil.copy2(
                f"agentdom_template/{image_file}",
                f"{self.local_site_dir}/uploads/{image_file}"
            )
            print(f"Скопировано изображение: {image_file}")
    
    def download_complete_site(self):
        """Скачивает весь сайт рекурсивно"""
        print("Начинаю полное скачивание сайта...")
        
        # Создаем структуру папок
        self.create_directory_structure()
        
        # Начинаем с главной страницы
        start_url = BASE_URL + "/"
        self.url_queue.append(start_url)
        
        processed_count = 0
        
        while self.url_queue:
            current_url = self.url_queue.popleft()
            
            # Пропускаем уже скачанные URL
            if current_url in self.downloaded_urls:
                continue
            
            # Скачиваем страницу
            html_content, success = self.download_page(current_url)
            
            if success:
                self.downloaded_urls.add(current_url)
                processed_count += 1
                
                # Извлекаем ссылки со страницы
                new_links = self.extract_links_from_page(html_content, current_url)
                
                # Добавляем новые ссылки в очередь
                for link in new_links:
                    if link not in self.downloaded_urls and link not in self.failed_urls:
                        self.url_queue.append(link)
                
                # Исправляем ссылки в скачанной странице
                try:
                    local_path = self.get_local_path(current_url)
                    fixed_content = self.fix_local_links(html_content)
                    
                    with open(local_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    print(f"Исправлены ссылки в: {local_path}")
                    
                except Exception as e:
                    print(f"Ошибка при исправлении ссылок в {local_path}: {e}")
                
                print(f"Обработано страниц: {processed_count}, В очереди: {len(self.url_queue)}")
                
            else:
                self.failed_urls.add(current_url)
            
            # Пауза между запросами
            time.sleep(1)
        
        print(f"\nСкачивание завершено!")
        print(f"Успешно скачано: {len(self.downloaded_urls)} страниц")
        print(f"Не удалось скачать: {len(self.failed_urls)} страниц")
        
        if self.failed_urls:
            print("\nНеудачные URL:")
            for url in self.failed_urls:
                print(f"  - {url}")
        
        # Копируем существующие файлы
        self.copy_existing_files()
        
        return len(self.downloaded_urls), len(self.failed_urls)

def main():
    print("Полное скачивание сайта agentdom.100200.ru")
    print("=" * 50)
    
    downloader = SiteDownloader()
    success_count, failed_count = downloader.download_complete_site()
    
    print(f"\nГотово! Локальный сайт создан в папке '{downloader.local_site_dir}'")
    print(f"Скачано страниц: {success_count}")
    print(f"Ошибок: {failed_count}")
    
    if success_count > 0:
        print("\nСтруктура созданного сайта:")
        print(f"   {downloader.local_site_dir}/")
        print("   ├── index.html (главная)")
        print("   ├── services/")
        print("   ├── catalog/")
        print("   ├── portfolios/")
        print("   ├── uploads/ (изображения)")
        print("   └── wp-content/ (стили и скрипты)")

if __name__ == "__main__":
    main()
