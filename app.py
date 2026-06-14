from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER,
            total INTEGER,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute('INSERT INTO results (name, score, total, date) VALUES (?, ?, ?, ?)',
              (data['name'], data['score'], data['total'], datetime.now().strftime('%Y-%m-%d %H:%M')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Saved!'})

@app.route('/results', methods=['GET'])
def get_results():
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute('SELECT * FROM results ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)