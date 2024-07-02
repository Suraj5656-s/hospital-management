from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_qrcode

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    flask_qrcode.QRcode(app)

    with app.app_context():
        from models import Patient
        db.create_all()

        from routes import main
        app.register_blueprint(main)

    return app
