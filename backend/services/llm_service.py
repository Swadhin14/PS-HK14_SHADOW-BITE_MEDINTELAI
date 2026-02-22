import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


def generate_response(prompt: str, temperature: float = 0.2):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        if response.status_code != 200:
            raise Exception(f"Ollama Error: {response.text}")

        return response.json().get("response", "").strip()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection error with Ollama: {str(e)}")