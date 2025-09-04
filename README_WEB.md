# Weather App - Web Interface

Este é o Weather App convertido para uma interface web usando Flask, mantendo toda a lógica original do seu app.

## 🚀 Como Funciona

- **`weather_service.py`**: Versão headless do seu `weather.py` original (sem tkinter)
- **`app.py`**: Flask app que usa o serviço de weather existente
- **Templates**: Interface web moderna que chama a API

## 🔧 Instalação

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação**:
   ```bash
   python app.py
   ```

3. **Acesse no navegador**:
   ```
   http://localhost:5000
   ```

## 📁 Estrutura

- **`weather_service.py`**: Lógica de weather do seu app original (sem tkinter)
- **`app.py`**: Flask app com rotas e API
- **`tamplates/`**: Páginas HTML (login, register, dashboard, weather, logs)
- **`database.py`**: Seu banco MongoDB existente
- **`user.py`**: Suas classes de usuário existentes

## 🔌 API Endpoints

- `POST /api/register` - Registro de usuário
- `POST /api/login` - Login de usuário  
- `POST /api/weather` - Consulta de previsão do tempo
- `GET /api/logs` - Obtenção de logs

## ✨ O que foi mantido

- ✅ Toda a lógica de weather do seu app original
- ✅ Sistema de logging existente
- ✅ Banco de dados MongoDB
- ✅ Classes de usuário
- ✅ Formato de dados e cálculos

## 🔄 O que foi alterado

- ❌ Removido tkinter (interface desktop)
- ✅ Adicionado Flask (interface web)
- ✅ Mantida toda a lógica de negócio

## 🌐 Páginas Web

- **Login**: `/login`
- **Registro**: `/register` 
- **Dashboard**: `/dashboard`
- **Weather**: `/weather`
- **Logs**: `/logs`

A aplicação usa exatamente o mesmo código de weather que você já tinha, só que agora é headless e chamado via API!

