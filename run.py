from flask import Flask, render_template
from app.api.mail_send import bp as mail_send_bp
from app.config import FLASK_PORT
from app.api.zidoc_proxy import bp as zidoc_bp

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# app.register_blueprint(mail_send_bp)
# app.register_blueprint(zidoc_bp)
app.register_blueprint(mail_send_bp, url_prefix='/api')
app.register_blueprint(zidoc_bp, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=FLASK_PORT)




