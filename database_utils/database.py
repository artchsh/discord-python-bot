from database_utils import init

db = init.db
cursor = db.cursor()

def checkCreateDatabase(database_name: str):
    cursor.execute("SHOW DATABASES")
    databases = []
    for x in cursor:
        databases.append(x[0])
    if database_name in databases:
        print(f"Database {database_name} is already exists.")
        return
    else:
        print(f"Creating database {database_name}...")
        cursor.execute(f'CREATE DATABASE {database_name}')
    
    

    