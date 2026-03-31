from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

# Carregar base de respostas externas
with open("respostas.json", "r", encoding="utf-8") as f:
    base = {item["pergunta"].lower(): [item["resposta"]] for item in json.load(f)}

# Histórico de mensagens e memória simples
historico = []
memoria = {
    "nome": None,
    "pet": None,
    "hobby": None,
    "humor": None
}

# Função de correspondência
from difflib import SequenceMatcher

def melhor_correspondencia(msg):
    melhor_score = 0
    melhor_resposta = None
    for pergunta, respostas in base.items():
        score = SequenceMatcher(None, msg, pergunta).ratio()
        if score > melhor_score:
            melhor_score = score
            melhor_resposta = random.choice(respostas)
    return melhor_resposta if melhor_score > 0.5 else None

def responder(msg):
    global historico, memoria
    msg = msg.lower()
    historico.append(msg)

    # Memória simples
    if "meu nome é" in msg:
        memoria["nome"] = msg.split("meu nome é")[-1].strip()
        return f"Prazer, {memoria['nome']}!"
    if "qual meu nome" in msg:
        return f"Seu nome é {memoria.get('nome', 'você ainda não me disse')}"

    # Resposta padrão
    resp = melhor_correspondencia(msg)
    if resp:
        if memoria.get("nome"):
            return f"{resp} {memoria['nome']}"
        return resp

    # fallback
    respostas_fallback = [
        "Interessante, me conte mais.",
        "Pode explicar melhor?",
        "Ainda estou aprendendo, mas estou te ouvindo.",
        "Uau, que legal!"
    ]
    return random.choice(respostas_fallback)

# -------- ROTAS --------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    resposta = responder(msg)
    return jsonify({"response": resposta})

# Inicialização
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)