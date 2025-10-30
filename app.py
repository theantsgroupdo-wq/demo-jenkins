from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.close()

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Dashboard Route (NEW)
@app.route('/dashboard')
def dashboard():
    conn = get_db()
    items = conn.execute('SELECT * FROM items ORDER BY id DESC').fetchall()
    
    # Statistics
    total_items = len(items)
    items_with_desc = len([item for item in items if item['description']])
    items_without_desc = total_items - items_with_desc
    
    # Recent items (last 5)
    recent_items = items[:5] if len(items) > 0 else []
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_items=total_items,
                         items_with_desc=items_with_desc,
                         items_without_desc=items_without_desc,
                         recent_items=recent_items)

# API for dashboard chart (NEW)
@app.route('/api/stats')
def api_stats():
    conn = get_db()
    items = conn.execute('SELECT created_at FROM items ORDER BY created_at').fetchall()
    conn.close()
    
    # Count items per day
    daily_counts = {}
    for item in items:
        if item['created_at']:
            date = item['created_at'].split()[0]  # Get date only
            daily_counts[date] = daily_counts.get(date, 0) + 1
    
    return jsonify({
        'dates': list(daily_counts.keys()),
        'counts': list(daily_counts.values())
    })

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

# About Page (NEW)
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)