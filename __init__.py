from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# =======================
# CONFIGURATION BASE DE DONNÉES (CORRECTION CRITIQUE)
# =======================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# =======================
# AUTHENTIFICATION
# =======================

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
# BIBLIOTHÈQUE (CODE EXISTANT CONSERVÉ)
# =======================

@app.route('/fiche_livre/<titre>')
def fiche_livre(titre):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',))
    data = cursor.fetchall()
    conn.close()

    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé", 403

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)',
            (titre, auteur, annee)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('ReadBDD'))

    return render_template('formulaire_livre.html')

# =======================
# GESTION DES TÂCHES (MINI PROJET PDF)
# =======================

@app.route('/taches')
def taches():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM taches ORDER BY created DESC')
    taches = cursor.fetchall()
    conn.close()

    return render_template('taches.html', taches=taches)

@app.route('/taches/ajouter', methods=['POST'])
def ajouter_tache():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    titre = request.form['titre']
    description = request.form['description']
    date_echeance = request.form['date_echeance']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO taches (titre, description, date_echeance) VALUES (?, ?, ?)',
        (titre, description, date_echeance)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('taches'))

@app.route('/taches/supprimer/<int:id>')
def supprimer_tache(id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('taches'))

@app.route('/taches/terminer/<int:id>')
def terminer_tache(id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE taches SET est_terminee = CASE est_terminee WHEN 1 THEN 0 ELSE 1 END WHERE id = ?',
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('taches'))

# =======================
# LANCEMENT
# =======================

if __name__ == "__main__":
    app.run(debug=True)
