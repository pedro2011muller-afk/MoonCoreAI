import random

historico = []

base = {
    "oi": ["Oi! 😄", "E aí!", "Olá!"],
    "como você está": ["Estou bem 😎", "Tudo certo!"],
    "qual seu nome": ["Sou a MoonCore 🤖"],
    "qual é sua comida favorita": ["Infelizmente eu não tenho comida favorita, pois eu sou uma IA."],
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

    # 🧠 memória de nome
    if "meu nome é" in msg:
        nome = msg.split("meu nome é")[-1].strip()
        historico.append({"nome": nome})
        return f"Prazer, {nome} 😎"

    if "meu nome" in msg:
        for item in reversed(historico):
            if isinstance(item, dict) and "nome" in item:
                return f"Seu nome é {item['nome']} 😉"
        return "Você ainda não me disse seu nome 😢"

    # 🤖 similaridade leve (sem sklearn)
    melhor_score = 0
    melhor_resposta = None

    for pergunta in base:
        score = pontuar(msg, pergunta)

        if score > melhor_score:
            melhor_score = score
            melhor_resposta = random.choice(base[pergunta])

    if melhor_score > 0:
        return melhor_resposta

    # 🎯 contexto
    if len(historico) > 1:
        ultima = historico[-2]

        if isinstance(ultima, str):
            if "triste" in ultima:
                return "Quer conversar sobre isso? 😔"
            if "feliz" in ultima:
                return "Que bom ouvir isso 😄"

    # 🎲 fallback
    return random.choice([
        "Hmm... interessante 👀",
        "Pode explicar melhor?",
        "Ainda estou aprendendo 🤖",
        "Isso parece importante 😎"
    ])