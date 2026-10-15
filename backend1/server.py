import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = 'db'
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_NAME = 'samples'

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    return connection

@app.route('/app1')
def home():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT counter FROM visits WHERE id = 1')
            result = cursor.fetchone()
            counter = result[0] if result else 0
        conn.commit()
        return f'Hello from Backend 1 - Visits: {counter}'
    finally:
        conn.close()

@app.route('/api')
def api():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT counter FROM visits WHERE id = 1')
            result = cursor.fetchone()
            counter = result[0] if result else 0
        conn.commit()
        return jsonify({
            'status': 'success',
            'message': 'Response from backend server',
            'visits': counter
        })
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)