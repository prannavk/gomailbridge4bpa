import datetime
from flask import g

def init_log_context():
    g.logs = []

def get_log_context():
    return getattr(g, 'logs', [])

def log(message, enable=True):
    if not enable:
        return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    if hasattr(g, 'logs'):
        g.logs.append(formatted)
