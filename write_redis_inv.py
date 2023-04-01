import pymysql
import sys
import redis

def connect_to_database(host, user, password, db_name):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def write_tweet(connection, user_id, tweet):
    with connection.cursor() as cursor:
        # Obtenemos los usuarios que sigue
        cursor.execute("INSERT INTO Tweets (sender_id, text, timestamp) VALUES (%s, %s, NOW())", (user_id, tweet))
        connection.commit()
         # Nos conectamos al cache
        r = redis.Redis(host='localhost', port=6379, db=0)
        # Invalidamos la cache
        r.delete(f"timeline_{user_id}") # FIXME No debería invalidar la cache del que escribe si no de sus seguidores.
                                        # FIXME Lo correcto es agregar el tweet al timeline de los seguidores.
    print ("Tweet enviado")

if __name__ == "__main__":
    connection = connect_to_database("localhost", "root", "123456", "twitter")
    user_id = int(sys.argv[1])
    tweet = sys.argv[2]
    write_tweet(connection, user_id, tweet)