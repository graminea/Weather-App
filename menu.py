import tkinter as tk
from tkinter import messagebox
from weather import WeatherApp

class Menu:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.minsize(400, 300)
        self.setup_menu()

    def setup_menu(self):
        if self.user.is_admin == 'admin':
            self.root.title("Main Menu de Admin")
            label_info = tk.Label(self.root, text=f"Main Menu de Admin: {self.user.username}")
            label_info.pack()

            button_start_weather_app = tk.Button(self.root, text="Buscar Previsão do Tempo", command=self.start_weather_app)
            button_start_weather_app.pack()

            button_view_users = tk.Button(self.root, text="Ver usuários", command=self.view_users_window)
            button_view_users.pack()

            button_add_user = tk.Button(self.root, text="Adicionar usuário", command=self.add_user_window)
            button_add_user.pack()

            button_remove_user = tk.Button(self.root, text="Remover usuário", command=self.remove_user_window)
            button_remove_user.pack()
        else:
            self.root.title("Main Menu")
            label_info = tk.Label(self.root, text=f"Main Menu de Usuário: {self.user.username}")
            label_info.pack()

            button_start_weather_app = tk.Button(self.root, text="Buscar Previsão do Tempo", command=self.start_weather_app)
            button_start_weather_app.pack()

        self.root.mainloop()

    def start_weather_app(self):
        self.root.destroy()  # Close the menu window
        app = WeatherApp(self.user.username)
        app.mainloop()

    def view_users_window(self):
        view_users_win = tk.Toplevel(self.root)
        view_users_win.title("Ver Usuários")
        users = self.user.view_users()
        users_text = "\n".join([f"{u.username} - {'Admin' if u.is_admin == 'admin' else 'Regular'}" for u in users])
        tk.Label(view_users_win, text=users_text).pack(padx=10, pady=10)

    def add_user_window(self):
        add_user_win = tk.Toplevel(self.root)
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
            self.user.add_user(new_user, new_password)
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
            add_user_win.destroy()

        button_add_new_user = tk.Button(add_user_win, text="Adicionar", command=perform_add_user)
        button_add_new_user.grid(row=2, column=0, columnspan=2, pady=5)

    def remove_user_window(self):
        remove_user_win = tk.Toplevel(self.root)
        remove_user_win.title("Remover Usuário")
        tk.Label(remove_user_win, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
        entry_remove_user = tk.Entry(remove_user_win)
        entry_remove_user.grid(row=0, column=1, padx=5, pady=5)

        def perform_remove_user():
            user_to_remove = entry_remove_user.get()
            self.user.remove_user(user_to_remove)
            messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
            remove_user_win.destroy()

        button_remove_user = tk.Button(remove_user_win, text="Remover", command=perform_remove_user)
        button_remove_user.grid(row=1, column=0, columnspan=2, pady=5)
