from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

# Fonction utilitaire pour se connecter à la base de données
# Elle permet aussi de récupérer les résultats sous forme de "dictionnaire" (plus facile à utiliser)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. ACCUEIL : Afficher la liste des tâches (Consultation)
# Remplace votre ancienne route 'hello_world' et 'consultation'
@app.route('/')
def index():
    conn = get_db_connection()
    # On récupère toutes les tâches de la table créée à l'étape précédente
    taches = conn.execute('SELECT * FROM taches').fetchall()
    conn.close()
    return render_template('index.html', taches=taches)

# 2. AJOUTER : Créer une nouvelle tâche
# Remplace 'enregistrer_livre'
@app.route('/ajouter', methods=('GET', 'POST'))
def ajouter():
    if request.method == 'POST':
        # On récupère les données du formulaire HTML
        titre = request.form['titre']
        description = request.form['description']
        date_echeance = request.form['date_echeance']

        # Connexion et insertion en base de données
        conn = get_db_connection()
        conn.execute('INSERT INTO taches (titre, description, date_echeance) VALUES (?, ?, ?)',
                     (titre, description, date_echeance))
        conn.commit()
        conn.close()
        # Une fois ajouté, on retourne à l'accueil
        return redirect(url_for('index'))
            
    return render_template('ajouter.html')

# 3. SUPPRIMER : Effacer une tâche
# Nouvelle fonctionnalité demandée dans le PDF
@app.route('/supprimer/<int:id>', methods=('POST',))
def supprimer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 4. TERMINER : Marquer une tâche comme faite
# Nouvelle fonctionnalité demandée dans le PDF
@app.route('/terminer/<int:id>', methods=('POST',))
def terminer(id):
    conn = get_db_connection()
    # On met à jour le champ 'est_terminee' à 1 (Vrai)
    conn.execute('UPDATE taches SET est_terminee = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
