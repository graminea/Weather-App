# main.py
from loginGUI import LoginApp
from menu import Menu

def on_login_success(user):
    menu = Menu(user)

if __name__ == '__main__':
    login_app = LoginApp(on_login_success)
    login_app.mainloop()
