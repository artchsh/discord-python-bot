from database_utils import init
import mysql.connector

db = init.db
cursor = db.cursor()

def checkTable():
    _SQL = '''
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            description VARCHAR(255) DEFAULT '',
            type VARCHAR(255) DEFAILT 'item',
            price INT DEFAULT 0
        );
    '''
    cursor.execute(_SQL)
    
def get(item_id: int):
    _SQL = '''
        SELECT *
        FROM items
        WHERE id = %d;
    '''
    cursor.execute(_SQL, (item_id,))
    result = cursor.fetchall()
    return result[0]
    
def create(name: str, description: str, type: str, price: int):
    try:
        _SQL = '''
            INSERT INTO items
            (name, description, type, price)
            VALUES
            (%s, %s, %s, %d);
        '''
        cursor.execute(_SQL, (name, description, type, price,))
        db.commit()
    except mysql.connector.Error as e:
        print(e)