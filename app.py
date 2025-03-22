import os
import openai
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração da chave da OpenAI
openai.api_key = "sk-proj-Z4vYo6XcGlJqZBTiL6eNP0AVi0aqL8A7auXGELOrF qZ8XAdx2XEaBdav21x-zkHOlpLwOG4TtJT3BlbkFJvGRsxUJpU0gCkP4JpXhXd 1Br-kyeHsrj6k4eDrxiKwZRbrTrXcwNZc1LVmnkYJ5PdUWev57doA"  # Substitua pela sua chave da OpenAI

# Caminhos para os arquivos de dados
financeiro_file = 'financeiro.json'
users_file = 'users.json'

# Função para carregar dados financeiros do arquivo
def carregar_dados_financeiros():
    if os.path.exists(financeiro_file):
        with open(financeiro_file, 'r') as f:
            return json.load(f)
    return {"entradas": [], "saidas": [], "metas": []}

# Função para salvar dados financeiros no arquivo
def salvar_dados_financeiros(dados):
    with open(financeiro_file, 'w') as f:
        json.dump(dados, f)

# Função para consultar a OpenAI para perguntas inteligentes
def perguntar_openai(question):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Escolha o modelo da OpenAI
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Pergunta não fornecida"}), 400

    resposta = perguntar_openai(question)
    return jsonify({"answer": resposta})

@app.route('/registrar_entrada', methods=['POST'])
def registrar_entrada():
    data = request.get_json()
    valor = data.get("valor")
    descricao = data.get("descricao")
    
    if not valor or not descricao:
        return jsonify({"error": "Valor e descrição são obrigatórios"}), 400
    
    dados = carregar_dados_financeiros()
    dados["entradas"].append({"valor": valor, "descricao": descricao})
    salvar_dados_financeiros(dados)
    return jsonify({"message": "Entrada registrada com sucesso!"})

@app.route('/registrar_saida', methods=['POST'])
def registrar_saida():
    data = request.get_json()
    valor = data.get("valor")
    descricao = data.get("descricao")
    
    if not valor or not descricao:
        return jsonify({"error": "Valor e descrição são obrigatórios"}), 400
    
    dados = carregar_dados_financeiros()
    dados["saidas"].append({"valor": valor, "descricao": descricao})
    salvar_dados_financeiros(dados)
    return jsonify({"message": "Saída registrada com sucesso!"})

@app.route('/consultar_saldo', methods=['GET'])
def consultar_saldo():
    dados = carregar_dados_financeiros()
    total_entradas = sum([entrada["valor"] for entrada in dados["entradas"]])
    total_saidas = sum([saida["valor"] for saida in dados["saidas"]])
    saldo = total_entradas - total_saidas
    return jsonify({"saldo": saldo})

@app.route('/definir_meta', methods=['POST'])
def definir_meta():
    data = request.get_json()
    meta = data.get("meta")
    
    if not meta:
        return jsonify({"error": "Meta não fornecida"}), 400

    dados = carregar_dados_financeiros()
    dados["metas"].append({"meta": meta, "concluida": False})
    salvar_dados_financeiros(dados)
    return jsonify({"message": "Meta definida com sucesso!"})

@app.route('/consultar_metas', methods=['GET'])
def consultar_metas():
    dados = carregar_dados_financeiros()
    return jsonify({"metas": dados["metas"]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
