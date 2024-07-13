import discord
from database_utils import init

db = init.db
cursor = db.cursor()


def checkTable():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            user_id VARCHAR(255),
            coins INT DEFAULT 0,
            lvl INT DEFAULT 1,
            club VARCHAR(255) DEFAULT 'None',
            family VARCHAR(255) DEFAULT 'None',
            inventory LONGTEXT DEFAULT '[]',
            last_work INT DEFAULT 0
        );
    ''')
    
    
def checkInTable(interaction_user: discord.Interaction.user):
    _SQL = '''
        SELECT * 
        FROM members 
        WHERE user_id = %s;
    '''
    cursor.execute(_SQL, (interaction_user.id,))
    members_matched = []
    for x in cursor:
        members_matched.append(x[0])
    if len(members_matched) <= 1:
        print(f"{interaction_user.name} does not exists in members. Creating new row")
        _SQL = '''INSERT INTO members (username, user_id) VALUES (%s, %s);'''
        cursor.execute(_SQL, (interaction_user.name, interaction_user.id,))
        db.commit()
    
def getInfo(user_id: str) -> dict[str, str | int]:
    _SQL = '''
        SELECT * 
        FROM members 
        WHERE user_id = %s;
    '''
    cursor.execute(_SQL, (user_id,))
    result = cursor.fetchall()

    return {
        "id": result[0][0],
        "username": result[0][1],
        "user_id": result[0][2],
        "coins": result[0][3],
        "level": result[0][4],
        "club": result[0][5],
        "family": result[0][6],
        "inventory": result[0][7],
        "last_work": result[0][8]
    }
    
def update(user_id: str, field: str, new_value: str):
    _SQL = '''
        UPDATE members
        SET %s = %s
        WHERE user_id = %s
    '''
    cursor.execute(_SQL, (field, new_value, user_id,))
    db.commit()
    