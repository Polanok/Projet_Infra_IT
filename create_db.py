import sqlite3

# Connexion à la base (création si elle n'existe pas)
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()

    # -------------------
    # Création des tables
    # -------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        annee_publication INTEGER,
        isbn TEXT,
        disponible BOOLEAN DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        adresse TEXT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # -------------------
    # Insertion Clients
    # -------------------
    clients = [
        ('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'),
        ('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'),
        ('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'),
        ('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'),
        ('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'),
        ('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'),
        ('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'),
        ('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris')
    ]
    cursor.executemany(
        "INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", clients
    )

    # -------------------
    # Insertion Livres
    # -------------------
    livres = [
        ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943, '1234567890', 1),
        ('1984', 'George Orwell', 1949, '0987654321', 1),
        ('Les Misérables', 'Victor Hugo', 1862, '1122334455', 1),
        ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 1997, '5566778899', 1),
        ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 1954, '6677889900', 1)
    ]
    cursor.executemany(
        "INSERT INTO livres (titre, auteur, annee_publication, isbn, disponible) VALUES (?, ?, ?, ?, ?)",
        livres
    )

    conn.commit()
    print("Base de données initialisée avec succès : tables clients et livres créées et remplies !")
