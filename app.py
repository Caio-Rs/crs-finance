import streamlit as st
import pandas as pd
import numpy as np
import re
import io
import json
import unicodedata
from datetime import datetime

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="CRS Finance",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS — Identidade CRS Finance ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #0f1923 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] {
    background-color: #1B2A4A !important;
    border-right: 2px solid #C9A84C !important;
}
[data-testid="stSidebar"] * { color: #c8d0e0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 3px;
    background: #C9A84C;
    margin-bottom: 0;
}
.main .block-container {
    background-color: #0f1923 !important;
    padding: 2rem 2.5rem !important;
    max-width: 1200px;
}
.crs-logo { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 700; color: #ffffff; letter-spacing: -2px; line-height: 1; }
.crs-logo span { color: #C9A84C; }
.crs-sub { font-size: 0.65rem; letter-spacing: 0.28em; text-transform: uppercase; color: #8899BB; font-weight: 300; margin-top: 2px; margin-bottom: 1.5rem; }
.stButton > button { background: transparent !important; border: none !important; border-radius: 8px !important; color: #8899BB !important; font-size: 0.88rem !important; font-weight: 400 !important; text-align: left !important; padding: 9px 12px !important; width: 100% !important; transition: all 0.15s !important; }
.stButton > button:hover { background: rgba(201,168,76,0.1) !important; color: #C9A84C !important; }
.page-title { font-family: 'Playfair Display', serif; font-size: 1.7rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.5px; margin-bottom: 0.25rem; }
.page-sub { font-size: 0.88rem; color: #8899BB; margin-bottom: 1.5rem; }
.hero-card { background: #1B2A4A; border-radius: 14px; padding: 2rem; border-top: 3px solid #C9A84C; margin-bottom: 1.5rem; }
.hero-brand { font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 700; color: #fff; letter-spacing: -2px; line-height: 1; }
.hero-brand span { color: #C9A84C; }
.hero-tagline { font-size: 0.7rem; letter-spacing: 0.3em; text-transform: uppercase; color: #8899BB; margin-top: 4px; }
.hero-slogan { font-family: 'Playfair Display', serif; font-size: 1rem; font-style: italic; color: #C9A84C; background: rgba(201,168,76,0.08); border: 0.5px solid rgba(201,168,76,0.3); border-radius: 8px; padding: 10px 16px; display: inline-block; margin-top: 1.2rem; }
.hero-name { font-size: 0.95rem; font-weight: 500; color: #fff; margin-top: 1.2rem; }
.hero-role { font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #C9A84C; }
.hero-city { font-size: 0.78rem; color: #556688; margin-top: 2px; }
.metric-card { background: #1B2A4A; border-radius: 10px; padding: 1rem 1.25rem; border-left: 3px solid #C9A84C; }
.metric-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #8899BB; margin-bottom: 6px; }
.metric-value { font-size: 1.6rem; font-weight: 600; color: #f1f5f9; line-height: 1; }
.metric-value.green { color: #4ade80; }
.metric-value.red   { color: #f87171; }
.metric-value.amber { color: #C9A84C; }
.section-card { background: #162236; border: 0.5px solid #253550; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; }
.section-card-title { font-size: 0.88rem; font-weight: 600; color: #C9A84C; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.75rem; padding-bottom: 0.6rem; border-bottom: 0.5px solid #253550; }
.badge-ok   { background:#14532d; color:#86efac; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-err  { background:#450a0a; color:#fca5a5; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-warn { background:#422006; color:#fcd34d; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-info { background:#1e3a5f; color:#93c5fd; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.stDataFrame { border: 0.5px solid #253550 !important; border-radius: 10px !important; background: #162236 !important; }
[data-testid="stDataFrameResizable"] { border: 0.5px solid #253550 !important; border-radius: 10px !important; }
[data-testid="stDataFrameResizable"] [role="gridcell"] { color: #e2e8f0 !important; }
[data-testid="stDataFrameResizable"] [role="columnheader"] { background: #1B2A4A !important; color: #C9A84C !important; font-size: 0.72rem !important; letter-spacing: 0.05em !important; }
/* ── Dropdown / Popover — fundo branco, texto PRETO em todos os estados ── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] *,
[data-baseweb="select"] [data-baseweb="popover"],
[data-baseweb="select"] [data-baseweb="popover"] *,
body > div[data-baseweb="popover"],
body > div[data-baseweb="popover"] * {
    background-color: #ffffff !important;
    color: #111827 !important;
}
[data-baseweb="popover"] {
    border: 2px solid #1B2A4A !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35) !important;
}
[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] li {
    background-color: #ffffff !important;
    color: #111827 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    padding: 8px 14px !important;
    border-bottom: 0.5px solid #f0f0f0 !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [role="option"]:hover *,
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li:hover * {
    background-color: #eff6ff !important;
    color: #111827 !important;
}
[data-baseweb="popover"] [aria-selected="true"],
[data-baseweb="popover"] [aria-selected="true"] * {
    background-color: #dbeafe !important;
    color: #111827 !important;
    font-weight: 600 !important;
}
[data-baseweb="popover"] input,
[data-baseweb="popover"] input * {
    background-color: #f9fafb !important;
    color: #111827 !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}
.stTextInput input, .stNumberInput input, .stSelectbox > div > div { background: #162236 !important; border: 0.5px solid #253550 !important; color: #e2e8f0 !important; border-radius: 8px !important; }
label { color: #8899BB !important; font-size: 0.82rem !important; }
.action-btn > button { background: #C9A84C !important; color: #1B2A4A !important; border: none !important; font-weight: 700 !important; border-radius: 8px !important; padding: 0.55rem 1.5rem !important; }
.action-btn > button:hover { opacity: 0.88 !important; }
.svc-card { background: #1B2A4A; border-radius: 10px; padding: 1.1rem 1.25rem; border-top: 2px solid #C9A84C; }
.svc-title { font-size: 0.92rem; font-weight: 600; color: #fff; margin-bottom: 5px; }
.svc-desc  { font-size: 0.82rem; color: #8899BB; line-height: 1.55; }
.svc-price { font-size: 0.82rem; font-weight: 600; color: #C9A84C; margin-top: 8px; }
hr { border-color: #253550 !important; margin: 1.5rem 0 !important; }
#MainMenu, footer, .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "marca"

# ── Chaves de estado persistente ──────────────────────────────────────────────
STATE_KEYS = [
    "_regras_storage",       # regras aprendidas
    "_exportados_storage",   # lançamentos já exportados
    "_contatos_mapa",        # dicionário manual de contatos
    "_base_contatos_md",     # base de contatos do Meu Dinheiro
    "_plano_carregado",      # plano de contas
    "_matriz_regras",        # ★ NOVO — matriz de regras fixas do Excel
    "_historico_class",      # ★ NOVO — histórico de classificações por lançamento
    "_clientes_db",          # clientes cadastrados
]

def exportar_estado() -> bytes:
    state = {k: st.session_state.get(k) for k in STATE_KEYS if k in st.session_state}
    return json.dumps(state, ensure_ascii=False, indent=2).encode("utf-8")

def importar_estado(raw: bytes) -> bool:
    try:
        state = json.loads(raw.decode("utf-8"))
        for k, v in state.items():
            if k in STATE_KEYS and v is not None:
                st.session_state[k] = v
        return True
    except Exception:
        return False

# ── Funções utilitárias ───────────────────────────────────────────────────────
def norm_str(s: str) -> str:
    """Normaliza string: minúsculo, sem acento, sem espaço duplo."""
    s = str(s).lower().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s)

def norm_p(s):
    return norm_str(s)

def fmt_brl(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_numeric(series: pd.Series) -> pd.Series:
    def to_float(v):
        if pd.isna(v):
            return np.nan
        s = str(v).strip().replace("R$", "").replace(" ", "").strip()
        if "," in s and "." in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".")
        s = re.sub(r"[^\d.\-]", "", s)
        try:
            return float(s)
        except Exception:
            return np.nan
    return series.apply(to_float)

def parse_ofx(content: str) -> pd.DataFrame:
    rows = []
    for block in re.finditer(r"<STMTTRN>(.*?)</STMTTRN>", content, re.DOTALL | re.IGNORECASE):
        b = block.group(1)
        def get(tag):
            m = re.search(rf"<{tag}>\s*([^\n<]+)", b, re.IGNORECASE)
            return m.group(1).strip() if m else ""
        try:
            dt = datetime.strptime(get("DTPOSTED")[:8], "%Y%m%d").strftime("%d/%m/%Y")
        except Exception:
            dt = get("DTPOSTED")
        try:
            val = float(get("TRNAMT").replace(",", "."))
        except Exception:
            val = 0.0
        rows.append({"Data": dt, "Descrição": get("MEMO") or get("NAME"), "Valor": val})
    return pd.DataFrame(rows)

def load_file(uploaded) -> pd.DataFrame:
    name = uploaded.name.lower()
    if name.endswith(".csv"):
        raw = uploaded.read()
        for enc in ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252"]:
            try:
                return pd.read_csv(io.BytesIO(raw), encoding=enc, sep=None, engine="python")
            except Exception:
                continue
        return pd.read_csv(io.BytesIO(raw), encoding="latin-1", sep=None, engine="python", on_bad_lines="skip")
    elif name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded)
    elif name.endswith((".ofx", ".ofc", ".txt")):
        raw = uploaded.read()
        for enc in ["utf-8", "latin-1", "iso-8859-1", "cp1252"]:
            try:
                return parse_ofx(raw.decode(enc))
            except Exception:
                continue
        return parse_ofx(raw.decode("utf-8", errors="replace"))
    return pd.DataFrame()

def run_conciliacao(df_ext, df_sis, col_val_ext, col_val_sis, col_desc_ext, col_desc_sis, col_data_ext, col_data_sis):
    ext = df_ext[[col_data_ext, col_desc_ext, col_val_ext]].copy()
    sis = df_sis[[col_data_sis, col_desc_sis, col_val_sis]].copy()
    ext.columns = ["Data", "Descrição", "Valor_Extrato"]
    sis.columns = ["Data", "Descrição", "Valor_Sistema"]
    ext["Valor_Extrato"] = parse_numeric(ext["Valor_Extrato"])
    sis["Valor_Sistema"]  = parse_numeric(sis["Valor_Sistema"])
    ext["_key"] = ext["Valor_Extrato"].round(2).astype(str)
    sis["_key"] = sis["Valor_Sistema"].round(2).astype(str)
    merged = pd.merge(ext, sis, on="_key", how="outer", suffixes=("_ext", "_sis")).drop(columns=["_key"])
    def status(row):
        ext_val = row.get("Valor_Extrato")
        sis_val = row.get("Valor_Sistema")
        has_ext = not (pd.isna(ext_val) if isinstance(ext_val, float) else False)
        has_sis = not (pd.isna(sis_val) if isinstance(sis_val, float) else False)
        if has_ext and has_sis:
            if abs(float(ext_val) - float(sis_val)) < 0.01:
                return "✅ Conciliado"
            return "❌ Divergência"
        if has_ext:
            return "⚠️ Só no Extrato"
        return "ℹ️ Só no Sistema"
    merged["Status"] = merged.apply(status, axis=1)
    merged["Diferença"] = merged["Valor_Extrato"] - merged["Valor_Sistema"]
    return merged

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Auditoria")
    return buf.getvalue()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="crs-logo">C<span>R</span>S</div>
    <div class="crs-sub">Finance · BPO</div>
    """, unsafe_allow_html=True)
    st.markdown("**Menu**")
    st.markdown("<hr style='margin:0.4rem 0 0.6rem;'>", unsafe_allow_html=True)
    nav = {
        "🏛️  Marca & Apresentação":     "marca",
        "👥  Gestão de Clientes":        "clientes",
        "🔎  Auditoria de Lançamentos": "auditoria",
        "⚖️  Conciliação de Saldo":     "conciliacao",
        "📊  Conversor OFX → Excel":    "conversor",
        "🤖  Classificador Caixinha":   "classificador",
        "💼  Serviços & Contato":       "servicos",
    }
    for label, key in nav.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='margin:1rem 0 0.6rem;'>", unsafe_allow_html=True)

    # ── ★ ESTADO PERSISTENTE ──────────────────────────────────────────────────
    with st.expander("💾  Estado do App"):
        st.caption("Salve todas as regras, histórico, plano e matriz num JSON. Restaure ao reabrir o app.")
        st.download_button(
            "⬇️  Salvar estado completo",
            data=exportar_estado(),
            file_name=f"crs_estado_{datetime.today().strftime('%d%m%Y')}.json",
            mime="application/json",
            use_container_width=True,
            key="btn_export_estado",
        )
        f_estado = st.file_uploader("Restaurar estado (JSON)", type=["json"], key="estado_upload", label_visibility="collapsed")
        if f_estado:
            if importar_estado(f_estado.read()):
                st.success("✅ Estado restaurado!")
                st.rerun()
            else:
                st.error("Arquivo inválido.")

    st.markdown("<hr style='margin:0.6rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem;color:#556688;line-height:1.7;'>
        <span style='color:#C9A84C;font-weight:600;'>Caio Rodrigues Silva</span><br>
        Especialista BPO Financeiro<br>
        Parnaíba · PI · Brasil
    </div>
    """, unsafe_allow_html=True)

# ── Páginas ───────────────────────────────────────────────────────────────────
page = st.session_state.page


# ════════════════════════════════════════════════════════════════════════════
# 1. MARCA & APRESENTAÇÃO
# ════════════════════════════════════════════════════════════════════════════
if page == "marca":
    st.markdown("""
    <div class="hero-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="font-size:0.65rem;letter-spacing:.3em;color:#C9A84C;text-transform:uppercase;margin-bottom:8px;">Identidade Profissional</div>
                <div class="hero-brand">C<span>R</span>S<br>Finance</div>
                <div class="hero-tagline">BPO · Gestão Financeira</div>
                <div class="hero-slogan">"Precisão que move o seu negócio."</div>
            </div>
            <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.2);border-radius:10px;padding:1rem 1.5rem;min-width:180px;">
                <div style="font-size:0.65rem;letter-spacing:.2em;color:#8899BB;text-transform:uppercase;margin-bottom:8px;">Especialidades</div>
                <div style="font-size:0.82rem;color:#C9A84C;line-height:2;">
                    ◆ Auditoria de Extrato<br>◆ Contas a Pagar/Receber<br>◆ Conciliação Bancária<br>◆ Relatórios Gerenciais
                </div>
            </div>
        </div>
        <div style="margin-top:1.5rem;padding-top:1rem;border-top:0.5px solid rgba(201,168,76,0.2);">
            <div class="hero-name">Caio Rodrigues Silva</div>
            <div class="hero-role">Especialista BPO Financeiro</div>
            <div class="hero-city">Parnaíba · Piauí · Brasil</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.15em;color:#C9A84C;text-transform:uppercase;margin-bottom:1rem;">Como funciona a auditoria</div>', unsafe_allow_html=True)
    steps = [("1","Extrato\nBancário"),("2","Importação\nOFX/Excel"),("3","Cruzamento\ncom Sistema"),("4","Identifica\nDivergências"),("5","Relatório\nAuditado")]
    for col, (num, label) in zip(st.columns(5), steps):
        col.markdown(f"""
        <div style="text-align:center;">
            <div style="width:44px;height:44px;border-radius:50%;background:#1B2A4A;border:2px solid #C9A84C;color:#C9A84C;font-size:1rem;font-weight:700;display:flex;align-items:center;justify-content:center;margin:0 auto 8px;">{num}</div>
            <div style="font-size:0.75rem;color:#8899BB;line-height:1.4;">{label}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card">
        <div class="section-card-title">Proposta de valor</div>
        <div style="font-size:0.88rem;color:#94a3b8;line-height:1.7;">
            A <strong style="color:#C9A84C;">CRS Finance</strong> garante que cada lançamento do extrato bancário
            esteja registrado corretamente no sistema de gestão — identificando inconsistências,
            duplicidades e lançamentos não conciliados antes que se tornem problemas contábeis ou fiscais.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 2. AUDITORIA DE LANÇAMENTOS
# ════════════════════════════════════════════════════════════════════════════
elif page == "auditoria":
    st.markdown('<div class="page-title">Auditoria de Lançamentos</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Verifica se cada lançamento do extrato bancário está registrado no sistema de gestão — linha por linha.</div>', unsafe_allow_html=True)
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("**Extrato Bancário**")
        st.caption("OFX · CSV · Excel")
        f_aud_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="aud_ext2", label_visibility="collapsed")
    with col_u2:
        st.markdown("**Sistema de Gestão**")
        st.caption("CSV · Excel")
        f_aud_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="aud_sis2", label_visibility="collapsed")
    if not f_aud_ext or not f_aud_sis:
        st.markdown('<div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;"><div style="font-size:2rem;margin-bottom:.5rem;">🔎</div><div style="color:#556688;font-size:0.85rem;">Carregue os dois arquivos para auditar os lançamentos</div></div>', unsafe_allow_html=True)
        st.stop()
    try:
        df_aud_ext = load_file(f_aud_ext)
        df_aud_sis = load_file(f_aud_sis)
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}"); st.stop()
    if df_aud_ext.empty or df_aud_sis.empty:
        st.warning("Um dos arquivos está vazio."); st.stop()
    aba_aud = None
    if f_aud_sis.name.endswith((".xlsx",".xls")):
        try:
            xls_a = pd.ExcelFile(f_aud_sis)
            if len(xls_a.sheet_names) > 1:
                aba_aud = st.selectbox("Aba do sistema", xls_a.sheet_names, key="aud_aba")
                df_aud_sis = pd.read_excel(f_aud_sis, sheet_name=aba_aud)
        except Exception:
            pass
    st.markdown("---")
    cols_ae = df_aud_ext.columns.tolist()
    cols_as = df_aud_sis.columns.tolist()
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: ae_data = st.selectbox("Data (extrato)", cols_ae, key="ae_data")
    with c2: ae_desc = st.selectbox("Descrição (extrato)", cols_ae, index=min(1,len(cols_ae)-1), key="ae_desc")
    with c3: ae_val  = st.selectbox("Valor (extrato)", cols_ae, index=min(2,len(cols_ae)-1), key="ae_val")
    with c4: as_data = st.selectbox("Data (sistema)", cols_as, key="as_data")
    with c5: as_desc = st.selectbox("Descrição (sistema)", cols_as, index=min(1,len(cols_as)-1), key="as_desc")
    with c6: as_val  = st.selectbox("Valor (sistema)", cols_as, index=min(2,len(cols_as)-1), key="as_val")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔎  Auditar Lançamentos", key="btn_audit2"):
        with st.spinner("Auditando…"):
            result = run_conciliacao(df_aud_ext, df_aud_sis, ae_val, as_val, ae_desc, as_desc, ae_data, as_data)
        total = len(result)
        ok    = (result["Status"]=="✅ Conciliado").sum()
        div   = (result["Status"]=="❌ Divergência").sum()
        only_e= (result["Status"]=="⚠️ Só no Extrato").sum()
        only_s= (result["Status"]=="ℹ️ Só no Sistema").sum()
        taxa  = round(ok/total*100,1) if total else 0
        m1,m2,m3,m4,m5,m6 = st.columns(6)
        for col,lbl,val,cls in [(m1,"Total",str(total),""),(m2,"Conciliados",str(ok),"green"),(m3,"Divergências",str(div),"red"),(m4,"Só Extrato",str(only_e),"amber"),(m5,"Só Sistema",str(only_s),"amber"),(m6,"Taxa",f"{taxa}%","green" if taxa>=95 else "amber")]:
            col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        filtro = st.selectbox("Filtrar", ["Todos","✅ Conciliado","❌ Divergência","⚠️ Só no Extrato","ℹ️ Só no Sistema"], key="aud_filter2")
        df_show = result if filtro=="Todos" else result[result["Status"]==filtro]
        for c in ["Valor_Extrato","Valor_Sistema","Diferença"]:
            if c in df_show.columns:
                df_show = df_show.copy()
                df_show[c] = df_show[c].apply(lambda v: fmt_brl(v) if not (isinstance(v,float) and np.isnan(v)) else "—")
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.download_button("⬇️  Exportar Excel", data=to_excel_bytes(result), file_name=f"auditoria_{datetime.today().strftime('%d%m%Y')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ════════════════════════════════════════════════════════════════════════════
# 3. CONCILIAÇÃO DE SALDO
# ════════════════════════════════════════════════════════════════════════════
elif page == "conciliacao":
    st.markdown('<div class="page-title">Conciliação de Saldo</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Escolha o modo conforme a estrutura de contas do cliente.</div>', unsafe_allow_html=True)

    def get_clientes_salvos():
        return json.loads(st.session_state.get("_clientes_db","{}"))
    def carregar_config_cliente(nome):
        return get_clientes_salvos().get(nome, {})
    def parse_aplic_xls(arquivo):
        from bs4 import BeautifulSoup
        try:
            conteudo = arquivo.read().decode("iso-8859-1", errors="replace")
        except Exception:
            arquivo.seek(0)
            conteudo = arquivo.read().decode("utf-8", errors="replace")
        soup = BeautifulSoup(conteudo, "html.parser")
        table = soup.find("table")
        if not table:
            return pd.DataFrame()
        rows_html = table.find_all("tr")
        transactions = []
        for row in rows_html:
            cells = [td.get_text(strip=True) for td in row.find_all(["td","th"])]
            cells = [c for c in cells if c != ""]
            if len(cells) < 2: continue
            data = cells[0]
            if not re.match(r"\d{2}/\d{2}/\d{4}", data): continue
            doc = cells[1] if len(cells) > 1 else ""
            if "Total" in str(cells): continue
            if doc.startswith("A") and len(cells) > 2:
                try:
                    valor = float(cells[2].replace(".","").replace(",","."))
                    transactions.append({"Data": data, "Valor": -valor, "Descrição": "APL APLIC AUT MAIS"})
                except Exception: pass
            elif doc.startswith("R") and len(cells) > 7:
                try:
                    valor = float(cells[7].replace(".","").replace(",","."))
                    transactions.append({"Data": data, "Valor": valor, "Descrição": "RES APLIC AUT MAIS"})
                except Exception: pass
        df = pd.DataFrame(transactions)
        if not df.empty:
            df["_data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
        return df

    clientes_db = get_clientes_salvos()
    nomes_clientes = list(clientes_db.keys())
    cfg = {}
    if nomes_clientes:
        col_cli, col_info = st.columns([2,3])
        with col_cli:
            cliente_sel = st.selectbox("Carregar configuração de cliente", ["— Sem cliente salvo —"] + nomes_clientes, key="conc_cliente_sel")
        with col_info:
            if cliente_sel != "— Sem cliente salvo —":
                cfg = carregar_config_cliente(cliente_sel)
                modo_default = cfg.get("modo_conc", "Simples")
                st.markdown(f'<div style="background:#1B2A4A;border-radius:8px;padding:8px 14px;margin-top:20px;font-size:0.8rem;"><span style="color:#C9A84C;font-weight:600;">{cliente_sel}</span><span style="color:#8899BB;margin-left:8px;">Modo: {modo_default}</span><span style="color:#8899BB;margin-left:8px;">Sistema: {cfg.get("sistema","—")}</span></div>', unsafe_allow_html=True)
            else:
                modo_default = "Simples"
    else:
        cliente_sel = "— Sem cliente salvo —"
        modo_default = "Simples"

    st.markdown("---")
    m1,m2,m3 = st.columns(3)
    for col, titulo, desc, tag, key_val in [
        (m1,"Simples","1 extrato + 1 sistema.","1 OFX + 1 CSV","Simples"),
        (m2,"Multi-Conta","1 extrato + 2 sistemas (CC + Aplicação).","1 OFX + 2 CSV","Multi-Conta"),
        (m3,"Consolidado","2 extratos + 1 sistema.","2 OFX + 1 CSV","Consolidado"),
    ]:
        ativo = (modo_default == key_val)
        borda = "2px solid #C9A84C" if ativo else "0.5px solid #253550"
        col.markdown(f'<div style="background:#162236;border:{borda};border-radius:10px;padding:1rem;height:100px;"><div style="font-size:0.88rem;font-weight:600;color:{"#C9A84C" if ativo else "#f1f5f9"};margin-bottom:6px;">{titulo}</div><div style="font-size:0.75rem;color:#8899BB;line-height:1.5;">{desc}</div><span style="font-size:0.7rem;background:#253550;color:#8899BB;padding:2px 8px;border-radius:4px;">{tag}</span></div>', unsafe_allow_html=True)

    modo_idx = ["Simples","Multi-Conta","Consolidado"].index(modo_default)
    modo = st.radio(" ", ["Simples","Multi-Conta (CC + Aplicação)","Consolidado"], index=modo_idx, horizontal=True, key="conc_modo", label_visibility="collapsed")
    modo_key = modo.split(" ")[0]
    st.markdown("---")

    f_aplic_sis = None
    f_aplic_ofx = None
    if modo_key == "Simples":
        u1,u2 = st.columns(2)
        with u1:
            st.markdown("**Extrato Bancário**"); f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Sistema de Gestão**"); f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")
    elif modo_key == "Multi-Conta":
        u1,u2,u3 = st.columns(3)
        with u1:
            st.markdown("**Extrato (OFX)**"); f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Sistema CC**"); f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")
        with u3:
            st.markdown("**Sistema Aplicação**"); f_aplic_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_aplic_sis", label_visibility="collapsed")
    else:
        u1,u2,u3 = st.columns(3)
        with u1:
            st.markdown("**Extrato CC**"); f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Extrato Aplicação**"); f_aplic_ofx = st.file_uploader(" ", type=["xls","xlsx","csv","txt"], key="conc_aplic_ofx", label_visibility="collapsed")
        with u3:
            st.markdown("**Sistema**"); f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")

    arquivos_ok = f_c_ext and f_c_sis
    if modo_key == "Multi-Conta": arquivos_ok = arquivos_ok and f_aplic_sis
    if modo_key == "Consolidado": arquivos_ok = arquivos_ok and f_aplic_ofx
    if not arquivos_ok:
        st.markdown('<div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;"><div style="font-size:2rem;">⚖️</div><div style="color:#556688;font-size:0.85rem;margin-top:.5rem;">Carregue todos os arquivos necessários</div></div>', unsafe_allow_html=True)
        st.stop()

    try:
        df_ext_raw = load_file(f_c_ext)
    except Exception as e:
        st.error(f"Erro ao ler extrato: {e}"); st.stop()

    aba_sis = None
    if f_c_sis.name.endswith((".xlsx",".xls")):
        try:
            xls_tmp = pd.ExcelFile(f_c_sis)
            abas = xls_tmp.sheet_names
            aba_sis = st.selectbox("Aba do sistema", abas, key="conc_aba") if len(abas)>1 else abas[0]
        except Exception: pass
    try:
        df_sis_raw = pd.read_excel(f_c_sis, sheet_name=aba_sis) if aba_sis else load_file(f_c_sis)
    except Exception as e:
        st.error(f"Erro ao ler sistema: {e}"); st.stop()

    df_aplic_sis_raw = pd.DataFrame()
    if modo_key == "Multi-Conta" and f_aplic_sis:
        try:
            df_aplic_sis_raw = load_file(f_aplic_sis)
        except Exception as e:
            st.warning(f"Erro ao ler conta aplicação: {e}")

    df_aplic_ofx_raw = pd.DataFrame()
    if modo_key == "Consolidado" and f_aplic_ofx:
        try:
            df_aplic_ofx_raw = parse_aplic_xls(f_aplic_ofx)
        except Exception as e:
            st.warning(f"Erro ao ler extrato aplicação: {e}")

    st.markdown("---")
    cols_ext = df_ext_raw.columns.tolist()
    cols_sis = df_sis_raw.columns.tolist()
    idx_de = cols_ext.index(cfg.get("col_data_e","")) if cfg.get("col_data_e","") in cols_ext else 0
    idx_ve = cols_ext.index(cfg.get("col_val_e",""))  if cfg.get("col_val_e","")  in cols_ext else min(2,len(cols_ext)-1)
    idx_ds = cols_sis.index(cfg.get("col_data_s","")) if cfg.get("col_data_s","") in cols_sis else 0
    idx_vs = cols_sis.index(cfg.get("col_val_s",""))  if cfg.get("col_val_s","")  in cols_sis else min(2,len(cols_sis)-1)
    c1,c2,c3,c4 = st.columns(4)
    with c1: col_data_e = st.selectbox("Data (extrato)", cols_ext, index=idx_de, key="cce_d2")
    with c2: col_val_e  = st.selectbox("Valor (extrato)", cols_ext, index=idx_ve, key="cce_v2")
    with c3: col_data_s = st.selectbox("Data (sistema)", cols_sis, index=idx_ds, key="ccs_d2")
    with c4: col_val_s  = st.selectbox("Valor (sistema)", cols_sis, index=idx_vs, key="ccs_v2")

    col_val_aplic_sis = None; col_data_aplic_sis = None
    if modo_key == "Multi-Conta" and not df_aplic_sis_raw.empty:
        cols_ap = df_aplic_sis_raw.columns.tolist()
        ca1,ca2 = st.columns(2)
        with ca1: col_data_aplic_sis = st.selectbox("Data (aplicação)", cols_ap, key="cap_d")
        with ca2: col_val_aplic_sis  = st.selectbox("Valor (aplicação)", cols_ap, index=min(2,len(cols_ap)-1), key="cap_v")

    if modo_key == "Simples":
        st.markdown("---")
        palavras_padrao = ["APLIC AUT","RES APLIC","APL APLIC","RENDIMENTOS REND PAGO","TRANSF PROPRIA","TED PROPRIA"]
        fe1,fe2 = st.columns([1,2])
        with fe1:
            usar_filtro_ext = st.checkbox("Excluir transferências internas do extrato", value=True, key="chk_ext_filtro")
        with fe2:
            if usar_filtro_ext:
                desc_cols_ext = [c for c in cols_ext if any(x in c.lower() for x in ["desc","memo","hist","nome","name"])]
                col_desc_filtro = st.selectbox("Coluna descrição", cols_ext, index=cols_ext.index(desc_cols_ext[0]) if desc_cols_ext else min(1,len(cols_ext)-1), key="cce_desc_f")
                palavras_excluir = st.multiselect("Palavras-chave", options=palavras_padrao, default=palavras_padrao, key="ext_palavras")
        if usar_filtro_ext and palavras_excluir:
            mask = df_ext_raw[col_desc_filtro].str.upper().str.contains("|".join([re.escape(p) for p in palavras_excluir]), na=False)
            n_antes = len(df_ext_raw)
            df_ext_raw = df_ext_raw[~mask].copy()
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;">✓ {n_antes-len(df_ext_raw)} excluídos · {len(df_ext_raw)} restantes</div>', unsafe_allow_html=True)

        ft1, ft2, ft3 = st.columns(3)
        with ft1:
            col_tipo_sis = st.selectbox("Coluna Tipo (sistema)", ["— Nenhum —"] + cols_sis, key="ccs_tipo")
        with ft2:
            col_conta_transf = st.selectbox("Coluna Conta destino", ["— Nenhum —"] + cols_sis, key="ccs_conta_transf")
        with ft3:
            palavras_conta_aplic = st.multiselect("Filtrar por conta destino", options=["Aplicação","Aplic","Auto Mais","Poupança","CDB","LCI","LCA","Reserva"], default=["Aplicação","Aplic","Auto Mais"], key="ccs_conta_palavras")
        n_antes = len(df_sis_raw)
        if col_tipo_sis != "— Nenhum —" and col_conta_transf != "— Nenhum —" and palavras_conta_aplic:
            mask_tipo = df_sis_raw[col_tipo_sis].astype(str).str.lower() == "transferência"
            mask_dest = df_sis_raw[col_conta_transf].astype(str).str.contains("|".join([re.escape(p) for p in palavras_conta_aplic]), case=False, na=False)
            df_sis_raw = df_sis_raw[~(mask_tipo & mask_dest)].copy()
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-top:4px;">✓ {n_antes-len(df_sis_raw)} transferências CC↔Aplicação removidas</div>', unsafe_allow_html=True)

    st.markdown("---")
    ca1,ca2 = st.columns([2,1])
    with ca1:
        tipo_analise = st.selectbox("Tipo de análise", ["Comparação de Valores por Dia","Comparação de Movimentações por Dia","Comparação por Chave Forte (Data+Valor)"], key="conc_tipo")
    with ca2:
        data_range = st.text_input("Filtrar período", placeholder="DD/MM/AAAA – DD/MM/AAAA", key="conc_range")

    with st.expander("💾  Salvar configuração deste cliente"):
        nome_novo = st.text_input("Nome do cliente", value=cliente_sel if cliente_sel != "— Sem cliente salvo —" else "", key="conc_save_nome")
        sistema_novo = st.text_input("Sistema usado", value=cfg.get("sistema",""), key="conc_save_sistema")
        if st.button("Salvar configuração", key="btn_save_cfg"):
            if nome_novo.strip():
                db = get_clientes_salvos()
                db[nome_novo.strip()] = {"modo_conc": modo_key, "sistema": sistema_novo, "col_data_e": col_data_e, "col_val_e": col_val_e, "col_data_s": col_data_s, "col_val_s": col_val_s}
                st.session_state["_clientes_db"] = json.dumps(db, ensure_ascii=False)
                st.success(f"✅ '{nome_novo.strip()}' salvo!")
            else:
                st.warning("Digite o nome do cliente.")

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.button("⚖️  Conciliar Saldo", key="btn_conc"):
        st.stop()

    try:
        df_ext = df_ext_raw.copy(); df_sis = df_sis_raw.copy()
        df_ext[col_val_e] = parse_numeric(df_ext[col_val_e])
        df_sis[col_val_s] = parse_numeric(df_sis[col_val_s])
        df_ext["_data"] = pd.to_datetime(df_ext[col_data_e], dayfirst=True, errors="coerce")
        df_sis["_data"] = pd.to_datetime(df_sis[col_data_s], dayfirst=True, errors="coerce")
        saldo_aplic_info = None
        if modo_key == "Multi-Conta" and not df_aplic_sis_raw.empty and col_val_aplic_sis:
            df_ap = df_aplic_sis_raw.copy()
            df_ap[col_val_aplic_sis] = parse_numeric(df_ap[col_val_aplic_sis])
            df_ap["_data"] = pd.to_datetime(df_ap[col_data_aplic_sis], dayfirst=True, errors="coerce")
            saldo_aplic_info = df_ap[col_val_aplic_sis].sum()
            df_ap_add = df_ap[["_data", col_val_aplic_sis]].rename(columns={col_val_aplic_sis: col_val_s})
            df_ap_add[col_data_s] = df_ap_add["_data"]
            df_sis = pd.concat([df_sis, df_ap_add], ignore_index=True)
        if modo_key == "Consolidado" and not df_aplic_ofx_raw.empty:
            df_ap_ofx = df_aplic_ofx_raw[["_data","Valor"]].copy()
            df_ap_ofx.columns = ["_data", col_val_e]
            df_ap_ofx[col_data_e] = df_ap_ofx["_data"]
            df_ext = pd.concat([df_ext, df_ap_ofx], ignore_index=True)
        dt_min = df_ext["_data"].min(); dt_max = df_ext["_data"].max()
        if data_range and "–" in data_range:
            try:
                partes = [p.strip() for p in data_range.split("–")]
                dt_min = pd.to_datetime(partes[0], dayfirst=True)
                dt_max = pd.to_datetime(partes[1], dayfirst=True)
            except Exception: pass
        df_ext_f = df_ext[(df_ext["_data"]>=dt_min)&(df_ext["_data"]<=dt_max)].copy()
        df_sis_f = df_sis[(df_sis["_data"]>=dt_min)&(df_sis["_data"]<=dt_max)].copy()
        saldo_banco = df_ext_f[col_val_e].sum(); saldo_erp = df_sis_f[col_val_s].sum(); diferenca = saldo_banco - saldo_erp
        periodo_txt = f"{dt_min.strftime('%d/%m/%Y')} a {dt_max.strftime('%d/%m/%Y')}"
        st.markdown("---")
        st.markdown(f'<div style="font-size:0.85rem;color:#8899BB;margin-bottom:1rem;">Período: <strong style="color:#C9A84C;">{periodo_txt}</strong></div>', unsafe_allow_html=True)
        m1,m2,m3 = st.columns(3)
        for col,lbl,val,origem in [(m1,"Saldo Banco",saldo_banco,"OFX"),(m2,"Saldo Sistema",saldo_erp,"ERP"),(m3,"Diferença",diferenca,"BRL")]:
            neg = val < 0 if lbl != "Diferença" else val != 0
            cor_val = "#f87171" if neg else "#4ade80"
            col.markdown(f'<div style="background:#1B2A4A;border-radius:10px;padding:0.9rem 1rem;border-left:3px solid {"#f87171" if (lbl=="Diferença" and diferenca!=0) else "#C9A84C"};margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;"><span style="font-size:0.65rem;color:#8899BB;font-weight:600;text-transform:uppercase;">{lbl}</span><span style="font-size:0.6rem;background:#253550;color:#8899BB;padding:1px 6px;border-radius:4px;">{origem}</span></div><div style="font-size:1.2rem;font-weight:700;color:{cor_val};">{fmt_brl(val)}</div></div>', unsafe_allow_html=True)

        if tipo_analise == "Comparação de Valores por Dia":
            grp_e = df_ext_f.groupby("_data")[col_val_e].sum().reset_index(); grp_s = df_sis_f.groupby("_data")[col_val_s].sum().reset_index()
            grp_e.columns=["Data","Banco"]; grp_s.columns=["Data","Sistema"]
            result = pd.merge(grp_e,grp_s,on="Data",how="outer").fillna(0)
            result["Diferença"] = (result["Banco"]-result["Sistema"]).round(2)
            result["Status"] = result["Diferença"].apply(lambda v: "✅ OK" if abs(v)<0.01 else "❌ DIFF")
            result["Data"] = result["Data"].dt.strftime("%d/%m/%Y")
            for c in ["Banco","Sistema","Diferença"]: result[c] = result[c].apply(fmt_brl)
        elif tipo_analise == "Comparação de Movimentações por Dia":
            grp_e = df_ext_f.groupby("_data")[col_val_e].count().reset_index(); grp_s = df_sis_f.groupby("_data")[col_val_s].count().reset_index()
            grp_e.columns=["Data","Qtd Banco"]; grp_s.columns=["Data","Qtd Sistema"]
            result = pd.merge(grp_e,grp_s,on="Data",how="outer").fillna(0)
            result["Diferença Qtd"] = (result["Qtd Banco"]-result["Qtd Sistema"]).astype(int)
            result["Status"] = result["Diferença Qtd"].apply(lambda v: "✅ OK" if v==0 else "❌ DIFF")
            result["Data"] = result["Data"].dt.strftime("%d/%m/%Y")
        else:
            df_ext_f["_chave"] = df_ext_f["_data"].dt.strftime("%Y%m%d")+"_"+df_ext_f[col_val_e].round(2).astype(str)
            df_sis_f["_chave"] = df_sis_f["_data"].dt.strftime("%Y%m%d")+"_"+df_sis_f[col_val_s].round(2).astype(str)
            cb=set(df_ext_f["_chave"]); cs=set(df_sis_f["_chave"])
            ck1,ck2,ck3=st.columns(3)
            for col,lbl,val,cls in [(ck1,"Conciliados",len(cb&cs),"green"),(ck2,"Só no Banco",len(cb-cs),"amber"),(ck3,"Só no Sistema",len(cs-cb),"amber")]:
                col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>',unsafe_allow_html=True)
            rows=[]
            for _,r in df_ext_f.iterrows():
                rows.append({"Data":r["_data"].strftime("%d/%m/%Y"),"Valor Banco":fmt_brl(r[col_val_e]),"Valor Sistema":"—","Status":"✅ Conciliado" if r["_chave"] in cs else "⚠️ Só no Banco"})
            for _,r in df_sis_f.iterrows():
                if r["_chave"] not in cb:
                    rows.append({"Data":r["_data"].strftime("%d/%m/%Y"),"Valor Banco":"—","Valor Sistema":fmt_brl(r[col_val_s]),"Status":"ℹ️ Só no Sistema"})
            result = pd.DataFrame(rows)
        st.markdown("<br>",unsafe_allow_html=True)
        st.dataframe(result, use_container_width=True, hide_index=True)
        st.download_button("⬇️  Baixar Relatório", data=to_excel_bytes(result), file_name=f"conciliacao_{datetime.today().strftime('%d%m%Y')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Erro ao processar: {e}")


# ════════════════════════════════════════════════════════════════════════════
# 4. GESTÃO DE CLIENTES
# ════════════════════════════════════════════════════════════════════════════
elif page == "clientes":
    st.markdown('<div class="page-title">Gestão de Clientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Cadastre clientes, salve configurações de conciliação e evite reconfigurar a cada uso.</div>', unsafe_allow_html=True)
    def get_db(): return json.loads(st.session_state.get("_clientes_db","{}"))
    def set_db(db): st.session_state["_clientes_db"] = json.dumps(db, ensure_ascii=False)
    db = get_db()
    tabs = st.tabs(["👥  Clientes cadastrados","➕  Novo cliente","✏️  Editar / Excluir"])
    with tabs[0]:
        if not db:
            st.info("Nenhum cliente cadastrado ainda.")
        else:
            for nome, cfg_c in db.items():
                with st.expander(f"**{nome}** — {cfg_c.get('sistema','—')} · Modo {cfg_c.get('modo_conc','—')}"):
                    c1,c2,c3,c4 = st.columns(4)
                    for col,lbl,val in [(c1,"Sistema",cfg_c.get("sistema","—")),(c2,"Modo",cfg_c.get("modo_conc","—")),(c3,"Col. Data",cfg_c.get("col_data_s","—")),(c4,"Col. Valor",cfg_c.get("col_val_s","—"))]:
                        col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value" style="font-size:0.9rem;">{val}</div></div>', unsafe_allow_html=True)
    with tabs[1]:
        n1,n2 = st.columns(2)
        with n1:
            novo_nome    = st.text_input("Nome do cliente *", key="nc_nome")
            novo_sistema = st.text_input("Sistema de gestão *", key="nc_sistema")
            novo_modo    = st.selectbox("Modo padrão", ["Simples","Multi-Conta","Consolidado"], key="nc_modo")
        with n2:
            novo_col_de = st.text_input("Coluna Data extrato", key="nc_de")
            novo_col_ve = st.text_input("Coluna Valor extrato", key="nc_ve")
            novo_col_ds = st.text_input("Coluna Data sistema",  key="nc_ds")
            novo_col_vs = st.text_input("Coluna Valor sistema", key="nc_vs")
        novo_obs = st.text_area("Observações", key="nc_obs", height=80)
        if st.button("➕  Cadastrar", key="btn_add_cliente"):
            if not novo_nome.strip():
                st.warning("Nome obrigatório.")
            elif novo_nome.strip() in db:
                st.warning("Já existe.")
            else:
                db[novo_nome.strip()] = {"sistema":novo_sistema,"modo_conc":novo_modo,"col_data_e":novo_col_de,"col_val_e":novo_col_ve,"col_data_s":novo_col_ds,"col_val_s":novo_col_vs,"observacoes":novo_obs}
                set_db(db); st.success(f"✅ '{novo_nome.strip()}' cadastrado!"); st.rerun()
    with tabs[2]:
        if not db:
            st.info("Nenhum cliente cadastrado.")
        else:
            cliente_ed = st.selectbox("Selecione", list(db.keys()), key="ed_sel")
            cfg_ed = db[cliente_ed]
            e1,e2 = st.columns(2)
            with e1:
                ed_sistema = st.text_input("Sistema", value=cfg_ed.get("sistema",""), key="ed_sis")
                ed_modo    = st.selectbox("Modo", ["Simples","Multi-Conta","Consolidado"], index=["Simples","Multi-Conta","Consolidado"].index(cfg_ed.get("modo_conc","Simples")), key="ed_modo")
                ed_col_de  = st.text_input("Col. Data extrato", value=cfg_ed.get("col_data_e",""), key="ed_de")
                ed_col_ve  = st.text_input("Col. Valor extrato", value=cfg_ed.get("col_val_e",""), key="ed_ve")
            with e2:
                ed_col_ds = st.text_input("Col. Data sistema", value=cfg_ed.get("col_data_s",""), key="ed_ds")
                ed_col_vs = st.text_input("Col. Valor sistema", value=cfg_ed.get("col_val_s",""), key="ed_vs")
                ed_obs    = st.text_area("Observações", value=cfg_ed.get("observacoes",""), key="ed_obs", height=100)
            bc1,bc2 = st.columns(2)
            with bc1:
                if st.button("💾  Salvar", key="btn_ed_save", use_container_width=True):
                    db[cliente_ed] = {"sistema":ed_sistema,"modo_conc":ed_modo,"col_data_e":ed_col_de,"col_val_e":ed_col_ve,"col_data_s":ed_col_ds,"col_val_s":ed_col_vs,"observacoes":ed_obs}
                    set_db(db); st.success("✅ Salvo!"); st.rerun()
            with bc2:
                confirmar_del = st.checkbox(f"Confirmo exclusão de '{cliente_ed}'", key="confirm_del_cli")
                if st.button("🗑️  Excluir", key="btn_del_cli", use_container_width=True):
                    if confirmar_del:
                        del db[cliente_ed]; set_db(db); st.success("Excluído."); st.rerun()
                    else:
                        st.warning("Confirme a exclusão.")
            st.download_button("⬇️  Exportar JSON", data=json.dumps(db, ensure_ascii=False, indent=2).encode("utf-8"), file_name="clientes_crs.json", mime="application/json")

# ════════════════════════════════════════════════════════════════════════════
# 5. CONVERSOR OFX → EXCEL
# ════════════════════════════════════════════════════════════════════════════
elif page == "conversor":
    st.markdown('<div class="page-title">Conversor OFX → Excel</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Converta extratos bancários OFX em planilha Excel estruturada</div>', unsafe_allow_html=True)
    f_ofx = st.file_uploader("Selecione o arquivo OFX", type=["ofx","ofc","txt"], key="conv_ofx")
    if f_ofx:
        content = f_ofx.read().decode("utf-8", errors="replace")
        df_ofx = parse_ofx(content)
        if df_ofx.empty:
            st.warning("Nenhuma transação encontrada.")
        else:
            total_cred = df_ofx[df_ofx["Valor"]>0]["Valor"].sum()
            total_deb  = df_ofx[df_ofx["Valor"]<0]["Valor"].sum()
            m1,m2,m3,m4 = st.columns(4)
            for col,lbl,val,cls in [(m1,"Transações",str(len(df_ofx)),""),(m2,"Créditos",fmt_brl(total_cred),"green"),(m3,"Débitos",fmt_brl(abs(total_deb)),"red"),(m4,"Saldo",fmt_brl(total_cred+total_deb),"green" if total_cred+total_deb>=0 else "red")]:
                col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}" style="font-size:1.1rem;">{val}</div></div>', unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            c1,c2 = st.columns([1,2])
            with c1: tipo_sel = st.selectbox("Tipo", ["Todos","Crédito","Débito"])
            with c2: busca = st.text_input("Buscar descrição")
            df_show = df_ofx.copy()
            if tipo_sel == "Crédito": df_show = df_show[df_show["Valor"]>0]
            elif tipo_sel == "Débito": df_show = df_show[df_show["Valor"]<0]
            if busca: df_show = df_show[df_show["Descrição"].str.contains(busca, case=False, na=False)]
            st.dataframe(df_show, use_container_width=True, hide_index=True)
            st.download_button("⬇️  Baixar Excel", data=to_excel_bytes(df_show), file_name=f"extrato_{f_ofx.name.split('.')[0]}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.markdown('<div class="section-card" style="text-align:center;padding:2.5rem;"><div style="font-size:2rem;">📄</div><div style="color:#556688;font-size:0.88rem;margin-top:.5rem;">Arraste um arquivo .ofx aqui</div></div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 6. CLASSIFICADOR CAIXINHA
# ════════════════════════════════════════════════════════════════════════════
elif page == "classificador":
    st.markdown('<div class="page-title">Classificador Caixinha</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Classifica automaticamente os lançamentos usando Histórico → Matriz → Regras Aprendidas → Regras Base.</div>', unsafe_allow_html=True)

    # ── Plano de contas padrão ────────────────────────────────────────────────
    PLANO_PADRAO = {"2.1 IMPOSTOS E TAXAS":["2.101 - Simples Nacional (DAS)","2.102 - Parcelamentos de Impostos"],"2.2 DEDUCOES DE RECEITAS":["2.201 - Devolucao de vendas/Reembolso","2.202 - Descontos","2.203 - Desembolso - Nota Fiscal","2.204 - Cancelamento/Glosas de Convenios"],"2.4 - CUSTOS DIRETOS COM INSUMOS (MAT)":["2.401 - Teste/Vacinas para Revenda","2.402 - Material de Consumo Clinico","2.403 - Material de Protecao (EPIs)"],"20 - SAIDAS OPERACIONAIS DE CAIXA - REPASSE (DFC)":["20.01 - Repasse Caixa - Medicos (% producao)","20.02 - Repasse Caixa - Terapeutas (% producao)","20.03 - Repasse Caixa - Medicos (valor fixo)","20.04 - Repasse Caixa - Terapeutas (valor fixo)"],"3.1 DESPESAS ADMINISTRATIVAS":["3.303 - Aluguel","3.304 - Assessoria Financeira (BPO)","3.307 - Energia Eletrica","3.308 - Material de Escritorio","3.310 - Material de Copa e Cozinha","3.312 - Material de Limpeza","3.313 - Seguranca e Monitoramento","3.314 - Contabilidade","3.315 - Telefone e Internet","3.317 - Manutencao de Equipamento","3.318 - Softwares e Sistemas de Gestao","3.319 - Servicos de Terceiros","3.320 - Pro-labore","3.326 - Manutencao e Conservacao","3.331 - Servico de Limpeza"],"3.2 - DESPESAS COM PESSOAL":["3.203 - Salarios (D)","3.204 - 13 Salario (D)","3.205 - Ferias (D)","3.206 - Vale Alimentacao (D)","3.207 - Vale Transporte (D)","3.211 - FGTS (D)","3.212 - Gratificacao (D)","3.214 - INSS/IRRF (D)","3.216 - Rescisao"],"3.3 - DESPESAS DE VENDAS E MARKETING":["3.308 - Meta Ads","3.309 - Outdoors","3.305 - Ornamentacao/Eventos","3.306 - Brindes"],"3.4 - DESPESAS FINANCEIRAS":["3.402 - Juros sobre Emprestimos","3.403 - Tarifas Bancarias","3.404 - Taxas de Cartao (MDR)","3.407 - IOF"],"4.1 - INVESTIMENTOS":["4.401 - Moveis e Utensilios","4.403 - Maquinas e Equipamentos","4.405 - Obras/Projeto Arquitetonico"],"5.1 - MOVIMENTACOES DE SOCIOS":["5.502 - Distribuicao de Lucros","5.505 - Financiamento - Pronampe","5.506 - Pagamento de Mutuo a Socios"],"1.1 - RECEITAS OPERACIONAIS (DRE)":["1.101 - Honorarios Clinicos - Medicos","1.102 - Honorarios Clinicos - Terapeutas","1.103 - Receita Notas Fiscais","1.104 - Receita venda de Vacinas"],"1.4 - RECEITAS FINANCEIRAS":["1.402 - Descontos obtidos","1.403 - Rendimentos de Aplicacoes"],"1.5 - MOVIMENTACOES DE SOCIOS":["1.501 - Aporte de Capital","1.503 - Mutuo de Socios"],"1.7 - MOVIMENTACOES TRANSITORIAS":["1.701 - Ajuste de Caixa a Regularizar","1.702 - Depositos nao Identificados","1.703 - Transferencias Transitorias"],"10 - RECEITAS OPERACIONAIS DE CAIXA (DFC)":["10.01 - Recebimento Pix/TED - Sinal","10.02 - Recebimento Pix/TED - Quitacao","10.03 - Recebimento Pix/TED - Terapias","10.05 - Recebimento Pix/TED - Convenios","10.06 - Recebimento Cartao Liquido","10.07 - Recebimento Pix/TED - Vacinas","10.08 - Recebimento Bruto Producao - Medicos","10.09 - Recebimento Bruto Producao - Terapeutas"]}

    def get_plano():
        if "_plano_carregado" in st.session_state:
            return json.loads(st.session_state["_plano_carregado"])
        return PLANO_PADRAO.copy()

    def set_plano(p):
        st.session_state["_plano_carregado"] = json.dumps(p, ensure_ascii=False)

    def carregar_plano_arquivo(arquivo):
        try:
            df = pd.read_excel(arquivo) if arquivo.name.endswith((".xlsx",".xls")) else pd.read_csv(arquivo)
            df.columns = [str(c).strip() for c in df.columns]
            col_cat = next((c for c in df.columns if "categ" in c.lower()), df.columns[0])
            col_sub = next((c for c in df.columns if "sub" in c.lower()), df.columns[1] if len(df.columns)>1 else None)
            plano = {}
            for _, row in df.iterrows():
                cat = str(row[col_cat]).strip()
                if cat in ("nan","") or not cat: continue
                sub = str(row[col_sub]).strip() if col_sub and pd.notna(row[col_sub]) else ""
                if cat not in plano: plano[cat] = []
                if sub and sub != "nan": plano[cat].append(sub)
            return plano if plano else PLANO_PADRAO.copy()
        except Exception as e:
            st.warning(f"Erro ao ler plano: {e}"); return PLANO_PADRAO.copy()

    # ── ★ MATRIZ DE REGRAS — storage ─────────────────────────────────────────
    def carregar_matriz() -> list:
        """Retorna lista de dicts: {palavra_chave, contato, tipo_mov, categoria, subcategoria, observacao}"""
        try:
            dados = st.session_state.get("_matriz_regras")
            if dados: return json.loads(dados)
        except Exception: pass
        return []

    def salvar_matriz(regras: list):
        st.session_state["_matriz_regras"] = json.dumps(regras, ensure_ascii=False)

    def carregar_matriz_de_excel(arquivo) -> list:
        """Lê Excel/CSV com colunas: Palavra-chave | Contato | Tipo | Categoria | Subcategoria"""
        try:
            df = pd.read_excel(arquivo) if arquivo.name.endswith((".xlsx",".xls")) else pd.read_csv(arquivo)
            df.columns = [str(c).strip() for c in df.columns]
            # Mapeamento flexível de colunas
            mapa = {}
            for c in df.columns:
                cl = c.lower()
                if "palavra" in cl or "chave" in cl or "keyword" in cl: mapa["palavra_chave"] = c
                elif "contato" in cl or "fornec" in cl: mapa["contato"] = c
                elif "tipo" in cl or "mov" in cl or "e/s" in cl: mapa["tipo_mov"] = c
                elif "sub" in cl: mapa["subcategoria"] = c
                elif "categ" in cl: mapa["categoria"] = c
                elif "obs" in cl or "nota" in cl: mapa["observacao"] = c
            regras = []
            for _, row in df.iterrows():
                r = {
                    "palavra_chave": str(row.get(mapa.get("palavra_chave",""), "")).strip(),
                    "contato":       str(row.get(mapa.get("contato",""),       "")).strip(),
                    "tipo_mov":      str(row.get(mapa.get("tipo_mov",""),       "")).strip().upper(),
                    "categoria":     str(row.get(mapa.get("categoria",""),      "")).strip(),
                    "subcategoria":  str(row.get(mapa.get("subcategoria",""),   "")).strip(),
                    "observacao":    str(row.get(mapa.get("observacao",""),     "")).strip(),
                }
                # Normaliza Tipo: E=Entrada, S=Saída, '' = ambos
                if r["tipo_mov"] in ("E","ENTRADA","RECEITA","R"): r["tipo_mov"] = "E"
                elif r["tipo_mov"] in ("S","SAIDA","SAÍDA","DESPESA","D"): r["tipo_mov"] = "S"
                else: r["tipo_mov"] = ""
                if r["categoria"] and r["categoria"] not in ("nan",""): regras.append(r)
            return regras
        except Exception as e:
            st.error(f"Erro ao importar Matriz: {e}"); return []

    # ── ★ HISTÓRICO DE CLASSIFICAÇÕES — storage ───────────────────────────────
    def carregar_historico() -> dict:
        """Retorna dict {chave_normalizada: {categoria, subcategoria, origem}}"""
        try:
            dados = st.session_state.get("_historico_class")
            if dados: return json.loads(dados)
        except Exception: pass
        return {}

    def salvar_historico(hist: dict):
        st.session_state["_historico_class"] = json.dumps(hist, ensure_ascii=False)

    def get_chave_historico(contato: str, descricao: str, mov: str) -> str:
        """Chave normalizada — ignora datas e meses para reconhecer recorrências."""
        c = norm_str(contato)
        d = norm_str(descricao)
        # Remove datas e referências de mês para não diferenciar meses
        d = re.sub(r'\d{2}/\d{2}/\d{4}', '', d)
        d = re.sub(r'\b(janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro|jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\b', '', d, flags=re.IGNORECASE)
        d = re.sub(r'\b20\d{2}\b', '', d)  # remove anos
        d = re.sub(r'\s+', ' ', d).strip()
        return f"{c}|{d}|{mov}"

    # ── Regras aprendidas e exportados ────────────────────────────────────────
    def carregar_regras_aprendidas():
        try:
            dados = st.session_state.get("_regras_storage")
            if dados: return json.loads(dados)
        except Exception: pass
        return []

    def salvar_regras_aprendidas(regras):
        st.session_state["_regras_storage"] = json.dumps(regras, ensure_ascii=False)

    def get_chave(row):
        data = str(row.get("Data","")).strip()
        cont = str(row.get("Contato","")).strip().lower()
        desc = str(row.get("Descricao","")).strip().lower()
        ent  = str(row.get("Entrada","")).strip()
        sai  = str(row.get("Saida","")).strip()
        return f"{data}|{cont}|{desc}|{ent}|{sai}"

    def carregar_exportados():
        try:
            dados = st.session_state.get("_exportados_storage")
            if dados: return set(json.loads(dados))
        except Exception: pass
        return set()

    def salvar_exportados(chaves: set):
        st.session_state["_exportados_storage"] = json.dumps(list(chaves), ensure_ascii=False)

    # ── ★ CLASSIFICAR — hierarquia: Histórico → Matriz → Aprendidas → Base ──
    REGRAS_BASE = [
        (["cx do dia","honorários","repasse","honorarios"],["luciany","rossania","marilia","airton","tarcizio","eulalio","isabela","priscila","raquel","nahara","sarita","camila","paloma","theresa","marcello","isadora","juliana","dra sandra","lia","kakel"],"E","10 - RECEITAS OPERACIONAIS DE CAIXA (DFC)","10.08 - Recebimento Bruto Producao - Medicos"),
        (["cx do dia","honorários","repasse","honorarios"],["antonio","marcia","thalita","vanessa","jussara","andressa","katrine","rondinara","iasmim","norla","alessia","brenda","francisca","narllyanna","leticia","vitorugo","jamille","elane","edilene","dayrla","espaco","fonocenter"],"E","10 - RECEITAS OPERACIONAIS DE CAIXA (DFC)","10.09 - Recebimento Bruto Producao - Terapeutas"),
        (["repasse","honorários","cx do dia"],["luciany","rossania","marilia","airton","tarcizio","eulalio","isabela","priscila","raquel","nahara","sarita","camila","paloma","theresa","marcello","isadora","juliana","dra sandra","lia","kakel"],"S","20 - SAIDAS OPERACIONAIS DE CAIXA - REPASSE (DFC)","20.01 - Repasse Caixa - Medicos (% producao)"),
        (["repasse","honorários","cx do dia"],["antonio","marcia","thalita","vanessa","jussara","andressa","katrine","rondinara","iasmim","norla","alessia","brenda","francisca","narllyanna","leticia","vitorugo","jamille","elane","edilene","dayrla","espaco","fonocenter"],"S","20 - SAIDAS OPERACIONAIS DE CAIXA - REPASSE (DFC)","20.02 - Repasse Caixa - Terapeutas (% producao)"),
        (["folha","salario","salário"],[],"S","3.2 - DESPESAS COM PESSOAL","3.203 - Salarios (D)"),
        (["gratificação","gratificacao"],[],"S","3.2 - DESPESAS COM PESSOAL","3.212 - Gratificacao (D)"),
        (["agua","água","galão","galoes","mineral"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.310 - Material de Copa e Cozinha"),
        (["energia","luz"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.307 - Energia Eletrica"),
        (["internet","telefone"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.315 - Telefone e Internet"),
        (["aluguel"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.303 - Aluguel"),
        (["limpeza","faxina"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.331 - Servico de Limpeza"),
        (["manutenção","manut","refriger","ar condic"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.317 - Manutencao de Equipamento"),
        (["material de escritorio","impressora","tinta","papel","caneta"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.308 - Material de Escritorio"),
        (["copa","cozinha","cafe","café","marmita","lanche","restaurante","bolo","toureiro","atacarejo","salgado"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.310 - Material de Copa e Cozinha"),
        (["segurança","monitoramento","camera"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.313 - Seguranca e Monitoramento"),
        (["detetizacao","detetização"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.326 - Manutencao e Conservacao"),
        (["armario","movel","cadeira","mesa"],[],"S","4.1 - INVESTIMENTOS","4.401 - Moveis e Utensilios"),
        (["simples","das "],[],"S","2.1 IMPOSTOS E TAXAS","2.101 - Simples Nacional (DAS)"),
        (["iof"],[],"S","3.4 - DESPESAS FINANCEIRAS","3.407 - IOF"),
        (["vacina","teste","exame","laborat"],[],"S","2.4 - CUSTOS DIRETOS COM INSUMOS (MAT)","2.401 - Teste/Vacinas para Revenda"),
        (["pró-labore","pro labore","prolabore"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.320 - Pro-labore"),
        (["retirada","retiradas"],[],"S","5.1 - MOVIMENTACOES DE SOCIOS","5.502 - Distribuicao de Lucros"),
        (["instagram","facebook","meta ads","publicidade","propaganda"],[],"S","3.3 - DESPESAS DE VENDAS E MARKETING","3.308 - Meta Ads"),
        (["ornamentacao","decoracao","flores","arranjo"],[],"S","3.3 - DESPESAS DE VENDAS E MARKETING","3.305 - Ornamentacao/Eventos"),
        (["tarifas bancarias","tarifa bancaria","tarifa"],[],"S","3.4 - DESPESAS FINANCEIRAS","3.403 - Tarifas Bancarias"),
        (["rendimento","rendimentos"],[],"E","1.4 - RECEITAS FINANCEIRAS","1.403 - Rendimentos de Aplicacoes"),
    ]

    def classificar(contato: str, descricao: str, tipo_mov: str,
                    regras_aprendidas: list, historico: dict = None, matriz: list = None):
        c = norm_str(contato)
        d = norm_str(descricao)
        t = tipo_mov  # "E" ou "S"

        # ── 1. Histórico (prioridade máxima — lançamento idêntico já classificado) ──
        if historico:
            chave_h = get_chave_historico(contato, descricao, tipo_mov)
            if chave_h in historico:
                h = historico[chave_h]
                return h["categoria"], h["subcategoria"], "⭐ Histórico"

        # ── 2. Matriz de regras fixas (importada do Excel) ─────────────────────
        if matriz:
            for r in matriz:
                palavra   = norm_str(r.get("palavra_chave",""))
                contato_r = norm_str(r.get("contato",""))
                mov_r     = str(r.get("tipo_mov","")).strip()
                if mov_r and mov_r != t:
                    continue
                match_desc = not palavra or (palavra in d) or (palavra in c)
                match_cont = not contato_r or (contato_r in c)
                if match_desc and match_cont and r.get("categoria",""):
                    return r["categoria"], r.get("subcategoria",""), "📋 Matriz"

        # ── 3. Regras aprendidas ──────────────────────────────────────────────
        for r in regras_aprendidas:
            if r.get("contato","") and norm_str(r["contato"]) in c:
                if r.get("mov","") in ("", t):
                    return r["categoria"], r["subcategoria"], "🧠 Aprendida"
            if r.get("palavra",""):
                if norm_str(r["palavra"]) in d or norm_str(r["palavra"]) in c:
                    if r.get("mov","") in ("", t):
                        return r["categoria"], r["subcategoria"], "🧠 Aprendida"

        # ── 4. Regras base ────────────────────────────────────────────────────
        for palavras_desc, palavras_contato, mov, cat, sub in REGRAS_BASE:
            if mov != "" and mov != t: continue
            desc_match = any(norm_str(p) in d for p in palavras_desc) or any(norm_str(p) in c for p in palavras_desc)
            if palavras_contato:
                contato_match = any(norm_str(p) in c for p in palavras_contato)
                if desc_match and contato_match: return cat, sub, "Alta"
                if contato_match:               return cat, sub, "Média"
            else:
                if desc_match: return cat, sub, "Alta"

        return "", "", "⚠️ Manual"


    # ── OFX generator ─────────────────────────────────────────────────────────
    def gerar_ofx(df_class, conta_nome="Caixinha"):
        linhas = ["OFXHEADER:100","DATA:OFSGML","VERSION:102","SECURITY:NONE","ENCODING:UTF-8","CHARSET:1252","COMPRESSION:NONE","OLDFILEUID:NONE","NEWFILEUID:NONE","","<OFX>","<BANKMSGSRSV1>","<STMTTRNRS>","<TRNUID>1001","<STATUS><CODE>0<SEVERITY>INFO</STATUS>","<STMTRS>","<CURDEF>BRL",f"<BANKACCTFROM><BANKID>0000<ACCTID>{conta_nome}<ACCTTYPE>CHECKING</BANKACCTFROM>","<BANKTRANLIST>"]
        for i, row in df_class.iterrows():
            try:
                dt = pd.to_datetime(row["Data"], dayfirst=True, errors="coerce")
                dt_str = dt.strftime("%Y%m%d") if pd.notna(dt) else "20260101"
            except Exception:
                dt_str = "20260101"
            entrada = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
            saida   = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
            valor   = (entrada if pd.notna(entrada) and entrada>0 else 0) - (saida if pd.notna(saida) and saida>0 else 0)
            trntype = "CREDIT" if valor>=0 else "DEBIT"
            memo    = str(row.get("Descricao",""))[:60].replace("<","").replace(">","")
            contato = str(row.get("Contato",""))[:40].replace("<","").replace(">","")
            linhas += ["<STMTTRN>",f"<TRNTYPE>{trntype}",f"<DTPOSTED>{dt_str}",f"<TRNAMT>{valor:.2f}",f"<FITID>CX{dt_str}{i:04d}",f"<NAME>{contato}",f"<MEMO>{memo}","</STMTTRN>"]
        linhas += ["</BANKTRANLIST>","</STMTRS>","</STMTTRNRS>","</BANKMSGSRSV1>","</OFX>"]
        return "\n".join(linhas)

    # ── CSV Meu Dinheiro ──────────────────────────────────────────────────────
    CONTAS_DISPONIVEIS = ["","Fechamento de caixa 2025;2026","Itaú 2025;2026","Banco do Brasil","Caixinha 2025;2026"]
    CONTA_PADRAO_CAIXINHA = "Caixinha 2025;2026"

    def montar_csv_meu_dinheiro(df, conta_nome="Caixinha 2025;2026"):
        def fmt_num(v, negativo=False):
            s = f"{abs(v):.2f}".replace(".", ",")
            return f"-{s}" if negativo else s
        rows = []
        for _, r in df.iterrows():
            entrada    = parse_numeric(pd.Series([r.get("Entrada","")])).iloc[0]
            saida      = parse_numeric(pd.Series([r.get("Saida","")])).iloc[0]
            tipo       = str(r.get("Tipo Lançamento","")).strip()
            conta_dest = str(r.get("Conta Destino","")).strip()
            cat        = str(r.get("Categoria","")).strip()
            sub        = str(r.get("SubCategoria","")).strip()
            contato    = str(r.get("Contato","")).strip()
            contato_md = str(r.get("Contato MD","")).strip()
            contato_md_clean = contato_md.lstrip("⚠️ ").strip() if contato_md else contato
            descricao  = str(r.get("Descricao",""))[:100].strip()
            data       = str(r.get("Data","")).strip()
            val_e = entrada if (pd.notna(entrada) and entrada>0) else 0.0
            val_s = saida   if (pd.notna(saida) and saida>0)   else 0.0
            eh_saida = val_s>0 and val_e==0
            nome_limpo = " ".join(w for w in contato.split() if w.lower().rstrip(".") not in ("dra","dr")).strip()
            def make_desc_cx(desc_orig, nome_l, data_l):
                dl = norm_str(desc_orig)
                if any(p in dl for p in ["cx do dia","cx dia"]):   pref = "Cx"
                elif any(p in dl for p in ["fechamento cx","fechamento de cx"]): pref = "Fechamento Cx"
                elif "fusma" in dl: pref = "Fusma"
                else: return desc_orig
                return f"{pref} {nome_l} {data_l}".strip() if nome_l else desc_orig
            if tipo == "Transferência":
                desc_export    = make_desc_cx(descricao, nome_limpo, data)
                valor_str      = fmt_num(val_s, negativo=True) if eh_saida else fmt_num(val_e)
                conta_transf   = conta_dest if conta_dest else "Fechamento de caixa 2025;2026"
                cat_export = sub_export = contato_export = ""
            elif tipo == "Receita":
                desc_export    = make_desc_cx(descricao, nome_limpo, data)
                valor_str      = fmt_num(val_e)
                conta_transf   = ""
                cat_export     = cat; sub_export = sub; contato_export = contato_md_clean or contato
            else:
                desc_export    = make_desc_cx(descricao, nome_limpo, data)
                valor_str      = fmt_num(val_s, negativo=True)
                conta_transf   = ""
                cat_export     = cat; sub_export = sub; contato_export = contato_md_clean or contato
            rows.append({"Data":data,"Valor":valor_str,"Descrição":desc_export,"Conta":conta_nome,"Conta Transferência":conta_transf,"Cartão":"","Categoria":cat_export,"Subcategoria":sub_export,"Contato":contato_export,"Centro":"","Projeto":"","Forma":"","N. Documento":"","Observações":"","Data Competência":data,"Tags":""})
        return pd.DataFrame(rows)

    # ── Contatos ──────────────────────────────────────────────────────────────
    PROFISSIONAIS_DB = [
        {"nome":"Luciany Martins Chaves","chaves":["luciany","chaves"],"eh_medico":True},
        {"nome":"Antonio Clayton Almeida de Araujo","chaves":["antonio","clayton"],"eh_medico":False},
        {"nome":"Rossania Marcedo","chaves":["rossania","marcedo"],"eh_medico":True},
        {"nome":"Thalita Nutri","chaves":["thalita","nutri"],"eh_medico":False},
        {"nome":"VANESSA NEUROPSICO","chaves":["vanessa","neuropsico"],"eh_medico":False},
        {"nome":"Jussara Arrais Basto","chaves":["jussara","arrais"],"eh_medico":False},
        {"nome":"Marcia Karina Carvalho","chaves":["marcia","karina"],"eh_medico":False},
        {"nome":"Marilia Mendes de Sousa","chaves":["marilia","mendes"],"eh_medico":True},
        {"nome":"ANDRESSA Psicóloga","chaves":["andressa","psicologa"],"eh_medico":False},
        {"nome":"TARCIZIO BRITO SANTOS","chaves":["tarcizio","brito"],"eh_medico":True},
        {"nome":"ISABELA LIMA DE ABREU","chaves":["isabela","abreu"],"eh_medico":True},
        {"nome":"PRISCILA FAVORITTO LOPES","chaves":["priscila","favoritto"],"eh_medico":True},
        {"nome":"KATRINE - Psico","chaves":["katrine"],"eh_medico":False},
        {"nome":"RAQUEL PAIVA ARRUDA","chaves":["raquel","paiva"],"eh_medico":True},
        {"nome":"Rondinara Sousa Amaral","chaves":["rondinara","amaral"],"eh_medico":False},
        {"nome":"Iasmim Barbosa dos Santos","chaves":["iasmim","barbosa"],"eh_medico":False},
        {"nome":"Norla Albuquerque","chaves":["norla","albuquerque"],"eh_medico":False},
        {"nome":"MARIA DO ROSARIO - Fono","chaves":["rosario"],"eh_medico":False},
        {"nome":"Alessia Maria Guimarães","chaves":["alessia","guimaraes"],"eh_medico":False},
        {"nome":"NAHARA LIMA JUREMA","chaves":["nahara","jurema"],"eh_medico":True},
        {"nome":"BRENDA DOS SANTOS DE SOUSA","chaves":["brenda"],"eh_medico":False},
        {"nome":"Sarita Sousa Bastos","chaves":["sarita","bastos"],"eh_medico":True},
        {"nome":"AIRTON - Pediatra","chaves":["airton"],"eh_medico":True},
        {"nome":"LETICIA DO VAL LEÓDIDO","chaves":["leticia","leodido"],"eh_medico":False},
        {"nome":"ANA CAMILA MARTINS MUNIZ","chaves":["camila","muniz"],"eh_medico":True},
        {"nome":"PALOMA SANTANA","chaves":["paloma","santana"],"eh_medico":True},
        {"nome":"FERNANDA","chaves":["fernanda"],"eh_medico":False},
        {"nome":"LYSLLY","chaves":["lyslly"],"eh_medico":False},
        {"nome":"Sara Micaela Bezerra","chaves":["sara","micaela"],"eh_medico":False},
        {"nome":"SAVIA NUNES PINTO","chaves":["savia","nunes"],"eh_medico":False},
        {"nome":"Juliana Alencar","chaves":["juliana","alencar"],"eh_medico":True},
        {"nome":"Vitorugo dos Santos Rocha","chaves":["vitorugo"],"eh_medico":False},
        {"nome":"Theresa Kerolayne","chaves":["theresa","kerolayne"],"eh_medico":True},
        {"nome":"Marcello Roberto Leite Soares","chaves":["marcello","roberto","leite"],"eh_medico":True},
        {"nome":"Jamille dos Santos Silva","chaves":["jamille"],"eh_medico":False},
        {"nome":"Elane Sena de Ferreira","chaves":["elane","sena"],"eh_medico":False},
        {"nome":"Edilene Soares da Costa","chaves":["edilene"],"eh_medico":False},
        {"nome":"Gisa Sampaio","chaves":["gisa","sampaio"],"eh_medico":True},
        {"nome":"Dra Sandra","chaves":["sandra"],"eh_medico":True},
        {"nome":"Dayrla Fernandes","chaves":["dayrla","fernandes"],"eh_medico":False},
        {"nome":"Espaco Andrezza Lopes","chaves":["andrezza"],"eh_medico":False},
        {"nome":"Clinica Fonocenter","chaves":["fonocenter","cecicane"],"eh_medico":False},
        {"nome":"Unimed","chaves":["unimed"],"eh_medico":False},
        {"nome":"Lia Kakel","chaves":["kakel","lia"],"eh_medico":True},
        {"nome":"Isadora Maria Oliveira Nunes","chaves":["isadora"],"eh_medico":True},
        {"nome":"Francisca Girlane Silva de Araujo","chaves":["girlane","gigi"],"eh_medico":False},
    ]

    _STOP_PROF = {"de","da","do","dos","das","filho","filha","ltda","junior","neto","sousa","santos","silva","lima","rocha","costa","pinto","lopes","soares","alves","ferreira","oliveira","martins","carvalho","mendes","arruda","basto","brito","paiva"}

    def resolver_profissional(contato_input: str):
        c = norm_str(contato_input)
        c = re.sub(r'^(dra?\.?\s+)', '', c)
        palavras = [w for w in c.split() if len(w)>=4 and w not in _STOP_PROF]
        melhor = None; melhor_score = 0
        for prof in PROFISSIONAIS_DB:
            chaves = set(prof["chaves"])
            score = sum(1 for w in palavras if w in chaves)
            if score > melhor_score:
                melhor_score = score; melhor = prof
        if melhor and melhor_score >= 1:
            return melhor["nome"], melhor["eh_medico"]
        return None, None

    def carregar_mapa_contatos():
        try:
            dados = st.session_state.get("_contatos_mapa")
            if dados: return json.loads(dados)
        except Exception: pass
        return {}

    def salvar_mapa_contatos(mapa):
        st.session_state["_contatos_mapa"] = json.dumps(mapa, ensure_ascii=False)

    def carregar_base_md():
        try:
            dados = st.session_state.get("_base_contatos_md")
            if dados: return json.loads(dados)
        except Exception: pass
        return []

    def salvar_base_md(nomes):
        st.session_state["_base_contatos_md"] = json.dumps(nomes, ensure_ascii=False)

    def resolver_contato(contato_input, mapa, base_md):
        cn = norm_str(contato_input)
        for chave, nome_md in mapa.items():
            if norm_str(chave) in cn: return nome_md, "mapa"
        palavras = [w for w in cn.split() if len(w)>3]
        melhor = None; melhor_score = 0
        for nome_md in base_md:
            palavras_md = set(norm_str(nome_md).split())
            score = sum(1 for p in palavras if p in palavras_md)
            if score > melhor_score: melhor_score = score; melhor = nome_md
        if melhor_score >= 1 and melhor: return melhor, "auto"
        return contato_input, "sem_match"

    MEDICOS    = [norm_str(p["nome"].split()[0]) for p in PROFISSIONAIS_DB if p["eh_medico"]]
    TERAPEUTAS = [norm_str(p["nome"].split()[0]) for p in PROFISSIONAIS_DB if not p["eh_medico"]]
    PESSOAL    = ["cacilene","kacilene","iara","simone","vanderlene","gleicyelle"]
    PALAVRAS_DESPESA_DIRETA = ["instagram","facebook","gratificacao","salario","vale","uniforme","ferias","curso","treinamento","inss","fgts","rescisao","retirada","retiradas","pro labore","prolabore","distribuicao","reembolso","material","limpeza","compra","energia","agua","internet","telefone","aluguel","manutencao","conserto","reparo","instalacao","montagem","salgado","bolo","cafe","lanche","marmita","restaurante","camiseta","brinde","papelaria","viagem","passagem","hospedagem","detetizacao","energia protestada"]

    def detectar_tipo_lancamento(contato, descricao):
        c = norm_str(contato); d = norm_str(descricao)
        palavras_cx = ["cx do dia","caixa do dia","cx dia","fechamento cx","fechamento de cx","fechamento caixa"]
        eh_cx = any(p in d for p in palavras_cx)
        eh_nota = any(p in d for p in ["pago com","pago no cx","pago cx"])
        eh_medico    = any(norm_str(p) in c for p in MEDICOS)
        eh_terapeuta = any(norm_str(p) in c for p in TERAPEUTAS)
        eh_prof = eh_medico or eh_terapeuta
        eh_desp_dir = any(norm_str(p) in d for p in PALAVRAS_DESPESA_DIRETA)
        if eh_cx and not eh_nota:
            if eh_medico:    return "CX_MEDICO", "", "", ""
            elif eh_terapeuta: return "CX_TERAPEUTA", "", "", ""
            else:              return "Transferência", "Fechamento de caixa 2025;2026", "", ""
        if eh_prof and not eh_desp_dir and not eh_nota:
            return "Transferência", "Fechamento de caixa 2025;2026", "", ""
        return None, "", "", ""


    # ── Caixinha parser ───────────────────────────────────────────────────────
    def parse_caixinha_df(df_raw):
        header_row = 0
        for i, row in df_raw.iterrows():
            if "DATA" in [str(v).upper().strip() for v in row.values]:
                header_row = i; break
        df_raw.columns = df_raw.iloc[header_row]
        df_raw = df_raw.iloc[header_row+1:].reset_index(drop=True)
        df_raw.columns = [str(c).strip() for c in df_raw.columns]
        col_map = {}
        for c in df_raw.columns:
            cu = str(c).upper()
            if "DATA" in cu: col_map[c] = "Data"
            elif "CONTATO" in cu or "FORNEC" in cu: col_map[c] = "Contato"
            elif "DESCRI" in cu: col_map[c] = "Descricao"
            elif "ENTRADA" in cu: col_map[c] = "Entrada"
            elif "SA" in cu and "DO" not in cu and len(c)<10: col_map[c] = "Saida"
            elif "SALDO" in cu: col_map[c] = "Saldo"
        df_raw = df_raw.rename(columns=col_map)
        needed = [c for c in ["Data","Contato","Descricao","Entrada","Saida"] if c in df_raw.columns]
        df_work = df_raw[needed].copy()
        df_work = df_work[df_work["Data"].notna() & (df_work["Data"].astype(str).str.strip()!="") & (df_work["Data"].astype(str)!="nan")]
        df_work["Data"] = pd.to_datetime(df_work["Data"], dayfirst=True, errors="coerce").dt.strftime("%d/%m/%Y")
        return df_work[df_work["Data"].notna()].reset_index(drop=True)

    # ── Carrega dados vigentes ────────────────────────────────────────────────
    regras_aprendidas = carregar_regras_aprendidas()
    historico_class   = carregar_historico()
    matriz_regras     = carregar_matriz()
    plano_atual       = get_plano()
    PLANO_CATS        = list(plano_atual.keys())
    subs_flat         = [""] + sorted(set(s for lst in plano_atual.values() for s in lst))

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab_class, tab_matriz, tab_plano, tab_contatos, tab_regras = st.tabs([
        "🤖  Classificar",
        "📊  Matriz de Regras",
        "📋  Plano de Contas",
        "👤  Contatos",
        "📚  Regras Aprendidas",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB: CLASSIFICAR
    # ════════════════════════════════════════════════════════════════════════
    with tab_class:
        # Indicadores do motor
        n_hist = len(historico_class)
        n_matr = len(matriz_regras)
        n_apre = len(regras_aprendidas)
        st.markdown(f"""
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
            <span style="background:#162236;border:1px solid #253550;border-radius:6px;padding:4px 12px;font-size:0.78rem;">
                ⭐ Histórico: <strong style="color:#4ade80;">{n_hist}</strong>
            </span>
            <span style="background:#162236;border:1px solid #253550;border-radius:6px;padding:4px 12px;font-size:0.78rem;">
                📋 Matriz: <strong style="color:#C9A84C;">{n_matr}</strong>
            </span>
            <span style="background:#162236;border:1px solid #253550;border-radius:6px;padding:4px 12px;font-size:0.78rem;">
                🧠 Aprendidas: <strong style="color:#93c5fd;">{n_apre}</strong>
            </span>
            <span style="background:#162236;border:1px solid #253550;border-radius:6px;padding:4px 12px;font-size:0.78rem;color:#8899BB;">
                Hierarquia: ⭐ Histórico → 📋 Matriz → 🧠 Aprendidas → Regras Base
            </span>
        </div>
        """, unsafe_allow_html=True)

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown("**Planilha da Caixinha**")
            st.caption("Excel com abas mensais · ou CSV")
            f_caixa = st.file_uploader(" ", type=["xlsx","xls","csv"], key="class_file", label_visibility="collapsed")
        with col_u2:
            st.markdown("**Cadastro de Contatos (opcional)**")
            f_contatos_up = st.file_uploader(" ", type=["xlsx","xls"], key="class_contatos", label_visibility="collapsed")

        if f_contatos_up:
            try:
                df_con_up = pd.ExcelFile(f_contatos_up).parse(0, header=0)
                extra_med = df_con_up[df_con_up["Categoria"].astype(str).str.contains("iatria|édico|eciatra|Pediatra", na=False, case=False)]["Nome"].str.lower().tolist()
                extra_ter = df_con_up[df_con_up["Categoria"].astype(str).str.contains("terapia|psicol|fono|nutri|fisio|musico|neuropsico|psicoped", na=False, case=False)]["Nome"].str.lower().tolist()
                MEDICOS    += extra_med; TERAPEUTAS += extra_ter
                st.success(f"Cadastro: +{len(extra_med)} médicos, +{len(extra_ter)} terapeutas")
            except Exception as e:
                st.warning(f"Não foi possível ler o cadastro: {e}")

        if not f_caixa:
            st.markdown('<div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;"><div style="font-size:2rem;">🤖</div><div style="color:#556688;font-size:0.85rem;margin-top:.5rem;">Carregue a planilha da Caixinha</div></div>', unsafe_allow_html=True)
            st.stop()

        nome_arquivo = f_caixa.name.lower()
        aba_sel = None
        if nome_arquivo.endswith(".csv"):
            raw_bytes = f_caixa.read(); df_csv_raw = None
            for enc in ["latin-1","cp1252","iso-8859-1","utf-8","utf-8-sig"]:
                for sep in [";",",","\t"]:
                    try:
                        df_csv_raw = pd.read_csv(io.BytesIO(raw_bytes), encoding=enc, sep=sep, header=None, on_bad_lines="skip", engine="python")
                        if len(df_csv_raw.columns) > 3: break
                    except Exception: continue
                if df_csv_raw is not None and len(df_csv_raw.columns) > 3: break
            if df_csv_raw is None or df_csv_raw.empty:
                st.error("Não foi possível ler o CSV."); st.stop()
            aba_sel = f_caixa.name.replace(".csv","").replace("_"," ")
            try:
                df_work = parse_caixinha_df(df_csv_raw)
            except Exception as e:
                st.error(f"Erro ao processar CSV: {e}"); st.stop()
        else:
            try:
                xl_caixa = pd.ExcelFile(f_caixa)
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}"); st.stop()
            abas_cx = [a for a in xl_caixa.sheet_names if "caixa" in a.lower()]
            aba_sel = st.selectbox("Selecione o mês", abas_cx if abas_cx else xl_caixa.sheet_names, key="class_aba")
            try:
                df_raw = xl_caixa.parse(aba_sel, header=None)
                df_work = parse_caixinha_df(df_raw)
            except Exception as e:
                st.error(f"Erro ao ler aba: {e}"); st.stop()

        st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin:.5rem 0 1rem;">Mês/Arquivo: <strong style="color:#C9A84C;">{aba_sel}</strong> · {len(df_work)} lançamentos</div>', unsafe_allow_html=True)

        exportados = carregar_exportados()
        n_ja_exp = sum(1 for _, row in df_work.iterrows() if get_chave(row) in exportados)
        if n_ja_exp > 0:
            st.markdown(f'<div style="background:#162236;border-left:3px solid #C9A84C;border-radius:0 8px 8px 0;padding:8px 14px;font-size:0.82rem;margin-bottom:12px;">📋 <strong style="color:#C9A84C;">{n_ja_exp}</strong> <span style="color:#8899BB;">já exportados anteriormente.</span> <strong style="color:#4ade80;">{len(df_work)-n_ja_exp} novos</strong></div>', unsafe_allow_html=True)

        mapa_contatos = carregar_mapa_contatos()
        base_md       = carregar_base_md()

        if st.button("🤖  Classificar Automaticamente", key="btn_class"):
            cats, subs, confs, tipos, contas_dest, ja_exp_flags, contatos_md, status_contatos = [], [], [], [], [], [], [], []
            for _, row in df_work.iterrows():
                entrada = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
                saida   = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
                tmov    = "E" if (pd.notna(entrada) and entrada>0) else "S"
                contato   = str(row.get("Contato",""))
                descricao = str(row.get("Descricao",""))
                chave     = get_chave(row)
                ja_exp    = chave in exportados
                tipo_det, conta_det, _, _ = detectar_tipo_lancamento(contato, descricao)
                if tipo_det == "Transferência":
                    tipos.append("Transferência"); contas_dest.append(conta_det)
                    cats.append(""); subs.append(""); confs.append("Auto" if not ja_exp else "✅ Exportado")
                elif tipo_det in ("CX_MEDICO","CX_TERAPEUTA"):
                    if tmov == "E":
                        tipo_fin = "Receita"
                        cat_fin = "10 - RECEITAS OPERACIONAIS DE CAIXA (DFC)"
                        sub_fin = "10.08 - Recebimento Bruto Producao - Medicos" if tipo_det=="CX_MEDICO" else "10.09 - Recebimento Bruto Producao - Terapeutas"
                    else:
                        tipo_fin = "Despesa"
                        cat_fin = "20 - SAIDAS OPERACIONAIS DE CAIXA - REPASSE (DFC)"
                        sub_fin = "20.01 - Repasse Caixa - Medicos (% producao)" if tipo_det=="CX_MEDICO" else "20.02 - Repasse Caixa - Terapeutas (% producao)"
                    tipos.append(tipo_fin); contas_dest.append("")
                    if ja_exp: cats.append(""); subs.append(""); confs.append("✅ Exportado")
                    else: cats.append(cat_fin); subs.append(sub_fin); confs.append("Alta")
                else:
                    tipo_fin = "Receita" if tmov=="E" else "Despesa"
                    tipos.append(tipo_fin); contas_dest.append("")
                    if ja_exp: cats.append(""); subs.append(""); confs.append("✅ Exportado")
                    else:
                        cat, sub, conf = classificar(contato, descricao, tmov, regras_aprendidas, historico_class, matriz_regras)
                        cats.append(cat); subs.append(sub); confs.append(conf)
                ja_exp_flags.append("✅ Sim" if ja_exp else "🆕 Novo")
                # Resolve contato
                tipo_final = tipos[-1]
                if tipo_final == "Transferência":
                    contatos_md.append(""); status_contatos.append("transf")
                else:
                    nome_prof, _ = resolver_profissional(contato)
                    if nome_prof:
                        contatos_md.append(nome_prof); status_contatos.append("auto")
                    else:
                        nome_res, status_res = resolver_contato(contato, mapa_contatos, base_md)
                        contatos_md.append(nome_res); status_contatos.append(status_res)
            df_work["Tipo Lançamento"]  = tipos
            df_work["Conta Destino"]    = contas_dest
            df_work["Categoria"]        = cats
            df_work["SubCategoria"]     = subs
            df_work["Confiança"]        = confs
            df_work["Status Export"]    = ja_exp_flags
            df_work["Contato MD"]       = contatos_md
            df_work["_status_contato"]  = status_contatos
            st.session_state["df_classificado"] = df_work.copy()

        if "df_classificado" not in st.session_state:
            st.stop()

        df_class = st.session_state["df_classificado"].copy()
        if "Status Export" not in df_class.columns: df_class["Status Export"] = "🆕 Novo"

        total_exp = (df_class["Status Export"]=="✅ Sim").sum()
        total_nov = (df_class["Status Export"]=="🆕 Novo").sum()
        hist_ok   = (df_class["Confiança"]=="⭐ Histórico").sum()
        matr_ok   = (df_class["Confiança"]=="📋 Matriz").sum()
        apre_ok   = (df_class["Confiança"]=="🧠 Aprendida").sum()
        manual_ok = (df_class[df_class["Status Export"]!="✅ Sim"]["Confiança"]=="⚠️ Manual").sum()

        m1,m2,m3,m4,m5,m6 = st.columns(6)
        for col,lbl,val,cls in [(m1,"Total",str(len(df_class)),""),(m2,"Histórico",str(hist_ok),"green"),(m3,"Matriz",str(matr_ok),"green"),(m4,"Aprendidas",str(apre_ok),"green"),(m5,"Manual",str(manual_ok),"red" if manual_ok>0 else "green"),(m6,"Já exportados",str(total_exp),"amber")]:
            col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Alerta sem match
        if "_status_contato" in df_class.columns:
            n_sem_match = (df_class["_status_contato"]=="sem_match").sum()
            if n_sem_match > 0:
                nomes_sem = list(dict.fromkeys(df_class[df_class["_status_contato"]=="sem_match"]["Contato MD"].tolist()))[:5]
                st.markdown(f'<div style="background:#422006;border-left:3px solid #f97316;border-radius:0 8px 8px 0;padding:10px 14px;font-size:0.82rem;margin-bottom:12px;">⚠️ <strong style="color:#fcd34d;">{n_sem_match} contato(s) sem match</strong> — revise a coluna Contato MD: <span style="color:#fdba74;font-size:0.78rem;">{" · ".join(str(n) for n in nomes_sem if n and str(n)!="nan")}</span></div>', unsafe_allow_html=True)

        st.markdown('<div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:0.82rem;color:#C9A84C;">✏️ Edite <strong>Categoria</strong>, <strong>SubCategoria</strong> e <strong>Contato MD</strong> diretamente na tabela. Salve para criar regras e atualizar o histórico.</div>', unsafe_allow_html=True)

        for col_init, val_init in [("Tipo Lançamento",""),("Conta Destino",""),("Contato MD",""),("_status_contato","sem_match")]:
            if col_init not in df_class.columns: df_class[col_init] = val_init

        df_edit = st.data_editor(
            df_class,
            column_config={
                "Tipo Lançamento": st.column_config.SelectboxColumn("Tipo Lançamento", options=["Receita","Despesa","Transferência"], width="medium"),
                "Conta Destino":   st.column_config.SelectboxColumn("Conta Destino",   options=CONTAS_DISPONIVEIS, width="large"),
                "Categoria":    st.column_config.SelectboxColumn("Categoria",    options=PLANO_CATS, width="large"),
                "SubCategoria": st.column_config.SelectboxColumn("SubCategoria", options=subs_flat,  width="large"),
                "Status Export":st.column_config.TextColumn("Export",    disabled=True, width="small"),
                "Contato MD":   st.column_config.TextColumn("Contato MD", width="medium"),
                "Confiança":    st.column_config.TextColumn("Confiança",  disabled=True, width="medium"),
                "Contato":      st.column_config.TextColumn("Contato"),
                "Descricao":    st.column_config.TextColumn("Descrição",  disabled=True),
                "Data":         st.column_config.TextColumn("Data",       disabled=True, width="small"),
                "Entrada":      st.column_config.TextColumn("Entrada",    disabled=True, width="small"),
                "Saida":        st.column_config.TextColumn("Saída",      disabled=True, width="small"),
            },
            use_container_width=True, hide_index=True, key="editor_class",
        )

        col_sv, _ = st.columns([1,2])
        with col_sv:
            if st.button("💾  Salvar correções + atualizar histórico", key="btn_salvar_regras", use_container_width=True):
                novas_regras = list(regras_aprendidas)
                hist_novo    = dict(historico_class)
                n_novas = 0; n_hist_novo = 0
                orig = st.session_state["df_classificado"]
                for i, row in df_edit.iterrows():
                    orig_cat = orig.loc[i,"Categoria"] if i < len(orig) else ""
                    new_cat  = row.get("Categoria","")
                    new_sub  = row.get("SubCategoria","")
                    if not new_cat: continue
                    contato   = str(row.get("Contato","")).strip()
                    descricao = str(row.get("Descricao","")).strip()
                    entrada   = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
                    saida     = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
                    mov       = "E" if (pd.notna(entrada) and entrada>0) else "S"
                    # ★ Salva no histórico independente de ter mudado ou não
                    chave_h = get_chave_historico(contato, descricao, mov)
                    hist_novo[chave_h] = {"categoria": new_cat, "subcategoria": new_sub, "origem": str(aba_sel)}
                    n_hist_novo += 1
                    # Cria regra aprendida só se mudou
                    if new_cat != orig_cat:
                        if contato and len(contato)>2:
                            r = {"tipo":"contato","contato":contato.lower(),"palavra":"","mov":mov,"categoria":new_cat,"subcategoria":new_sub,"origem":str(aba_sel)}
                            if not any(x.get("contato","").lower()==r["contato"] and x.get("mov","")==mov for x in novas_regras):
                                novas_regras.insert(0, r); n_novas += 1
                        palavras = [p for p in descricao.lower().split() if len(p)>4]
                        if palavras:
                            chave = palavras[0]
                            r2 = {"tipo":"descricao","contato":"","palavra":chave,"mov":mov,"categoria":new_cat,"subcategoria":new_sub,"origem":str(aba_sel)}
                            if not any(x.get("palavra","").lower()==chave and x.get("mov","")==mov for x in novas_regras):
                                novas_regras.insert(0, r2); n_novas += 1
                salvar_regras_aprendidas(novas_regras)
                salvar_historico(hist_novo)
                st.session_state["df_classificado"] = df_edit.copy()
                st.success(f"✅ {n_novas} regras criadas · {n_hist_novo} lançamentos no histórico!")
                st.rerun()

        st.markdown("---")
        nome_base = f"caixinha_{str(aba_sel).replace(' ','_').replace('$','').strip()}_{datetime.today().strftime('%d%m%Y')}"
        status_col = "Status Export" if "Status Export" in df_edit.columns else None
        df_novos = df_edit[df_edit[status_col]!="✅ Sim"].copy() if status_col else df_edit.copy()
        df_csv_md = montar_csv_meu_dinheiro(df_novos, conta_nome=CONTA_PADRAO_CAIXINHA)
        n_novos_export = len(df_novos)

        dl1, dl2, dl3 = st.columns(3)
        with dl1:
            st.markdown("**CSV — Meu Dinheiro**")
            st.caption(f"{n_novos_export} lançamentos novos")
            import csv as _csv
            buf = io.StringIO()
            df_csv_md.to_csv(buf, index=False, sep=",", quoting=_csv.QUOTE_MINIMAL)
            csv_bytes = buf.getvalue().encode("utf-8")
            if st.download_button(f"⬇️  Baixar CSV", data=csv_bytes, file_name=f"{nome_base}_meu_dinheiro.csv", mime="text/csv"):
                exp_atual = carregar_exportados()
                for _, row in df_novos.iterrows(): exp_atual.add(get_chave(row))
                salvar_exportados(exp_atual)
                st.success(f"✅ {n_novos_export} marcados como exportados!")
                st.rerun()
        with dl2:
            st.markdown("**Excel — revisão**")
            st.caption("Planilha completa com confiança")
            st.download_button("⬇️  Baixar Excel", data=to_excel_bytes(df_edit), file_name=f"{nome_base}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with dl3:
            st.markdown("**OFX — extrato**")
            st.caption("Para conciliação bancária")
            st.download_button("⬇️  Baixar OFX", data=gerar_ofx(df_edit, conta_nome=str(aba_sel)).encode("utf-8"), file_name=f"{nome_base}.ofx", mime="application/octet-stream")

        st.markdown('<div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;margin-top:8px;font-size:0.8rem;color:#8899BB;">💡 <strong style="color:#C9A84C;">Dica:</strong> Após salvar as correções, use <strong>💾 Estado do App</strong> no menu lateral para não perder o histórico.</div>', unsafe_allow_html=True)


    # ════════════════════════════════════════════════════════════════════════
    # TAB: ★ MATRIZ DE REGRAS
    # ════════════════════════════════════════════════════════════════════════
    with tab_matriz:
        st.markdown('<div class="page-sub">Importe uma planilha Excel com regras fixas de classificação. A Matriz tem prioridade sobre as Regras Aprendidas e as Regras Base.</div>', unsafe_allow_html=True)

        # Formato esperado
        st.markdown("""
        <div style="background:#162236;border:0.5px solid #253550;border-radius:10px;padding:1rem 1.25rem;margin-bottom:1rem;">
            <div style="font-size:0.75rem;font-weight:600;color:#C9A84C;letter-spacing:.05em;text-transform:uppercase;margin-bottom:.5rem;">Formato da planilha Excel</div>
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;font-size:0.78rem;">
                <div style="background:#1B2A4A;border-radius:6px;padding:6px 10px;"><strong style="color:#C9A84C;">Palavra-chave</strong><br><span style="color:#8899BB;">energia, aluguel…</span></div>
                <div style="background:#1B2A4A;border-radius:6px;padding:6px 10px;"><strong style="color:#C9A84C;">Contato</strong><br><span style="color:#8899BB;">Nome parcial do contato</span></div>
                <div style="background:#1B2A4A;border-radius:6px;padding:6px 10px;"><strong style="color:#C9A84C;">Tipo</strong><br><span style="color:#8899BB;">E = entrada · S = saída</span></div>
                <div style="background:#1B2A4A;border-radius:6px;padding:6px 10px;"><strong style="color:#C9A84C;">Categoria</strong><br><span style="color:#8899BB;">Do plano de contas</span></div>
                <div style="background:#1B2A4A;border-radius:6px;padding:6px 10px;"><strong style="color:#C9A84C;">Subcategoria</strong><br><span style="color:#8899BB;">Do plano de contas</span></div>
            </div>
            <div style="font-size:0.75rem;color:#556688;margin-top:8px;">ℹ️ As colunas Contato e Tipo são opcionais. Deixe em branco para aplicar a qualquer contato ou tipo de movimento.</div>
        </div>
        """, unsafe_allow_html=True)

        # Download do template
        template_rows = [
            {"Palavra-chave":"energia","Contato":"","Tipo":"S","Categoria":"3.1 DESPESAS ADMINISTRATIVAS","Subcategoria":"3.307 - Energia Eletrica","Observacao":"Conta de luz"},
            {"Palavra-chave":"aluguel","Contato":"","Tipo":"S","Categoria":"3.1 DESPESAS ADMINISTRATIVAS","Subcategoria":"3.303 - Aluguel","Observacao":""},
            {"Palavra-chave":"cx do dia","Contato":"luciany","Tipo":"E","Categoria":"10 - RECEITAS OPERACIONAIS DE CAIXA (DFC)","Subcategoria":"10.08 - Recebimento Bruto Producao - Medicos","Observacao":"Receita Luciany"},
            {"Palavra-chave":"salario","Contato":"","Tipo":"S","Categoria":"3.2 - DESPESAS COM PESSOAL","Subcategoria":"3.203 - Salarios (D)","Observacao":""},
        ]
        st.download_button(
            "⬇️  Baixar template Excel",
            data=to_excel_bytes(pd.DataFrame(template_rows)),
            file_name="matriz_template_crs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.markdown("---")
        st.markdown("**Importar Matriz do Excel**")
        f_matriz = st.file_uploader(" ", type=["xlsx","xls","csv"], key="matriz_upload", label_visibility="collapsed")
        if f_matriz:
            regras_importadas = carregar_matriz_de_excel(f_matriz)
            if regras_importadas:
                # Mescla com regras existentes (importadas têm prioridade no início)
                matriz_atual = carregar_matriz()
                # Remove duplicatas por palavra_chave+contato+tipo_mov
                chaves_novas = {(r["palavra_chave"], r["contato"], r["tipo_mov"]) for r in regras_importadas}
                matriz_filtrada = [r for r in matriz_atual if (r["palavra_chave"], r["contato"], r["tipo_mov"]) not in chaves_novas]
                matriz_final = regras_importadas + matriz_filtrada
                salvar_matriz(matriz_final)
                st.success(f"✅ {len(regras_importadas)} regras importadas! Total: {len(matriz_final)}")
                matriz_regras = matriz_final
                st.rerun()
            else:
                st.warning("Nenhuma regra válida encontrada no arquivo.")

        st.markdown("---")
        # Editor da matriz atual
        if not matriz_regras:
            st.info("Nenhuma regra na Matriz ainda. Importe um Excel ou adicione manualmente abaixo.")
        else:
            st.markdown(f'<div style="font-size:0.82rem;color:#C9A84C;margin-bottom:8px;">{len(matriz_regras)} regras ativas · <span style="color:#8899BB;">Prioridade: primeira regra que bate vence</span></div>', unsafe_allow_html=True)

        # Adicionar regra manualmente
        with st.expander("➕  Adicionar regra manualmente"):
            ma1,ma2,ma3 = st.columns(3)
            with ma1:
                nova_palavra  = st.text_input("Palavra-chave", placeholder="ex: energia", key="m_palavra")
                novo_contato  = st.text_input("Contato (opcional)", placeholder="ex: luciany", key="m_contato")
                novo_tipo     = st.selectbox("Tipo", ["","E — Entrada","S — Saída"], key="m_tipo")
            with ma2:
                nova_cat = st.selectbox("Categoria", ["— selecione —"] + PLANO_CATS, key="m_cat")
            with ma3:
                subs_nova_cat = plano_atual.get(nova_cat, []) if nova_cat != "— selecione —" else []
                nova_sub = st.selectbox("Subcategoria", [""] + subs_nova_cat, key="m_sub")
            nova_obs = st.text_input("Observação (opcional)", key="m_obs")
            if st.button("➕  Adicionar à Matriz", key="btn_add_matriz"):
                if not nova_palavra.strip():
                    st.warning("Palavra-chave é obrigatória.")
                elif nova_cat == "— selecione —":
                    st.warning("Selecione a categoria.")
                else:
                    tipo_val = novo_tipo[0] if novo_tipo else ""
                    nova_regra = {"palavra_chave": nova_palavra.strip().lower(), "contato": novo_contato.strip().lower(), "tipo_mov": tipo_val, "categoria": nova_cat, "subcategoria": nova_sub, "observacao": nova_obs}
                    mtz = carregar_matriz()
                    mtz.insert(0, nova_regra)
                    salvar_matriz(mtz)
                    st.success("Regra adicionada!"); st.rerun()

        # Editor tabular
        if matriz_regras:
            df_matriz = pd.DataFrame(matriz_regras)
            df_matriz_edit = st.data_editor(
                df_matriz,
                column_config={
                    "palavra_chave": st.column_config.TextColumn("Palavra-chave", width="medium"),
                    "contato":       st.column_config.TextColumn("Contato",       width="medium"),
                    "tipo_mov":      st.column_config.SelectboxColumn("Tipo", options=["","E","S"], width="small"),
                    "categoria":     st.column_config.SelectboxColumn("Categoria",    options=PLANO_CATS, width="large"),
                    "subcategoria":  st.column_config.SelectboxColumn("Subcategoria", options=subs_flat,  width="large"),
                    "observacao":    st.column_config.TextColumn("Observação", width="medium"),
                },
                num_rows="dynamic", use_container_width=True, hide_index=True, key="editor_matriz",
            )
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                if st.button("💾  Salvar Matriz", key="btn_save_matriz", use_container_width=True):
                    regras_salvas = [r for r in df_matriz_edit.to_dict("records") if str(r.get("palavra_chave","")).strip() and str(r.get("categoria","")).strip()]
                    salvar_matriz(regras_salvas)
                    st.success(f"✅ {len(regras_salvas)} regras salvas!"); st.rerun()
            with mc2:
                st.download_button("⬇️  Exportar Excel",
                    data=to_excel_bytes(df_matriz_edit),
                    file_name=f"matriz_crs_{datetime.today().strftime('%d%m%Y')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True)
            with mc3:
                if st.button("🗑️  Limpar Matriz", key="btn_clear_matriz", use_container_width=True):
                    salvar_matriz([]); st.success("Matriz limpa."); st.rerun()


    # ════════════════════════════════════════════════════════════════════════
    # TAB: PLANO DE CONTAS
    # ════════════════════════════════════════════════════════════════════════
    with tab_plano:
        st.markdown('<div class="page-sub">Gerencie categorias e subcategorias. O plano é usado no Classificador e na Matriz.</div>', unsafe_allow_html=True)
        plano = get_plano(); cats_list = list(plano.keys())

        st.markdown("**Importar plano do Meu Dinheiro**")
        f_plano = st.file_uploader(" ", type=["xlsx","xls","csv"], key="plano_file", label_visibility="collapsed")
        if f_plano:
            plano_importado = carregar_plano_arquivo(f_plano)
            set_plano(plano_importado)
            st.success(f"Plano carregado: {len(plano_importado)} categorias"); st.rerun()

        st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin:.5rem 0 1rem;">{len(cats_list)} categorias · {sum(len(v) for v in plano.values())} subcategorias</div>', unsafe_allow_html=True)
        st.markdown("---")

        add1,add2 = st.columns(2)
        with add1:
            st.markdown("**Nova categoria**")
            nova_cat_nome = st.text_input(" ", placeholder="Ex: 7.1 - NOVA CATEGORIA", key="nova_cat_inp", label_visibility="collapsed")
            if st.button("➕  Adicionar categoria", key="btn_add_cat", use_container_width=True):
                if nova_cat_nome.strip():
                    p = get_plano()
                    if nova_cat_nome.strip() not in p:
                        p[nova_cat_nome.strip()] = []; set_plano(p); st.success("Adicionada!"); st.rerun()
                    else: st.warning("Já existe.")
                else: st.warning("Digite o nome.")
        with add2:
            st.markdown("**Nova subcategoria**")
            cat_mae = st.selectbox("Categoria mãe", ["— selecione —"]+cats_list, key="sub_cat_mae")
            nova_sub_nome = st.text_input(" ", placeholder="Ex: 7.101 - Descrição", key="nova_sub_inp", label_visibility="collapsed")
            if st.button("➕  Adicionar subcategoria", key="btn_add_sub", use_container_width=True):
                if cat_mae == "— selecione —": st.warning("Selecione a categoria.")
                elif not nova_sub_nome.strip(): st.warning("Digite o nome.")
                else:
                    p = get_plano()
                    if nova_sub_nome.strip() not in p[cat_mae]:
                        p[cat_mae].append(nova_sub_nome.strip()); set_plano(p); st.success("Adicionada!"); st.rerun()
                    else: st.warning("Já existe.")
        st.markdown("---")

        ed1,ed2 = st.columns(2)
        with ed1:
            st.markdown("**Renomear categoria**")
            cat_renomear = st.selectbox("", ["— selecione —"]+cats_list, key="cat_renomear_sel", label_visibility="collapsed")
            novo_nome_cat = st.text_input(" ", placeholder="Novo nome", key="novo_nome_cat_inp", label_visibility="collapsed")
            if st.button("✏️  Renomear", key="btn_rename_cat", use_container_width=True):
                if cat_renomear != "— selecione —" and novo_nome_cat.strip():
                    p = get_plano()
                    p_novo = {(novo_nome_cat.strip() if k==cat_renomear else k): v for k,v in p.items()}
                    set_plano(p_novo); st.success("Renomeada!"); st.rerun()
        with ed2:
            st.markdown("**Excluir subcategoria**")
            cat_mae_ex = st.selectbox("Categoria mãe", ["— selecione —"]+cats_list, key="sub_ex_mae")
            if cat_mae_ex != "— selecione —":
                subs_ex = plano.get(cat_mae_ex, [])
                if subs_ex:
                    sub_excluir = st.selectbox("Subcategoria", ["— selecione —"]+subs_ex, key="sub_excluir_sel")
                    if sub_excluir != "— selecione —":
                        confirmar_sub = st.checkbox(f"Confirmo exclusão de '{sub_excluir}'", key="confirm_del_sub")
                        if st.button("🗑️  Excluir subcategoria", key="btn_del_sub", use_container_width=True):
                            if confirmar_sub:
                                p = get_plano(); p[cat_mae_ex].remove(sub_excluir); set_plano(p); st.success("Excluída."); st.rerun()
                            else: st.warning("Confirme a exclusão.")
        st.markdown("---")

        for cat, subs in plano.items():
            with st.expander(f"**{cat}** — {len(subs)} sub"):
                for s in subs: st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;↳ {s}")
                if not subs: st.caption("Sem subcategorias.")

        rows_dl = [{"Categoria":cat,"Subcategoria":s} for cat,subs in plano.items() for s in (subs if subs else [""])]
        st.download_button("⬇️  Baixar plano Excel", data=to_excel_bytes(pd.DataFrame(rows_dl)), file_name=f"plano_contas_crs_{datetime.today().strftime('%d%m%Y')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # ════════════════════════════════════════════════════════════════════════
    # TAB: CONTATOS
    # ════════════════════════════════════════════════════════════════════════
    with tab_contatos:
        st.markdown('<div class="page-sub">Mapeie contatos do input para nomes exatos do Meu Dinheiro.</div>', unsafe_allow_html=True)
        mapa_atual = carregar_mapa_contatos(); base_atual = carregar_base_md()

        st.markdown("**Base de contatos do Meu Dinheiro**")
        f_base_md = st.file_uploader(" ", type=["xlsx","xls","csv"], key="base_md_upload", label_visibility="collapsed")
        if f_base_md:
            try:
                df_base = pd.read_excel(f_base_md) if f_base_md.name.endswith((".xlsx",".xls")) else pd.read_csv(f_base_md)
                col_nome = next((c for c in df_base.columns if "nome" in c.lower()), df_base.columns[0])
                nomes_base = [str(n).strip() for n in df_base[col_nome].dropna() if str(n).strip()]
                salvar_base_md(nomes_base); base_atual = nomes_base
                st.success(f"✅ {len(nomes_base)} contatos carregados!")
            except Exception as e: st.warning(f"Erro: {e}")

        if base_atual: st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-bottom:12px;">📋 {len(base_atual)} contatos na base — auto-match ativo</div>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("**Dicionário manual**")
        ma1,ma2,ma3 = st.columns([2,3,1])
        with ma1: nova_chave = st.text_input(" ", placeholder="Palavra-chave", key="novo_map_chave", label_visibility="collapsed")
        with ma2:
            if base_atual:
                novo_nome = st.selectbox(" ", ["— selecione —"]+sorted(base_atual), key="novo_map_nome_sel", label_visibility="collapsed")
                if novo_nome == "— selecione —": novo_nome = st.text_input(" ", placeholder="Nome exato", key="novo_map_nome_txt", label_visibility="collapsed")
            else:
                novo_nome = st.text_input(" ", placeholder="Nome exato no Meu Dinheiro", key="novo_map_nome_txt", label_visibility="collapsed")
        with ma3:
            if st.button("➕", key="btn_add_mapa", use_container_width=True):
                if nova_chave.strip() and novo_nome and novo_nome not in ("— selecione —",""):
                    mapa_edit = carregar_mapa_contatos()
                    mapa_edit[nova_chave.strip().lower()] = novo_nome.strip()
                    salvar_mapa_contatos(mapa_edit); st.success("Adicionado!"); st.rerun()
                else: st.warning("Preencha os dois campos.")

        if mapa_atual:
            df_mapa = pd.DataFrame([{"Palavra-chave": k, "Nome no Meu Dinheiro": v} for k,v in mapa_atual.items()])
            df_mapa_edit = st.data_editor(df_mapa, column_config={"Palavra-chave":st.column_config.TextColumn(width="medium"),"Nome no Meu Dinheiro":st.column_config.TextColumn(width="large")}, num_rows="dynamic", use_container_width=True, hide_index=True, key="editor_mapa")
            mc1,mc2 = st.columns(2)
            with mc1:
                if st.button("💾  Salvar", key="btn_save_mapa", use_container_width=True):
                    novo_mapa = {str(r["Palavra-chave"]).strip().lower(): str(r["Nome no Meu Dinheiro"]).strip() for _,r in df_mapa_edit.iterrows() if str(r.get("Palavra-chave","")).strip()}
                    salvar_mapa_contatos(novo_mapa); st.success("Salvo!"); st.rerun()
            with mc2:
                st.download_button("⬇️  Exportar JSON", data=json.dumps(mapa_atual, ensure_ascii=False, indent=2).encode("utf-8"), file_name="contatos_mapa_crs.json", mime="application/json", use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB: REGRAS APRENDIDAS + HISTÓRICO
    # ════════════════════════════════════════════════════════════════════════
    with tab_regras:
        st.markdown('<div class="page-sub">Regras criadas pelas suas correções e histórico de classificações — prioridade máxima.</div>', unsafe_allow_html=True)

        # Histórico
        with st.expander(f"⭐  Histórico de Classificações ({len(historico_class)} lançamentos)"):
            st.caption("Lançamentos idênticos (mesmo contato + descrição + tipo) são classificados automaticamente pelo histórico.")
            if historico_class:
                df_hist = pd.DataFrame([{"Chave": k, "Categoria": v["categoria"], "Subcategoria": v["subcategoria"], "Origem": v.get("origem","")} for k,v in historico_class.items()])
                st.dataframe(df_hist, use_container_width=True, hide_index=True)
                hc1,hc2 = st.columns(2)
                with hc1:
                    st.download_button("⬇️  Exportar histórico JSON", data=json.dumps(historico_class, ensure_ascii=False, indent=2).encode("utf-8"), file_name="historico_class_crs.json", mime="application/json", use_container_width=True)
                with hc2:
                    if st.button("🗑️  Limpar histórico", key="btn_clear_hist", use_container_width=True):
                        salvar_historico({}); st.success("Histórico limpo."); st.rerun()
            else:
                st.info("Histórico vazio. Salve correções no Classificador para popular.")

        st.markdown("---")
        # Exportados
        exportados_hist = carregar_exportados()
        st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin-bottom:8px;">📋 <strong style="color:#C9A84C;">{len(exportados_hist)}</strong> lançamentos marcados como exportados.</div>', unsafe_allow_html=True)
        if st.button("🗑️  Limpar histórico de exportados", key="btn_clear_exp"):
            salvar_exportados(set()); st.success("Limpo."); st.rerun()
        st.markdown("---")

        # Regras aprendidas
        regras_atual = carregar_regras_aprendidas()
        if "_plano_carregado" in st.session_state:
            PLANO_CATS_R = list(json.loads(st.session_state["_plano_carregado"]).keys())
            subs_flat_r  = [""] + sorted(set(s for lst in json.loads(st.session_state["_plano_carregado"]).values() for s in lst))
        else:
            PLANO_CATS_R = list(PLANO_PADRAO.keys())
            subs_flat_r  = [""] + sorted(set(s for lst in PLANO_PADRAO.values() for s in lst))

        if not regras_atual:
            st.info("Nenhuma regra aprendida ainda.")
        else:
            st.markdown(f'<div style="font-size:0.82rem;color:#C9A84C;margin-bottom:1rem;">🧠 {len(regras_atual)} regras aprendidas</div>', unsafe_allow_html=True)
            df_regras = pd.DataFrame(regras_atual)
            df_regras_edit = st.data_editor(df_regras, column_config={"tipo":st.column_config.TextColumn("Tipo",disabled=True,width="small"),"contato":st.column_config.TextColumn("Contato",width="medium"),"palavra":st.column_config.TextColumn("Palavra",width="medium"),"mov":st.column_config.SelectboxColumn("Mov",options=["E","S",""],width="small"),"categoria":st.column_config.SelectboxColumn("Categoria",options=PLANO_CATS_R,width="large"),"subcategoria":st.column_config.SelectboxColumn("Subcategoria",options=subs_flat_r,width="large"),"origem":st.column_config.TextColumn("Origem",disabled=True,width="medium")}, num_rows="dynamic", use_container_width=True, hide_index=True, key="editor_regras")
            r1,r2,r3 = st.columns(3)
            with r1:
                if st.button("💾  Salvar", key="btn_salvar_r2", use_container_width=True):
                    salvar_regras_aprendidas(df_regras_edit.to_dict("records")); st.success("Salvo!"); st.rerun()
            with r2:
                st.download_button("⬇️  Exportar JSON", data=json.dumps(regras_atual, ensure_ascii=False, indent=2).encode("utf-8"), file_name="regras_caixinha.json", mime="application/json", use_container_width=True)
            with r3:
                if st.button("🗑️  Apagar todas", key="btn_del_r", use_container_width=True):
                    salvar_regras_aprendidas([]); st.warning("Apagadas."); st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# 7. SERVIÇOS & CONTATO
# ════════════════════════════════════════════════════════════════════════════
elif page == "servicos":
    st.markdown('<div class="page-title">Serviços & Contato</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">CRS Finance · BPO Financeiro · Parnaíba, Piauí</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    servicos = [
        ("Auditoria de Extrato","Cruzamento sistemático do extrato bancário com o sistema de gestão.","A partir de R$ 490/mês"),
        ("Contas a Pagar/Receber","Gestão completa do fluxo com conciliação diária e relatórios de inadimplência.","A partir de R$ 690/mês"),
        ("Conciliação Bancária","Conferência entre saldos bancários e registros do sistema.","A partir de R$ 390/mês"),
        ("Relatórios Gerenciais","DRE simplificado, fluxo de caixa e painel financeiro.","A partir de R$ 290/mês"),
    ]
    for i,(titulo,desc,preco) in enumerate(servicos):
        col = c1 if i%2==0 else c2
        col.markdown(f'<div class="svc-card" style="margin-bottom:12px;"><div class="svc-title">{titulo}</div><div class="svc-desc">{desc}</div><div class="svc-price">{preco}</div></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card" style="margin-top:1rem;">
        <div class="section-card-title">Entre em contato</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;"><div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">WhatsApp</div><div style="color:#94a3b8;">(86) 9 xxxx-xxxx</div></div>
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;"><div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">Instagram</div><div style="color:#94a3b8;">@crsfinance</div></div>
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;"><div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">LinkedIn</div><div style="color:#94a3b8;">Caio Rodrigues Silva</div></div>
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;"><div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">Localização</div><div style="color:#94a3b8;">Parnaíba · PI · Brasil</div></div>
        </div>
    </div>
    <div style="background:#1B2A4A;border-radius:12px;padding:1.5rem 2rem;border-top:2px solid #C9A84C;text-align:center;margin-top:1rem;">
        <div style="font-size:0.65rem;letter-spacing:.25em;color:#C9A84C;text-transform:uppercase;margin-bottom:8px;">CRS Finance</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-style:italic;color:#fff;">"Precisão que move o seu negócio."</div>
    </div>
    """, unsafe_allow_html=True)
