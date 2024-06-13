import json
import os
import time
from admin import Admin
from regularUser import RegularUser


class Login:
    def __init__(self):
        self.users = []
        self.folder_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.folder_path, 'logins.json')
        self.load_users()

    def load_users(self):
        try:
            with open(self.file_path, 'r') as file:
                user_data = json.load(file)
                for data in user_data:
                    if data.get('adm', False):
                        user = Admin(data)
                    else:
                        user = RegularUser(data)
                    self.users.append(user)
        except FileNotFoundError:
            print("Arquivo de logins não encontrado. Criando um novo.")

    def save_users(self):
        with open(self.file_path, 'w') as file:
            json.dump([user.__dict__ for user in self.users], file)

    def register(self, username, password, is_admin=False):
        if any(user.username == username for user in self.users):
            return False  # Username already exists
        if is_admin:
            new_user = Admin(username, password)
        else:
            new_user = RegularUser(username, password)
        self.users.append(new_user)
        self.save_users()
        return True

    def remove_user(self, username):
        self.users = [user for user in self.users if user.username != username]
        self.save_users()

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.check_password(password):
                return user
        return None
