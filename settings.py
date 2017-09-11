import os
from Flask_D01 import app

DEBUG = True
DATABASE = os.path.join(app.root_path, 'db/flaskr.db')
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'
BASE_DIR = "Flask_D01"