DROP TABLE IF EXISTS passwords;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(50) NOT NULL UNIQUE,
    money_amount INT,
    card_number VARCHAR(20) UNIQUE,
    status BOOLEAN
);

CREATE TABLE IF NOT EXISTS passwords (
    user_id INT,
    password VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Очищаем таблицы, если они уже существовали
DELETE FROM passwords;
DELETE FROM users;

-- Вставляем тестовых пользователей
INSERT INTO users (login, money_amount, card_number, status) VALUES
('admin', 10 , '4539578763621486', TRUE),
('archie', 250000, '4916338590382832', TRUE),
('kinstintin', 5000000, '4556723586888855', FALSE),
('kostya', 100000, '4024000070339509', FALSE),
('vadiiiiiim', 200000, '8733329465573310', FALSE),
('yarik', 100000, '3455802550211111', TRUE),
('vova', 10, '4444444444444567', TRUE);


-- Вставляем пароли для пользователей
INSERT INTO passwords (user_id, password) VALUES
(1, 'password'),
(2, 'dantist'),
(3, 'realize'),
(4, 'Nizshe'),
(5, 'astra'),
(6, 'saint_acmetron'),
(7, 'anime');