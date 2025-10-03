@echo off
echo Запуск локального сервера для сайта...
echo.

if not exist "complete_local_site" (
    echo Ошибка: Папка 'complete_local_site' не найдена!
    echo Убедитесь, что вы находитесь в правильной директории.
    pause
    exit /b 1
)

echo Переходим в папку complete_local_site...
cd complete_local_site

echo.
echo Сервер запущен!
echo Откройте браузер и перейдите по адресу: http://localhost:8000
echo.
echo Нажмите Ctrl+C для остановки сервера
echo.

python -m http.server 8000

echo.
echo Сервер остановлен.
pause
