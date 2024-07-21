import yaml
import json

# Ruta del archivo JSON
json_path = 'merged_lotes_finales.json'

# Leer el archivo JSON
with open(json_path, 'r', encoding='utf-8') as json_file:
    messages = json.load(json_file)

# Separar mensajes según el rol
user_messages = [msg for msg in messages if msg["role"] == "user"]
assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]

# Guardar mensajes en archivos YAML
with open('user_messages.yml', 'w', encoding='utf-8') as user_file:
    yaml.dump(user_messages, user_file, allow_unicode=True, default_flow_style=False)

with open('assistant_messages.yml', 'w', encoding='utf-8') as assistant_file:
    yaml.dump(assistant_messages, assistant_file, allow_unicode=True, default_flow_style=False)

print("Archivos YAML generados exitosamente.")
