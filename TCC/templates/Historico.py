HTMLHISTORICO = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historico - Academic Write AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --purple-50:#EEEDFE; --purple-100:#CECBF6; --purple-400:#7F77DD;
            --purple-600:#534AB7; --purple-800:#3C3489; --purple-900:#26215C;
        }
        *{box-sizing:border-box;}
        body{margin:0;min-height:100vh;background:#f0efe8;font-family:'DM Sans',sans-serif;color:#2a2928;}
        .page{min-height:100vh;background:#f7f6f1;}
        .top-header{background:#fffffe;border-radius:16px;padding:16px 22px;border:1px solid #e2e0d8;margin-bottom:24px;}
        .logo-box{width:58px;height:58px;background:var(--purple-900);border-radius:14px;display:flex;align-items:center;justify-content:center;overflow:hidden;}
        .logo-box img{width:44px;height:44px;object-fit:contain;}
        .app-title{font-family:'Lora',serif;font-weight:600;font-size:20px;color:var(--purple-900);margin:0;}
        .app-subtitle{font-size:13px;color:#888780;margin:0;}
        .menu-btn,.icon-btn{width:44px;height:44px;border:1px solid #e2e0d8;border-radius:10px;background:transparent;font-size:22px;color:var(--purple-800);transition:.15s;display:flex;align-items:center;justify-content:center;}
        .menu-btn:hover,.icon-btn:hover{background:var(--purple-50);border-color:var(--purple-100);}
        .sidebar{position:fixed;top:0;left:-290px;width:290px;height:100vh;background:var(--purple-900);z-index:3000;transition:.28s cubic-bezier(.4,0,.2,1);padding:28px 22px;border-right:1px solid var(--purple-800);}
        .sidebar.active{left:0;}
        .sidebar-header{color:white;margin-bottom:32px;}
        .sidebar-header h4{font-family:'Lora',serif;font-weight:600;font-size:18px;margin:0;color:#fffffe;}
        .sidebar-btn{width:100%;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.07);color:rgba(255,255,255,.85);padding:13px 16px;border-radius:10px;text-align:left;font-size:15px;font-family:'DM Sans',sans-serif;transition:.15s;}
        .sidebar-btn:hover{background:rgba(255,255,255,.14);color:white;}
        .section-title{font-family:'Lora',serif;font-size:30px;font-weight:600;color:var(--purple-900);margin:0;}
        .section-subtitle{font-size:14px;color:#888780;margin:4px 0 0;}
        .history-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;}
        .history-card{background:#fffffe;border:1px solid #e2e0d8;border-radius:14px;padding:20px;text-align:left;width:100%;cursor:pointer;transition:.16s;}
        .history-card:hover{border-color:var(--purple-100);transform:translateY(-1px);box-shadow:0 10px 26px rgba(38,33,92,.07);}
        .history-top{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;margin-bottom:12px;}
        .history-title{font-family:'Lora',serif;font-size:19px;font-weight:600;color:var(--purple-900);margin:0;line-height:1.3;}
        .history-date{font-size:12px;color:#888780;white-space:nowrap;margin-top:3px;}
        .note-box{min-width:68px;height:68px;border-radius:14px;background:var(--purple-900);color:#fffffe;display:flex;flex-direction:column;align-items:center;justify-content:center;}
        .note-label{font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:var(--purple-100);line-height:1;}
        .note-value{font-family:'Lora',serif;font-size:26px;font-weight:600;line-height:1.1;margin-top:4px;}
        .history-text{font-family:'Lora',Georgia,serif;font-size:15px;line-height:1.7;color:#5f5e5a;margin:0;display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden;}
        .open-hint{font-size:12px;color:var(--purple-600);margin-top:14px;font-weight:600;}
        .empty-state{background:#fffffe;border:1px solid #e2e0d8;border-radius:14px;padding:42px 24px;text-align:center;}
        .empty-icon{width:54px;height:54px;border-radius:14px;background:var(--purple-50);color:var(--purple-600);display:flex;align-items:center;justify-content:center;font-size:24px;margin:0 auto 14px;}
        .empty-state h2{font-family:'Lora',serif;font-size:24px;color:var(--purple-900);margin:0 0 6px;}
        .empty-state p{color:#888780;margin:0 0 18px;}
        .primary-link{display:inline-flex;align-items:center;gap:8px;text-decoration:none;background:var(--purple-900);color:white;border-radius:11px;padding:12px 18px;font-weight:500;}
        .primary-link:hover{background:var(--purple-800);color:white;}
        .detail-overlay{position:fixed;inset:0;background:rgba(22,19,49,.48);z-index:4000;display:none;padding:24px;overflow-y:auto;}
        .detail-overlay.active{display:block;}
        .detail-modal{background:#f7f6f1;border-radius:16px;max-width:1120px;margin:0 auto;min-height:calc(100vh - 48px);border:1px solid #e2e0d8;overflow:hidden;}
        .detail-header{background:#fffffe;border-bottom:1px solid #e2e0d8;padding:18px 22px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
        .detail-title{font-family:'Lora',serif;font-size:24px;color:var(--purple-900);margin:0;line-height:1.25;}
        .detail-date{font-size:13px;color:#888780;margin-top:4px;}
        .detail-body{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:18px;padding:20px;}
        .detail-panel{background:#fffffe;border:1px solid #e2e0d8;border-radius:14px;padding:20px;}
        .detail-panel h3{font-size:14px;font-weight:700;color:#2a2928;margin:0 0 16px;text-transform:uppercase;letter-spacing:.6px;}
        .essay-text{font-family:'Lora',Georgia,serif;font-size:16px;line-height:1.8;color:#3b3a37;white-space:pre-wrap;margin:0;}
        .big-note{background:var(--purple-900);border-radius:16px;padding:22px;color:white;margin-bottom:14px;}
        .big-note .label{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--purple-100);}
        .big-note .value{font-family:'Lora',serif;font-size:58px;line-height:1;margin-top:6px;}
        .chart{display:flex;align-items:flex-end;justify-content:space-between;height:210px;gap:12px;margin-top:8px;}
        .bar-col{flex:1;display:flex;flex-direction:column;align-items:center;min-width:0;}
        .bar-track{height:145px;width:36px;background:#f0efe8;border-radius:10px;overflow:hidden;display:flex;align-items:flex-end;}
        .bar-fill{width:100%;height:0;background:var(--purple-400);transition:height .35s ease;}
        .bar-value{font-size:13px;font-weight:700;margin-top:8px;color:#2a2928;}
        .bar-label{font-size:11px;color:#888780;text-align:center;margin-top:3px;line-height:1.2;}
        .feedback-item{padding:14px 0;border-bottom:1px solid #f0efe8;}
        .feedback-item:last-child{border-bottom:none;padding-bottom:0;}
        .feedback-label{font-size:11px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:var(--purple-600);margin-bottom:5px;display:flex;align-items:center;gap:6px;}
        .feedback-label .dot{width:5px;height:5px;border-radius:50%;background:var(--purple-400);}
        .feedback-text{font-size:14px;color:#5f5e5a;line-height:1.6;margin:0;}
        @media (max-width: 880px){
            .detail-body{grid-template-columns:1fr;}
            .detail-modal{min-height:auto;}
        }
        @media (max-width: 700px){
            .top-header{padding:14px;}
            .section-title{font-size:25px;}
            .history-top{flex-direction:column;}
            .note-box{width:68px;}
            .detail-overlay{padding:10px;}
            .detail-header{padding:14px;}
            .detail-body{padding:12px;}
            .detail-title{font-size:20px;}
        }
    </style>
</head>
<body>

<div id="sidebar" class="sidebar">
    <div class="sidebar-header d-flex justify-content-between align-items-center">
        <h4>Menu</h4>
        <button class="btn-close btn-close-white" onclick="toggleSidebar()"></button>
    </div>

    <h5 class="px-3 text-white">Olá, {{ session.get("nome", "visitante") }}!</h5>

    <a href="/"><button class="sidebar-btn"><i class="bi bi-house-door me-2"></i>Início</button></a>
    <a href="/historico"><button class="sidebar-btn mt-2"><i class="bi bi-clock-history me-2"></i>Histórico de Redações</button></a>
    <a href="/logout"><button class="sidebar-btn mt-2"><i class="bi bi-box-arrow-left me-2"></i>Sair</button></a>
</div>

<main class="page p-4">
    <div class="top-header d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
            <button class="menu-btn" onclick="toggleSidebar()"><i class="bi bi-list"></i></button>
            <div class="logo-box"><img src="static/uploads/images/Logo.png" alt="Logo"></div>
            <div>
                <p class="app-title">Academic Write AI</p>
                <p class="app-subtitle">Histórico de correções salvas</p>
            </div>
        </div>
    </div>

    <section class="mb-4">
        <h1 class="section-title">Histórico</h1>
        <p class="section-subtitle">Clique em uma redação para ver a correção completa.</p>
    </section>

    {% if historico %}
    <section class="history-grid">
        {% for item in historico %}
        <button class="history-card" type="button" onclick="abrirDetalhes({{ loop.index0 }})">
            <div class="history-top">
                <div>
                    <h2 class="history-title">{{ item.titulo or "Redação sem título" }}</h2>
                    <div class="history-date">{{ item.data_formatada }}</div>
                </div>
                <div class="note-box">
                    <span class="note-label">Nota</span>
                    <span class="note-value">{{ "%.1f"|format(item.nota or 0) }}</span>
                </div>
            </div>
            <p class="history-text">{{ item.conteudo or "Texto não encontrado." }}</p>
            <div class="open-hint"><i class="bi bi-eye me-1"></i>Ver correção completa</div>
        </button>
        {% endfor %}
    </section>
    {% else %}
    <section class="empty-state">
        <div class="empty-icon"><i class="bi bi-journal-text"></i></div>
        <h2>Nenhuma redação salva</h2>
        <p>Corrija uma redação enquanto estiver logado para ela aparecer aqui.</p>
        <a href="/" class="primary-link"><i class="bi bi-pencil-square"></i>Corrigir redação</a>
    </section>
    {% endif %}
</main>

<div id="detailOverlay" class="detail-overlay" onclick="fecharDetalhes(event)">
    <div class="detail-modal" onclick="event.stopPropagation()">
        <div class="detail-header">
            <div>
                <h2 id="detailTitle" class="detail-title"></h2>
                <div id="detailDate" class="detail-date"></div>
            </div>
            <button class="icon-btn" type="button" onclick="fecharDetalhes()"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="detail-body">
            <section class="detail-panel">
                <h3>Redação enviada</h3>
                <p id="detailEssay" class="essay-text"></p>
            </section>
            <aside>
                <div class="big-note">
                    <div class="label">Nota geral</div>
                    <div id="detailNote" class="value">0.0</div>
                </div>
                <section class="detail-panel mb-3">
                    <h3>Notas por critério</h3>
                    <div id="detailChart" class="chart"></div>
                </section>
                <section class="detail-panel">
                    <h3>Correções detalhadas</h3>
                    <div id="detailFeedback"></div>
                </section>
            </aside>
        </div>
    </div>
</div>

<script>
const historico = {{ historico_json|tojson }};

function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle("active");
}

function corNota(nota){
    if(nota >= 8) return "#1D9E75";
    if(nota >= 6) return "#7F77DD";
    if(nota >= 4) return "#BA7517";
    return "#E24B4A";
}

function textoOuPadrao(valor){
    return valor && String(valor).trim() ? valor : "Nenhuma observação salva para este item.";
}

function escaparHtml(valor){
    return String(valor)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function abrirDetalhes(indice){
    const item = historico[indice];
    if(!item) return;

    document.getElementById("detailTitle").innerText = item.titulo;
    document.getElementById("detailDate").innerText = item.data;
    document.getElementById("detailEssay").innerText = item.conteudo;
    document.getElementById("detailNote").innerText = Number(item.nota || 0).toFixed(1);

    const criterios = [
        ["Estrutura", item.nEstrutura],
        ["Tema", item.nTema],
        ["Gramática", item.nGramatica],
        ["Repertório", item.nRepertorio],
        ["Oralidade", item.nOralidade]
    ];

    document.getElementById("detailChart").innerHTML = criterios.map(([label, valor]) => {
        const nota = Number(valor || 0);
        const altura = Math.max(0, Math.min(100, nota * 10));
        return `
            <div class="bar-col">
                <div class="bar-track">
                    <div class="bar-fill" style="height:${altura}%;background:${corNota(nota)}"></div>
                </div>
                <div class="bar-value">${nota.toFixed(1)}</div>
                <div class="bar-label">${label}</div>
            </div>
        `;
    }).join("");

    const feedback = item.feedback || {};
    const blocos = [
        ["Avisos", feedback.txtAviso],
        ["Estrutura", feedback.txtStruct],
        ["Tema", feedback.txtTema],
        ["Gramática e Coerência", feedback.txtGeC],
        ["Repertório", feedback.txtRep],
        ["Oralidade", feedback.txtOra],
        ["Recomendações", feedback.txtTip]
    ];

    document.getElementById("detailFeedback").innerHTML = blocos.map(([label, texto]) => `
        <div class="feedback-item">
            <div class="feedback-label"><span class="dot"></span>${label}</div>
            <p class="feedback-text">${escaparHtml(textoOuPadrao(texto))}</p>
        </div>
    `).join("");

    document.getElementById("detailOverlay").classList.add("active");
}

function fecharDetalhes(event){
    if(event && event.target.id !== "detailOverlay") return;
    document.getElementById("detailOverlay").classList.remove("active");
}

document.addEventListener("keydown", (event) => {
    if(event.key === "Escape") fecharDetalhes();
});
</script>
</body>
</html>
"""
