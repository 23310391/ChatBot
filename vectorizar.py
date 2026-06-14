import sqlite3
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

connection = sqlite3.connect('chatbot_peliculas.db')
c = connection.cursor()

# ↓ Aquí va el cambio — antes era SELECT entrada, respuesta FROM pares_dialogo
rows = c.execute("""
    SELECT entrada, respuesta FROM pares_dialogo
    WHERE length(entrada) > 10
    AND length(respuesta) > 10
    ORDER BY RANDOM()
    LIMIT 300000
""").fetchall()

connection.close()

entradas   = [r[0] for r in rows]
respuestas = [r[1] for r in rows]

print(f"Pares cargados: {len(entradas):,}")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(entradas)

print("Vectorización completa. Guardando archivos...")

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('matrix.pkl', 'wb') as f:
    pickle.dump(X, f)
with open('respuestas.pkl', 'wb') as f:
    pickle.dump(respuestas, f)

print(f"✅ Listo. {len(entradas):,} pares vectorizados.")