from flask import Flask, render_template, request
from flask_cors import CORS
from app.mail_api.api.mail_send import bp as mail_send_bp
from app.zidoc_api.api.zidoc_proxy import zidoc_bp
from app.hf_vanilla_api.api.hf_proxy import hf_bp
from app.config import FLASK_PORT

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# CORS(app, resources={
#     r"/api/*": {
#         "origins": "*",
#         "allow_headers": ["Authorization", "Content-Type"],
#         "supports_credentials": True
#     }
# })

CORS(app, 
     origins="*",
     allow_headers=["Content-Type", "Authorization", "Accept"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

app.register_blueprint(mail_send_bp, url_prefix='/api')
app.register_blueprint(zidoc_bp, url_prefix='/api')
app.register_blueprint(hf_bp, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=FLASK_PORT)
    app.run(debug=True, port=FLASK_PORT)