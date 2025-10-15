from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# ✅ Your Neon PostgreSQL connection string
DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_Uf5iQT9NLDeY@ep-square-bush-adm63pyh-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

def get_connection():
    return psycopg2.connect(DB_URL)

@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, is_complete FROM tasks ORDER BY id ASC;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    if title:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET is_complete = TRUE WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        new_title = request.form['title']
        cur.execute("UPDATE tasks SET title = %s WHERE id = %s;", (new_title, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT id, title FROM tasks WHERE id = %s;", (id,))
        task = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('edit.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
