import json
import os
from user import User, Admin
from database import Database

class Login:
    def __init__(self):
        self.users = []
        self.db = Database(db_name="userdata_weather_app")
        self.load_users()

    def load_users(self):
        try:
            users_data = self.db.find_many("users", {})  

            for data in users_data:
                if data.get("is_admin") == "admin":
                    user = Admin(data["username"], data["password"])
                else:
                    user = User(data["username"], data["password"], is_admin="regular")

                self.users.append(user)

            print(f"Loaded {len(self.users)} users.")
        except Exception as e:
            print(f"Failed to load users from DB: {e}")


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
        self.save_user(user)

    def save_user(self, user):
        print(self.users)
        query = {"username": user.username}
        update_values = user.to_dict() 
        self.db.update_one("users", query, update_values, upsert=True)   

    def remove_user(self, username):
        query = {"username": username}
        self.db.delete_one(query)
    

    
