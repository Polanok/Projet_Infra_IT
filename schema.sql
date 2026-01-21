DROP TABLE IF EXISTS livres;

CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    annee_publication INTEGER,
    isbn TEXT,
    disponible BOOLEAN DEFAULT 1 -- 1 pour disponible, 0 pour emprunté
);
