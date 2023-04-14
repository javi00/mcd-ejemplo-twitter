CREATE DATABASE tweets;
USE tweets;

CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  screen_name VARCHAR(255) NOT NULL,
  profile_image VARCHAR(255) NOT NULL
);

CREATE TABLE Tweets (
  tweet_id INT AUTO_INCREMENT PRIMARY KEY,
  sender_id INT NOT NULL,
  text TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES Users(user_id)
);

CREATE TABLE Follows (
  user_follow_id INT NOT NULL,
  user_followee_id INT NOT NULL,
  PRIMARY KEY (user_follow_id, user_followee_id),
  FOREIGN KEY (user_follow_id) REFERENCES Users(user_id),
  FOREIGN KEY (user_followee_id) REFERENCES Users(user_id)
);

-- Inserts de prueba para la tabla Users
INSERT INTO Users (screen_name, profile_image) VALUES
('jperez1', 'https://example.com/profile_images/usuario1.png'),
('mgomez2', 'https://example.com/profile_images/usuario2.png'),
('lfernanz3', 'https://example.com/profile_images/usuario3.png'),
('marco4', 'https://example.com/profile_images/usuario4.png'),
('julio5', 'https://example.com/profile_images/usuario5.png');

-- Inserts de prueba para la tabla Tweets
INSERT INTO Tweets (sender_id, text) VALUES
(1, 'Este es mi primer tweet'),
(1, '¡Hola, mundo!'),
(1, 'Hoy es un gran día'),
(1, 'Me encanta programar'),
(1, 'Estoy aprendiendo mucho'),
(2, '¡Acabo de publicar mi primer artículo en mi blog!'),
(2, '¡Feliz viernes!'),
(2, 'Estoy disfrutando de mi fin de semana'),
(2, 'Acabo de ver una película increíble'),
(2, 'Me encanta leer libros'),
(3, 'Estoy emocionado por mi próximo viaje'),
(3, '¡Qué hermoso día hace hoy!'),
(3, 'Hoy estoy cocinando una cena especial'),
(3, 'Estoy escuchando mi álbum favorito'),
(3, '¡Estoy ganando mi apuesta!'),
(4, 'Hoy estoy en el parque jugando futbol con mis amigos'),
(4, 'Estoy aprendiendo a tocar la guitarra'),
(4, 'Acabo de terminar un proyecto importante'),
(4, 'Estoy muy feliz por los logros que he conseguido'),
(4, 'Estoy disfrutando del día en la playa'),
(5, 'Acabo de comenzar mi propio negocio'),
(5, 'Estoy trabajando duro para lograr mis objetivos'),
(5, 'Hoy estoy en una reunión importante'),
(5, 'Estoy emocionado por el futuro de mi negocio'),
(5, 'Estoy aprendiendo mucho de mis mentores');

-- Usuario 1 sigue a usuario 2 y 3
INSERT INTO Follows (user_follow_id, user_followee_id) VALUES
(1, 2),
(1, 3);

-- Usuario 2 sigue a usuario 1, 4 y 5
INSERT INTO Follows (user_follow_id, user_followee_id) VALUES
(2, 1),
(2, 4),
(2, 5);

-- Usuario 3 sigue a usuario 1 y 5
INSERT INTO Follows (user_follow_id, user_followee_id) VALUES
(3, 1),
(3, 5);

-- Usuario 4 sigue a usuario 3 y 5
INSERT INTO Follows (user_follow_id, user_followee_id) VALUES
(4, 3),
(4, 5);

-- Usuario 5 sigue a usuario 1, 2 y 4
INSERT INTO Follows (user_follow_id, user_followee_id) VALUES
(5, 1),
(5, 2),
(5, 4);


SELECT t.sender_id, t.text, t.timestamp 
FROM Tweets t 
JOIN Follows f ON f.user_followee_id = t.sender_id
JOIN Users u ON u.user_id = f.user_follow_id 
WHERE
u.user_id = 3
ORDER BY timestamp DESC;