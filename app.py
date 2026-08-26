from flask import Flask, request, jsonify, render_template_string, redirect ,session
from openai import OpenAI
import json
import os
from templates.Index import HTML
from templates.Login import HTMLLOGIN
from templates.Historico import HTMLHISTORICO
from templates.Sobre import HTMLSOBRE

from db.database import MysqlDatabase
import logging
import traceback

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "academic-write-ai-dev-secret")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

API_KEY = "sua_chave"

client = OpenAI(
    api_key=API_KEY
)

db = MysqlDatabase(
    host="127.0.0.1",
    user="root",
    password="",
    database="mydb"
)

logger.info("API_KEY carregada.")


@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/salvar_texto", methods=["POST"])
def salvar_texto():

    if "idUsuario" not in session:
        return redirect("/login")

    titulo = request.form.get("titulo")
    conteudo = request.form.get("conteudo")

    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Texto (titulo, conteudo, Usuario_idUsuario)
        VALUES (%s, %s, %s)
    """, (titulo, conteudo, session["idUsuario"]))

    conn.commit()

    # 🔥 pega o ID REAL do último insert
    cursor.execute("SELECT LAST_INSERT_ID()")
    id_texto = cursor.fetchone()[0]

    session["idTexto"] = id_texto

    cursor.close()
    conn.close()

    return redirect("/historico")

@app.route("/historico")
def historico():

    if "idUsuario" not in session:
        return redirect("/login")

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        t.idTexto,
        t.titulo,
        t.conteudo,
        c.nota,
        c.nEstrutura,
        c.nTema,
        c.nGramatica,
        c.nRepertorio,
        c.nCoesao,
        c.recomendacoes,
        c.data_correcao
    FROM Texto t
    INNER JOIN correcoes c
        ON c.Texto_idTexto = t.idTexto
    WHERE t.Usuario_idUsuario = %s
    ORDER BY c.data_correcao DESC
    """,
    (session["idUsuario"],))

    historico = cursor.fetchall()

    for item in historico:
        try:
            item["feedback"] = json.loads(item.get("recomendacoes") or "{}")
        except json.JSONDecodeError:
            item["feedback"] = {}

        item["data_formatada"] = (
            item["data_correcao"].strftime("%d/%m/%Y %H:%M")
            if item.get("data_correcao")
            else "Sem data"
        )

    historico_json = [
        {
            "titulo": item.get("titulo") or "Redação sem título",
            "conteudo": item.get("conteudo") or "Texto não encontrado.",
            "nota": float(item.get("nota") or 0),
            "nEstrutura": float(item.get("nEstrutura") or 0),
            "nTema": float(item.get("nTema") or 0),
            "nGramatica": float(item.get("nGramatica") or 0),
            "nRepertorio": float(item.get("nRepertorio") or 0),
            "nCoesao": float(item.get("nCoesao") or 0),
            "data": item.get("data_formatada"),
            "feedback": item.get("feedback") or {}
        }
        for item in historico
    ]

    cursor.close()
    conn.close()

    return render_template_string(
        HTMLHISTORICO,
        historico=historico,
        historico_json=historico_json
    )
    
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM Usuario
            WHERE email=%s AND senha=%s
        """, (email, senha))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if not usuario:
            return "Email ou senha inválidos"

        session["idUsuario"] = usuario["idUsuario"]
        session["nome"] = usuario["nome"]

        return redirect("/")

    return render_template_string(HTMLLOGIN)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/sobre")
def sobre():
    return render_template_string(HTMLSOBRE)

@app.route("/cadastro", methods=["POST"])
def cadastro():

    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]

    try:

        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Usuario(nome,email,senha)
            VALUES (%s,%s,%s)
            """,
            (nome,email,senha)
        )

        conn.commit()

        cursor.close()
        conn.close()
        

        return redirect("/login")

    except Exception as e:

        return f"Erro: {str(e)}"

logger.info("Enviando requisição para a API OpenAi...")

@app.route("/corrigir", methods=["POST"])

