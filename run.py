from flask import Flask
from app.api.mail_send import bp as mail_send_bp
from app.config import FLASK_PORT
from app.api.zidoc_proxy import bp as zidoc_bp

app = Flask(__name__)
app.register_blueprint(mail_send_bp)
app.register_blueprint(zidoc_bp)


if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)




