from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# ---------------------------
# Fonction d'authentification
# ---------------------------
def est_authentifie():
    return session.get('authentifie')


# ---------------------------
# Route accueil
# ---------------------------
@app.route('/')
def home():
    return render_template('hello.html')


# ---------------------------
# Route lecture / dashboard
# ---------------------------
@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    return render_template(
        'lecture.html',
        username=session.get('username'),
        role=session.get('role')
    )


# ---------------------------
# Route authentification
# ---------------------------
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

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

        else:
            error = "Nom d'utilisateur ou mot de passe incorrect."

    return render_template('formulaire_authentification.html', error=error)


# ---------------------------
# Fonction universelle pour lire une table
# ---------------------------
def lire_table(table):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table}')
            data = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
        return data, headers
    except sqlite3.OperationalError as e:
        return [], []


# ---------------------------
# Route consultation livres
# ---------------------------
@app.route('/consultation/')
def ReadLivres():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    data, headers = lire_table('livres')
    return render_template('read_data.html', data=data, headers=headers)


# ---------------------------
# Route consultation clients
# ---------------------------
@app.route('/clients/')
def ReadClients():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    data, headers = lire_table('clients')
    return render_template('read_data.html', data=data, headers=headers)


# ---------------------------
# Route recherche d'un livre par titre
# ---------------------------
@app.route('/fiche_livre/<titre>')
def fiche_livre(titre):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',))
            data = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
    except sqlite3.OperationalError:
        data, headers = [], []

    return render_template('read_data.html', data=data, headers=headers)


# ---------------------------
# Route ajout d'un livre
# ---------------------------
@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé : Seul l'administrateur peut ajouter des livres.", 403

    error = None

    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        auteur = request.form.get('auteur', '').strip()
        annee = request.form.get('annee', '').strip()

        if not titre or not auteur:
            error = "Titre et auteur sont obligatoires."
            return render_template('formulaire_livre.html', error=error)

        try:
            annee = int(annee) if annee else None
        except ValueError:
            error = "Année invalide."
            return render_template('formulaire_livre.html', error=error)

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)',
                    (titre, auteur, annee)
                )
        except Exception as e:
            error = f"Erreur lors de l'enregistrement : {e}"
            return render_template('formulaire_livre.html', error=error)

        return redirect(url_for('ReadLivres'))

    return render_template('formulaire_livre.html', error=error)


# ---------------------------
# Route déconnexion
# ---------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# ---------------------------
# Lancement
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
