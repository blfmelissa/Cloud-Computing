# Utilise une image Python
FROM python:3.9

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers dans le conteneur
COPY . /app

# Installe les dépendances
RUN pip install -r requirements.txt

# Installe les dépendances pour pyodbc et le driver SQL Server
RUN apt-get update && apt-get install -y \
    unixodbc-dev curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Expose le port 8080
EXPOSE 8080

# Commande par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
