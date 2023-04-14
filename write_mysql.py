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
    print ("Tweet enviado")

if __name__ == "__main__":
    connection = connect_to_database("localhost", "root", "123456", "tweets")
    user_id = int(sys.argv[1])
    tweet = sys.argv[2]
    write_tweet(connection, user_id, tweet)