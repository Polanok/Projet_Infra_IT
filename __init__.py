from flask import Flask, render_template, jsonify, request, redirect, url_for, session, Response
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# =========================
# OUTILS
# =========================

def est_authentifie():
    return session.get('authentifie')

def get_db():
    return sqlite3.connect("database.db")

def check_user_auth(auth):
    return auth and auth.username == "user" and auth.password == "12345"

# =========================
# ROUTES EXISTANTES
# =========================

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié (ADMIN)</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)',
        (1002938, nom, prenom, "ICI")
    )
    conn.commit()
    conn.close()
    return redirect('/consultation/')

# =========================
# 🔥 SÉQUENCE 5 — NOUVELLE ROUTE
# =========================

@app.route("/fiche_nom/", methods=["GET"])
def fiche_nom():
    # 🔐 Protection USER
    auth = request.authorization
    if not check_user_auth(auth):
        return Response(
            "Accès réservé à l'utilisateur",
            401,
            {"WWW-Authenticate": 'Basic realm="User Access"'}
        )

    # 🔎 Recherche par nom
    nom = request.args.get("nom")
    if not nom:
        return "Nom manquant", 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE nom = ?", (nom,))
    client = cursor.fetchone()
    conn.close()

    if client is None:
        return "Client non trouvé", 404

    return jsonify(client)

# =========================

if __name__ == "__main__":
    app.run(debug=True)
