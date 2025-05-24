from flask import Flask, render_template, request
from flask_cors import CORS
from app.mail_api.api.mail_send import bp as mail_send_bp
from app.zidoc_api.api.zidoc_proxy import zidoc_bp
from app.hf_vanilla_api.api.hf_proxy import hf_bp
from app.home.home_endpoints import hbp
from app.config import FLASK_PORT

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# CORS(app, resources={
#     r"/api/*": {
#         "origins": "*",
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Authorization", "Content-Type"]
#     }
# })

CORS(app, 
     origins="*",
     allow_headers=["Content-Type", "Authorization", "Accept"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

app.register_blueprint(mail_send_bp, url_prefix='/api')
app.register_blueprint(zidoc_bp, url_prefix='/api')
app.register_blueprint(hf_bp, url_prefix='/api')
app.register_blueprint(hbp)

@app.route('/')
def home():
    return render_template('index.html')

# @app.before_request
# def handle_content_type_for_get():
#     print("A0..............All")
#     if request.method == 'GET':
#         print("A1............Only GET")
#         print(f"Ok {request.access_control_request_headers}")
#         try:
#             hdrs = dict(request.headers)
#             print(f"Header Data: {hdrs}")            
#             if "Content-Type" in hdrs:
#                 print("A2............If Content-Type in Hdrs")
#                 # print(f"Before deleting: {hdrs[request.content_type]}") -> Issue
#                 print(f"Before deleting: {hdrs['Content-Type']}")
#                 del hdrs["Content-Type"] 
#                 print("ok 41.....")
#                 # print(f"Is there? : {hdrs['Content-Type']}") -> Issue
#                 print("oK AND 43.....")
#                 # del hdrs[request.content_type] _> Nope issue
#                 print("oK AND 45.....")

#                 # print(f"Going to delete in headers.........{request.headers.get['Content-Type']}") -> OOPS.... 'method' object is not subscriptable
#                 print(f"Going to delete in headers.........{request.headers['Content-Type']}")
#                 print("49.....")
#                 print(f"Wait,...{request.headers}")
#                 # del request.headers["Content-Type"] -> OOPS.... 'EnvironHeaders' objects are immutable
#                 print("51......")

#                 print("A4....................environ approach??...")    
#                 environ = request.environ
#                 print(f'Aw .. What is environ?.........{environ}.....\n.......')
#                 print(f"{environ.items}........ok...........")                
#                 if 'HTTP_CONTENT_TYPE' in environ:
#                     print("A5..........")
#                     del environ['HTTP_CONTENT_TYPE']
#                     app.logger.debug("Removed Content-Type header for GET request")
#                     print("A6...Removed Content-Type ???.............")
#                     print(f"to check environ {environ['HTTP_CONTENT_TYPE']}")
#                 if 'CONTENT_TYPE' in environ:
#                     print("A5.......... yes CONTENT_TYPE is there")
#                     del environ['CONTENT_TYPE']
#                     app.logger.debug("Removed Content-Type header for GET request")
#                     print("A6...Removed Content-Type ???.............")
#                     print(f"to check environ {environ['CONTENT_TYPE']}")
#                 # print("Ax............Checking both ???....")
#                 # print(f'{request.headers["Content-Type"]} and \n {hdrs["Content-Type"]}')            
#             print("Ay.......Probably now we have removed Content-Type...")
#         except Exception as e:
#             print(f"OOPS.... {e}")
#         print("A...LAST.......")        

# 4 the thing with BPA
@app.before_request
def handle_content_type_for_get():    
    if request.method == 'GET':                
        try:
            hdrs = dict(request.headers)            
            if "Content-Type" in hdrs:                
                # print(f"Before deleting: {hdrs[request.content_type]}") -> Issue                                
                # print(f"Is there? : {hdrs['Content-Type']}") -> Issue                
                # del hdrs[request.content_type] _> Nope issue                
                # print(f"Going to delete in headers.........{request.headers.get['Content-Type']}") -> OOPS.... 'method' object is not subscriptable                                                
                # del request.headers["Content-Type"] -> OOPS.... 'EnvironHeaders' objects are immutable
                del hdrs["Content-Type"]                 
                environ = request.environ                                
                if 'HTTP_CONTENT_TYPE' in environ:                    
                    del environ['HTTP_CONTENT_TYPE']
                    app.logger.debug("Removed Content-Type header for GET request")                    
                    # print(f"to check environ {environ['HTTP_CONTENT_TYPE']}")
                if 'CONTENT_TYPE' in environ:                    
                    del environ['CONTENT_TYPE']
                    app.logger.debug("Removed Content-Type header for GET request")                    
                    # print(f"to check environ {environ['CONTENT_TYPE']}")            
        except Exception as e:
            print(f"OOPS.... See Issue -> {e}")        


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=FLASK_PORT)
    # app.run(debug=True, port=FLASK_PORT)