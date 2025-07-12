from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from config import Config
from app import login_manager


class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.id = username  # for Flask-Login

    @staticmethod
    def get_user(username):
        with open(Config.USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    return User(row['username'], row['password_hash'])
        return None

    @staticmethod
    def create_user(username, password):
        password_hash = generate_password_hash(password)
        if User.get_user(username):
            return False

        users = []
        try:
            with open(Config.USERS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                users = list(reader)
        except FileNotFoundError:
            pass

        users.append({
            'username': username,
            'password_hash': password_hash
        })

        with open(Config.USERS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'password_hash'])
            writer.writeheader()
            writer.writerows(users)
        return True

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(username):
    return User.get_user(username)