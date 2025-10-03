#!/usr/bin/env python3
"""
Альтернативный простой HTTP сервер
"""

import os
import sys

def start_simple_server():
    """Запускает простой HTTP сервер"""
    
    # Проверяем, существует ли папка с сайтом
    if not os.path.exists("complete_local_site"):
        print("Ошибка: Папка 'complete_local_site' не найдена!")
        print("Убедитесь, что вы находитесь в правильной директории.")
        return
    
    print("Запуск простого HTTP сервера...")
    print("Переходим в папку complete_local_site")
    
    # Переходим в папку с сайтом
    os.chdir("complete_local_site")
    
    print("Сервер запущен!")
    print("Откройте браузер и перейдите по одному из адресов:")
    print("  http://localhost:8000")
    print("  http://127.0.0.1:8000")
    print("\nНажмите Ctrl+C для остановки")
    
    # Запускаем встроенный HTTP сервер Python
    try:
        os.system("python -m http.server 8000")
    except KeyboardInterrupt:
        print("\nСервер остановлен")

if __name__ == "__main__":
    start_simple_server()
