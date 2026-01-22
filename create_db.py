import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('1984', 'George Orwell'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Le Seigneur des Anneaux', 'J.R.R. Tolkien'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('L''Étranger', 'Albert Camus'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Harry Potter à l''école des sorciers', 'J.K. Rowling'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Le Père Goriot', 'Honoré de Balzac'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Les Misérables', 'Victor Hugo'))
cur.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Une vie', 'Guy de Maupassant'))

connection.commit()
connection.close()
