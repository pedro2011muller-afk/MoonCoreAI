from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

# memória
historico = []

# base de conhecimento
base = {
    "oi": ["Oi! 😄", "E aí!", "Olá!"],
    "como você está": ["Estou funcionando perfeitamente 😎", "Tudo certo por aqui!"],
    "qual seu nome": ["Sou a MoonCore 🤖"],
    "o que você faz": ["Converso com você e evoluo 🚀"]
}

def detectar_resposta(msg):
    perguntas = list(base.keys())
    respostas = list(base.values())

    textos = perguntas + [msg]

    vectorizer = TfidfVectorizer().fit_transform(textos)
    similaridade = cosine_similarity(vectorizer[-1], vectorizer[:-1])

    indice = similaridade.argmax()

    if similaridade[0][indice] > 0.3:
        return random.choice(respostas[indice])
    
    return None


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
        return "Você não me disse seu nome ainda 😢"

    # 🤖 IA por similaridade
    resposta = detectar_resposta(msg)
    if resposta:
        return resposta

    # 🎯 contexto simples
    if len(historico) > 1:
        ultima = historico[-2]

        if isinstance(ultima, str):
            if "triste" in ultima:
                return "Quer conversar sobre isso? 😔"
            if "feliz" in ultima:
                return "Que bom 😄"

    # 🎲 fallback inteligente
    return random.choice([
        "Hmm... interessante 👀",
        "Pode explicar melhor?",
        "Ainda estou aprendendo 🤖",
        "Isso parece importante 😎"
    ])