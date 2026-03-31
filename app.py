from flask import Flask, render_template, request, jsonify
import random
import json
import os
import unicodedata
import string
from bs4 import BeautifulSoup
import requests
from sentence_transformers import SentenceTransformer
import numpy as np

app = Flask(__name__)

# -------- ARQUIVO JSON --------
JSON_FILE = "respostas.json"

# -------- CARREGA BASE --------
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        base_data = json.load(f)
else:
    base_data = []

base = {item["pergunta"].lower(): [item["resposta"]] for item in base_data}

# -------- MEMÓRIA SIMPLES --------
memoria = {"nome": None, "hobby": None}
historico = []  # histórico para embeddings

# -------- MODELO DE EMBEDDINGS --------
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# -------- FUNÇÕES AUXILIARES --------
def limpar_texto(msg):
    msg = ''.join(c for c in unicodedata.normalize('NFD', msg)
                  if unicodedata.category(c) != 'Mn')
    msg = msg.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    return msg

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

def similaridade(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def responder_com_embeddings(msg):
    if not historico:
        return None

    vetor_msg = modelo.encode(msg)
    maior_sim = -1
    resposta_escolhida = None
    for item in historico[::-1]:  # começa do mais recente
        vetor_antigo = modelo.encode(item["pergunta"])
        sim = similaridade(vetor_msg, vetor_antigo)
        if sim > maior_sim:
            maior_sim = sim
            resposta_escolhida = item["resposta"]

    if maior_sim > 0.6:
        return resposta_escolhida
    return None

# -------- FUNÇÃO RESPONDER HÍBRIDA --------
def responder(msg):
    global memoria, base_data, base, historico
    msg_clean = msg.lower().strip()

    # MEMÓRIA
    if "meu nome é" in msg_clean:
        memoria["nome"] = msg_clean.split("meu nome é")[-1].strip()
        return f"Prazer em te conhecer, {memoria['nome']}!"
    if "qual meu nome" in msg_clean:
        return f"Seu nome é {memoria.get('nome', 'você ainda não me disse')}"
    if "meu hobby é" in msg_clean:
        memoria["hobby"] = msg_clean.split("meu hobby é")[-1].strip()
        return f"Vou lembrar que seu hobby é {memoria['hobby']}."
    if "como estou" in msg_clean and memoria.get("nome"):
        return f"{memoria['nome']}, você parece bem hoje!"

    # CORRESPONDÊNCIA JSON
    if msg_clean in base:
        resposta = random.choice(base[msg_clean])
        historico.append({"pergunta": msg, "resposta": resposta})
        return resposta

    for pergunta, respostas in base.items():
        palavras = pergunta.lower().split()
        if any(palavra in msg_clean for palavra in palavras):
            resposta = random.choice(respostas)
            historico.append({"pergunta": msg, "resposta": resposta})
            return resposta

    # -------- EMBEDDINGS (contexto) --------
    resposta_contexto = responder_com_embeddings(msg)
    if resposta_contexto:
        historico.append({"pergunta": msg, "resposta": resposta_contexto})
        return resposta_contexto

    # -------- LIMPAR TERMO PARA BUSCA --------
    termo = msg_clean.replace("?", "").replace("como", "").replace("qual", "").replace("o que", "").strip()
    palavras_chave = [p for p in termo.split() if len(p) > 3]

    respostas_temp = []
    for palavra in palavras_chave:
        r = buscar_wikipedia(palavra)
        if r:
            respostas_temp.append(r)

    if respostas_temp:
        resposta_final = " ".join(respostas_temp[:2])
        base[msg_clean] = [resposta_final]
        base_data.append({"pergunta": msg_clean, "resposta": resposta_final})
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(base_data, f, ensure_ascii=False, indent=2)
        historico.append({"pergunta": msg, "resposta": resposta_final})
        return resposta_final

    # FALLBACK
    fallback = "Não entendi exatamente, pode explicar melhor?"
    historico.append({"pergunta": msg, "resposta": fallback})
    return fallback

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