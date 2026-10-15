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

# ── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"] { visibility:hidden; }

.stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
[data-testid="stSidebar"] { display:none; }

/* INPUTS */
.stTextInput>div>div>input, .stTextArea>div>textarea,
.stSelectbox>div>div>div, .stNumberInput>div>div>input,
.stPasswordInput>div>div>input {
    background-color:#FFFFFF !important; color:#1A1A2E !important;
    border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    border-radius:8px !important;
}
.stTextArea>div>textarea:focus, .stTextInput>div>div>input:focus {
    border-color:#16A34A !important;
    box-shadow:0 0 0 2px rgba(22,163,74,0.12) !important;
}
.stTextArea>div>textarea { resize:vertical !important; }

/* BOTÕES */
.stButton>button {
    width:100%; border-radius:10px; height:3.2em;
    background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
    font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
    font-family:'Inter',sans-serif !important; font-size:14px !important;
    transition:all 0.2s ease;
}
.stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
.stApp .stButton>button, .stApp .stButton>button p,
.stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

/* TÍTULOS */
.stApp h1,.stApp h2,.stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

/* CARDS */
.card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong { color:#14532D !important; }

.card-agent {
    background:linear-gradient(135deg,#F0FDF4,#DCFCE7);
    border:1px solid #86EFAC; border-left:4px solid #16A34A;
    border-radius:4px 14px 14px 4px; padding:16px 20px; margin:10px 0;
    font-size:14px; line-height:1.7; word-wrap:break-word;
}
.stApp .card-agent, .stApp .card-agent p, .stApp .card-agent span,
.stApp .card-agent div, .stApp .card-agent strong { color:#14532D !important; }

.card-user {
    background:#FFFFFF; border:1px solid #CED4DA; border-right:4px solid #9CA3AF;
    border-radius:14px 4px 14px 14px; padding:14px 18px; margin:10px 0;
    font-size:13px; word-wrap:break-word;
}
.stApp .card-user, .stApp .card-user p, .stApp .card-user span,
.stApp .card-user div { color:#374151 !important; }

.card-success { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); border:1px solid #86EFAC; border-radius:14px; padding:16px 20px; margin:10px 0; }
.stApp .card-success, .stApp .card-success p, .stApp .card-success span,
.stApp .card-success div { color:#14532D !important; }

.card-warn { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border:1px solid #FCD34D; border-radius:14px; padding:16px 20px; margin:10px 0; }
.stApp .card-warn, .stApp .card-warn p, .stApp .card-warn span,
.stApp .card-warn div { color:#78350F !important; }

.card-terminal { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px; padding:16px 20px; margin-bottom:12px; }
.stApp .card-terminal, .stApp .card-terminal p, .stApp .card-terminal span,
.stApp .card-terminal div { color:#1A1A2E !important; }

/* STAT BOX */
.stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
.stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
.stat-val { font-size:2em; font-weight:700; color:#166534 !important; }
.stat-lbl { font-size:11px; color:#6B7280 !important; text-transform:uppercase; letter-spacing:0.06em; margin-top:4px; }

/* HIST ITEM */
.hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
.stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span,
.stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

/* LABELS */
.mono-label { font-size:11px; color:#6B7280 !important; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:6px; font-weight:600; }
.mono-title { font-size:15px; font-weight:700; color:#14532D !important; }

/* BADGES */
.badge        { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-verde  { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-green  { background:#059669; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
.badge-gold   { background:#B45309; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
.badge-red    { background:#DC2626; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
.badge-azul   { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

/* CARDS EXTRAS */
.card-blue   { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }
.card-red    { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }
.card-gold   { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:20px; border-radius:14px; border:1px solid #FCD34D; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card-gold, .stApp .card-gold p, .stApp .card-gold span, .stApp .card-gold div { color:#78350F !important; }
.card-purple { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); padding:20px; border-radius:14px; border:1px solid #C4B5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card-purple, .stApp .card-purple p, .stApp .card-purple span, .stApp .card-purple div { color:#3B0764 !important; }
.card-dark   { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }
.card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
.stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

/* ALERTAS */
.alert-info    { background:#EFF6FF; border:1px solid #93C5FD; border-radius:8px; padding:10px 14px; font-size:13px; color:#1E40AF !important; margin-bottom:8px; }
.alert-warn    { background:#FFFBEB; border:1px solid #FCD34D; border-radius:8px; padding:10px 14px; font-size:13px; color:#92400E !important; margin-bottom:8px; }
.alert-danger  { background:#FFF5F5; border:1px solid #FECACA; border-radius:8px; padding:10px 14px; font-size:13px; color:#991B1B !important; margin-bottom:8px; }
.alert-success { background:#F0FDF4; border:1px solid #86EFAC; border-radius:8px; padding:10px 14px; font-size:13px; color:#166534 !important; margin-bottom:8px; }

/* CHAT */
.chat-ai   { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
.stApp .chat-ai, .stApp .chat-ai p, .stApp .chat-ai span, .stApp .chat-ai div { color:#14532D !important; }
.chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
.stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

/* PROGRESS */
.prog-wrap { background:#E5E7EB; border-radius:999px; height:7px; overflow:hidden; margin:5px 0; }
.prog-fill { height:100%; border-radius:999px; transition:width 0.4s ease; }

/* DIVIDER */
.divider { border:none; border-top:1px solid #D1FAE5; margin:16px 0; }

/* ABAS */
.stTabs [data-baseweb="tab-list"] { background:#FFFFFF !important; border-bottom:2px solid #D1FAE5 !important; gap:4px !important; }
.stTabs [data-baseweb="tab"] {
    background:transparent !important; color:#6B7280 !important;
    font-family:'Inter',sans-serif !important; font-size:13px !important;
    font-weight:500 !important; border-radius:8px 8px 0 0 !important;
    padding:10px 16px !important; border-bottom:2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color:#14532D !important; font-weight:700 !important;
    border-bottom:2px solid #16A34A !important;
    background:rgba(22,163,74,0.06) !important;
}
.stTabs [data-baseweb="tab"]:hover { color:#374151 !important; background:rgba(0,0,0,0.03) !important; }

/* EXPANDER */
.streamlit-expanderHeader {
    background:#FFFFFF !important; border:1px solid #CED4DA !important;
    border-radius:8px !important; font-family:'Inter',sans-serif !important;
    font-size:13px !important; color:#374151 !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background:#FFFFFF !important; border:1px dashed #CED4DA !important; border-radius:8px !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton>button {
    background:#FFFFFF !important; border:1px solid #CED4DA !important;
    color:#374151 !important; font-size:13px !important; font-family:'Inter',sans-serif !important;
    border-radius:8px !important; font-weight:500 !important;
}
.stDownloadButton>button:hover { border-color:#16A34A !important; color:#14532D !important; }
.stDownloadButton>button p,.stDownloadButton>button span { color:inherit !important; }

/* SPINNER / ALERTS */
.stSpinner>div { border-top-color:#16A34A !important; }
.stAlert { background:#FFFFFF !important; border:1px solid #CED4DA !important; border-radius:8px !important; }
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
        st.markdown(f'<div class="card"><div class="mono-label">📭 Sem mensagens</div>Inicie uma conversa abaixo.</div>', unsafe_allow_html=True)
        return
    for msg in msgs:
        h = msg.get("hora", "")
        conteudo = msg["content"].replace("\n", "<br>")
        if msg["role"] == "user":
            st.markdown(f"""<div class="chat-user">
                <div class="mono-label">👤 Você · {h}</div>
                {conteudo}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-ai">
                <div class="mono-label">🤖 Agente · {h}</div>
                {conteudo}
            </div>""", unsafe_allow_html=True)

def chat_input_enviar(chat_key: str, placeholder: str, btn_label: str = "Enviar →"):
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
    st.markdown("""
    <div style="text-align:center; padding:30px 20px 20px 20px;">
      <div style="font-size:56px; margin-bottom:8px;">🤖</div>
      <h1 style="font-size:28px; margin:0; color:#1A1A2E;">PRESENÇA IA</h1>
      <p style="font-size:13px; color:#4B5563; letter-spacing:2px; margin-top:6px;">PREPARE • SIMULE • TREINE • PASSE</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")

    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None

        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave.strip()
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

    st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#5B50E8;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════
# ── APP
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.etapa == "App":
    salvar_perfil_cache(st.session_state.usuario)
    hist = st.session_state.get("historico_simulador_entrevista", [])

    # ── TOP BAR ──
    chats_ativos = sum(1 for k in SYSTEM_PROMPTS if st.session_state.get(f"chat_{k}"))
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        st.markdown(f"<h1 style='margin:0;font-size:24px;color:#1A1A2E;'>🤖 Simulador de {st.session_state.usuario}</h1>", unsafe_allow_html=True)
    with c2:
        nivel_txt = f"{st.session_state.total_respostas} respostas · {chats_ativos} módulos"
        st.markdown(f"<div style='padding:14px 0;text-align:right;'><span class='badge-verde' style='padding:6px 14px;font-size:12px;'>{nivel_txt}</span></div>", unsafe_allow_html=True)
    with c3:
        if st.button("🚪 Sair", key="sim_sair"):
            st.session_state.etapa = "Login"
            st.rerun()

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
        st.markdown(f"## 🎯 Olá, {st.session_state.usuario}!")
        c1h, c2h, c3h, c4h = st.columns(4)
        with c1h:
            st.markdown(f"""<div class="stat-box"><div class="stat-val">{st.session_state.total_respostas}</div><div class="stat-lbl">Respostas dadas</div></div>""", unsafe_allow_html=True)
        with c2h:
            st.markdown(f"""<div class="stat-box"><div class="stat-val">{len(hist)}</div><div class="stat-lbl">Interações totais</div></div>""", unsafe_allow_html=True)
        with c3h:
            st.markdown(f"""<div class="stat-box"><div class="stat-val">{chats_ativos}</div><div class="stat-lbl">Módulos usados</div></div>""", unsafe_allow_html=True)
        with c4h:
            st.markdown(f"""<div class="stat-box"><div class="stat-val">10</div><div class="stat-lbl">Módulos disponíveis</div></div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown('<div class="mono-label">Módulos disponíveis</div>', unsafe_allow_html=True)

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
                    st.markdown(f"""<div class="card">
                        <div style="font-size:1.6em;margin-bottom:8px;">{ico}</div>
                        <div style="font-size:14px;font-weight:700;margin-bottom:4px;">{nome}</div>
                        <div style="font-size:13px;opacity:0.8;">{desc}</div>
                    </div>""", unsafe_allow_html=True)

        if hist:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown('<div class="mono-label">Histórico recente</div>', unsafe_allow_html=True)
            for item in reversed(hist[-6:]):
                st.markdown(f"""<div class="hist-item">
                    <small style="color:#6B7280;">{item['data']} · {item['aba']}</small><br>
                    <span style="font-size:13px;">{item['resumo']}…</span>
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
        st.markdown('<div class="card"><div class="mono-label">💼 Prep por Área/Cargo</div>Descreva a vaga e o agente gera as perguntas mais prováveis para aquela posição, com respostas modelo.</div>', unsafe_allow_html=True)
        render_chat("cargo")
        chat_input_enviar("cargo", "Ex: Vou entrevistar para Product Manager Sênior numa empresa de e-commerce B2B. Quais perguntas devo esperar?")

    # ── POR EMPRESA ──
    with abas[4]:
        st.markdown("## 🏢 Por Empresa")
        st.markdown('<div class="card"><div class="mono-label">🏢 Inteligência de Processo Seletivo</div>Diga para qual empresa você vai entrevistar e o agente prepara um guia completo.</div>', unsafe_allow_html=True)
        render_chat("empresa")
        chat_input_enviar("empresa", "Ex: Vou entrevistar para o Nubank para vaga de engenheiro de software. Como é o processo e o que valorizam?")

    # ── COMPORTAMENTAL ──
    with abas[5]:
        st.markdown("## 🧠 Perguntas Comportamentais")
        st.markdown('<div class="card"><div class="mono-label">🧠 Método STAR</div>Treine respostas situacionais. O agente avalia se você usou Situação → Tarefa → Ação → Resultado.</div>', unsafe_allow_html=True)
        render_chat("comportamental")
        chat_input_enviar("comportamental", "Ex: Me faça 5 perguntas comportamentais para vaga de liderança técnica e avalie minhas respostas.")

    # ── TÉCNICAS ──
    with abas[6]:
        st.markdown("## 💡 Perguntas Técnicas")
        st.markdown('<div class="card"><div class="mono-label">💡 Avaliação Técnica</div>O agente faz perguntas técnicas adequadas ao seu nível e avalia profundidade e precisão.</div>', unsafe_allow_html=True)
        render_chat("tecnica")
        chat_input_enviar("tecnica", "Ex: Sou desenvolvedor Python backend pleno. Pode me entrevistar com foco em APIs REST e bancos de dados?")

    # ── FEEDBACK ──
    with abas[7]:
        st.markdown("## 🗣️ Feedback em Tempo Real")
        st.markdown('<div class="card"><div class="mono-label">🗣️ Análise de Resposta</div>Cole aqui uma pergunta + sua resposta. O agente dá diagnóstico completo com versão melhorada.</div>', unsafe_allow_html=True)
        render_chat("feedback")
        chat_input_enviar("feedback", 'Ex: Pergunta: "Fale sobre um desafio que você superou."\nMinha resposta: "Uma vez tive um prazo apertado e entreguei mesmo assim."')

    # ── DESEMPENHO ──
    with abas[8]:
        st.markdown("## 📊 Meu Desempenho")
        st.markdown('<div class="card"><div class="mono-label">📊 Análise de Padrões</div>Descreva como têm sido suas entrevistas, onde você trava, o que costuma ouvir. O agente cria um plano de melhoria.</div>', unsafe_allow_html=True)
        render_chat("desempenho")
        chat_input_enviar("desempenho", "Ex: Já fiz 4 entrevistas esse mês. Passo a técnica mas não passo na etapa comportamental/cultural. Como melhorar?")

    # ── RESPOSTAS MODELO ──
    with abas[9]:
        st.markdown("## 📝 Respostas Modelo")
        st.markdown('<div class="card"><div class="mono-label">📝 Biblioteca de Respostas</div>Diga a pergunta e o cargo/contexto. O agente gera uma resposta de alto nível para você adaptar.</div>', unsafe_allow_html=True)
        render_chat("modelo")
        chat_input_enviar("modelo", 'Ex: Gere uma resposta modelo para "Qual seu maior defeito?" para vaga de engenheiro de software sênior.')

    # ── CONQUISTAS ──
    with abas[10]:
        st.markdown("## 🏆 Conquistas")
        st.markdown('<div class="card"><div class="mono-label">🏆 Storytelling Profissional</div>Descreva uma conquista sua, mesmo que simplesmente. O agente transforma em história impactante com dados.</div>', unsafe_allow_html=True)
        render_chat("conquistas")
        chat_input_enviar("conquistas", "Ex: Automatizei um relatório que levava 2 horas para ficar pronto. Como transformar isso numa boa história para entrevista?")

    # ── RODAPÉ ──
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-size:12px;color:#9CA3AF;padding:8px 0;">
      © 2026 Simulador de Entrevista IA · meusagentesia.com.br · Powered by Groq
    </div>
    """, unsafe_allow_html=True)
