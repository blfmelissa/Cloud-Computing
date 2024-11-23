from fastapi import FastAPI, HTTPException
from models import Book
from database import get_connection

app = FastAPI()

@app.on_event("startup")
def create_tables():
    """Crée la table des livres au démarrage si elle n'existe pas."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='books' AND xtype='U')
        CREATE TABLE books (
            id INT IDENTITY PRIMARY KEY,
            title NVARCHAR(255) NOT NULL,
            author NVARCHAR(255) NOT NULL,
            year INT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur le site de gestion de livres !"}

@app.get("/books")
def get_books():
    """Récupère tous les livres."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, author, year FROM books")
    books = cursor.fetchall()
    connection.close()
    return [{"id": row.id, "title": row.title, "author": row.author, "year": row.year} for row in books]

@app.post("/books")
def create_book(book: Book):
    """Ajoute un nouveau livre."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                   book.title, book.author, book.year)
    connection.commit()
    connection.close()
    return {"message": "Livre ajouté avec succès"}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    """Récupère un livre par son ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, author, year FROM books WHERE id = ?", book_id)
    row = cursor.fetchone()
    connection.close()
    if not row:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return {"id": row.id, "title": row.title, "author": row.author, "year": row.year}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    """Met à jour un livre existant."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",
                   book.title, book.author, book.year, book_id)
    connection.commit()
    connection.close()
    return {"message": "Livre mis à jour avec succès"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """Supprime un livre."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", book_id)
    connection.commit()
    connection.close()
    return {"message": "Livre supprimé avec succès"}
