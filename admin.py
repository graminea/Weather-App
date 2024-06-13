from user import User

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_user(self, login_system, username, password):
        login_system.register(username, password, is_admin=False)

    def remove_user(self, login_system, username):
        login_system.remove_user(username)

    def view_users(self, login_system):
        return login_system.users
