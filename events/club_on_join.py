from database_utils import club, user, init as db_

db = db_.db
cursor = db.cursor()

def init(club_id: str):
    _SQL = '''
        SELECT *
        FROM members
        WHERE club = %s;
    '''
    cursor.execute(_SQL, (club_id))
    club_members = cursor.fetchall()
    club_members_levels = []
    for member in club_members:
        club_members_levels.append(member[4])
    new_club_level: int = round(sum(club_members_levels)/len(club_members_levels))
    _SQL = '''
        UPDATE clubs
        SET lvl = %s
        WHERE id = %s;
    '''
    cursor.execute(_SQL, (new_club_level, club_id))
    db.commit()
    return
    
