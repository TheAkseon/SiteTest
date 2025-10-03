#!/usr/bin/env python3
"""
Скрипт для скачивания шаблона сайта agentdom.100200.ru
Сохраняет все файлы (HTML, CSS, JS, изображения) в отдельную папку
"""

import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
import re
from pathlib import Path
import mimetypes

class WebsiteDownloader:
    def __init__(self, base_url, output_dir="agentdom_template"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.visited_urls = set()
        self.downloaded_files = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Создаем выходную папку
        self.output_dir.mkdir(exist_ok=True)
        
    def is_valid_url(self, url):
        """Проверяет, является ли URL валидным для скачивания"""
        parsed = urlparse(url)
        return parsed.netloc == urlparse(self.base_url).netloc
    
    def get_file_extension(self, url, content_type=None):
        """Определяет расширение файла по URL и content-type"""
        parsed = urlparse(url)
        path = parsed.path
        
        # Если есть расширение в пути
        if '.' in path:
            return os.path.splitext(path)[1]
        
        # Определяем по content-type
        if content_type:
            ext = mimetypes.guess_extension(content_type.split(';')[0])
            if ext:
                return ext
        
        return '.html'  # По умолчанию
    
    def sanitize_filename(self, filename):
        """Очищает имя файла от недопустимых символов"""
        # Удаляем недопустимые символы
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Удаляем множественные подчеркивания
        filename = re.sub(r'_+', '_', filename)
        return filename
    
    def download_file(self, url, local_path):
        """Скачивает файл по URL"""
        try:
            print(f"Скачиваю: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Создаем директории если нужно
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Записываем файл
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            self.downloaded_files.add(url)
            print(f"✓ Сохранено: {local_path}")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка при скачивании {url}: {e}")
            return False
    
    def extract_resources(self, html_content, base_url):
        """Извлекает все ресурсы из HTML (CSS, JS, изображения)"""
        soup = BeautifulSoup(html_content, 'html.parser')
        resources = []
        
        # CSS файлы
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                resources.append(urljoin(base_url, href))
        
        # JavaScript файлы
        for script in soup.find_all('script', src=True):
            resources.append(urljoin(base_url, script['src']))
        
        # Изображения
        for img in soup.find_all('img', src=True):
            resources.append(urljoin(base_url, img['src']))
        
        # Фоновые изображения в CSS
        for style in soup.find_all('style'):
            if style.string:
                # Ищем url() в CSS
                urls = re.findall(r'url\(["\']?([^"\']+)["\']?\)', style.string)
                for url in urls:
                    resources.append(urljoin(base_url, url))
        
        return resources
    
    def process_html(self, html_content, url):
        """Обрабатывает HTML и заменяет пути на локальные"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Заменяем пути в CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                if self.is_valid_url(full_url):
                    local_path = self.get_local_path(full_url)
                    link['href'] = str(local_path.relative_to(self.output_dir))
        
        # Заменяем пути в JavaScript
        for script in soup.find_all('script', src=True):
            src = script['src']
            full_url = urljoin(url, src)
            if self.is_valid_url(full_url):
                local_path = self.get_local_path(full_url)
                script['src'] = str(local_path.relative_to(self.output_dir))
        
        # Заменяем пути в изображениях
        for img in soup.find_all('img', src=True):
            src = img['src']
            full_url = urljoin(url, src)
            if self.is_valid_url(full_url):
                local_path = self.get_local_path(full_url)
                img['src'] = str(local_path.relative_to(self.output_dir))
        
        return str(soup)
    
    def get_local_path(self, url):
        """Определяет локальный путь для URL"""
        parsed = urlparse(url)
        path = parsed.path
        
        # Убираем начальный слеш
        if path.startswith('/'):
            path = path[1:]
        
        # Если путь пустой, используем index.html
        if not path or path.endswith('/'):
            path = 'index.html'
        
        # Добавляем расширение если его нет
        if '.' not in path:
            path += '.html'
        
        # Очищаем имя файла
        path = self.sanitize_filename(path)
        
        return self.output_dir / path
    
    def download_website(self):
        """Основной метод для скачивания сайта"""
        print(f"Начинаю скачивание сайта: {self.base_url}")
        print(f"Сохраняю в папку: {self.output_dir}")
        
        # Скачиваем главную страницу
        try:
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            html_content = response.text
            
            # Сохраняем главную страницу
            main_path = self.output_dir / 'index.html'
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✓ Главная страница сохранена: {main_path}")
            
            # Извлекаем ресурсы
            resources = self.extract_resources(html_content, self.base_url)
            print(f"Найдено ресурсов: {len(resources)}")
            
            # Скачиваем все ресурсы
            for resource_url in resources:
                if resource_url not in self.downloaded_files and self.is_valid_url(resource_url):
                    local_path = self.get_local_path(resource_url)
                    self.download_file(resource_url, local_path)
                    time.sleep(0.5)  # Небольшая пауза между запросами
            
            # Обрабатываем HTML для замены путей
            processed_html = self.process_html(html_content, self.base_url)
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(processed_html)
            
            print(f"\n✓ Скачивание завершено!")
            print(f"✓ Всего скачано файлов: {len(self.downloaded_files) + 1}")
            print(f"✓ Файлы сохранены в: {self.output_dir.absolute()}")
            
        except Exception as e:
            print(f"✗ Ошибка при скачивании сайта: {e}")

def main():
    """Главная функция"""
    base_url = "https://agentdom.100200.ru/"
    output_dir = "agentdom_template"
    
    print("=" * 60)
    print("СКАЧИВАНИЕ ШАБЛОНА САЙТА AGENTDOM")
    print("=" * 60)
    
    downloader = WebsiteDownloader(base_url, output_dir)
    downloader.download_website()
    
    print("\n" + "=" * 60)
    print("СКАЧИВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)

if __name__ == "__main__":
    main()