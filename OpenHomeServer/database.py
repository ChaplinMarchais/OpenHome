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

def connect_device(db, device_code, name):
    openid_sub = get_user_sub(db, device_code)
    query(db, 'INSERT INTO Devices (id, openid_sub, name, status) VALUES ((SELECT id FROM Devices WHERE openid_sub = ? AND name = ?), ?, ?, "connected") ON CONFLICT(id) DO UPDATE SET status = "connected"',
          params = (openid_sub, name, openid_sub, name))
    
def disconnect_device(db, device_code, name):
    openid_sub = get_user_sub(db, device_code)
    query(db, 'UPDATE Devices SET status = "disconnected" FROM (SELECT id FROM Devices WHERE openid_sub = ? AND name = ?) AS existing WHERE Devices.id = existing.id',
            params = (openid_sub, name))
    
    
def generate_device_id(db, device_code):
    return f"{device_code}:{get_user_sub(db, device_code)}"

def get_devices(db, user_session):
    oidc_sub = get_oidc_sub(user_session)
    return query(db, 'SELECT * FROM Devices WHERE openid_sub = ?', params = (oidc_sub, ))


def get_oidc_sub(user_session):
    return user_session["userinfo"]["sub"]