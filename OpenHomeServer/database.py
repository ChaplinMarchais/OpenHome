import sqlite3

def query(db, query, params=None):
    """
    Query the database for a given SQL statement with the provided optional arguements.

    Args:
        db (string): Connection string for the db
        query (string): SQL query to execute
        params (optional): Optional params to pass to the SQL statement. Defaults to None.

    Returns:
        Object: Result of query
    """
    try:
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if query.lower().startswith("select"):
                return cursor.fetchall()
            else:
                 conn.commit()
                 return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def get_user_sub(db, device_code):
    return query(db, 'SELECT openid_sub FROM Users WHERE device_code = ?', 
                 params = (device_code,))[0]["openid_sub"]

def register_device(db, ):
    return None
    
    
def generate_device_id(db, device_code):
    return f"{device_code}:{get_user_sub(db, device_code)}"
