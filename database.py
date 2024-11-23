import pyodbc
import os

# Récupère les informations de connexion depuis les variables d'environnement
DB_NAME = os.getenv("DB_NAME", "books_db")
DB_USER = os.getenv("DB_USER", "melissa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "781227moi!")
DB_HOST = os.getenv("DB_HOST", "db")  # Nom du conteneur de la base de données

# Chaîne de connexion à SQL Server
connection_string = (
    f"DRIVER=ODBC Driver 17 for SQL Server;"
    f"SERVER={DB_HOST};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)

def get_connection():
    """Ouvre une connexion à la base de données."""
    return pyodbc.connect(connection_string)
