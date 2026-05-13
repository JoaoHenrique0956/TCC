from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# 🔐 API KEY direto no código
API_KEY = "Sua_Chave"

print("API_KEY carregada:", API_KEY)

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Corretor de Redação</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<div class="container mt-5">
    <h2>Corretor de Redação</h2>

    <select id="genero" class="form-control mb-3">
        <option>Dissertação Argumentativa</option>
        <option>Monografia</option>
        <option>Artigo Científico</option>
    </select>

    <textarea id="texto" class="form-control mb-3" rows="6" placeholder="Digite sua redação"></textarea>

    <button onclick="enviar()" class="btn btn-success">Corrigir</button>

    <pre id="resposta" class="mt-4 bg-light p-3" style="height:300px; overflow:auto;"></pre>
</div>

<script>
async function enviar() {
    const texto = document.getElementById("texto").value;
    const genero = document.getElementById("genero").value;

    if (!texto.trim()) {
        alert("Digite uma redação primeiro.");
        return;
    }

    document.getElementById("resposta").innerText = "Corrigindo...";

    const res = await fetch("/corrigir", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ texto, genero })
    });

    const data = await res.json();
    document.getElementById("resposta").innerText = data.resposta;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/corrigir", methods=["POST"])
def corrigir():

    if not API_KEY:
        return jsonify({"resposta": "Erro: API KEY não definida."})

    data = request.json
    texto = data.get("texto", "").strip()
    genero = data.get("genero", "").strip()

    if not texto:
        return jsonify({"resposta": "Erro: texto vazio."})

    prompt = f"""
Você irá corrigir uma redação do gênero {genero}
Atue como um Corretor de redações Rígido, que não alivie críticas, a fim de expor ao máximo possíveis melhorias
Para isso, é preciso que você avalie:

Estrutura do Texto:
O texto deve seguir rigidamente as normas do gênero escolhido, não abrindo espaço para exceções.

tema:
Caso seja identificado um tema específico no texto, verifique se ele permanece no mesmo tema do início ao fim do texto.

Gramática e coerência:
Busque por erros gramaticais, ou erros de coerência e destaque-os.

(situacional) Análise de Repertório:
caso o gênero textual tenha a necessidade de possuir argumentos e repertório, analise a existência desses argumentos/repertórios e julgue a pertinência deles em relação ao tema.

(situacional) Oralidade:
Caso o gênero textual não permita a presença de oralidade no texto, analise a presença da oralidade, e destaque trechos que possuírem. 

nota: 
Após a análise dos critérios anteriores, faça uma estimativa de nota, variando de 0-10, para maior compreensão do que deve melhorar.

Recomendações:
Aponte o que e como deve ser melhorado, destacando o critério e o que deve mudar.

→ Não Reescreva a redação ←

O texto analisado será: {texto}

Formate a Resposta da Seguinte Maneira:

txtStruct: “<resposta sobre estrutura do texto aqui>”

txtTema: ”<resposta sobre tema aqui>”

txtGeC: “<resposta sobre gramática e coerência aqui>”

txtRep: “<resposta sobre repositório e argumentos aqui (vazio se não possuir correção)>”

txtOra: “<resposta sobre oralidade aqui (vazio se não possuir correção)>”

txtNota: “<resposta sobre a estimativa de nota aqui>”

txtTip: ”<resposta sobre as recomendações aqui>”
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    try:
        response = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })

        resposta_json = response.json()

        if "candidates" in resposta_json:
            resultado = resposta_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            resultado = f"Erro da API: {resposta_json}"

    except Exception as e:
        resultado = f"Erro geral: {str(e)}"

    return jsonify({"resposta": resultado})


if __name__ == "__main__":
    app.run(debug=True)
