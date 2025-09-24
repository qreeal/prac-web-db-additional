#!/bin/bash

echo "=== Установка веб-приложения ==="

# Проверяем зависимости
if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен"
    exit 1
fi

if ! command -v mysql &> /dev/null; then
    echo "MySQL не установлен"
    exit 1
fi

python3 -m venv venv

echo "Установка зависимостей..."
. venv/bin/activate
pip install -r requirements.txt --break-system-packages

sudo mysql -e "CREATE DATABASE IF NOT EXISTS user_management;" 2>/dev/null
sudo mysql -e "DROP USER IF EXISTS 'app_user'@'localhost';" 2>/dev/null
sudo mysql -e "CREATE USER 'app_user'@'localhost' IDENTIFIED BY '';" 2>/dev/null
sudo mysql -e "GRANT ALL PRIVILEGES ON user_management.* TO 'app_user'@'localhost';" 2>/dev/null
sudo mysql -e "FLUSH PRIVILEGES;" 2>/dev/null

echo "Инициализация базы данных..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS user_management;" 2>/dev/null
sudo mysql user_management < init-db.sql 2>/dev/null
echo "База данных инициализирована"

echo "Установка завершена!"
echo ""
echo "Для запуска приложения выполните: ./run.sh"
