import requests

def test_integration():
    url = 'http://localhost:5005/webhooks/rest/webhook'
    conversation = [
        {"input": "Hola", "output": "Hola, ¿en qué puedo ayudarte?"},
        {"input": "Quiero saber más sobre la ansiedad", "output": "La ansiedad es"},
        # Agrega más interacciones para completar el flujo
    ]

    for step in conversation:
        response = requests.post(url, json={"message": step["input"]})
        response_text = response.json()[0]['text']
        assert step["output"] in response_text

if __name__ == '__main__':
    test_integration()
