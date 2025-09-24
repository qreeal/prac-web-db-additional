from flask import Flask, render_template_string, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'app_user',
    'password': '',
    'database': 'user_management'
}

def db_connect():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

# Простой CSS
CSS = '''
<style>
    body {
        font-family: Arial, sans-serif;
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        background: #f5f5f5;
    }
    .header {
        background: #2c3e50;
        color: white;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .nav {
        display: flex;
        gap: 20px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        flex: 1;
        min-width: 250px;
    }
    .btn {
        background: #3498db;
        color: white;
        padding: 10px 15px;
        text-decoration: none;
        border-radius: 3px;
        display: inline-block;
        margin: 5px;
    }
    .btn:hover {
        background: #2980b9;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        margin: 20px 0;
    }
    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background: #34495e;
        color: white;
    }
    tr:hover {
        background: #f5f5f5;
    }
    .user-info {
        background: white;
        padding: 20px;
        border-radius: 5px;
        margin: 20px 0;
    }
    .status-active {
        color: green;
        font-weight: bold;
    }
    .status-inactive {
        color: red;
        font-weight: bold;
    }
    input[type="text"], input[type="number"] {
        width: 100%;
        padding: 8px;
        margin: 5px 0;
        border: 1px solid #ddd;
        border-radius: 3px;
    }
    input[type="submit"] {
        background: #27ae60;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }
</style>
'''

@app.route('/')
def index():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Управление пользователями</title>
        {CSS}
    </head>
    <body>
        <div class="header">
            <h1>📊 Система управления пользователями</h1>
        </div>
        
        <div class="nav">
            <div class="card">
                <h3>👥 Все пользователи</h3>
                <p>Список активных пользователей</p>
                <a href="/users" class="btn">Открыть список</a>
            </div>
            
            <div class="card">
                <h3>🔍 Поиск по логину</h3>
                <form action="/by-login">
                    <input type="text" name="login" placeholder="Введите логин" required>
                    <input type="submit" value="Найти">
                </form>
            </div>
            
            <div class="card">
                <h3>🔎 Поиск по ID</h3>
                <form action="/by-id">
                    <input type="number" name="id" placeholder="Введите ID" required>
                    <input type="submit" value="Найти">
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/users')
def users():
    conn = db_connect()
    if conn is None:
        return "Ошибка подключения к базе данных"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, login FROM users WHERE status = TRUE')
        active_users = cursor.fetchall()

        html = f'''
        <!DOCTYPE html>
        <html>
        <head><title>Активные пользователи</title>{CSS}</head>
        <body>
            <div class="header">
                <h1>👥 Активные пользователи</h1>
            </div>
            
            <a href="/" class="btn">← Назад</a>
            
            <table>
                <tr>
                    <th>ID</th>
                    <th>Логин</th>
                    <th>Действия</th>
                </tr>
        '''
        
        for user in active_users:
            html += f'''
                <tr>
                    <td><strong>{user['id']}</strong></td>
                    <td>{user['login']}</td>
                    <td>
                        <a href="/by-id?id={user['id']}" class="btn">Просмотр</a>
                    </td>
                </tr>
            '''
        
        html += f'''
            </table>
            <p>Найдено пользователей: {len(active_users)}</p>
        </body>
        </html>
        '''
        
        return html

    except mysql.connector.Error as e:
        return f"Ошибка базы данных: {e}"
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/by-login')
def by_login():
    login = request.args.get('login', '')
    if not login:
        return "Не указан логин. <a href='/' class='btn'>Назад</a>"

    conn = db_connect()
    if conn is None:
        return "Ошибка подключения к базе данных"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, login, status FROM users WHERE login = %s', (login,))
        user = cursor.fetchone()

        if user is None:
            return f'''
            <!DOCTYPE html>
            <html>
            <head><title>Ошибка</title>{CSS}</head>
            <body>
                <div class="header">
                    <h1>❌ Пользователь не найден</h1>
                </div>
                <p>Пользователь "{login}" не найден.</p>
                <a href="/" class="btn">На главную</a>
            </body>
            </html>
            '''

        status_text = "активен" if user['status'] else "неактивен"
        status_class = "status-active" if user['status'] else "status-inactive"

        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Пользователь {user['login']}</title>{CSS}</head>
        <body>
            <div class="header">
                <h1>👤 Найден пользователь</h1>
            </div>
            
            <a href="/" class="btn">← Назад</a>
            
            <div class="user-info">
                <h3>Информация о пользователе:</h3>
                <p><strong>ID:</strong> {user['id']}</p>
                <p><strong>Логин:</strong> {user['login']}</p>
                <p><strong>Статус:</strong> <span class="{status_class}">{status_text}</span></p>
            </div>
        </body>
        </html>
        '''

    except mysql.connector.Error as e:
        return f"Ошибка базы данных: {e}"
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/by-id')
def by_id():
    user_id = request.args.get('id', type=int)
    if user_id is None:
        return "Неверный ID. <a href='/' class='btn'>Назад</a>"

    conn = db_connect()
    if conn is None:
        return "Ошибка подключения к базе данных"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, login, status FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()

        if user is None:
            return f'''
            <!DOCTYPE html>
            <html>
            <head><title>Ошибка</title>{CSS}</head>
            <body>
                <div class="header">
                    <h1>❌ Пользователь не найден</h1>
                </div>
                <p>Пользователь с ID {user_id} не найден.</p>
                <a href="/" class="btn">На главную</a>
            </body>
            </html>
            '''

        status_text = "активен" if user['status'] else "неактивен"
        status_class = "status-active" if user['status'] else "status-inactive"

        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Пользователь #{user['id']}</title>{CSS}</head>
        <body>
            <div class="header">
                <h1>👤 Найден пользователь</h1>
            </div>
            
            <a href="/" class="btn">← Назад</a>
            
            <div class="user-info">
                <h3>Информация о пользователе:</h3>
                <p><strong>ID:</strong> {user['id']}</p>
                <p><strong>Логин:</strong> {user['login']}</p>
                <p><strong>Статус:</strong> <span class="{status_class}">{status_text}</span></p>
            </div>
        </body>
        </html>
        '''

    except mysql.connector.Error as e:
        return f"Ошибка базы данных: {e}"
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)