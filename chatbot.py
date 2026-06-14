# chatbot.py
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Cargar modelos
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('matrix.pkl', 'rb') as f:
    X = pickle.load(f)
with open('respuestas.pkl', 'rb') as f:
    respuestas = pickle.load(f)

UMBRAL = 0.3  # Si la similitud es menor, el bot "no sabe"

def responder(mensaje: str) -> str:
    vec = vectorizer.transform([mensaje])
    sims = cosine_similarity(vec, X)
    idx  = int(np.argmax(sims))
    if sims[0, idx] < UMBRAL:
        return "No sé cómo responder a eso. 🎬"
    return respuestas[idx]

if __name__ == "__main__":
    print("Chatbot de películas. Escribe 'salir' para terminar.\n")
    while True:
        entrada = input("Tú: ").strip()
        if entrada.lower() == "salir":
            break
        print(f"Bot: {responder(entrada)}\n")