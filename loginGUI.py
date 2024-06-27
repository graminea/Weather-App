import tkinter as tk
import tkinter.messagebox as messagebox
from weather import WeatherApp
from login import Login

from user import Admin, User

class LoginApp(tk.Tk):
    def __init__(self, on_login_success):
        super().__init__()
        self.login_system = Login()
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
        username = self.entry_user.get()
        password = self.entry_password.get()

        logged_in_user = self.login_system.login(username, password)
        if logged_in_user:
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")
            self.destroy()
            self.on_login_success(logged_in_user, self.login_system)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def perform_register(self):
        username = self.entry_user.get()
        password = self.entry_password.get()
        self.login_system.register(username, password)
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso! Realize o login.")

    def toggle_password(self):
        if self.show_password:
            self.entry_password.config(show="*")
        else:
            self.entry_password.config(show="")
        self.show_password = not self.show_password

if __name__ == '__main__':
    def on_login_success(user):
        root = tk.Tk()
        root.minsize(400, 300)  # Set the minimum size of the main menu window

        if user.is_admin == 'admin':
            root.title("Main Menu de Admin")
            label_info = tk.Label(root, text=f"Main Menu de Admin: {user.username}")
            label_info.pack()

            def start_weather_app():
                app = WeatherApp(user.username)
                app.mainloop()

            button_start_weather_app = tk.Button(root, text="Buscar Previsão do Tempo", command=start_weather_app)
            button_start_weather_app.pack()

            def view_users_window():
                view_users_win = tk.Toplevel(root)
                view_users_win.title("Ver Usuários")
                users = user.view_users(login_app.login_system)
                users_text = "\n".join([f"{u.username} - {'Admin' if u.is_admin == 'admin' else 'Regular'}" for u in users])
                tk.Label(view_users_win, text=users_text).pack(padx=10, pady=10)

            button_view_users = tk.Button(root, text="Ver usuários", command=view_users_window)
            button_view_users.pack()

            def add_user_window():
                add_user_win = tk.Toplevel(root)
                add_user_win.title("Adicionar Usuário")
                tk.Label(add_user_win, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
                entry_new_user = tk.Entry(add_user_win)
                entry_new_user.grid(row=0, column=1, padx=5, pady=5)

                tk.Label(add_user_win, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
                entry_new_password = tk.Entry(add_user_win, show="*")
                entry_new_password.grid(row=1, column=1, padx=5, pady=5)

                def perform_add_user():
                    new_user = entry_new_user.get()
                    new_password = entry_new_password.get()
                    user.add_user(login_app.login_system, new_user, new_password)
                    messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
                    add_user_win.destroy()

                button_add_new_user = tk.Button(add_user_win, text="Adicionar", command=perform_add_user)
                button_add_new_user.grid(row=2, column=0, columnspan=2, pady=5)

            button_add_user = tk.Button(root, text="Adicionar usuário", command=add_user_window)
            button_add_user.pack()

            def remove_user_window():
                remove_user_win = tk.Toplevel(root)
                remove_user_win.title("Remover Usuário")
                tk.Label(remove_user_win, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
                entry_remove_user = tk.Entry(remove_user_win)
                entry_remove_user.grid(row=0, column=1, padx=5, pady=5)

                def perform_remove_user():
                    user_to_remove = entry_remove_user.get()
                    user.remove_user(login_app.login_system, user_to_remove)
                    messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
                    remove_user_win.destroy()

                button_remove_user = tk.Button(remove_user_win, text="Remover", command=perform_remove_user)
                button_remove_user.grid(row=1, column=0, columnspan=2, pady=5)

            button_remove_user = tk.Button(root, text="Remover usuário", command=remove_user_window)
            button_remove_user.pack()

            def view_users_window():
                view_users_win = tk.Toplevel(root)
                view_users_win.title("Ver Usuários")
                users = user.view_users(login_app.login_system)
                users_text = "\n".join([f"{u.username} - {'Admin' if u.is_admin == 'admin' else 'Regular'}" for u in users])
                tk.Label(view_users_win, text=users_text).pack(padx=10, pady=10)

        else:
            root.title("Main Menu")
            label_info = tk.Label(root, text=f"Main Menu de Usuário: {user.username}")
            label_info.pack()

            def start_weather_app():
                app = WeatherApp(user.username)
                app.mainloop()

            button_start_weather_app = tk.Button(root, text="Buscar Previsão do Tempo", command=start_weather_app)
            button_start_weather_app.pack()

        root.mainloop()

    login_app = LoginApp(on_login_success)
    login_app.mainloop()


