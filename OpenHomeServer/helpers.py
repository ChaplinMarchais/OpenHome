import sqlite3

from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    """
    Decorates routes to redirect to the login endpoint if the current session contains no user object.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    Args:
        f (_type_): function to wrap
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function

def query(db_name, query, params=None):
    """
    Query the database for a given SQL statement with the provided optional arguements.

    Args:
        db_name (string): Connection string for the db
        query (string): SQL query to execute
        params (optional): Optional params to pass to the SQL statement. Defaults to None.

    Returns:
        Object: Result of query
    """
    try:
        with sqlite3.connect(db_name) as conn:
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