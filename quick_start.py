#!/usr/bin/env python3
"""
Быстрый запуск анализатора безопасности
Простой интерфейс для тестирования сайта 100200.ru
"""

import sys
import os
from pathlib import Path

def main():
    print("🔐 Быстрый анализатор безопасности сайта 100200.ru")
    print("=" * 60)
    
    # Проверяем наличие необходимых файлов
    required_files = ['security_analyzer.py', 'vulnerability_scanner.py', 'template_extractor.py']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        print("Убедитесь, что все файлы находятся в текущей директории")
        return
    
    print("✅ Все необходимые файлы найдены")
    print()
    
    # Меню выбора
    while True:
        print("Выберите действие:")
        print("1. 🔍 Полный анализ безопасности")
        print("2. 🛡️ Только сканирование уязвимостей")
        print("3. 📁 Только извлечение шаблонов")
        print("4. ⚙️ Настройки")
        print("5. ❌ Выход")
        print()
        
        choice = input("Введите номер (1-5): ").strip()
        
        if choice == '1':
            print("\n🔐 Запуск полного анализа...")
            os.system("python security_analyzer.py --url https://100200.ru")
            break
            
        elif choice == '2':
            print("\n🛡️ Запуск сканирования уязвимостей...")
            os.system("python security_analyzer.py --url https://100200.ru --scan-only")
            break
            
        elif choice == '3':
            print("\n📁 Запуск извлечения шаблонов...")
            os.system("python security_analyzer.py --url https://100200.ru --extract-only")
            break
            
        elif choice == '4':
            print("\n⚙️ Настройки:")
            delay = input("Задержка между запросами (сек, по умолчанию 1.0): ").strip()
            if not delay:
                delay = "1.0"
            
            url = input("URL для анализа (по умолчанию https://100200.ru): ").strip()
            if not url:
                url = "https://100200.ru"
                
            print(f"\nЗапуск с настройками: URL={url}, задержка={delay}с")
            os.system(f"python security_analyzer.py --url {url} --delay {delay}")
            break
            
        elif choice == '5':
            print("👋 До свидания!")
            break
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
