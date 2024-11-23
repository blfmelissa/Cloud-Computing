from fastapi import FastAPI
import pyodbc
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Azure!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Connexion à la base de données
@app.on_event("startup")
def startup_db():
    global connection
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=tcp:mlizsqlserver.database.windows.net,1433;'
        'DATABASE=books-db;'
        'UID=melissa;'
        'PWD={your_password}'
    )

@app.on_event("shutdown")
def shutdown_db():
    connection.close()

