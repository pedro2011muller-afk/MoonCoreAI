from flask import Flask, render_template, request, jsonify
import random
import os  # necessário para Render

app = Flask(__name__)

# memória de sessão
historico = []

# base de respostas expandida
base = {
    "oi": ["Oi! 😄", "E aí!", "Olá! Como vai?"],
    "bom dia": ["Bom dia! ☀️", "Dia ótimo pra gente conversar 😎"],
    "boa tarde": ["Boa tarde! 😄", "Espero que esteja tendo uma boa tarde!"],
    "boa noite": ["Boa noite! 🌙", "Durma bem depois! 😴"],
    "como você está": ["Estou bem 😎", "Tudo certo!", "Animado para conversar com você!"],
    "qual seu nome": ["Sou a MoonCore 🤖", "MoonCore AI à disposição!"],
    "o que você faz": ["Converso com você 🚀", "Estou aqui pra bater papo e aprender contigo 😎"],
    "tchau": ["Até mais! 👋", "Falou 😎", "Até a próxima!"],
    "obrigado": ["De nada! 😄", "Imagina! 😉"],
    "qual a sua função": ["Responder suas perguntas e bater papo 😎"],
    "você gosta de conversar": ["Sim! Adoro conversar 😄", "Claro, é pra isso que fui feito 🤖"],
    "estou triste": ["Sinto muito 😔 Quer conversar sobre isso?", "Estou aqui pra te ouvir 😢"],
    "estou feliz": ["Que bom ouvir isso! 😄", "Fico feliz por você! 😎"]
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

# função de pontuação simples
def pontuar(msg, pergunta):
    palavras_msg = msg.split()
    palavras_pergunta = pergunta.split()
    score = 0
    for p in palavras_pergunta:
        if p in palavras_msg:
            score += 1
    return score

# função principal de resposta
def responder(msg):
    global historico
    msg = msg.lower()
    msg = substituir_sinonimos(msg)
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

    # memória de pet (exemplo de aprendizado simples)
    if "meu animal de estimação é" in msg:
        pet = msg.split("meu animal de estimação é")[-1].strip()
        historico.append({"pet": pet})
        return f"Que legal! Vou me lembrar que seu pet é {pet} 😄"

    if "qual meu pet" in msg:
        for item in reversed(historico):
            if isinstance(item, dict) and "pet" in item:
                return f"Seu pet é {item['pet']} 😉"
        return "Você ainda não me contou sobre seu pet 😢"

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

    # contexto simples baseado na última mensagem
    if len(historico) > 1:
        ultima = historico[-2]
        if isinstance(ultima, str):
            if "triste" in ultima or "chateado" in ultima:
                return "Quer conversar sobre isso? 😔"
            if "feliz" in ultima or "animado" in ultima:
                return "Que bom ouvir isso! 😄"

    # fallback divertido
    respostas_fallback = [
        "Hmm... interessante 👀 Me conte mais!",
        "Pode explicar melhor? Quero entender 😄",
        "Ainda estou aprendendo 🤖, mas estou te ouvindo!",
        "Isso parece importante 😎 Conte-me mais detalhes!",
        "Uau, que legal! 😲 Me fale mais sobre isso!"
    ]

    return random.choice(respostas_fallback)

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

# inicialização do app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)