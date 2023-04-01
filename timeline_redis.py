import pymysql
import sys
import redis
import json

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

def get_user_timeline(connection, user_id):
    # Deberia verificar en CACHE (Redis) si el timeline ya esta en cache

    # Nos conectamos a la BBDD
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Intetamos traer el timeline del usuario. Ej timeline_1
    print(f"Buscando timeline_{user_id} en CACHE")
    key = f"timeline_{user_id}"

    timeline = r.lrange(key, 0, -1)

    if timeline:
        print("El timeline esta en CACHE")
        # Si el timeline es distinto de null, entonces este es un string que representa un JSON
        return [json.loads(tweet) for tweet in timeline][0]
    else :
        print("El timeline no esta en CACHE")
        # Consultamos a la BBDD del usuario por el timeline y lo almacenamos en CACHE
        with connection.cursor() as cursor:
            # Obtenemos los usuarios que sigue
            cursor.execute("""
            SELECT t.sender_id, t.text, t.timestamp 
                FROM Tweets t 
                JOIN Follows f ON f.user_followee_id = t.sender_id
                JOIN Users u ON u.user_id = f.user_follow_id 
                WHERE
                u.user_id = %s
                ORDER BY timestamp DESC; 
            """, (user_id,))
            timeline_mysql = cursor.fetchall()
            # Procesamos las fechas:
            converted_list = []
            for d in timeline_mysql:
                d["timestamp"] = d["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                converted_list.append(d)
            # Guardamos el timeline en CACHE
            print("Guardando timeline en CACHE")
            r.lpush(key, json.dumps(converted_list) )
            return timeline_mysql

if __name__ == "__main__":
    connection = connect_to_database("localhost", "root", "123456", "twitter")
    user_id = int(sys.argv[1])
    timeline = get_user_timeline(connection, user_id)
    # print(timeline[0])
    for tweet in timeline:
        print(f"{tweet['sender_id']} - {tweet['timestamp']}: {tweet['text']}")