def corrigir():

    if not API_KEY:
        return jsonify({
            "erro": "API KEY não definida."
        })

    data = request.json

    texto = data.get("texto", "").strip()
    genero = data.get("genero", "").strip()
    assunto = data.get("tema", "").strip()

    logger.debug(f"Texto recebido: {texto[:150]}")
    logger.debug(f"Gênero recebido: {genero}")
    logger.debug(f"tema recebido: {assunto}")

    if not texto:
        return jsonify({
            "erro": "Texto vazio."
        })

    prompt = f"""
Atue como um corretor de redação rigido, mas nem tanto , crítico , imparcial e principalmente justo , a fim de expor as melhorias sobre o gênero textual: {genero}


Normas exigidas para a correção:

*Estrutura do Texto:*
O texto deve seguir rigidamente as normas do gênero escolhido, não abrindo espaço para exceções.

*Tema:*
Caso seja Fornecido um tema específico ao texto, verifique se ele permanece no mesmo tema do início ao fim do texto em casos de desvio total todos os atributos serão atribuidos a nota ZERO.

*Gramática:*
Busque por erros gramaticais, ou erros de coerência e destaque-os ,busque seguir a norma culta da língua portuguesa, em casos de gêneros textuais que não admitem Oralidade, pontue os trechos que a possuem e descorte nota de acordo.

*(situacional) Análise de Repertório:*
caso o gênero textual tenha a necessidade de possuir argumentos e repertório, analise a existência desses argumentos/repertórios e julgue a pertinência deles em relação ao tema , valorize repertório como obras audiovisuais , voz de autoridade e conhecimento da autalidade global.

*Coesão Textual:*
Busque por erros de Coesão Textual no texto, analise a presença da articuladores textuais, se eles fazem sentido com o período e se o texto flui bem.

*nota:*
Após a análise dos critérios anteriores, faça uma estimativa de nota para cada um dos critérios e logo depois uma estimativa geral (dê preferencia a uma média aritimética das notas dos critérios), variando de 0-10.

A nota deve conter até no máximo 1 casa decimal, não arredonde a nota.

Recomendações:
Aponte o que e como deve ser melhorado, destacando o critério e o que deve mudar.

→ Não Reescreva a redação ←

O tema será:
{assunto}

O texto analisado será:
{texto}

Responda APENAS em JSON válido no seguinte formato:

{{
"txtStruct": "",
"txtTema": "",
"txtGeC": "",
"txtRep": "",
"txtCoe": "",
"txtNota": "",
"txtTip": "",

"nota_estrutura": 0,
"nota_tema": 0,
"nota_gramatica": 0,
"nota_repertorio": 0,
"nota_coesaoTextual": 0
    
}}

Regras:
- Não escreva nada fora do JSON
- Não use markdown
- Não use ```json
- Todas as respostas devem ser breves, claras e diretas
- As respostas devem conter APENAS o que precisa ser corrigido
- Não faça elogios
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um corretor de redações e deve responder apenas JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        resultado = response.choices[0].message.content

    except Exception as e:

        logger.error(str(e))

        return jsonify({
            "erro": "Erro ao consultar a OpenAI",
            "detalhes": str(e)
        })

    resultado = (
        resultado
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        resultado_dict = json.loads(resultado)

        print(json.dumps(resultado_dict, indent=4, ensure_ascii=False))

        estrutura = resultado_dict.get("txtStruct", "")
        tema = resultado_dict.get("txtTema", "")
        gec = resultado_dict.get("txtGeC", "")
        repertorio = resultado_dict.get("txtRep", "")
        coesaoTextual = resultado_dict.get("txtCoe", "")
        nota = resultado_dict.get("txtNota", "")
        dicas = resultado_dict.get("txtTip", "")

        def para_float(valor):
            try:
                return float(valor)
            except (TypeError, ValueError):
                return 0

        nota_estrutura = para_float(resultado_dict.get("nota_estrutura", 0))
        nota_tema = para_float(resultado_dict.get("nota_tema", 0))
        nota_gramatica = para_float(resultado_dict.get("nota_gramatica", 0))
        nota_repertorio = para_float(resultado_dict.get("nota_repertorio", 0))
        nota_coesaoTextual = para_float(resultado_dict.get("nota_coesaoTextual", 0))
        

        if isinstance(nota, dict):
            nota = f"Nota geral: {nota.get('Geral', '--')}"

        media = (nota_estrutura+nota_gramatica+nota_coesaoTextual+nota_repertorio+nota_tema)/5
        
        if "idUsuario" in session:
            conn = db.get_connection()
            cursor = conn.cursor()

            titulo = texto.strip().splitlines()[0][:80] if texto.strip() else "Redação sem título"

            cursor.execute("""
                INSERT INTO Texto (titulo, conteudo, Usuario_idUsuario)
                VALUES (%s, %s, %s)
            """, (
                titulo,
                texto,
                session["idUsuario"]
            ))

            id_texto = cursor.lastrowid
            session["idTexto"] = id_texto

            cursor.execute("""
                INSERT INTO correcoes
                (nota, nEstrutura, nTema, nGramatica, nRepertorio, nCoesao, recomendacoes, data_correcao, Texto_idTexto)
                VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),%s)
            """, (
                media,
                nota_estrutura,
                nota_tema,
                nota_gramatica,
                nota_repertorio,
                nota_coesaoTextual,
                json.dumps({
                    "txtStruct": estrutura,
                    "txtTema": tema,
                    "txtGeC": gec,
                    "txtRep": repertorio,
                    "txtCoe": coesaoTextual,
                    "txtTip": dicas
                }, ensure_ascii=False),
                id_texto
            ))

            conn.commit()
            cursor.close()
            conn.close()
        
     
        

        return jsonify({
"txtStruct": estrutura,
"txtTema": tema,
"txtGeC": gec,
"txtRep": repertorio,
"txtCoe": coesaoTextual,
"txtNota": str(media),
"txtTip": dicas,

"nota_estrutura": nota_estrutura,
"nota_tema": nota_tema,
"nota_gramatica": nota_gramatica,
"nota_repertorio": nota_repertorio,
"nota_coesaoTextual": nota_coesaoTextual

})
        
        

    except json.JSONDecodeError as e:

        logger.error("Erro ao converter JSON da IA")
        logger.error(str(e))
        logger.error(f"Resposta recebida: {resultado}")

        return jsonify({
            "erro": "A IA não retornou JSON válido.",
            "resposta_bruta": resultado
        })

    except Exception as e:

        logger.error("ERRO GERAL")
        logger.error(str(e))
        logger.error(traceback.format_exc())

        return jsonify({
            "erro": "Erro geral",
            "detalhes": str(e)
        })
    


if __name__ == "__main__":
    app.run(debug=True)
