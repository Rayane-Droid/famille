
from flask import Flask, render_template, request, redirect
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connexion à la base Neon PostgreSQL
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# Création de la table users si elle n'existe pas
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    email TEXT
)
""")
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    nom = request.form['nom']
    email = request.form['email']
    cur.execute("INSERT INTO users (nom, email) VALUES (%s, %s)", (nom, email))
    conn.commit()
    return redirect('/merci')


@app.route('/merci')
def merci():
    cur.execute("SELECT nom, email FROM users ORDER BY id DESC")
    users = cur.fetchall()  # Liste de tuples [(nom1, email1), (nom2, email2), ...]
    return render_template('view.html', users=users)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
