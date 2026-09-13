import streamlit as st
from groq import Groq
from datetime import datetime
import json

st.set_page_config(page_title="Simulador de Entrevista IA", page_icon="🎯", layout="wide")

st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background-color:#FFFBEB; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }
    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }
    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#B45309,#D97706) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#D97706,#B45309) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }
    .stApp h1, .stApp h2, .stApp h3 { color:#78350F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }
    .card { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:20px; border-radius:14px; border:1px solid #FCD34D; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong { color:#78350F !important; }
    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue div { color:#1E3A8A !important; }
    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red div { color:#7F1D1D !important; }
    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green div { color:#14532D !important; }
    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow div { color:#78350F !important; }
    .badge { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#FCD34D,transparent); margin:18px 0; }
    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #FCD34D; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div { color:#78350F !important; }
    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #FCD34D; }
    .stApp .stat-box div, .stApp .stat-box span { color:#78350F !important; }
    .chat-user { background:#FFFFFF; border:1px solid #FCD34D; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user div { color:#78350F !important; }
    .chat-persona { background:#FEF3C7; border:1px solid #FCD34D; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona div { color:#78350F !important; }

    </style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = "Você é um coach de carreira especialista em processos seletivos. Simula entrevistas reais, avalia respostas com critérios profissionais (clareza, relevância, exemplo concreto, impacto) e oferece coaching específico. Português do Brasil."

@st.cache_resource
def get_cache_simulador_entrev():
    return {"perfis": {}}

_cache = get_cache_simulador_entrev()

CHAVES_SALVAR = ["usuario","historico_simulador_entrevista"]

def gerar_json():
    return json.dumps({k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith("_") and k not in ("api_key",)}, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return [p for p in _cache["perfis"].keys() if len(p.strip()) >= 2]

def carregar_perfil_cache(usuario):
    return _cache["perfis"].get(usuario)

defaults = {
    "etapa": "Login", "usuario": "", "api_key": "",
    "historico_simulador_entrevista": [],
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ──
if st.session_state.etapa == "Login":
    st.markdown("# 🎯 Simulador de Entrevista IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
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
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":
    historico = st.session_state.get("historico_simulador_entrevista", [])
    salvar_perfil_cache(st.session_state.usuario)

    _tab_home_se, _tab_perfil_se, _tab_simular, _tab_por_cargo, _tab_por_empresa, _tab_comportamental, _tab_tecnicas, _tab_feedback_se, _tab_desempenho_se, _tab_respostas_modelo, _tab_conquistas_se = st.tabs(['🏠 Home', '👤 Meu Perfil Profissional', '🎯 Simular Entrevista', '💼 Por Área/Cargo', '🏢 Por Empresa', '🧠 Perguntas Comportamentais', '💡 Perguntas Técnicas', '🗣️ Feedback em Tempo Real', '📊 Meu Desempenho', '📝 Respostas Modelo', '🏆 Conquistas'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_simulado")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_simulado", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_home_se:
        st.title(f"🎯 Olá, {st.session_state.usuario}!")
        st.markdown(f"*Treine como um profissional — passe em qualquer entrevista.*")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown(f"### Bem-vindo ao **Simulador de Entrevista IA**")
        st.markdown(f"<div class='card'>Use as abas acima para navegar entre as funcionalidades. Cada aba oferece uma ferramenta diferente com IA.</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>🏠</div><div style='font-size:0.8em;'>Simulador de Entrevista IA</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>🤖</div><div style='font-size:0.8em;'>Powered by IA</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='stat-box'><div style='font-size:1.8em;'>💾</div><div style='font-size:0.8em;'>Salve seus dados</div></div>", unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_sv, _ = st.columns([1,3])
        with col_sv:
            st.download_button("💾 Salvar dados (.json)", data=json.dumps({k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith("_") and k not in ("api_key",)}, ensure_ascii=False, indent=2, default=str), file_name=f"simulador_entrevista_{st.session_state.usuario}.json", mime="application/json", key="dl_simula_1")

    with _tab_perfil_se:
        st.header("👤 Meu Perfil Profissional")
        prompt_perfil_se = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_perfil_se", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_perfil_se", use_container_width=True):
            if prompt_perfil_se.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_perfil_se}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_perfil_se = resp.choices[0].message.content
                        if resultado_perfil_se: st.session_state['res_perfil_se_simula1'] = str(resultado_perfil_se)
                        st.session_state["res_perfil_se"] = resultado_perfil_se
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Meu Perfil Profissional","resumo":prompt_perfil_se[:60],"conteudo":resultado_perfil_se})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_perfil_se"):
            st.markdown(f"<div class='card'>{st.session_state['res_perfil_se']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_perfil_se"], file_name="perfil_se_resultado.txt", mime="text/plain", key="dl_perfil_se")

    with _tab_simular:
        st.header("🎯 Simular Entrevista")
        prompt_simular = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_simular", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_simular", use_container_width=True):
            if prompt_simular.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_simular}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_simular = resp.choices[0].message.content
                        if resultado_simular: st.session_state['res_simular_simula2'] = str(resultado_simular)
                        st.session_state["res_simular"] = resultado_simular
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Simular Entrevista","resumo":prompt_simular[:60],"conteudo":resultado_simular})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_simular"):
            st.markdown(f"<div class='card'>{st.session_state['res_simular']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_simular"], file_name="simular_resultado.txt", mime="text/plain", key="dl_simular")

    with _tab_por_cargo:
        st.header("💼 Por Área/Cargo")
        prompt_por_cargo = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_por_cargo", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_por_cargo", use_container_width=True):
            if prompt_por_cargo.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_por_cargo}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_por_cargo = resp.choices[0].message.content
                        if resultado_por_cargo: st.session_state['res_por_cargo_simula3'] = str(resultado_por_cargo)
                        st.session_state["res_por_cargo"] = resultado_por_cargo
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Por Área/Cargo","resumo":prompt_por_cargo[:60],"conteudo":resultado_por_cargo})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_por_cargo"):
            st.markdown(f"<div class='card'>{st.session_state['res_por_cargo']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_por_cargo"], file_name="por_cargo_resultado.txt", mime="text/plain", key="dl_por_cargo")

    with _tab_por_empresa:
        st.header("🏢 Por Empresa")
        prompt_por_empresa = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_por_empresa", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_por_empresa", use_container_width=True):
            if prompt_por_empresa.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_por_empresa}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_por_empresa = resp.choices[0].message.content
                        if resultado_por_empresa: st.session_state['res_por_empresa_simula4'] = str(resultado_por_empresa)
                        st.session_state["res_por_empresa"] = resultado_por_empresa
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Por Empresa","resumo":prompt_por_empresa[:60],"conteudo":resultado_por_empresa})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_por_empresa"):
            st.markdown(f"<div class='card'>{st.session_state['res_por_empresa']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_por_empresa"], file_name="por_empresa_resultado.txt", mime="text/plain", key="dl_por_empresa")

    with _tab_comportamental:
        st.header("🧠 Perguntas Comportamentais")
        prompt_comportamental = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_comportamental", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_comportamental", use_container_width=True):
            if prompt_comportamental.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_comportamental}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_comportamental = resp.choices[0].message.content
                        if resultado_comportamental: st.session_state['res_comportament_simula5'] = str(resultado_comportamental)
                        st.session_state["res_comportamental"] = resultado_comportamental
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Perguntas Comportamentais","resumo":prompt_comportamental[:60],"conteudo":resultado_comportamental})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_comportamental"):
            st.markdown(f"<div class='card'>{st.session_state['res_comportamental']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_comportamental"], file_name="comportamental_resultado.txt", mime="text/plain", key="dl_comportamental")

    with _tab_tecnicas:
        st.header("💡 Perguntas Técnicas")
        prompt_tecnicas = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_tecnicas", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_tecnicas", use_container_width=True):
            if prompt_tecnicas.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_tecnicas}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_tecnicas = resp.choices[0].message.content
                        if resultado_tecnicas: st.session_state['res_tecnicas_simula6'] = str(resultado_tecnicas)
                        st.session_state["res_tecnicas"] = resultado_tecnicas
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Perguntas Técnicas","resumo":prompt_tecnicas[:60],"conteudo":resultado_tecnicas})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_tecnicas"):
            st.markdown(f"<div class='card'>{st.session_state['res_tecnicas']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_tecnicas"], file_name="tecnicas_resultado.txt", mime="text/plain", key="dl_tecnicas")

    with _tab_feedback_se:
        st.header("🗣️ Feedback em Tempo Real")
        prompt_feedback_se = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_feedback_se", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_feedback_se", use_container_width=True):
            if prompt_feedback_se.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_feedback_se}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_feedback_se = resp.choices[0].message.content
                        if resultado_feedback_se: st.session_state['res_feedback_se_simula7'] = str(resultado_feedback_se)
                        st.session_state["res_feedback_se"] = resultado_feedback_se
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Feedback em Tempo Real","resumo":prompt_feedback_se[:60],"conteudo":resultado_feedback_se})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_feedback_se"):
            st.markdown(f"<div class='card'>{st.session_state['res_feedback_se']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_feedback_se"], file_name="feedback_se_resultado.txt", mime="text/plain", key="dl_feedback_se")

    with _tab_desempenho_se:
        st.header("📊 Meu Desempenho")
        prompt_desempenho_se = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_desempenho_se", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_desempenho_se", use_container_width=True):
            if prompt_desempenho_se.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_desempenho_se}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_desempenho_se = resp.choices[0].message.content
                        if resultado_desempenho_se: st.session_state['res_desempenho_s_simula8'] = str(resultado_desempenho_se)
                        st.session_state["res_desempenho_se"] = resultado_desempenho_se
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Meu Desempenho","resumo":prompt_desempenho_se[:60],"conteudo":resultado_desempenho_se})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_desempenho_se"):
            st.markdown(f"<div class='card'>{st.session_state['res_desempenho_se']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_desempenho_se"], file_name="desempenho_se_resultado.txt", mime="text/plain", key="dl_desempenho_se")

    with _tab_respostas_modelo:
        st.header("📝 Respostas Modelo")
        prompt_respostas_modelo = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_respostas_modelo", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_respostas_modelo", use_container_width=True):
            if prompt_respostas_modelo.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_respostas_modelo}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_respostas_modelo = resp.choices[0].message.content
                        if resultado_respostas_modelo: st.session_state['res_respostas_mo_simula9'] = str(resultado_respostas_modelo)
                        st.session_state["res_respostas_modelo"] = resultado_respostas_modelo
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Respostas Modelo","resumo":prompt_respostas_modelo[:60],"conteudo":resultado_respostas_modelo})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_respostas_modelo"):
            st.markdown(f"<div class='card'>{st.session_state['res_respostas_modelo']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_respostas_modelo"], file_name="respostas_modelo_resultado.txt", mime="text/plain", key="dl_respostas_modelo")

    with _tab_conquistas_se:
        st.header("🏆 Conquistas")
        prompt_conquistas_se = st.text_area("Descreva sua situação ou dúvida:", height=120, key="prompt_conquistas_se", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_conquistas_se", use_container_width=True):
            if prompt_conquistas_se.strip():
                with st.spinner("A IA está analisando..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        msgs = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt_conquistas_se}]
                        resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=2048)
                        resultado_conquistas_se = resp.choices[0].message.content
                        if resultado_conquistas_se: st.session_state['res_conquistas_s_simula10'] = str(resultado_conquistas_se)
                        st.session_state["res_conquistas_se"] = resultado_conquistas_se
                        historico.append({"data":datetime.now().strftime("%d/%m %H:%M"),"aba":"Conquistas","resumo":prompt_conquistas_se[:60],"conteudo":resultado_conquistas_se})
                        st.session_state.historico_simulador_entrevista = historico
                    except Exception as e:
                        st.error(f"Erro na API: {e}")
            else:
                st.warning("Digite sua situação antes de gerar.")
        if st.session_state.get("res_conquistas_se"):
            st.markdown(f"<div class='card'>{st.session_state['res_conquistas_se']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar resultado", data=st.session_state["res_conquistas_se"], file_name="conquistas_se_resultado.txt", mime="text/plain", key="dl_conquistas_se")


# --- RODAPÉ ---
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;font-size:0.75em;color:#94A3B8;'>© 2026 Simulador de Entrevista IA · Quiz Com Prêmios</div>", unsafe_allow_html=True)
