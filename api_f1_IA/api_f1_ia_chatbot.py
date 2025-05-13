from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Usa tu token de Hugging Face (obligatorio, crea uno gratis en https://huggingface.co/settings/tokens)
HF_TOKEN = os.getenv("HF_TOKEN", "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")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": f"[INST] Eres un experto en Fórmula 1 y ayudas a los usuarios con sus dudas. {question} [/INST]",
            "parameters": {"max_new_tokens": 256, "temperature": 0.7}
        }
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            # El API puede devolver una lista o un dict, manejamos ambos
            if isinstance(result, list) and 'generated_text' in result[0]:
                answer = result[0]['generated_text'].split('[/INST]')[-1].strip()
            elif isinstance(result, dict) and 'generated_text' in result:
                answer = result['generated_text'].split('[/INST]')[-1].strip()
            else:
                answer = str(result)
            return jsonify({'answer': answer})
        else:
            return jsonify({'error': response.text}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
