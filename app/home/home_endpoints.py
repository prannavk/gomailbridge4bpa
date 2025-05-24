from flask import Blueprint, request, jsonify
from app.utils.decorators import log_request_response
from app.utils.logger import log

hbp = Blueprint("home_endpoint", __name__)

@hbp.route('/api/debug', methods=['GET', 'POST', 'PUT', 'DELETE'])
@log_request_response
def debug_endpoint():
    return {
        'method': request.method,
        'headers': dict(request.headers),
        'args': dict(request.args),
        'json': request.get_json(silent=True),
        'data': request.get_data().decode('utf-8'),
        'url': request.url
    }

@hbp.route('/empty', methods=['GET'])
@log_request_response
def empty_endpoint():
    log("Empty Endpoint.....")
    return """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">    
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>EMPTY</h1>
        <hr>
        <p>There is Nothing in this Page-Response</p>
    </body>
    </html>
    """






