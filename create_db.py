import sqlite3
import os

# Chemin ABSOLU vers le dossier du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemin ABSOLU vers la base SQLite
DB_PATH = os.path.join(BASE_DIR, "database.db")

print("Création de la base de données ici :", DB_PATH)

# Connexion (le fichier sera créé s'il n'existe pas)
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Création de la table taches (mini projet gestion de tâches)
cursor.execute("""
CREATE TABLE IF NOT EXISTS taches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    titre TEXT NOT NULL,
    description TEXT,
    date_echeance TEXT,
    est_terminee BOOLEAN DEFAULT 0
)
""")

connection.commit()
connection.close()

print("Base de données et table 'taches' créées avec succès.")
