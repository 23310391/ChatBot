# vectorizar.py
import sqlite3
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

connection = sqlite3.connect('chatbot_peliculas.db')
c = connection.cursor()
rows = c.execute("SELECT entrada, respuesta FROM pares_dialogo").fetchall()
connection.close()

entradas  = [r[0] for r in rows]
respuestas = [r[1] for r in rows]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(entradas)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('matrix.pkl', 'wb') as f:
    pickle.dump(X, f)
with open('respuestas.pkl', 'wb') as f:
    pickle.dump(respuestas, f)

print(f"✅ Vectorizado. {len(entradas):,} pares listos.")