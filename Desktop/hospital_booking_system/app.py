from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('appointments.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL
)
""")
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name  = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date  = request.form['date']
        time  = request.form['time']

        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (name, email, phone, date, time) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, date, time)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('success'))

    return render_template('appointment.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/bookings')
def bookings():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, phone, date, time FROM appointments')
    rows = cursor.fetchall()
    conn.close()
    return render_template('bookings.html', rows=rows)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appointments WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('bookings'))


if __name__ == '__main__':
    app.run(debug=True)