from functools import wraps
from flask import session, redirect, abort
from ..config.database import get_connection 

def guest_admin(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if session.get("ADMIN_LOGIN"): return redirect("/owner/dashboard")
    return func(*args, **kwargs)
  return wrapper


def autheticated_admin(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not session.get("ADMIN_LOGIN"): return redirect("/owner/")
    return func(*args, **kwargs)
  return wrapper


def prevent_multiple(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    db = get_connection()
    if not db: return abort(500, "Failed to connect to DB")

    conn, cursor = db
    query = "SELECT * FROM admin"
    cursor.execute(query)

    count = cursor.rowcount
    if count: return redirect("/owner")

    return func(*args, **kwargs)
  return wrapper
