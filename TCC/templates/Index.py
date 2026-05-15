HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Corretor Feliz</title>

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Bootstrap Icons -->
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

    <style>

        body{
            background: #f4f5f7;
            overflow: hidden;
            font-family: Arial, Helvetica, sans-serif;
        }

        textarea{
            resize: none;
            border-radius: 15px !important;
            border: 1px solid #dcdcdc !important;
            font-size: 15px;
        }

        .left-panel{
            background: white;
            height: 100vh;
            border-right: 1px solid #e6e6e6;
        }

        .right-panel{
            background: #fafafa;
            height: 100vh;
            overflow-y: auto;
        }

        .top-icons button{
            width: 45px;
            height: 45px;
            border-radius: 12px;
        }

        .nota-card{
            background: linear-gradient(135deg, #7c3aed, #5b21b6);
            color: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .nota-numero{
            font-size: 75px;
            font-weight: bold;
            line-height: 1;
        }

        .nivel-card{
            background: white;
            border-radius: 18px;
            padding: 20px;
            margin-top: 20px;
            border-left: 6px solid #7c3aed;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        }

        .feedback-card{
            background: white;
            border-radius: 18px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        }

        .feedback-item{
            border-left: 5px solid #7c3aed;
            padding-left: 15px;
            margin-bottom: 20px;
        }

        .feedback-item:last-child{
            margin-bottom: 0;
        }

        .btn-purple{
            background: #7c3aed;
            color: white;
            border: none;
        }

        .btn-purple:hover{
            background: #6d28d9;
            color: white;
        }

        .status-badge{
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 50px;
        }

        .loading{
            opacity: 0.7;
            pointer-events: none;
        }

        .section-title{
            font-size: 14px;
            font-weight: bold;
            color: #7c3aed;
            margin-bottom: 5px;
            text-transform: uppercase;
        }

    </style>
</head>
<body>

<div class="container-fluid">
    <div class="row">

        <!-- ÁREA PRINCIPAL -->
        <div class="col-lg-8 left-panel p-4">

            <!-- TOPO -->
            <div class="d-flex justify-content-between align-items-center mb-4">

                <div>
                    <h2 class="fw-bold mb-0">
                        Corretor Feliz
                    </h2>

                    <small class="text-muted">
                        Plataforma de correção textual
                    </small>
                </div>

                <div class="top-icons d-flex gap-2">

                    <button class="btn btn-light shadow-sm">
                        <i class="bi bi-printer"></i>
                    </button>

                    <button class="btn btn-light shadow-sm">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button class="btn btn-light shadow-sm">
                        <i class="bi bi-search"></i>
                    </button>

                    <button class="btn btn-light shadow-sm">
                        <i class="bi bi-download"></i>
                    </button>

                </div>
            </div>

            <!-- SELECT -->
            <div class="row mb-4">

                <div class="col-md-6">

                    <label class="form-label fw-semibold">
                        Gênero textual
                    </label>

                    <select id="genero" class="form-select">

                        <option>Dissertação Argumentativa</option>
                        <option>Artigo de Opinião</option>
                        <option>Carta</option>
                        <option>Poema</option>

                    </select>

                </div>

            </div>

            <!-- TEXTO -->
            <div class="mb-4">

                <textarea
                    id="texto"
                    class="form-control p-4"
                    rows="18"
                    placeholder="Digite sua redação aqui..."
                ></textarea>

            </div>

            <!-- BOTÃO -->
            <div class="mb-4">

                <button
                    id="btnEnviar"
                    onclick="enviar()"
                    class="btn btn-purple btn-lg px-5">

                    <i class="bi bi-send-fill"></i>
                    Corrigir redação

                </button>

            </div>

        </div>

        <!-- LADO DIREITO -->
        <div class="col-lg-4 right-panel p-4">

            <!-- NOTA -->
            <div class="nota-card">

                <small class="fw-semibold">
                    SUA NOTA
                </small>

                <div id="notaNumero" class="nota-numero">
                    --
                </div>

                <div class="mt-2">
                    <span id="nivelBadge"
                          class="badge bg-light text-dark status-badge">
                        Aguardando análise
                    </span>
                </div>

            </div>

            <!-- NÍVEL -->
            <div class="nivel-card">

                <div class="d-flex align-items-center gap-2 mb-3">

                    <i class="bi bi-bar-chart-fill text-primary"></i>

                    <h5 class="mb-0 fw-bold">
                        Avaliação Geral
                    </h5>

                </div>

                <p id="notaTexto" class="text-muted mb-0">
                    A análise da redação aparecerá aqui.
                </p>

            </div>

            <!-- FEEDBACK -->
            <div class="feedback-card">

                <h5 class="fw-bold mb-4">
                    Correções
                </h5>

                <div class="feedback-item">
                    <div class="section-title">
                        Avisos
                    </div>

                    <p id="txtAviso" class="text-muted mb-0">
                        --
                    </p>
                </div>

                <div class="feedback-item">
                    <div class="section-title">
                        Estrutura
                    </div>

                    <p id="txtStruct" class="text-muted mb-0">
                        --
                    </p>
                </div>

                <div class="feedback-item">
                    <div class="section-title">
                        Tema
                    </div>

                    <p id="txtTema" class="text-muted mb-0">
                        --
                    </p>
                </div>

                <div class="feedback-item">
                    <div class="section-title">
                        Gramática e Coerência
                    </div>

                    <p id="txtGeC" class="text-muted mb-0">
                        --
                    </p>
                </div>

                <div class="feedback-item">
                    <div class="section-title">
                        Repertório
                    </div>

                    <p id="txtRep" class="text-muted mb-0">
                        --
                    </p>
                </div>

                <div class="feedback-item">
                    <div class="section-title">
                        Oralidade
                    </div>

                    <p id="txtOra" class="text-muted mb-0">
                        --
                    </p>
                </div>

                <div class="feedback-item">
                    <div class="section-title">
                        Recomendações
                    </div>

                    <p id="txtTip" class="text-muted mb-0">
                        --
                    </p>
                </div>

            </div>

        </div>

    </div>
</div>

<script>

function extrairNota(textoNota){

    const match = textoNota.match(/\\d+(\\.\\d+)?/);

    if(match){
        return match[0];
    }

    return "--";
}

function definirNivel(nota){

    nota = parseFloat(nota);

    if(isNaN(nota)){
        return "Sem avaliação";
    }

    if(nota >= 9){
        return "Excelente";
    }

    if(nota >= 7){
        return "Bom";
    }

    if(nota >= 5){
        return "Regular";
    }

    return "Insuficiente";
}

async function enviar() {

    const texto = document.getElementById("texto").value;
    const genero = document.getElementById("genero").value;

    if (!texto.trim()) {

        alert("Digite uma redação primeiro.");
        return;
    }

    const botao = document.getElementById("btnEnviar");

    botao.innerHTML = `
        <span class="spinner-border spinner-border-sm"></span>
        Corrigindo...
    `;

    botao.classList.add("loading");

    try {

        const res = await fetch("/corrigir", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                texto,
                genero
            })

        });

        const data = await res.json();

        if(data.erro){

            alert(data.erro);
            console.log(data);

            return;
        }

        // PREENCHE CAMPOS

        document.getElementById("txtAviso").innerText =
            data.txtAviso || "Nenhum aviso";

        document.getElementById("txtStruct").innerText =
            data.txtStruct || "--";

        document.getElementById("txtTema").innerText =
            data.txtTema || "--";

        document.getElementById("txtGeC").innerText =
            data.txtGeC || "--";

        document.getElementById("txtRep").innerText =
            data.txtRep || "--";

        document.getElementById("txtOra").innerText =
            data.txtOra || "--";

        document.getElementById("txtTip").innerText =
            data.txtTip || "--";

        document.getElementById("notaTexto").innerText =
            data.txtNota || "--";

        // NOTA

        const nota = extrairNota(data.txtNota);

        document.getElementById("notaNumero").innerText =
            nota;

        document.getElementById("nivelBadge").innerText =
            definirNivel(nota);

    } catch (erro) {

        console.error(erro);

        alert("Erro ao conectar com o servidor.");

    } finally {

        botao.innerHTML = `
            <i class="bi bi-send-fill"></i>
            Corrigir redação
        `;

        botao.classList.remove("loading");
    }
}

</script>

</body>
</html>
"""

