from flask import request, jsonify
import os
from functools import wraps

API_KEY = os.getenv("API_KEY")

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("lemma")
        if not key or key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper
