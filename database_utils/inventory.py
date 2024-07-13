from database_utils import init
import json

db = init.db
cursor = db.cursor()

def get(user_id: str) -> list[str]:
    _SQL = '''
        SELECT inventory FROM members WHERE user_id = %s;
    '''
    cursor.execute(user_id)
    result = cursor.fetchall()
    return result[0]


def put(user_id: str, item_id: str):
    user_inventory = get(user_id)
    user_inventory.append(item_id)
    _SQL = '''
        UPDATE members
        SET inventory = %s
        WHERE user_id = %s
    '''
    cursor.execute(_SQL, (user_inventory, user_id,))
    db.commit()

def remove(user_id: str, item_id: str):
    """
    Removes item from user's inventory. \n
    Returns `True` if successful otherwise `False`
    """
    user_inventory = get(user_id)
    if item_id in user_inventory:
        user_inventory.remove(item_id)
        _SQL = '''
            UPDATE members
            SET inventory = %s
            WHERE user_id = %s
        '''
        cursor.execute(_SQL, (user_inventory, user_id,))
        db.commit()
    else:
        return False
    return True