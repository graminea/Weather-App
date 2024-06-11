import time
import json
import os

class Login:
    def __init__(self):
        self.logins = []  
        self.userslist = []
        self.variable = 1  
        self.index_logged_user = None
        self.folder_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.folder_path, 'logins.json')
        self.get_logins() 

    def login(self): 
        while self.variable == 1:
            print('\nBem Vindo a Sagás Pizzaria ')
            h = input('Você tem cadastro? (S/N): ').upper()
            if h == 'S':
                print('LOGIN.', end='')
                for i in range(2):
                    print('.', end='', flush=True)
                    time.sleep(1)
                
                user = input('\nDigite o usuário: ')
                password = input('Digite a senha: ')
                for i in range(len(self.logins)):
                    if self.logins[i]['user'] == user and self.logins[i]['password'] == password:
                        self.logged_user = user
                        self.index_logged_user = i  
                        self.variable = 0
                        print('Login efetuado com sucesso!!')
                        print('Entrando.', end='')
                        for i in range(2):
                            print('.', end='', flush=True)
                            time.sleep(1)
                        print()
                        break
                else:
                    print('Usuário ou senha incorretos!!')
                    print('Faça o login novamente!!')
                    print()
                    continue

            else:
                x = input('Deseja fazer o cadastro? (S/N): ').upper()
                if x == 'S':
                    self.login_make()

    def login_make(self):
        user = input('Crie um usuário: ')
        password = input('Crie uma senha: ')
        self.logins.append({'user': user, 'password': password, 'balance': 0, 'adm': False})
        self.userslist.append(user)
        print('Usuário criado com sucesso!')
        print('Realize o login para continuar.', end='')
        for _ in range(2):
            print('.', end='', flush=True)
            time.sleep(1)

        self.save_logins() 
        print()
    
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
    

login = Login()
login.login()
