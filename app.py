from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import asyncio
import os
from weather_service import WeatherService
from database import Database
from user import User, Admin
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app)

# Initialize database and weather service
db = Database()
weather_service = WeatherService()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get user info to check if admin
    user = db.find_one('users', {'username': session['username']})
    is_admin = user.get('is_admin', 'regular') == 'admin' if user else False
    
    return render_template('dashboard.html', username=session['username'], is_admin=is_admin)

@app.route('/weather')
def weather():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('weather.html', username=session['username'])

@app.route('/logs')
def logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('logs.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# API endpoints
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Check if user already exists
    existing_user = db.find_one('users', {'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Hash password and create user
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = User(username, hashed_password)
    
    try:
        db.insert_one('users', user.to_dict())
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Hash password and check user
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = db.find_one('users', {'username': username, 'password': hashed_password})
    
    if user:
        session['username'] = username
        return jsonify({'message': 'Login successful', 'redirect': '/dashboard'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/weather', methods=['POST'])
def api_weather():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    city = data.get('city')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if not city or not start_date or not end_date:
        return jsonify({'error': 'City, start date, and end date are required'}), 400
    
    try:
        # Use the existing weather service logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        forecasts = loop.run_until_complete(weather_service.get_weather(city, start_date, end_date))
        loop.close()
        
        if forecasts:
            # Log the weather data using the existing method
            weather_service.log_weather(session['username'], city, forecasts)
            return jsonify({'forecasts': forecasts, 'city': weather_service.returned_city}), 200
        else:
            return jsonify({'error': 'No weather data found for the specified period'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Failed to fetch weather: {str(e)}'}), 500

@app.route('/api/logs')
def api_logs():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Use the existing weather service to get logs
        logs = weather_service.get_logs()
        return jsonify({'logs': logs}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to read logs: {str(e)}'}), 500

@app.route('/api/logs/db')
def api_logs_db():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get logs from database
        username = request.args.get('username')  # Optional filter
        limit = int(request.args.get('limit', 50))
        
        logs = weather_service.get_logs_from_db(username, limit)
        
        # Convert datetime objects to strings for JSON serialization
        for log in logs:
            if 'query_date' in log:
                log['query_date'] = log['query_date'].isoformat()
        
        return jsonify({'logs': logs}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to read logs from database: {str(e)}'}), 500

@app.route('/api/user/stats')
def api_user_stats():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        username = request.args.get('username', session['username'])
        stats = weather_service.get_user_stats(username)
        
        # Convert datetime objects to strings for JSON serialization
        for activity in stats.get('recent_activity', []):
            if 'query_date' in activity:
                activity['query_date'] = activity['query_date'].isoformat()
        
        return jsonify({'stats': stats}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get user stats: {str(e)}'}), 500

# Admin API endpoints
@app.route('/api/admin/users')
def api_admin_users():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is admin
    user = db.find_one('users', {'username': session['username']})
    if not user or user.get('is_admin', 'regular') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        users = list(db.find_many('users', {}))
        # Remove password from response for security
        for user in users:
            user.pop('password', None)
            user['_id'] = str(user['_id'])
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch users: {str(e)}'}), 500

@app.route('/api/admin/users', methods=['POST'])
def api_admin_add_user():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is admin
    user = db.find_one('users', {'username': session['username']})
    if not user or user.get('is_admin', 'regular') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', 'regular')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Check if user already exists
    existing_user = db.find_one('users', {'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    try:
        # Hash password and create user
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(username, hashed_password, is_admin)
        db.insert_one('users', new_user.to_dict())
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to create user: {str(e)}'}), 500

@app.route('/api/admin/users/<username>', methods=['DELETE'])
def api_admin_delete_user(username):
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is admin
    user = db.find_one('users', {'username': session['username']})
    if not user or user.get('is_admin', 'regular') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    # Prevent admin from deleting themselves
    if username == session['username']:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    try:
        result = db.delete_one('users', {'username': username})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500

@app.route('/api/admin/stats')
def api_admin_stats():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is admin
    user = db.find_one('users', {'username': session['username']})
    if not user or user.get('is_admin', 'regular') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        # Get basic stats
        total_users = db.get_collection('users').count_documents({})
        admin_users = db.get_collection('users').count_documents({'is_admin': 'admin'})
        regular_users = total_users - admin_users
        
        # Get logs info from database
        total_weather_queries = db.get_collection('weather_logs').count_documents({})
        unique_cities = len(db.get_collection('weather_logs').distinct('city'))
        
        stats = {
            'total_users': total_users,
            'admin_users': admin_users,
            'regular_users': regular_users,
            'total_weather_queries': total_weather_queries,
            'unique_cities_queried': unique_cities,
            'system_status': 'online'
        }
        
        return jsonify({'stats': stats}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500

@app.route('/api/admin/clear-logs', methods=['POST'])
def api_admin_clear_logs():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check if user is admin
    user = db.find_one('users', {'username': session['username']})
    if not user or user.get('is_admin', 'regular') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        with open(log_file_path, 'w') as log_file:
            log_file.write("Weather logs:\n")
        return jsonify({'message': 'Logs cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to clear logs: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

