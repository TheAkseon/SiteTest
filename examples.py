#!/usr/bin/env python3
"""
Примеры использования анализатора безопасности
Демонстрация различных сценариев тестирования
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Выполнение команды с описанием"""
    print(f"\n🔧 {description}")
    print(f"Команда: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Команда выполнена успешно")
            if result.stdout:
                print("Вывод:")
                print(result.stdout)
        else:
            print("❌ Ошибка выполнения команды")
            if result.stderr:
                print("Ошибка:")
                print(result.stderr)
    except Exception as e:
        print(f"❌ Исключение: {e}")

def main():
    print("📚 Примеры использования анализатора безопасности")
    print("=" * 60)
    
    examples = [
        {
            "command": "python security_analyzer.py --url https://100200.ru",
            "description": "Базовое сканирование главного сайта"
        },
        {
            "command": "python security_analyzer.py --url https://bansaun.100200.ru --delay 2.0",
            "description": "Сканирование поддомена с увеличенной задержкой"
        },
        {
            "command": "python security_analyzer.py --url https://100200.ru --scan-only",
            "description": "Только поиск уязвимостей без извлечения файлов"
        },
        {
            "command": "python security_analyzer.py --url https://100200.ru --extract-only",
            "description": "Только извлечение шаблонов без сканирования уязвимостей"
        },
        {
            "command": "python vulnerability_scanner.py --url https://100200.ru --delay 1.5",
            "description": "Использование только сканера уязвимостей"
        },
        {
            "command": "python template_extractor.py --url https://100200.ru --output my_templates",
            "description": "Извлечение шаблонов в кастомную директорию"
        }
    ]
    
    print("Доступные примеры:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['description']}")
    
    print("\nВыберите пример для выполнения (1-6) или 0 для выхода:")
    
    try:
        choice = int(input("Введите номер: "))
        
        if choice == 0:
            print("👋 До свидания!")
            return
        elif 1 <= choice <= len(examples):
            example = examples[choice - 1]
            
            print(f"\n⚠️ ВНИМАНИЕ: Будет выполнена команда:")
            print(f"   {example['command']}")
            print(f"\nЭто может занять некоторое время...")
            
            confirm = input("Продолжить? (y/N): ").strip().lower()
            if confirm in ['y', 'yes', 'да']:
                run_command(example['command'], example['description'])
            else:
                print("❌ Отменено пользователем")
        else:
            print("❌ Неверный выбор")
            
    except ValueError:
        print("❌ Введите корректный номер")
    except KeyboardInterrupt:
        print("\n❌ Прервано пользователем")

if __name__ == "__main__":
    main()
