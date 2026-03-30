from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "MoonCore está online! Use /chat?msg=SuaMensagem para testar."

@app.route("/chat")
def chat():
    user_msg = request.args.get("msg", "")
    resposta = f"Você disse: {user_msg}"
    return resposta

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
