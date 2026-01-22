import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Table livres (bibliothèque)
cursor.execute("""
CREATE TABLE IF NOT EXISTS livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    annee_publication INTEGER
)
""")

# Table taches (mini projet PDF)
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

# Données de test uniquement si livres est vide
cursor.execute("SELECT COUNT(*) FROM livres")
if cursor.fetchone()[0] == 0:
    livres = [
        ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943),
        ('1984', 'George Orwell', 1949),
        ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 1954),
        ("L'Étranger", 'Albert Camus', 1942),
        ("Harry Potter à l'école des sorciers", 'J.K. Rowling', 1997)
    ]
    cursor.executemany(
        "INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)",
        livres
    )

connection.commit()
connection.close()

print("Base de données initialisée sans perte de données.")
