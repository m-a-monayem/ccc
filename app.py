from flask import Flask, jsonify, request, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'tasks.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    title = request.json['title']
    description = request.json.get('description', '')
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Task created'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
    title = request.json.get('title')
    description = request.json.get('description')
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Task updated'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Task deleted'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)