# On part d'une image Linux légère contenant déjà Python 3.12
FROM python:3.12-slim

# On met à jour le système et on installe Java (JRE)
RUN apt-get update && \
    apt-get install -y default-jre && \
    rm -rf /var/lib/apt/lists/*

# On définit le dossier de travail
WORKDIR /app

# On copie nos fichiers et on installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le reste de notre code
COPY . .

# On lance le serveur Gunicorn sur le port attendu par Render
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
