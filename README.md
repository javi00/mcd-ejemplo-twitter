# Maestría en Ciencia de Datos - Ejemplo Twitter.

## Cómo ejecutar este proyecto.

### Configurar el virtual env

Inicializamos el virtual env. Para inicializar un entorno virtual en Python y usar pip, sigue los siguientes pasos: 
1. Abre una terminal o línea de comandos en tu sistema operativo. 
2. Navega hasta el directorio donde deseas crear el entorno virtual. 
3. Ejecuta el siguiente comando para crear el entorno virtual:

```

python -m venv twitter
```



Donde "nombre_del_entorno" es el nombre que quieras darle al entorno virtual. 
4. Una vez creado el entorno virtual, actívalo con el siguiente comando:

```bash

source twitter/bin/activate
```


### Instalamos las dependecias.

```

pip install -r requirements.txt

```

En caso de que se desee actualizar los requerimientos: `pip freeze > requirements.txt`


Esto restablecerá el prompt de la línea de comandos a su estado original y dejará de usar el entorno virtual.

## Preparamos la BBDD Relacional.
-  A continuación el código SQL para crear las tablas en una base de datos MySQL:

```sql

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
```

La tabla "Users" tiene una columna "user_id" que actúa como clave principal y se genera automáticamente mediante el uso de "AUTO_INCREMENT". También hay dos columnas obligatorias "screen_name" y "profile_image", que representan el nombre de usuario de Twitter y la imagen de perfil, respectivamente.

La tabla "Tweets" tiene una columna "tweet_id" que actúa como clave principal y se genera automáticamente mediante el uso de "AUTO_INCREMENT". También tiene una columna "sender_id" que representa el ID del usuario que envió el tweet y se relaciona con la tabla "Users" mediante una clave externa.

La tabla "Follows" se utiliza para almacenar las relaciones de seguimiento entre los usuarios. Tiene dos columnas "user_follow_id" y "user_followee_id", que representan el ID del usuario que sigue y el ID del usuario que es seguido, respectivamente. Estas columnas se combinan para crear una clave principal compuesta. Además, cada columna se relaciona con la tabla "Users" mediante una clave externa.

### Inserts para la BBDD de ejemplo

- ¡Claro! Aquí te proporciono los inserts de prueba para 5 usuarios con más de 4 tweets cada uno en la tabla "Users" y "Tweets":

```sql

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
```



Este código inserta 5 usuarios con diferentes nombres y URLs de imagen de perfil en la tabla "Users". Además, cada usuario tiene al menos 5 tweets diferentes en la tabla "Tweets" con diferentes textos y timestamps.

### Insert para seguidores
```sql

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
```

Este código inserta algunas relaciones de seguimiento en la tabla "Follows". Por ejemplo, el usuario 1 sigue al usuario 2 y 3, mientras que el usuario 2 sigue al usuario 1, 4 y 5. El usuario 5 sigue al usuario 1, 2 y 4. Puedes agregar más relaciones de seguimiento según sea necesario.

## Consultamos el Timeline

Para obtener el timeline se debería ejecutar la siguiente consulta:

```sql
-- Me muestra el timeline del usuario 3, que solo debería tener los tweets de las personas a las que sigue.

SELECT t.sender_id, t.text, t.timestamp 
FROM Tweets t 
JOIN Follows f ON f.user_followee_id = t.sender_id
JOIN Users u ON u.user_id = f.user_follow_id 
WHERE
u.user_id = 3
ORDER BY timestamp DESC;

```



## Primera aproximación

En el archivo twitter_mysql.py se tiene la lógica tradicional de acceso.
