import os
import shutil
from pathlib import Path

# Создаем структуру папок
template_dir = Path("agentdom_template")
template_dir.mkdir(exist_ok=True)

# Создаем подпапки
for subdir in ['css', 'js', 'images', 'assets']:
    (template_dir / subdir).mkdir(exist_ok=True)

print("📁 Создана структура папок для шаблона")

# Копируем файлы из extracted_templates
extracted_dir = Path("extracted_templates")

if extracted_dir.exists():
    # Копируем CSS файлы
    css_dir = extracted_dir / "css"
    if css_dir.exists():
        for file in css_dir.iterdir():
            if file.is_file():
                shutil.copy2(file, template_dir / "css" / file.name)
                print(f"✅ CSS: {file.name}")
    
    # Копируем JS файлы
    js_dir = extracted_dir / "js"
    if js_dir.exists():
        for file in js_dir.iterdir():
            if file.is_file():
                shutil.copy2(file, template_dir / "js" / file.name)
                print(f"✅ JS: {file.name}")
    
    # Копируем изображения
    images_dir = extracted_dir / "images"
    if images_dir.exists():
        for file in images_dir.iterdir():
            if file.is_file():
                shutil.copy2(file, template_dir / "images" / file.name)
                print(f"✅ Image: {file.name}")
    
    # Копируем файлы из other (основные файлы шаблона)
    other_dir = extracted_dir / "other"
    if other_dir.exists():
        for file in other_dir.iterdir():
            if file.is_file():
                filename = file.name
                if filename.endswith('.css'):
                    shutil.copy2(file, template_dir / "css" / filename)
                    print(f"✅ CSS: {filename}")
                elif filename.endswith('.js'):
                    shutil.copy2(file, template_dir / "js" / filename)
                    print(f"✅ JS: {filename}")
                elif filename.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
                    shutil.copy2(file, template_dir / "images" / filename)
                    print(f"✅ Image: {filename}")
                else:
                    shutil.copy2(file, template_dir / "assets" / filename)
                    print(f"✅ Asset: {filename}")

print(f"\n✅ Шаблон организован в папке: {template_dir.absolute()}")
