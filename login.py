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
    def __init__(self, login_system, on_login_success):
        super().__init__()
        self.login_system = login_system
        self.on_login_success = on_login_success
        self.title("Login")
        self.geometry("300x200")

        self.label_user = tk.Label(self, text="Usuário:")
        self.label_user.grid(row=0, column=0, padx=5, pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = tk.Label(self, text="Senha:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.show_password = False
        self.show_password_button = tk.Button(self, text='👁️', command=self.toggle_password)
        self.show_password_button.grid(row=1, column=2, padx=5, pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.perform_login)
        self.button_login.grid(row=2, column=0, columnspan=3, pady=5)

        self.button_register = tk.Button(self, text="Registrar", command=self.perform_register)
        self.button_register.grid(row=3, column=0, columnspan=3, pady=5)

    def perform_login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        if self.login_system.login(user, password):
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")
            self.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def perform_register(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        self.login_system.register(user, password)
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso! Realize o login.")

    def toggle_password(self):
        if self.show_password:
            self.entry_password.config(show="*")
        else:
            self.entry_password.config(show="")
        self.show_password = not self.show_password


if __name__ == '__main__':
    def on_login_success(user):
        app = WeatherApp(user)
        app.mainloop()

    login_system = Login()
    login_app = LoginApp(login_system, on_login_success)
    login_app.mainloop()
