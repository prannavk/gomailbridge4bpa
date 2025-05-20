from functools import wraps
from flask import request
from app.utils.logger import log, init_log_context

def log_request_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        getlogs = request.json.get("getlogs") if request.is_json else False
        init_log_context() if getlogs else None
        log(f"Calling: {func.__name__}", enable=getlogs)
        result = func(*args, **kwargs)
        log(f"Finished: {func.__name__}", enable=getlogs)
        return result
    return wrapper
