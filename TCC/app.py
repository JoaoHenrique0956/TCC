from flask import Flask, request, jsonify, render_template_string
import requests
import json
from templates.Index import HTML

app = Flask(__name__)

API_KEY = "AIzaSyAVql-e5jftFIewwoH5Yy-zATZoMU2FHlg"

print("API_KEY carregada:", API_KEY)


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/corrigir", methods=["POST"])
def corrigir():

    if not API_KEY:
        return jsonify({
            "erro": "API KEY não definida."
        })

    data = request.json

    texto = data.get("texto", "").strip()
    genero = data.get("genero", "").strip()

    if not texto:
        return jsonify({
            "erro": "Texto vazio."
        })

    prompt = f"""
Você irá corrigir uma redação do gênero {genero}

Atue como um Corretor de redações Rígido, que não alivie críticas, a fim de expor ao máximo possíveis melhorias.

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
Após a análise dos critérios anteriores, faça uma estimativa de nota para cada um dos critérios e logo depois uma estimativa geral (dê preferencia a uma média aritimética das notas dos critérios), variando de 0-10.

A nota deve conter até no máximo 1 casa decimal, não arredonde a nota.

Recomendações:
Aponte o que e como deve ser melhorado, destacando o critério e o que deve mudar.

Avisos:
Em caso de erros graves, por exemplo, se o texto distoa muito de seu gênero esperado, é necessário detalhar um aviso.
Caso não exista erros graves, não faça nenhum aviso.

→ Não Reescreva a redação ←

O texto analisado será:
{texto}

Responda APENAS em JSON válido no seguinte formato:

{{
    "txtAviso": "",
    "txtStruct": "",
    "txtTema": "",
    "txtGeC": "",
    "txtRep": "",
    "txtOra": "",
    "txtNota": "",
    "txtTip": ""
}}

Regras:
- Não escreva nada fora do JSON
- Não use markdown
- Não use ```json
- Todas as respostas devem ser breves, claras e diretas
- As respostas devem conter APENAS o que precisa ser corrigido
- Não faça elogios
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    try:

        response = requests.post(
            url,
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "response_mime_type": "application/json"
                }
            }
        )

        resposta_json = response.json()

        if "candidates" not in resposta_json:
            return jsonify({
                "erro": "Erro da API",
                "detalhes": resposta_json
            })

        resultado = resposta_json["candidates"][0]["content"]["parts"][0]["text"]

        # limpa possíveis markdowns
        resultado = (
            resultado
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            resultado_dict = json.loads(resultado)

            aviso = resultado_dict.get("txtAviso", "")
            estrutura = resultado_dict.get("txtStruct", "")
            tema = resultado_dict.get("txtTema", "")
            gec = resultado_dict.get("txtGeC", "")
            repertorio = resultado_dict.get("txtRep", "")
            oralidade = resultado_dict.get("txtOra", "")
            nota = resultado_dict.get("txtNota", "")
            dicas = resultado_dict.get("txtTip", "")

            return jsonify({
                "txtAviso": aviso,
                "txtStruct": estrutura,
                "txtTema": tema,
                "txtGeC": gec,
                "txtRep": repertorio,
                "txtOra": oralidade,
                "txtNota": nota,
                "txtTip": dicas
            })

        except json.JSONDecodeError:

            return jsonify({
                "erro": "A IA não retornou JSON válido.",
                "resposta_bruta": resultado
            })

    except Exception as e:

        return jsonify({
            "erro": "Erro geral",
            "detalhes": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)