from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Memória simples
historico = []

def responder(msg):
    msg = msg.lower()

    if "oi" in msg or "ola" in msg:
        return "Oi! Como posso te ajudar? 😊"

    elif "tudo bem" in msg:
        return "Estou funcionando perfeitamente 😎"

    elif "seu nome" in msg:
        return "Sou a MoonCore, sua IA 😏"

    elif "hora" in msg:
        from datetime import datetime
        return f"Agora são {datetime.now().strftime('%H:%M')}"

    elif "tchau" in msg:
        return "Até mais! 👋"

    else:
        return "Hmm... ainda estou aprendendo 🤔"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    historico.append(user_msg)

    resposta = responder(user_msg)

    return jsonify({"response": resposta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)