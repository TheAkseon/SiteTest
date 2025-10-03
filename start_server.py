#!/usr/bin/env python3
"""
Простой HTTP сервер для тестирования локального сайта
"""

import http.server
import socketserver
import os
import webbrowser
import socket
from pathlib import Path

def find_free_port(start_port=8000):
    """Находит свободный порт"""
    port = start_port
    while port < start_port + 100:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            port += 1
    return None

def start_server(port=None):
    """Запускает HTTP сервер"""
    
    # Проверяем, существует ли папка с сайтом
    if not os.path.exists("complete_local_site"):
        print("Ошибка: Папка 'complete_local_site' не найдена!")
        print("Убедитесь, что вы находитесь в правильной директории.")
        return
    
    # Переходим в папку с сайтом
    original_dir = os.getcwd()
    os.chdir("complete_local_site")
    
    try:
        # Находим свободный порт
        if port is None:
            port = find_free_port()
            if port is None:
                print("Ошибка: Не удалось найти свободный порт!")
                return
        
        # Создаем обработчик
        handler = http.server.SimpleHTTPRequestHandler
        
        # Запускаем сервер
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Сервер запущен на http://localhost:{port}")
            print("Нажмите Ctrl+C для остановки")
            
            # Открываем браузер
            try:
                webbrowser.open(f"http://localhost:{port}")
            except Exception as e:
                print(f"Не удалось открыть браузер: {e}")
                print(f"Откройте браузер вручную: http://localhost:{port}")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nСервер остановлен")
    
    finally:
        # Возвращаемся в исходную директорию
        os.chdir(original_dir)

if __name__ == "__main__":
    start_server()
