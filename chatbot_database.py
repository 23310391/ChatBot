import sqlite3
import json
import os

dataset_path = 'RC_2026-06'  # Carpeta principal

connection = sqlite3.connect('chatbot_peliculas.db')
c = connection.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS pares_dialogo
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               entrada TEXT,
               respuesta TEXT)""")
    connection.commit()

def format_data(data):
    data = data.replace("\n", " ").replace("\r", " ").replace('"', "'").strip()
    return data

def acceptable(data):
    if len(data.split(' ')) > 50:
        return False
    if len(data) < 2:
        return False
    if len(data) > 500:
        return False
    return True

def insertar_par(entrada, respuesta):
    try:
        c.execute("INSERT INTO pares_dialogo (entrada, respuesta) VALUES (?, ?)",
                  (entrada, respuesta))
    except Exception as e:
        pass

def procesar_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        dialogues = data.get('dialogues', [])
        for dialogo in dialogues:
            # Cada dialogo es un string con turnos separados por \n
            turnos = [format_data(t) for t in dialogo.split('\n') if format_data(t)]
            # Crear pares: (turno_i → turno_i+1)
            for i in range(len(turnos) - 1):
                entrada = turnos[i]
                respuesta = turnos[i + 1]
                if acceptable(entrada) and acceptable(respuesta):
                    insertar_par(entrada, respuesta)

if __name__ == "__main__":
    create_table()
    archivos = 0
    pares = 0

    # Recorre todas las subcarpetas recursivamente
    for root, dirs, files in os.walk(dataset_path):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                procesar_json(filepath)
                archivos += 1

                if archivos % 1000 == 0:
                    connection.commit()  # Guardar cada 1000 archivos
                    resultado = c.execute("SELECT COUNT(*) FROM pares_dialogo").fetchone()[0]
                    print(f"Archivos procesados: {archivos:,} | Pares guardados: {resultado:,}")

    connection.commit()
    total = c.execute("SELECT COUNT(*) FROM pares_dialogo").fetchone()[0]
    print(f"\n✅ Listo. Archivos: {archivos:,} | Pares totales: {total:,}")
    connection.close()