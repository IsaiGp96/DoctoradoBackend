import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

def init_db(app):
    load_dotenv()
    required_vars = ['USER_USERNAME', 'USER_PASSWORD', 'ADMIN_USERNAME', 'ADMIN_PASSWORD', 'SUPERADMIN_USERNAME', 'SUPERADMIN_PASSWORD']
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Variable de entorno {var} faltante en .env")

    with app.app_context():
        db.create_all()
        if not User.query.first():
            users = [
                User(
                    username=os.getenv('USER_USERNAME'),
                    password_hash=generate_password_hash(os.getenv('USER_PASSWORD')),
                    role='user'
                ),
                User(
                    username=os.getenv('ADMIN_USERNAME'),
                    password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD')),
                    role='admin'
                ),
                User(
                    username=os.getenv('SUPERADMIN_USERNAME'),
                    password_hash=generate_password_hash(os.getenv('SUPERADMIN_PASSWORD')),
                    role='superadmin'
                )
            ]
            db.session.add_all(users)
            db.session.commit()
