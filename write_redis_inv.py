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

def write_tweet(connection, user_id, tweet, ufollowee):
    with connection.cursor() as cursor:
        # Obtenemos los usuarios que sigue
        cursor.execute("INSERT INTO Tweets (sender_id, text, timestamp) VALUES (%s, %s, NOW())", (user_id, tweet))
        connection.commit()

         # Nos conectamos al cache
        r = redis.Redis(host='localhost', port=6379, db=0)
        # Invalidamos la cache

        for user_del in ufollowee:
            r.delete(f"timeline_{user_del}")
        
        # r.delete(f"timeline_{user_id}") # FIXME No debería invalidar la cache del que escribe si no de sus seguidores.
                                        # FIXME Lo correcto es agregar el tweet al timeline de los seguidores.
    print ("Tweet enviado")

def user_followee_list(connection, user_id):
    with connection.cursor() as cursor:
        # Obtenemos los usuarios que sigue
        cursor.execute("""
        SELECT DISTINCT (t.sender_id)
            FROM Tweets t 
            JOIN Follows f ON f.user_followee_id = t.sender_id
            JOIN Users u ON u.user_id = f.user_follow_id 
            WHERE
            u.user_id = %s
        """, (user_id,))
        timeline = cursor.fetchall()
        print("timeline deleted on redis:",timeline)

        users_list = []
        for tweet in timeline:
            users_list.append(tweet['sender_id'])

        return users_list

if __name__ == "__main__":
    connection = connect_to_database("localhost", "root", "123456", "tweets")
    user_id = int(sys.argv[1])
    tweet = sys.argv[2]
    ufollowee = user_followee_list(connection, user_id)
    write_tweet(connection, user_id, tweet, ufollowee)