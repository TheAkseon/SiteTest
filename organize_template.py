#!/usr/bin/env python3
"""
Скрипт для организации файлов шаблона агентства недвижимости
Перемещает все файлы, относящиеся к шаблону agentdom.100200.ru, в отдельную папку
"""

import os
import shutil
import json
from pathlib import Path

def organize_template():
    """Организация файлов шаблона агентства недвижимости"""
    
    # Пути
    base_dir = Path(".")
    extracted_dir = base_dir / "extracted_templates"
    template_dir = base_dir / "agentdom_template"
    
    # Создаем структуру папок для шаблона
    template_dirs = {
        'css': template_dir / 'css',
        'js': template_dir / 'js', 
        'images': template_dir / 'images',
        'assets': template_dir / 'assets',
        'screenshots': template_dir / 'screenshots'
    }
    
    for dir_path in template_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("📁 Создана структура папок для шаблона агентства недвижимости")
    
    # Читаем метаданные извлечения
    metadata_file = extracted_dir / "extraction_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        print(f"📊 Найдено {metadata['total_files']} файлов из {metadata['base_url']}")
        
        # Фильтруем файлы, относящиеся к agentdom.100200.ru
        agentdom_files = []
        for file_info in metadata['files']:
            if 'agentdom.100200.ru' in file_info['url']:
                agentdom_files.append(file_info)
        
        print(f"🎯 Найдено {len(agentdom_files)} файлов шаблона агентства недвижимости")
        
        # Перемещаем файлы по категориям
        moved_files = {
            'css': 0,
            'js': 0,
            'images': 0,
            'other': 0
        }
        
        for file_info in agentdom_files:
            source_path = Path(file_info['path'])
            filename = file_info['filename']
            file_type = file_info['type']
            
            if source_path.exists():
                # Определяем целевую папку
                if file_type == 'css':
                    target_dir = template_dirs['css']
                    moved_files['css'] += 1
                elif file_type == 'js':
                    target_dir = template_dirs['js']
                    moved_files['js'] += 1
                elif file_type == 'images':
                    target_dir = template_dirs['images']
                    moved_files['images'] += 1
                else:
                    target_dir = template_dirs['assets']
                    moved_files['other'] += 1
                
                # Копируем файл
                target_path = target_dir / filename
                try:
                    shutil.copy2(source_path, target_path)
                    print(f"✅ Скопирован: {filename} -> {target_dir.name}/")
                except Exception as e:
                    print(f"❌ Ошибка копирования {filename}: {e}")
        
        # Также перемещаем файлы из папки other, которые относятся к шаблону
        other_dir = extracted_dir / "other"
        if other_dir.exists():
            for file_path in other_dir.iterdir():
                if file_path.is_file():
                    filename = file_path.name
                    
                    # Определяем тип файла по расширению
                    if filename.endswith('.css'):
                        target_dir = template_dirs['css']
                        moved_files['css'] += 1
                    elif filename.endswith('.js'):
                        target_dir = template_dirs['js']
                        moved_files['js'] += 1
                    elif filename.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
                        target_dir = template_dirs['images']
                        moved_files['images'] += 1
                    else:
                        target_dir = template_dirs['assets']
                        moved_files['other'] += 1
                    
                    target_path = target_dir / filename
                    try:
                        shutil.copy2(file_path, target_path)
                        print(f"✅ Скопирован: {filename} -> {target_dir.name}/")
                    except Exception as e:
                        print(f"❌ Ошибка копирования {filename}: {e}")
        
        # Перемещаем изображения из папки images
        images_dir = extracted_dir / "images"
        if images_dir.exists():
            for file_path in images_dir.iterdir():
                if file_path.is_file():
                    filename = file_path.name
                    target_path = template_dirs['images'] / filename
                    try:
                        shutil.copy2(file_path, target_path)
                        moved_files['images'] += 1
                        print(f"✅ Скопирован: {filename} -> images/")
                    except Exception as e:
                        print(f"❌ Ошибка копирования {filename}: {e}")
        
        # Перемещаем JS файлы
        js_dir = extracted_dir / "js"
        if js_dir.exists():
            for file_path in js_dir.iterdir():
                if file_path.is_file():
                    filename = file_path.name
                    target_path = template_dirs['js'] / filename
                    try:
                        shutil.copy2(file_path, target_path)
                        moved_files['js'] += 1
                        print(f"✅ Скопирован: {filename} -> js/")
                    except Exception as e:
                        print(f"❌ Ошибка копирования {filename}: {e}")
        
        # Перемещаем CSS файлы
        css_dir = extracted_dir / "css"
        if css_dir.exists():
            for file_path in css_dir.iterdir():
                if file_path.is_file():
                    filename = file_path.name
                    target_path = template_dirs['css'] / filename
                    try:
                        shutil.copy2(file_path, target_path)
                        moved_files['css'] += 1
                        print(f"✅ Скопирован: {filename} -> css/")
                    except Exception as e:
                        print(f"❌ Ошибка копирования {filename}: {e}")
        
        # Создаем README файл для шаблона
        readme_content = f"""# Шаблон сайта агентства недвижимости

Этот шаблон был извлечен с сайта agentdom.100200.ru

## Структура файлов

- **css/** - Стили CSS ({moved_files['css']} файлов)
- **js/** - JavaScript файлы ({moved_files['js']} файлов)  
- **images/** - Изображения ({moved_files['images']} файлов)
- **assets/** - Прочие ресурсы ({moved_files['other']} файлов)

## Основные файлы

### CSS
- main.css - основные стили темы
- style.min.css - стили WordPress блоков
- fancybox.css - стили для галереи

### JavaScript
- main.js - основной функционал сайта
- script.js - дополнительные скрипты
- fancybox.umd.js - библиотека галереи
- jquery.mask.min.js - маски для форм

### Изображения
- Иконки социальных сетей
- Фотографии объектов недвижимости
- SVG иконки и элементы дизайна

## Использование

Этот шаблон можно использовать как основу для создания сайта агентства недвижимости.

**Внимание:** Убедитесь, что у вас есть права на использование этих файлов.
"""
        
        readme_path = template_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n📋 Создан README.md с описанием шаблона")
        
        # Выводим итоговую статистику
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"📁 CSS файлы: {moved_files['css']}")
        print(f"📁 JavaScript файлы: {moved_files['js']}")
        print(f"📁 Изображения: {moved_files['images']}")
        print(f"📁 Прочие файлы: {moved_files['other']}")
        print(f"📁 Всего файлов: {sum(moved_files.values())}")
        
        print(f"\n✅ Шаблон агентства недвижимости успешно организован в папке: {template_dir}")
        
    else:
        print("❌ Файл метаданных не найден")

if __name__ == "__main__":
    organize_template()
