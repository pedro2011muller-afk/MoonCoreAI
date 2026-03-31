from flask import Flask, render_template, request, jsonify
import random
import json
import os
import unicodedata
import string
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# -------- ARQUIVO JSON --------
JSON_FILE = "respostas.json"

# -------- CARREGA BASE --------
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        base_data = json.load(f)
else:
    base_data = []

# Transformar em dicionário para busca rápida
base = {item["pergunta"].lower(): [item["resposta"]] for item in base_data}

# -------- MEMÓRIA SIMPLES --------
historico = []
memoria = {
    "nome": None,
    "hobby": None,
    "humor": None
}

# -------- FUNÇÕES AUXILIARES --------
def limpar_texto(msg):
    msg = ''.join(c for c in unicodedata.normalize('NFD', msg)
                  if unicodedata.category(c) != 'Mn')
    msg = msg.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    return msg

# -------- FUNÇÃO DE BUSCA WIKIPÉDIA --------
def buscar_wikipedia(termo):
    url = f"https://pt.wikipedia.org/wiki/{termo.replace(' ', '_')}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        p = soup.find('p')
        if p:
            texto = p.get_text()
            return texto.strip()
    except Exception as e:
        print("Erro ao buscar Wikipedia:", e)
        return None

# -------- FUNÇÃO DE RESPOSTA AVANÇADA --------
def responder(msg):
    global historico, memoria, base_data, base
    msg_clean = msg.lower().strip()
    historico.append(msg_clean)

    # -------- MEMÓRIA --------
    if "meu nome é" in msg_clean:
        memoria["nome"] = msg_clean.split("meu nome é")[-1].strip()
        return f"Prazer em te conhecer, {memoria['nome']}!"
    if "qual meu nome" in msg_clean:
        return f"Seu nome é {memoria.get('nome', 'você ainda não me disse')}"

    if "meu hobby é" in msg_clean:
        memoria["hobby"] = msg_clean.split("meu hobby é")[-1].strip()
        return f"Legal! Vou lembrar que seu hobby é {memoria['hobby']}."

    if "como estou" in msg_clean and memoria.get("nome"):
        return f"{memoria['nome']}, você parece bem hoje!"

    # -------- CORRESPONDÊNCIA INTELIGENTE --------
    for pergunta, respostas in base.items():
        if msg_clean == pergunta.lower():  # exata
            return random.choice(respostas)
    for pergunta, respostas in base.items():  # palavras-chave
        palavras = pergunta.lower().split()
        if any(palavra in msg_clean for palavra in palavras):
            return random.choice(respostas)

    # -------- BUSCA AVANÇADA NA INTERNET --------
    resposta_internet = buscar_wikipedia(msg_clean)
    if not resposta_internet:
        palavras_chave = [p for p in msg_clean.split() if len(p) > 3]  # evita palavras curtas
        respostas_temp = []
        for palavra in palavras_chave:
            r = buscar_wikipedia(palavra)
            if r:
                respostas_temp.append(r)
        if respostas_temp:
            resposta_internet = " ".join(respostas_temp[:2])

    # Salva no JSON se encontrou
    if resposta_internet:
        base[msg_clean] = [resposta_internet]
        base_data.append({"pergunta": msg_clean, "resposta": resposta_internet})
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(base_data, f, ensure_ascii=False, indent=2)
        return resposta_internet

    # -------- FALLBACK --------
    respostas_fallback = [
        "Interessante, me conte mais.",
        "Pode explicar melhor?",
        "Ainda estou aprendendo, mas estou te ouvindo.",
        "Uau, que legal!",
        "Hmm… não entendi direito, pode tentar de outra forma?"
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

# -------- INICIALIZAÇÃO --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)