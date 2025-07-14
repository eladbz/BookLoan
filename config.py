import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STUDENTS_FILE = os.path.join(BASE_DIR, 'students.csv')
    USERS_FILE = os.path.join(BASE_DIR, 'users.csv')
    DISTRIBUTIONS_FILE = os.path.join(BASE_DIR, 'data', 'distributions.csv')