from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criação do banco de dados
def init_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news ORDER BY date DESC')
    news_items = c.fetchall()
    conn.close()
    return render_template('index.html', news_items=news_items)

@app.route('/add', methods=['GET', 'POST'])
def add_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']

        conn = sqlite3.connect('news.db')
        c = conn.cursor()
        c.execute("INSERT INTO news (title, content, date) VALUES (?, ?, ?)", (title, content, date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_news.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
