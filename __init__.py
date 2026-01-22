from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return f"<h2>Bienvenue, {session.get('username')} ({session.get('role')})</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['authentifie'] = True
            session['username'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('lecture'))

        elif username == 'user' and password == '12345':
            session['authentifie'] = True
            session['username'] = 'user'
            session['role'] = 'user'
            return redirect(url_for('lecture'))

        return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# =======================
# GESTION DES TÂCHES
# =======================

@app.route('/taches')
def taches():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM taches ORDER BY created DESC")
    data = cursor.fetchall()
    conn.close()

    return render_template('taches.html', taches=data)

@app.route('/taches/ajouter', methods=['POST'])
def ajouter_tache():
    titre = request.form['titre']
    description = request.form['description']
    date_echeance = request.form['date_echeance']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO taches (titre, description, date_echeance) VALUES (?, ?, ?)",
        (titre, description, date_echeance)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('taches'))

@app.route('/taches/supprimer/<int:id>')
def supprimer_tache(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM taches WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('taches'))

@app.route('/taches/terminer/<int:id>')
def terminer_tache(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE taches 
        SET est_terminee = CASE est_terminee WHEN 1 THEN 0 ELSE 1 END 
        WHERE id = ?
    """, (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('taches'))

if __name__ == "__main__":
    app.run(debug=True)
