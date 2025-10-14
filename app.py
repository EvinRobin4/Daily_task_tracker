from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',              
    'password': 'tiger',  
    'database': 'task_tracker'
}


@app.route('/')
def index(): # this is the home page
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():# this is the function to add task
    title = request.form['title']
    if title:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):# this is the function to complete task
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_complete = TRUE WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id): # this is the function to edit task
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        new_title = request.form['title']
        cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", (new_title, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
        task = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id): # this is the function to delete task
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(host='0.0.0.0', port=port, debug=True)  

