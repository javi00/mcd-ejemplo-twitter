import pymysql
import sys

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
        timeline = cursor.fetchall()

    return timeline

if __name__ == "__main__":
    connection = connect_to_database("localhost", "root", "123456", "twitter")
    user_id = int(sys.argv[1])
    timeline = get_user_timeline(connection, user_id)
    
    for tweet in timeline:
        print(f"{tweet['sender_id']} - {tweet['timestamp']}: {tweet['text']}")
