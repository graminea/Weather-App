import tkinter as tk
import tkinter.messagebox as messagebox
from weather import WeatherApp
import json
import os
import time

class Login:
    def __init__(self):
        self.logins = []
        self.userslist = []
        self.variable = 1
        self.index_logged_user = None
        self.folder_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.folder_path, 'logins.json')
        self.get_logins()

    def login(self, user, password):
        for i in range(len(self.logins)):
            if self.logins[i]['user'] == user and self.logins[i]['password'] == password:
                self.logged_user = user
                self.index_logged_user = i
                return True
        return False

    def register(self, user, password):
        self.logins.append({'user': user, 'password': password, 'balance': 0, 'adm': False})
        self.userslist.append(user)
        self.save_logins()

    def get_logins(self):
        try:
            with open(self.file_path, 'r') as file:
                self.logins = json.load(file)
                self.userslist = [login['user'] for login in self.logins]
        except FileNotFoundError:
            print("Arquivo de logins não encontrado. Criando um novo.")

    def save_logins(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.logins, file)


class LoginApp(tk.Tk):
    def __init__(self, on_login_success):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")
        self.login_manager = Login()
        self.on_login_success = on_login_success
        
        self.label_user = tk.Label(self, text="Usuário:")
        self.label_user.pack()
        self.entry_user = tk.Entry(self)
        self.entry_user.pack()

        self.label_password = tk.Label(self, text="Senha:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(self, text="Login", command=self.perform_login)
        self.button_login.pack()

        self.button_register = tk.Button(self, text="Registrar", command=self.perform_register)
        self.button_register.pack()

    def perform_login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        if self.login_manager.login(user, password):
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")
            self.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def perform_register(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        self.login_manager.register(user, password)
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso! Realize o login.")

if __name__ == '__main__':
    def on_login_success(user):
        app = WeatherApp(user)
        app.mainloop()

    login_app = LoginApp(on_login_success)
    login_app.mainloop()
