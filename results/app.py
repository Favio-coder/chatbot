from flask import Flask, request, jsonify
from rasa.shared.core.agent import load_agent # type: ignore

app = Flask(__name__)

# Cargar el modelo de Rasa
model_path = "chatbot/results/20240629-194611-violet-depth"
agent = load_agent(model_path)

@app.route('/webhook', methods=['POST'])
def webhook():
    input_data = request.json
    message = input_data['message']
    
    # Manejar el texto de entrada con el agente de Rasa
    response = agent.handle_text(message)
    
    return jsonify(response[0]['text'])

if __name__ == '__main__':
    app.run(debug=True)
