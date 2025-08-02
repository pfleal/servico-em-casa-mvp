import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from models.user import User
from config.database import db
from main import app

with app.app_context():
    user = User.query.filter_by(email='cliente@teste.com').first()
    print(f'User found: {user is not None}')
    if user:
        print(f'User details: {user.to_dict()}')
        print(f'Password check: {user.check_password("123456")}')
    else:
        print('User not found')