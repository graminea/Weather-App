import json
import os
from user import User, Admin

class Login:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(folder_path, 'logins.json')
        try:
            with open(file_path, 'r') as file:
                users_data = json.load(file)
                for data in users_data:
                    if data['is_admin'] == 'admin':
                        user = Admin(data['username'], data['password'])
                    else:
                        user = User(data['username'], data['password'], is_admin='regular')
                    self.users.append(user)
        except FileNotFoundError:
            print("Arquivo de logins não encontrado. Criando um novo.")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def register(self, username, password, is_admin='regular'):
        if is_admin == 'admin':
            user = Admin(username, password)
        else:
            user = User(username, password, is_admin='regular')
        self.users.append(user)
        self.save_users()

    def save_users(self):
        folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(folder_path, 'logins.json')
        with open(file_path, 'w') as file:
            json.dump([user.__dict__ for user in self.users], file, indent=4)

    def remove_user(self, username):
        self.users = [user for user in self.users if user.username != username]
        self.save_users()
