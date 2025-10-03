#!/usr/bin/env python3
"""
Модуль для извлечения шаблонов с сайта
Использует различные методы для получения файлов шаблонов
"""

import requests
import os
import re
import time
from urllib.parse import urljoin, urlparse
from pathlib import Path
import json
import hashlib

class TemplateExtractor:
    def __init__(self, base_url, output_dir='extracted_templates'):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.extracted_files = []
        self.failed_extractions = []
        
    def log(self, message, level="INFO"):
        """Логирование"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def make_request(self, url, **kwargs):
        """HTTP запрос с обработкой ошибок"""
        try:
            time.sleep(0.5)  # Задержка между запросами
            response = self.session.get(url, timeout=10, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"Ошибка запроса к {url}: {e}", "ERROR")
            return None
            
    def extract_from_directory_listing(self, directory_url):
        """Извлечение файлов из directory listing"""
        self.log(f"Извлечение из directory listing: {directory_url}")
        
        response = self.make_request(directory_url)
        if not response or response.status_code != 200:
            return []
            
        # Поиск ссылок на файлы
        file_links = re.findall(r'href=["\']([^"\']+)["\']', response.text)
        extracted_files = []
        
        for link in file_links:
            if link.startswith('/'):
                file_url = self.base_url + link
            else:
                file_url = urljoin(directory_url, link)
                
            # Пропускаем ссылки на директории
            if link.endswith('/') or link in ['../', './']:
                continue
                
            # Извлекаем файл
            file_content = self.extract_file(file_url)
            if file_content:
                extracted_files.append({
                    'url': file_url,
                    'filename': os.path.basename(link),
                    'size': len(file_content),
                    'method': 'directory_listing'
                })
                
        return extracted_files
        
    def extract_file(self, file_url):
        """Извлечение содержимого файла"""
        response = self.make_request(file_url)
        if response and response.status_code == 200:
            return response.content
        return None
        
    def save_file(self, content, filename, subdirectory=''):
        """Сохранение файла на диск"""
        if subdirectory:
            save_dir = self.output_dir / subdirectory
            save_dir.mkdir(exist_ok=True)
        else:
            save_dir = self.output_dir
            
        file_path = save_dir / filename
        
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            return str(file_path)
        except Exception as e:
            self.log(f"Ошибка сохранения файла {filename}: {e}", "ERROR")
            return None
            
    def extract_templates_from_source(self):
        """Извлечение шаблонов из исходного кода страниц"""
        self.log("Поиск шаблонов в исходном коде...")
        
        # Получаем главную страницу
        response = self.make_request(self.base_url)
        if not response:
            return []
            
        # Ищем ссылки на CSS, JS и другие ресурсы
        css_links = re.findall(r'href=["\']([^"\']*\.css[^"\']*)["\']', response.text)
        js_links = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', response.text)
        image_links = re.findall(r'src=["\']([^"\']*\.(?:jpg|jpeg|png|gif|svg)[^"\']*)["\']', response.text)
        
        all_links = css_links + js_links + image_links
        extracted_files = []
        
        for link in all_links:
            if link.startswith('http'):
                file_url = link
            elif link.startswith('/'):
                file_url = self.base_url + link
            else:
                file_url = urljoin(self.base_url, link)
                
            file_content = self.extract_file(file_url)
            if file_content:
                filename = os.path.basename(urlparse(file_url).path)
                if not filename:
                    filename = f"file_{hashlib.md5(file_url.encode()).hexdigest()[:8]}"
                    
                # Определяем тип файла
                if link.endswith('.css'):
                    file_type = 'css'
                elif link.endswith('.js'):
                    file_type = 'js'
                elif any(link.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']):
                    file_type = 'images'
                else:
                    file_type = 'other'
                    
                saved_path = self.save_file(file_content, filename, file_type)
                if saved_path:
                    extracted_files.append({
                        'url': file_url,
                        'filename': filename,
                        'path': saved_path,
                        'size': len(file_content),
                        'type': file_type,
                        'method': 'source_extraction'
                    })
                    
        return extracted_files
        
    def extract_from_common_paths(self):
        """Извлечение из общих путей"""
        self.log("Поиск файлов по общим путям...")
        
        common_paths = [
            '/templates/', '/themes/', '/css/', '/js/', '/images/',
            '/assets/', '/static/', '/public/', '/includes/',
            '/wp-content/themes/', '/wp-content/plugins/',
            '/admin/templates/', '/admin/css/', '/admin/js/'
        ]
        
        extracted_files = []
        
        for path in common_paths:
            url = self.base_url + path
            response = self.make_request(url)
            
            if response and response.status_code == 200:
                # Проверяем, является ли это directory listing
                if any(indicator in response.text.lower() for indicator in [
                    'index of', 'parent directory', 'directory listing'
                ]):
                    files = self.extract_from_directory_listing(url)
                    extracted_files.extend(files)
                else:
                    # Сохраняем содержимое как файл
                    filename = f"index_{path.replace('/', '_').strip('_')}.html"
                    saved_path = self.save_file(response.content, filename, 'directories')
                    if saved_path:
                        extracted_files.append({
                            'url': url,
                            'filename': filename,
                            'path': saved_path,
                            'size': len(response.content),
                            'method': 'common_path'
                        })
                        
        return extracted_files
        
    def extract_from_sitemap(self):
        """Извлечение из sitemap.xml"""
        self.log("Поиск sitemap.xml...")
        
        sitemap_urls = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemaps.xml',
            '/sitemap/sitemap.xml'
        ]
        
        extracted_files = []
        
        for sitemap_url in sitemap_urls:
            url = self.base_url + sitemap_url
            response = self.make_request(url)
            
            if response and response.status_code == 200:
                # Извлекаем URL из sitemap
                urls = re.findall(r'<loc>(.*?)</loc>', response.text)
                
                for url in urls:
                    if url.startswith(self.base_url):
                        # Проверяем, является ли это файлом шаблона
                        if any(url.endswith(ext) for ext in ['.css', '.js', '.html', '.php', '.tpl']):
                            file_content = self.extract_file(url)
                            if file_content:
                                filename = os.path.basename(urlparse(url).path)
                                saved_path = self.save_file(file_content, filename, 'sitemap')
                                if saved_path:
                                    extracted_files.append({
                                        'url': url,
                                        'filename': filename,
                                        'path': saved_path,
                                        'size': len(file_content),
                                        'method': 'sitemap'
                                    })
                                    
        return extracted_files
        
    def run_extraction(self):
        """Запуск полного извлечения"""
        self.log(f"Начинаем извлечение шаблонов с {self.base_url}")
        
        all_extracted = []
        
        # Различные методы извлечения
        methods = [
            self.extract_templates_from_source,
            self.extract_from_common_paths,
            self.extract_from_sitemap
        ]
        
        for method in methods:
            try:
                files = method()
                all_extracted.extend(files)
                self.log(f"Извлечено {len(files)} файлов методом {method.__name__}")
            except Exception as e:
                self.log(f"Ошибка в методе {method.__name__}: {e}", "ERROR")
                
        # Сохраняем метаданные
        metadata = {
            'base_url': self.base_url,
            'extraction_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_files': len(all_extracted),
            'files': all_extracted
        }
        
        metadata_path = self.output_dir / 'extraction_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            
        self.log(f"Извлечение завершено. Всего файлов: {len(all_extracted)}")
        self.log(f"Результаты сохранены в {self.output_dir}")
        
        return all_extracted
        
    def print_summary(self, extracted_files):
        """Вывод сводки извлечения"""
        print("\n" + "="*60)
        print("СВОДКА ИЗВЛЕЧЕНИЯ ШАБЛОНОВ")
        print("="*60)
        
        # Группировка по типам файлов
        file_types = {}
        for file_info in extracted_files:
            file_type = file_info.get('type', 'unknown')
            if file_type not in file_types:
                file_types[file_type] = []
            file_types[file_type].append(file_info)
            
        for file_type, files in file_types.items():
            print(f"\n{file_type.upper()}: {len(files)} файлов")
            total_size = sum(f['size'] for f in files)
            print(f"  Общий размер: {total_size:,} байт")
            
            # Показываем первые 5 файлов каждого типа
            for file_info in files[:5]:
                print(f"  - {file_info['filename']} ({file_info['size']:,} байт)")
                
            if len(files) > 5:
                print(f"  ... и еще {len(files) - 5} файлов")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Извлечение шаблонов с сайта')
    parser.add_argument('--url', default='https://100200.ru', help='URL для извлечения')
    parser.add_argument('--output', default='extracted_templates', help='Директория для сохранения')
    
    args = parser.parse_args()
    
    print("📁 Извлечение шаблонов с сайта")
    print(f"🎯 Цель: {args.url}")
    print(f"📂 Сохранение в: {args.output}")
    print("-" * 60)
    
    extractor = TemplateExtractor(args.url, args.output)
    
    try:
        extracted_files = extractor.run_extraction()
        extractor.print_summary(extracted_files)
        
    except KeyboardInterrupt:
        print("\n❌ Извлечение прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
