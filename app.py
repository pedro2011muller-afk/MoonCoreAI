from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# memória
historico = []

# base de respostas
base = {
    "oi": ["Oi! 😄", "E aí!", "Olá!"],
    "como você está": ["Estou bem 😎", "Tudo certo!"],
    "qual seu nome": ["Sou a MoonCore 🤖"],
    "o que você faz": ["Converso com você 🚀"],
    "tchau": ["Até mais! 👋", "Falou 😎"]
}

def pontuar(msg, pergunta):
    palavras_msg = msg.split()
    palavras_pergunta = pergunta.split()
    score = 0
    for p in palavras_pergunta:
        if p in palavras_msg:
            score += 1
    return score

def responder(msg):
    global historico
    msg = msg.lower()
    historico.append(msg)

    # memória de nome
    if "meu nome é" in msg:
        nome = msg.split("meu nome é")[-1].strip()
        historico.append({"nome": nome})
        return f"Prazer, {nome} 😎"

    if "meu nome" in msg:
        for item in reversed(historico):
            if isinstance(item, dict) and "nome" in item:
                return f"Seu nome é {item['nome']} 😉"
        return "Você ainda não me disse seu nome 😢"

    # similaridade simples
    melhor_score = 0
    melhor_resposta = None
    for pergunta in base:
        score = pontuar(msg, pergunta)
        if score > melhor_score:
            melhor_score = score
            melhor_resposta = random.choice(base[pergunta])

    if melhor_score > 0:
        return melhor_resposta

    # contexto simples
    if len(historico) > 1:
        ultima = historico[-2]
        if isinstance(ultima, str):
            if "triste" in ultima:
                return "Quer conversar sobre isso? 😔"
            if "feliz" in ultima:
                return "Que bom ouvir isso 😄"

    # fallback
    return random.choice([
        "Hmm... interessante 👀",
        "Pode explicar melhor?",
        "Ainda estou aprendendo 🤖",
        "Isso parece importante 😎"
    ])

# rota do site
@app.route("/")
def home():
    return render_template("index.html")

# rota de chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    resposta = responder(msg)
    return jsonify({"response": resposta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)