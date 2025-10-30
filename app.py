from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.close()

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    items = conn.execute('SELECT * FROM items ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    description = request.form.get('description', '')
    conn = get_db()
    conn.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        conn.execute('UPDATE items SET name=?, description=? WHERE id=?', (name, description, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        item = conn.execute('SELECT * FROM items WHERE id=?', (id,)).fetchone()
        conn.close()
        return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM items WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/view/<int:id>')
def view(id):
    conn = get_db()
    item = conn.execute('SELECT * FROM items WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('view.html', item=item)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)