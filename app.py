from flask import Flask, render_template, request, jsonify
import random
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# memória de sessão
historico = []
memoria = {
    "nome": None,
    "pet": None,
    "hobby": None,
    "humor": None
}

# base inicial de respostas
base = {
    "oi": ["Oi! 😄", "E aí!", "Olá! Como vai?"],
    "bom dia": ["Bom dia! ☀️", "Dia ótimo pra gente conversar 😎"],
    "boa tarde": ["Boa tarde! 😄", "Espero que esteja tendo uma boa tarde!"],
    "boa noite": ["Boa noite! 🌙", "Durma bem depois! 😴"],
    "como você está": ["Estou bem 😎", "Tudo certo!", "Animado para conversar com você!"],
    "qual seu nome": ["Sou a MoonCore 🤖", "MoonCore AI à disposição!"],
    "o que você faz": ["Converso com você 🚀", "Estou aqui pra bater papo e aprender contigo 😎"],
    "tchau": ["Até mais! 👋", "Falou 😎", "Até a próxima!"],
    "obrigado": ["De nada! 😄", "Imagina! 😉"]
}

# sinônimos simples
sinonimos = {
    "oi": ["oi", "ola", "olá", "e aí", "hey"],
    "tchau": ["tchau", "adeus", "falou", "até mais"]
}

def substituir_sinonimos(msg):
    for chave, lista in sinonimos.items():
        for s in lista:
            if s in msg:
                return chave
    return msg

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
    msg = substituir_sinonimos(msg)
    historico.append(msg)

    # memória de nome
    if "meu nome é" in msg:
        nome = msg.split("meu nome é")[-1].strip()
        memoria["nome"] = nome
        return f"Prazer, {nome}! 😎"
    if "qual meu nome" in msg:
        return f"Seu nome é {memoria.get('nome', 'você ainda não me disse 😢')}"

    # memória de hobby
    if "meu hobby é" in msg:
        memoria["hobby"] = msg.split("meu hobby é")[-1].strip()
        return f"Que legal! Vou lembrar que seu hobby é {memoria['hobby']} 😄"
    if "qual meu hobby" in msg:
        return f"Seu hobby é {memoria.get('hobby', 'você ainda não me contou 😢')}"

    # memória de pet
    if "meu animal de estimação é" in msg:
        memoria["pet"] = msg.split("meu animal de estimação é")[-1].strip()
        return f"Que legal! Vou lembrar que seu pet é {memoria['pet']} 😄"
    if "qual meu pet" in msg:
        return f"Seu pet é {memoria.get('pet', 'você ainda não me contou 😢')}"

    # memória de humor
    if "estou triste" in msg or "me sinto triste" in msg:
        memoria["humor"] = "triste"
        return "Sinto muito 😔 Quer conversar sobre isso?"
    if "estou feliz" in msg or "me sinto feliz" in msg:
        memoria["humor"] = "feliz"
        return "Que bom 😄 Fico feliz por você!"

    # aprendizado de sessão
    if "ensine" in msg:
        try:
            partes = msg.split("ensine")[1].split("->")
            pergunta, resposta = partes[0].strip().lower(), partes[1].strip()
            base[pergunta] = [resposta]
            return "Aprendi isso! 😎"
        except:
            return "Formato incorreto. Use: ensine <pergunta> -> <resposta>"

    # melhor correspondência
    resp = melhor_correspondencia(msg)
    if resp:
        # personalização com nome
        if memoria.get("nome"):
            templates = [
                resp + f" {memoria['nome']} 😄",
                f"{memoria['nome']}, {resp}",
                resp
            ]
            return random.choice(templates)
        return resp

    # fallback
    respostas_fallback = [
        "Hmm... interessante 👀 Me conte mais!",
        "Pode explicar melhor? Quero entender 😄",
        "Ainda estou aprendendo 🤖, mas estou te ouvindo!",
        "Isso parece importante 😎 Conte-me mais detalhes!",
        "Uau, que legal! 😲 Me fale mais sobre isso!"
    ]
    return random.choice(respostas_fallback)

# rota principal
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

# inicialização
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)