import mysql.connector
from config import MYSQL_CREDENTIALS

def connect():
    conn = None
    
    try: 
        conn = mysql.connector.connect(
            host=MYSQL_CREDENTIALS["host"],
            user=MYSQL_CREDENTIALS["user"],
            password=MYSQL_CREDENTIALS["password"],
            database=MYSQL_CREDENTIALS["database"]
        )
        print(f"MYSQL Database {MYSQL_CREDENTIALS['database']} is connected!")
    except mysql.connector.Error as e:
        print(e)
    
    return conn

db = connect()
