import streamlit as st
from groq import Groq
from datetime import datetime
import json, re

st.set_page_config(
    page_title="Simulador de Entrevista IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS TERMINAL ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"] { visibility:hidden; }

/* BASE */
.stApp {
    background-color:#FFFFFF !important;
    font-family:'Inter',sans-serif !important;
    color:#1A1A2E !important;
}
.stApp * { color:#1A1A2E !important; }

/* sidebar oculta */
[data-testid="stSidebar"] { display:none; }

/* INPUTS */
.stTextInput>div>div>input,
.stTextArea>div>textarea,
.stSelectbox>div>div>div,
.stNumberInput>div>div>input,
.stPasswordInput>div>div>input {
    background-color:#F8FAFC !important;
    color:#1A1A2E !important;
    border:1px solid #D1D5DB !important;
    border-radius:6px !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:13px !important;
}
.stTextArea>div>textarea:focus,
.stTextInput>div>div>input:focus {
    border-color:#16A34A !important;
    box-shadow:0 0 0 2px rgba(22,163,74,0.12) !important;
}
.stTextArea>div>textarea { resize:vertical !important; }

/* BOTÕES PRIMÁRIOS */
.stButton>button {
    background:linear-gradient(135deg,#15803D,#16A34A) !important;
    color:#FFFFFF !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:12px !important;
    font-weight:700 !important;
    letter-spacing:0.08em !important;
    text-transform:uppercase !important;
    border:none !important;
    border-radius:4px !important;
    padding:10px 20px !important;
    transition:all 0.15s !important;
    width:100% !important;
}
.stButton>button:hover {
    background:linear-gradient(135deg,#16A34A,#22C55E) !important;
    box-shadow:0 4px 12px rgba(22,163,74,0.25) !important;
    transform:translateY(-1px) !important;
}
.stButton>button p,.stButton>button span,.stButton>button div {
    color:#FFFFFF !important;
    font-weight:700 !important;
}

/* ABAS */
.stTabs [data-baseweb="tab-list"] {
    background:#F8FAFC !important;
    border-bottom:1px solid #E5E7EB !important;
    gap:0 !important;
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important;
    color:#6B7280 !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important;
    font-weight:500 !important;
    letter-spacing:0.04em !important;
    border-radius:0 !important;
    padding:10px 16px !important;
    border-bottom:2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color:#16A34A !important;
    border-bottom:2px solid #16A34A !important;
    background:rgba(22,163,74,0.05) !important;
}
.stTabs [data-baseweb="tab"]:hover { color:#374151 !important; }

/* TÍTULOS */
.stApp h1,.stApp h2,.stApp h3 {
    font-family:'JetBrains Mono',monospace !important;
    color:#15803D !important;
    font-weight:700 !important;
    letter-spacing:0.04em !important;
}

/* CARDS */
.card-terminal {
    background:#F8FAFC;
    border:1px solid #E5E7EB;
    border-radius:8px;
    padding:16px 20px;
    margin-bottom:12px;
}
.card-agent {
    background:#F0FDF4;
    border:1px solid #BBF7D0;
    border-left:3px solid #16A34A;
    border-radius:2px 8px 8px 2px;
    padding:14px 18px;
    margin:10px 0;
    font-size:14px;
    line-height:1.7;
}
.card-user {
    background:#F8FAFC;
    border:1px solid #E5E7EB;
    border-right:3px solid #9CA3AF;
    border-radius:8px 2px 8px 8px;
    padding:12px 16px;
    margin:10px 0;
    font-size:13px;
}
.card-success {
    background:#F0FDF4;
    border:1px solid #86EFAC;
    border-radius:8px;
    padding:14px 18px;
    margin:10px 0;
}
.card-warn {
    background:#FFFBEB;
    border:1px solid #FCD34D;
    border-radius:8px;
    padding:14px 18px;
    margin:10px 0;
}

/* STAT BOX */
.stat-box {
    background:#F8FAFC;
    border:1px solid #E5E7EB;
    border-radius:8px;
    padding:16px;
    text-align:center;
}
.stat-val  { font-family:'JetBrains Mono',monospace; font-size:28px; font-weight:700; color:#15803D !important; }
.stat-lbl  { font-size:11px; color:#6B7280 !important; text-transform:uppercase; letter-spacing:0.08em; margin-top:4px; }

/* HIST ITEM */
.hist-item {
    background:#F8FAFC;
    border-left:3px solid #D1D5DB;
    border-radius:0 6px 6px 0;
    padding:10px 14px;
    margin-bottom:6px;
    font-size:12px;
}

/* LABELS */
.mono-label {
    font-family:'JetBrains Mono',monospace;
    font-size:10px;
    color:#6B7280 !important;
    letter-spacing:0.1em;
    text-transform:uppercase;
    margin-bottom:6px;
}
.mono-title {
    font-family:'JetBrains Mono',monospace;
    font-size:14px;
    font-weight:700;
    color:#15803D !important;
    letter-spacing:0.06em;
}

/* DIVIDER */
.divider { border:none; height:1px; background:linear-gradient(to right,transparent,#E5E7EB,transparent); margin:16px 0; }

/* EXPANDER */
.streamlit-expanderHeader {
    background:#F8FAFC !important;
    border:1px solid #E5E7EB !important;
    border-radius:6px !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important;
    color:#6B7280 !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background:#F8FAFC !important;
    border:1px dashed #D1D5DB !important;
    border-radius:6px !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton>button {
    background:transparent !important;
    border:1px solid #D1D5DB !important;
    color:#6B7280 !important;
    font-size:11px !important;
    padding:6px 14px !important;
    font-family:'JetBrains Mono',monospace !important;
}
.stDownloadButton>button:hover { border-color:#16A34A !important; color:#16A34A !important; }
.stDownloadButton>button p,.stDownloadButton>button span { color:inherit !important; }

/* SPINNER */
.stSpinner>div { border-top-color:#16A34A !important; }

/* ALERTS */
.stAlert { background:#F8FAFC !important; border:1px solid #E5E7EB !important; border-radius:6px !important; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ─────────────────────────────────────────────────────────────
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPTS = {
    "simular": """Você é um entrevistador sênior de RH de uma empresa de tecnologia.
Conduza uma simulação de entrevista real: faça perguntas uma por vez, ouça as respostas e
dê feedback detalhado antes de avançar. Avalie: clareza, exemplos concretos, impacto e postura.
Use o método STAR para avaliar respostas comportamentais. Seja direto, profissional e construtivo.
Português do Brasil.""",

    "perfil": """Você é um coach de carreira especialista em posicionamento profissional.
Analise o perfil do usuário e ofereça orientação personalizada sobre como se apresentar melhor,
destacar pontos fortes e endereçar gaps. Seja específico e prático. Português do Brasil.""",

    "cargo": """Você é um especialista em recrutamento com foco em tecnologia, produto e dados.
Prepare o usuário para perguntas específicas da vaga/área que ele descrever.
Gere perguntas reais que seriam feitas para aquela posição e dê respostas modelo. Português do Brasil.""",

    "empresa": """Você é um especialista em cultura organizacional e processos seletivos.
Ajude o usuário a se preparar para uma empresa específica: cultura, valores,
formato de entrevista e crie um prep guide personalizado. Português do Brasil.""",

    "comportamental": """Você é especialista em entrevistas comportamentais (STAR, CAR).
Gere perguntas comportamentais, avalie as respostas e ensine a estruturar
respostas com Situação, Tarefa, Ação e Resultado quantificado. Português do Brasil.""",

    "tecnica": """Você é um engenheiro sênior que conduz entrevistas técnicas.
Faça perguntas técnicas adequadas ao nível e área do usuário, avalie as respostas
e explique onde a resposta poderia ser mais completa ou precisa. Português do Brasil.""",

    "feedback": """Você é um coach de comunicação especializado em entrevistas.
O usuário vai te contar como respondeu a uma pergunta — analise: pontos fortes,
pontos fracos, o que adicionar, o que remover, como reformular.
Dê sempre uma versão melhorada da resposta ao final. Português do Brasil.""",

    "desempenho": """Você é um analista de performance de entrevistas.
Com base no que o usuário descrever, identifique padrões, pontos recorrentes de melhoria
e crie um plano de ação com 3-5 ações prioritárias e práticas. Português do Brasil.""",

    "modelo": """Você é um redator especialista em comunicação profissional para processos seletivos.
Gere respostas modelo de alta qualidade para as perguntas que o usuário indicar,
adaptadas ao cargo/nível/setor descrito. Use linguagem natural, não corporativa. Português do Brasil.""",

    "conquistas": """Você é um coach de storytelling profissional.
Ajude o usuário a identificar e narrar conquistas de forma impactante:
transforme realizações vagas em histórias quantificadas com o método STAR. Português do Brasil.""",
}

# ── DEFAULTS ───────────────────────────────────────────────────────────────
defaults = {
    "etapa": "Login", "usuario": "", "api_key": "",
    "historico_simulador_entrevista": [],
    "total_respostas": 0,
    **{f"chat_{k}": [] for k in SYSTEM_PROMPTS.keys()},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CACHE ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_cache_simulador():
    return {"perfis": {}}

_cache = get_cache_simulador()

CHAVES_SALVAR = [
    "usuario", "historico_simulador_entrevista", "total_respostas",
    *[f"chat_{k}" for k in SYSTEM_PROMPTS.keys()],
]

def carregar_json_sessao(dados):
    _bloq = {'api_key', 'etapa', 'nome_login', 'chave_login', 'upload_login', 'btn_entrar_login'}
    _pref = ('btn_', 'sel_', 'ul_', 'dl_', '_sub', '_sm', '_tab', '_bsc', 'ativo_', 'rem_')
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def gerar_json_dados():
    dados = {k: st.session_state.get(k)
             for k in st.session_state.keys()
             if not k.startswith("_") and k not in ("api_key",)}
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

# ── HELPERS ────────────────────────────────────────────────────────────────
def hora():
    return datetime.now().strftime("%H:%M:%S")

def render_chat(chat_key: str):
    """Renderiza histórico de conversa de uma aba."""
    msgs = st.session_state.get(f"chat_{chat_key}", [])
    if not msgs:
        st.markdown(f'<div class="card-terminal"><div class="mono-label">// SEM MENSAGENS</div>Inicie uma conversa abaixo.</div>', unsafe_allow_html=True)
        return
    for msg in msgs:
        h = msg.get("hora", "")
        conteudo = msg["content"].replace("\n", "<br>")
        if msg["role"] == "user":
            st.markdown(f"""<div class="card-user">
                <div class="mono-label">👤 VOCÊ · {h}</div>
                {conteudo}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="card-agent">
                <div class="mono-label" style="color:#15803D !important;">🤖 AGENTE · {h}</div>
                {conteudo}
            </div>""", unsafe_allow_html=True)

def chat_input_enviar(chat_key: str, placeholder: str, btn_label: str = "▶ ENVIAR"):
    """Input + botão de envio padronizado para todas as abas."""
    col_i, col_b = st.columns([4, 1])
    with col_i:
        txt = st.text_area("", placeholder=placeholder, height=100,
                           key=f"input_{chat_key}", label_visibility="collapsed")
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        enviar = st.button(btn_label, key=f"btn_{chat_key}", use_container_width=True)

    col_l, _ = st.columns([1, 3])
    with col_l:
        limpar = st.button("🗑 Limpar conversa", key=f"clear_{chat_key}")

    if limpar:
        st.session_state[f"chat_{chat_key}"] = []
        st.rerun()

    if enviar and txt.strip():
        chat = st.session_state[f"chat_{chat_key}"]
        chat.append({"role": "user", "content": txt.strip(), "hora": hora()})
        with st.spinner("Agente processando..."):
            try:
                client = Groq(api_key=st.session_state.api_key)
                msgs_api = [{"role": m["role"], "content": m["content"]} for m in chat]
                resp = client.chat.completions.create(
                    messages=[{"role": "system", "content": SYSTEM_PROMPTS[chat_key]}] + msgs_api,
                    model=MODEL, max_tokens=2048
                )
                resposta = resp.choices[0].message.content
                chat.append({"role": "assistant", "content": resposta, "hora": hora()})
                st.session_state[f"chat_{chat_key}"] = chat
                st.session_state.total_respostas += 1
                st.session_state.historico_simulador_entrevista.append({
                    "data": datetime.now().strftime("%d/%m %H:%M"),
                    "aba": chat_key,
                    "resumo": txt[:60],
                })
            except Exception as e:
                st.error(f"Erro na API Groq: {e}")
        st.rerun()
    elif enviar:
        st.warning("Digite algo antes de enviar.")

# ══════════════════════════════════════════════════════════════════════════
# ── LOGIN
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.etapa == "Login":
    _, col_form, _ = st.columns([1, 2, 1])
    with col_form:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 24px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#6B7280;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px;">SISTEMA ATIVO · meusagentesia.com.br</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:700;color:#15803D;letter-spacing:.06em;">🤖 SIMULADOR DE ENTREVISTA</div>
          <div style="font-size:13px;color:#6B7280;margin-top:6px;">Treine como um profissional. Passe em qualquer entrevista.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card-terminal">', unsafe_allow_html=True)
        st.markdown('<div class="mono-label">// AUTENTICAÇÃO</div>', unsafe_allow_html=True)

        nome  = st.text_input("Nome:", placeholder="Seu nome completo", key="nome_login")
        chave = st.text_input("Chave API Groq:", type="password",
                              placeholder="gsk_...", key="chave_login")
        arq_j = st.file_uploader("Carregar sessão salva (.json):",
                                 type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None

        if st.button("▶ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Nome precisa ter pelo menos 2 caracteres.")
            elif not chave.strip():
                st.warning("Informe sua chave API Groq.")
            else:
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave.strip()
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#6B7280;">
          Não tem chave?
          <a href="https://console.groq.com/keys" target="_blank" style="color:#16A34A;text-decoration:none;">
            Obter gratuitamente →
          </a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# ── APP
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.etapa == "App":
    salvar_perfil_cache(st.session_state.usuario)
    hist = st.session_state.get("historico_simulador_entrevista", [])

    # ── TOP BAR ──
    c1, c2, c3, c4, c5 = st.columns([4, 1, 1, 1, 1])
    with c1:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0;">
          <div style="width:8px;height:8px;border-radius:50%;background:#16A34A;box-shadow:0 0 6px rgba(22,163,74,0.4);flex-shrink:0;"></div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:#15803D;letter-spacing:.06em;">SIMULADOR DE ENTREVISTA IA</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#6B7280;">· {st.session_state.usuario}</span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-box"><div class="stat-val">{st.session_state.total_respostas}</div><div class="stat-lbl">Respostas</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-box"><div class="stat-val">{len(hist)}</div><div class="stat-lbl">Interações</div></div>""", unsafe_allow_html=True)
    with c4:
        chats_ativos = sum(1 for k in SYSTEM_PROMPTS if st.session_state.get(f"chat_{k}"))
        st.markdown(f"""<div class="stat-box"><div class="stat-val">{chats_ativos}</div><div class="stat-lbl">Módulos</div></div>""", unsafe_allow_html=True)
    with c5:
        st.download_button("💾 Salvar", data=gerar_json_dados(),
            file_name=f"entrevista_{st.session_state.usuario}.json",
            mime="application/json", key="dl_top")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── SALVAR/CARREGAR ──
    with st.expander("💾 Gerenciar dados da sessão", expanded=False):
        _b1, _b2 = st.columns(2)
        with _b1:
            st.download_button("⬇ Exportar tudo (.json)", data=gerar_json_dados(),
                file_name=f"simulador_{st.session_state.usuario}.json",
                mime="application/json", key="dl_barra")
        with _b2:
            _fup = st.file_uploader("⬆ Importar dados:", type=["json"],
                                    key="ul_barra", label_visibility="collapsed")
            if _fup:
                try:
                    carregar_json_sessao(json.loads(_fup.read().decode()))
                    st.success("✅ Dados restaurados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

    # ── ABAS ──
    abas = st.tabs([
        "🏠 Home", "👤 Meu Perfil", "🎯 Simular Entrevista",
        "💼 Por Área/Cargo", "🏢 Por Empresa", "🧠 Comportamental",
        "💡 Técnicas", "🗣️ Feedback", "📊 Desempenho",
        "📝 Respostas Modelo", "🏆 Conquistas",
    ])

    # ── HOME ──
    with abas[0]:
        st.markdown(f"## 🎯 Olá, {st.session_state.usuario}")
        c1h, c2h, c3h, c4h = st.columns(4)
        with c1h: st.markdown(f"""<div class="stat-box"><div class="stat-val">{st.session_state.total_respostas}</div><div class="stat-lbl">Respostas dadas</div></div>""", unsafe_allow_html=True)
        with c2h: st.markdown(f"""<div class="stat-box"><div class="stat-val">{len(hist)}</div><div class="stat-lbl">Interações totais</div></div>""", unsafe_allow_html=True)
        with c3h: st.markdown(f"""<div class="stat-box"><div class="stat-val">{chats_ativos}</div><div class="stat-lbl">Módulos usados</div></div>""", unsafe_allow_html=True)
        with c4h: st.markdown(f"""<div class="stat-box"><div class="stat-val">10</div><div class="stat-lbl">Módulos disponíveis</div></div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown('<div class="mono-label">// MÓDULOS DISPONÍVEIS</div>', unsafe_allow_html=True)

        modulos = [
            ("🎯", "Simular Entrevista",   "Entrevista real conduzida pelo agente, pergunta por pergunta"),
            ("👤", "Meu Perfil",           "Análise e orientações de posicionamento profissional"),
            ("💼", "Por Área/Cargo",       "Prep específico para a vaga que você está buscando"),
            ("🏢", "Por Empresa",          "Guia focado na cultura e processo da empresa-alvo"),
            ("🧠", "Comportamental",       "Treinamento STAR para perguntas situacionais"),
            ("💡", "Técnicas",             "Perguntas técnicas avaliadas com explicações"),
            ("🗣️", "Feedback",            "Análise profunda de respostas com versão melhorada"),
            ("📊", "Desempenho",           "Padrões identificados + plano de melhoria"),
            ("📝", "Respostas Modelo",     "Respostas de alto nível para as perguntas mais comuns"),
            ("🏆", "Conquistas",           "Transforme realizações em histórias impactantes"),
        ]
        for i in range(0, len(modulos), 2):
            cc1, cc2 = st.columns(2)
            for col, (ico, nome, desc) in zip([cc1, cc2], modulos[i:i+2]):
                with col:
                    st.markdown(f"""<div class="card-terminal">
                        <div style="font-size:1.4em;margin-bottom:6px;">{ico}</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#15803D;margin-bottom:4px;">{nome}</div>
                        <div style="font-size:12px;color:#6B7280;">{desc}</div>
                    </div>""", unsafe_allow_html=True)

        if hist:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown('<div class="mono-label">// HISTÓRICO RECENTE</div>', unsafe_allow_html=True)
            for item in reversed(hist[-6:]):
                st.markdown(f"""<div class="hist-item">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#6B7280;">{item['data']} · {item['aba']}</span><br>
                    <span style="font-size:12px;">{item['resumo']}…</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.download_button("💾 Salvar dados da sessão (.json)", data=gerar_json_dados(),
            file_name=f"simulador_entrevista_{st.session_state.usuario}.json",
            mime="application/json", key="dl_home")

    # ── PERFIL ──
    with abas[1]:
        st.markdown("## 👤 Meu Perfil Profissional")
        st.markdown('<div class="card-warn">💡 <b>Como usar:</b> Descreva sua trajetória, cargo atual, anos de experiência, área e objetivo. O agente analisa seu perfil e dá orientações de posicionamento.</div>', unsafe_allow_html=True)
        render_chat("perfil")
        chat_input_enviar("perfil", "Ex: Sou analista de dados com 3 anos de experiência em SQL e Python, quero migrar para engenharia de dados. Como me posicionar?")

    # ── SIMULAR ──
    with abas[2]:
        st.markdown("## 🎯 Simular Entrevista")
        st.markdown('<div class="card-success">✅ <b>Modo entrevista real:</b> O agente conduz a entrevista completa. Diga o cargo e nível. Ele fará perguntas uma por vez e avaliará cada resposta.</div>', unsafe_allow_html=True)
        render_chat("simular")
        chat_input_enviar("simular", "Ex: Quero simular uma entrevista para Desenvolvedor Full-Stack Pleno em startup de fintech. Pode começar?")

    # ── POR CARGO ──
    with abas[3]:
        st.markdown("## 💼 Por Área/Cargo")
        st.markdown('<div class="card-terminal"><div class="mono-label">// PREP ESPECIALIZADO</div>Descreva a vaga e o agente gera as perguntas mais prováveis para aquela posição, com respostas modelo.</div>', unsafe_allow_html=True)
        render_chat("cargo")
        chat_input_enviar("cargo", "Ex: Vou entrevistar para Product Manager Sênior numa empresa de e-commerce B2B. Quais perguntas devo esperar?")

    # ── POR EMPRESA ──
    with abas[4]:
        st.markdown("## 🏢 Por Empresa")
        st.markdown('<div class="card-terminal"><div class="mono-label">// INTELIGÊNCIA DE PROCESSO SELETIVO</div>Diga para qual empresa você vai entrevistar e o agente prepara um guia completo.</div>', unsafe_allow_html=True)
        render_chat("empresa")
        chat_input_enviar("empresa", "Ex: Vou entrevistar para o Nubank para vaga de engenheiro de software. Como é o processo e o que valorizam?")

    # ── COMPORTAMENTAL ──
    with abas[5]:
        st.markdown("## 🧠 Perguntas Comportamentais")
        st.markdown('<div class="card-terminal"><div class="mono-label">// MÉTODO STAR</div>Treine respostas situacionais. O agente avalia se você usou Situação → Tarefa → Ação → Resultado.</div>', unsafe_allow_html=True)
        render_chat("comportamental")
        chat_input_enviar("comportamental", "Ex: Me faça 5 perguntas comportamentais para vaga de liderança técnica e avalie minhas respostas.")

    # ── TÉCNICAS ──
    with abas[6]:
        st.markdown("## 💡 Perguntas Técnicas")
        st.markdown('<div class="card-terminal"><div class="mono-label">// AVALIAÇÃO TÉCNICA</div>O agente faz perguntas técnicas adequadas ao seu nível e avalia profundidade e precisão.</div>', unsafe_allow_html=True)
        render_chat("tecnica")
        chat_input_enviar("tecnica", "Ex: Sou desenvolvedor Python backend pleno. Pode me entrevistar com foco em APIs REST e bancos de dados?")

    # ── FEEDBACK ──
    with abas[7]:
        st.markdown("## 🗣️ Feedback em Tempo Real")
        st.markdown('<div class="card-terminal"><div class="mono-label">// ANÁLISE DE RESPOSTA</div>Cole aqui uma pergunta + sua resposta. O agente dá diagnóstico completo com versão melhorada.</div>', unsafe_allow_html=True)
        render_chat("feedback")
        chat_input_enviar("feedback", 'Ex: Pergunta: "Fale sobre um desafio que você superou."\nMinha resposta: "Uma vez tive um prazo apertado e entreguei mesmo assim."')

    # ── DESEMPENHO ──
    with abas[8]:
        st.markdown("## 📊 Meu Desempenho")
        st.markdown('<div class="card-terminal"><div class="mono-label">// ANÁLISE DE PADRÕES</div>Descreva como têm sido suas entrevistas, onde você trava, o que costuma ouvir. O agente cria um plano de melhoria.</div>', unsafe_allow_html=True)
        render_chat("desempenho")
        chat_input_enviar("desempenho", "Ex: Já fiz 4 entrevistas esse mês. Passo a técnica mas não passo na etapa comportamental/cultural. Como melhorar?")

    # ── RESPOSTAS MODELO ──
    with abas[9]:
        st.markdown("## 📝 Respostas Modelo")
        st.markdown('<div class="card-terminal"><div class="mono-label">// BIBLIOTECA DE RESPOSTAS</div>Diga a pergunta e o cargo/contexto. O agente gera uma resposta de alto nível para você adaptar.</div>', unsafe_allow_html=True)
        render_chat("modelo")
        chat_input_enviar("modelo", 'Ex: Gere uma resposta modelo para "Qual seu maior defeito?" para vaga de engenheiro de software sênior.')

    # ── CONQUISTAS ──
    with abas[10]:
        st.markdown("## 🏆 Conquistas")
        st.markdown('<div class="card-terminal"><div class="mono-label">// STORYTELLING PROFISSIONAL</div>Descreva uma conquista sua, mesmo que simplesmente. O agente transforma em história impactante com dados.</div>', unsafe_allow_html=True)
        render_chat("conquistas")
        chat_input_enviar("conquistas", "Ex: Automatizei um relatório que levava 2 horas para ficar pronto. Como transformar isso numa boa história para entrevista?")

    # ── RODAPÉ ──
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-family:'JetBrains Mono',monospace;font-size:10px;color:#9CA3AF;padding:8px 0;">
      © 2026 Simulador de Entrevista IA · meusagentesia.com.br · Powered by Groq
    </div>
    """, unsafe_allow_html=True)
