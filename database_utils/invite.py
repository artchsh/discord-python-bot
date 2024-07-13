from database_utils import init

db = init.db
cursor = db.cursor()

def checkTable():
    _SQL = '''
        CREATE TABLE IF NOT EXISTS invites (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sender VARCHAR(255),
        recepient VARCHAR(255),
        club VARCHAR(255)
        )
    '''
    cursor.execute(_SQL)
    
    
def create(sender_id: str, recepient_id: str, club_id: str):
    _SQL = '''
        INSERT INTO invites (sender, recepient, club) VALUES (%s, %s, %s)
    '''
    cursor.execute(_SQL, (sender_id, recepient_id, club_id,))
    db.commit()
    _SQL = '''
        SELECT * FROM invites WHERE sender = %s AND recepient = %s;
    '''
    cursor.execute(_SQL, (sender_id, recepient_id,))
    result = cursor.fetchall()
    
    return result[0][0]

def isExistsById(invite_id: str):
    _SQL = '''
        SELECT * 
        FROM invites 
        WHERE id = %s;
    '''
    cursor.execute(_SQL, (invite_id,))
    result = cursor.fetchall()
    if len(result) != 0:
        return True
    return False
    
def getInfo(invite_id: str):
    _SQL = '''
        SELECT * 
        FROM invites 
        WHERE id = %s;
    '''
    cursor.execute(_SQL, (invite_id,))
    result = cursor.fetchall()
    return dict(
        id=result[0][0],
        sender=result[0][1],
        recepient=result[0][2],
        club=result[0][3],
    )