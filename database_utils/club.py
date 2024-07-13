from database_utils import init
import json

db = init.db
cursor = db.cursor()

def checkTable():
    _SQL = '''
        CREATE TABLE IF NOT EXISTS clubs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            description VARCHAR(255) DEFAULT '',
            tag VARCHAR(255),
            lvl INT DEFAULT 1,
            creator VARCHAR(255)
        );
    '''
    cursor.execute(_SQL)
    
def getInfo(club_id: str):
    _SQL = '''
        SELECT * 
        FROM clubs 
        WHERE id = %s;
    '''
    cursor.execute(_SQL, (club_id,))
    result = cursor.fetchall()
    class ClubInfo():
        id: int
        name: str
        description: str
        tag: str
        level: str
        creator: str
    club_info = ClubInfo()
    club_info.name = 'None'
    if len(result) > 0:
        club_info.id=result[0][0],
        club_info.name=result[0][1],
        club_info.description=result[0][2],
        club_info.tag=result[0][3],
        club_info.level=result[0][4],
        club_info.creator=result[0][5]
    return club_info
    # return dict(
    #     id=result[0][0],
    #     name=result[0][1],
    #     description=result[0][2],
    #     tag=result[0][3],
    #     level=result[0][4],
    #     creator=result[0][5]
    # )
    
def create(club_name: str, club_tag: str, club_description: str, creator_id: str):
    club_name = str(club_name)
    club_tag = str(club_tag)
    club_description = str(club_description)
    
    _SQL = '''
        INSERT INTO clubs 
        (name, description, tag, creator) 
        VALUES 
        (%s, %s,%s , %s);
    '''
    cursor.execute(_SQL, (club_name, club_description, club_tag, creator_id,))
    db.commit()
    _SQL = '''
        SELECT * 
        FROM clubs 
        WHERE name = %s;
    '''
    cursor.execute(_SQL, (club_name,))
    result = cursor.fetchall()
    _SQL = '''
        UPDATE members
        SET club = %s
        WHERE user_id = %s;
    '''
    cursor.execute(_SQL, (result[0][0], creator_id))
    db.commit()
    return result[0]

def isExists(club_name: str) -> bool:
    _SQL = '''
        SELECT * 
        FROM clubs 
        WHERE name = %s;
    '''
    cursor.execute(_SQL, (str(club_name),))
    result = cursor.fetchall()
    
    if (len(result) != 0):
        return True
    return False