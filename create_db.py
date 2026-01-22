import sqlite3

# Connexion à la base de données (le fichier sera créé s'il n'existe pas)
connection = sqlite3.connect('database.db')

# Lecture et exécution du fichier schema.sql (qui contient CREATE TABLE livres)
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion de quelques livres pour tester votre application Bibliothèque
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", 
            ('Le Petit Prince', 'Antoine de Saint-Exupéry'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", 
            ('1984', 'George Orwell'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", 
            ('Le Seigneur des Anneaux', 'J.R.R. Tolkien'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", 
            ('L''Étranger', 'Albert Camus'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", 
            ('Harry Potter à l''école des sorciers', 'J.K. Rowling'))

connection.commit()
connection.close()

print("Base de données initialisée avec succès avec la table 'livres' !")
