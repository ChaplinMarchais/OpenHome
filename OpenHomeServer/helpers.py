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