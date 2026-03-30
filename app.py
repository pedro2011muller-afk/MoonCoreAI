from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

API_KEY = os.environ.get("OPENAI_API_KEY")

def responder_ia(msg):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": msg}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    res = response.json()

    return res["choices"][0]["message"]["content"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    resposta = responder_ia(user_msg)

    return jsonify({"response": resposta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)