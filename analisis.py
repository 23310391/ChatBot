import json

filepath = 'RC_2026-06/1/9/9/9/1956819991.jsonl'

with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            print(f"\n--- Línea {i} ---")
            print("Claves:", list(data.keys()))
            for key, value in data.items():
                if isinstance(value, str):
                    print(f"  [{key}]: {value[:150]}")
                else:
                    print(f"  [{key}]: {value}")
        except Exception as e:
            print(f"Error: {e}")

        if i >= 2:
            break