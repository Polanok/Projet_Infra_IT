from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# =========================
# OUTILS
# =========================

def get_db():
    return sqlite3.connect("database.db")

def est_authentifie():
    return session.get('authentifie')

def check_admin(auth):
    return auth and auth.username == "admin" and auth.password == "password"

def check_user(auth):
    return auth and auth.username == "user" and auth.password == "12345"

# =========================
# ROUTES AUTHENTIFICATION
# =========================

@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/auth', methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['authentifie'] = True
            session['role'] = 'admin'
            return redirect(url_for('list_books'))
        elif username == 'user' and password == '12345':
            session['authentifie'] = True
            session['role'] = 'user'
            return redirect(url_for('list_books'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# =========================
# ROUTES LIVRES
# =========================

@app.route('/books')
def list_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('list_books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Vérifier admin
    auth = request.authorization
    if not (est_authentifie() and session.get('role') == 'admin'):
        return Response("Accès refusé", 401, {"WWW-Authenticate": 'Basic realm="Admin Access"'})

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))

    return render_template('formulaire_livre.html')

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    auth = request.authorization
    if not (est_authentifie() and session.get('role') == 'admin'):
        return Response("Accès refusé", 401, {"WWW-Authenticate": 'Basic realm="Admin Access"'})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_books'))

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    if not (est_authentifie() and session.get('role') == 'user'):
        return Response("Accès refusé", 401, {"WWW-Authenticate": 'Basic realm="User Access"'})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if not book or book[0] == 0:
        conn.close()
        return "Livre indisponible", 400

    cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_books'))

@app.route('/search', methods=['GET'])
def search_books():
    title = request.args.get('title', '')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? AND available = 1", (f"%{title}%",))
    results = cursor.fetchall()
    conn.close()
    return render_template('search_results.html', books=results)

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
