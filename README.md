# Дополнительное тестовое задание номер 1

Веб-приложение на Flask для работы с базой данных Mysql

## Функциональность

- Главная страница с навигацией
- Просмотр списка активных пользователей
- Поиск пользователей по логину
- Поиск пользователей по ID

## Структура базы данных

### Таблица `users`
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT) - уникальный идентификатор
- `login` (VARCHAR(50), UNIQUE) - имя пользователя
- `money_amount` (INT) - количество денег
- `card_number` (VARCHAR(20), UNIQUE) - номер кредитной карты
- `status` (BOOLEAN) - статус активности (TRUE - активен, FALSE - неактивен)

### Таблица `passwords`
- `user_id` (INT, FOREIGN KEY) - ссылка на users.id
- `password` (VARCHAR(50)) - пароль пользователя

## Зависимости

- Python 3.7+
- Flask==2.3.3
- mysql-connector-python==8.1.0

## Установка и запуск

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/qreeal/prac-web-db-additional
cd prac-web-db-additional
chmod +x setup.sh run.sh
./setup.sh
./run.sh
