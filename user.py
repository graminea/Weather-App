class User:
    def __init__(self, username, password, is_admin='regular'):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return self.username

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, is_admin='admin')

    def add_user(self, login_system, username, password):
        login_system.register(username, password, is_admin='regular')

    def remove_user(self, login_system, username):
        login_system.remove_user(username)

    def view_users(self, login_system):
        return login_system.users
