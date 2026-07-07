import streamlit as st
import pandas as pd
import numpy as np
import re
import io
import json
from datetime import datetime

# ── Persistent config store (module-level so @st.cache_resource survives re-runs) ──
@st.cache_resource
def _cfg_store():
    """Retorna dict mutável compartilhado entre sessões (persiste até restart do servidor)."""
    return {
        "plano":      {},    # {cat: [sub, ...]}
        "base_md":    [],    # [nome_str, ...]   — PF + PJ unificados
        "matriz":     [],    # [{"cf","cat","sub","tipo_es"}, ...]
        "mapa":       {},    # {alias: nome_md}  — dicionário manual
        "regras":     [],    # [{tipo, contato/palavra, mov, categoria, subcategoria}]
        "exportados": set(), # chaves já exportadas
    }

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

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #1B2A4A !important;
    border-right: 2px solid #C9A84C !important;
}
[data-testid="stSidebar"] * { color: #c8d0e0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Barra dourada topo sidebar ── */
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 3px;
    background: #C9A84C;
    margin-bottom: 0;
}

/* ── Main ── */
.main .block-container {
    background-color: #0f1923 !important;
    padding: 2rem 2.5rem !important;
    max-width: 1200px;
}

/* ── Logo ── */
.crs-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -2px;
    line-height: 1;
}
.crs-logo span { color: #C9A84C; }
.crs-sub {
    font-size: 0.65rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #8899BB;
    font-weight: 300;
    margin-top: 2px;
    margin-bottom: 1.5rem;
}

/* ── Navegação sidebar ── */
.stButton > button {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: #8899BB !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 9px 12px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: rgba(201,168,76,0.1) !important;
    color: #C9A84C !important;
}

/* ── Títulos de página ── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.5px;
    margin-bottom: 0.25rem;
}
.page-sub {
    font-size: 0.88rem;
    color: #8899BB;
    margin-bottom: 1.5rem;
}

/* ── Hero card ── */
.hero-card {
    background: #1B2A4A;
    border-radius: 14px;
    padding: 2rem;
    border-top: 3px solid #C9A84C;
    margin-bottom: 1.5rem;
}
.hero-brand {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: -2px;
    line-height: 1;
}
.hero-brand span { color: #C9A84C; }
.hero-tagline {
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #8899BB;
    margin-top: 4px;
}
.hero-slogan {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-style: italic;
    color: #C9A84C;
    background: rgba(201,168,76,0.08);
    border: 0.5px solid rgba(201,168,76,0.3);
    border-radius: 8px;
    padding: 10px 16px;
    display: inline-block;
    margin-top: 1.2rem;
}
.hero-name { font-size: 0.95rem; font-weight: 500; color: #fff; margin-top: 1.2rem; }
.hero-role { font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #C9A84C; }
.hero-city { font-size: 0.78rem; color: #556688; margin-top: 2px; }

/* ── Metric cards ── */
.metric-card {
    background: #1B2A4A;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    border-left: 3px solid #C9A84C;
}
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8899BB;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1;
}
.metric-value.green { color: #4ade80; }
.metric-value.red   { color: #f87171; }
.metric-value.amber { color: #C9A84C; }

/* ── Section card ── */
.section-card {
    background: #162236;
    border: 0.5px solid #253550;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.section-card-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #C9A84C;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    padding-bottom: 0.6rem;
    border-bottom: 0.5px solid #253550;
}

/* ── Upload zone ── */
.upload-zone {
    border: 1.5px dashed #253550;
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
    color: #556688;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}

/* ── Status badges ── */
.badge-ok   { background:#14532d; color:#86efac; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-err  { background:#450a0a; color:#fca5a5; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-warn { background:#422006; color:#fcd34d; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-info { background:#1e3a5f; color:#93c5fd; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }

/* ── Tabela e Data Editor ── */
.stDataFrame {
    border: 0.5px solid #253550 !important;
    border-radius: 10px !important;
    background: #162236 !important;
}

/* Data editor — células com tema escuro */
[data-testid="stDataFrameResizable"] {
    border: 0.5px solid #253550 !important;
    border-radius: 10px !important;
}
[data-testid="stDataFrameResizable"] [role="gridcell"] {
    color: #e2e8f0 !important;
}
[data-testid="stDataFrameResizable"] [role="columnheader"] {
    background: #1B2A4A !important;
    color: #C9A84C !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.05em !important;
}

/* Popup do SelectboxColumn — tema CLARO forçado */
[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 2px solid #1B2A4A !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
}
[data-baseweb="popover"] div,
[data-baseweb="popover"] ul,
[data-baseweb="popover"] li,
[data-baseweb="popover"] span,
[data-baseweb="popover"] p {
    background-color: #ffffff !important;
    color: #111827 !important;
}
[data-baseweb="popover"] [role="option"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    padding: 8px 14px !important;
    border-bottom: 0.5px solid #e5e7eb !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background-color: #dbeafe !important;
    color: #1B2A4A !important;
}
[data-baseweb="popover"] [aria-selected="true"],
[data-baseweb="popover"] [aria-selected="true"] * {
    background-color: #1B2A4A !important;
    color: #C9A84C !important;
    font-weight: 600 !important;
}
[data-baseweb="menu"] {
    background-color: #ffffff !important;
}
[data-baseweb="menu"] ul {
    background-color: #ffffff !important;
}
[data-baseweb="menu"] li,
[data-baseweb="menu"] li * {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-size: 13px !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li:hover * {
    background-color: #dbeafe !important;
    color: #1B2A4A !important;
}
[data-baseweb="popover"] input {
    background-color: #f9fafb !important;
    color: #111827 !important;
    border: 1.5px solid #1B2A4A !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input,
.stSelectbox > div > div {
    background: #162236 !important;
    border: 0.5px solid #253550 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
label { color: #8899BB !important; font-size: 0.82rem !important; }

/* ── Botão de ação ── */
.action-btn > button {
    background: #C9A84C !important;
    color: #1B2A4A !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.5rem !important;
}
.action-btn > button:hover { opacity: 0.88 !important; }

/* ── Serviços ── */
.svc-card {
    background: #1B2A4A;
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    border-top: 2px solid #C9A84C;
}
.svc-title { font-size: 0.92rem; font-weight: 600; color: #fff; margin-bottom: 5px; }
.svc-desc  { font-size: 0.82rem; color: #8899BB; line-height: 1.55; }
.svc-price { font-size: 0.82rem; font-weight: 600; color: #C9A84C; margin-top: 8px; }

/* ── Pipeline ── */
.pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1.2rem 0;
}
.pipe-step {
    flex: 1;
    text-align: center;
}
.pipe-num {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: #1B2A4A;
    border: 2px solid #C9A84C;
    color: #C9A84C;
    font-size: 0.85rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 6px;
}
.pipe-label { font-size: 0.72rem; color: #8899BB; }
.pipe-arrow { color: #C9A84C; font-size: 1rem; flex-shrink: 0; }

/* ── Divider ── */
hr { border-color: #253550 !important; margin: 1.5rem 0 !important; }

/* ── Hide Streamlit defaults ── */
#MainMenu, footer, .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "marca"


# ── Funções utilitárias ───────────────────────────────────────────────────────
def fmt_brl(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_numeric(series: pd.Series) -> pd.Series:
    """Converte coluna de valores para float, suportando formato BR (vírgula decimal)."""
    def to_float(v):
        if pd.isna(v):
            return np.nan
        s = str(v).strip()
        # Remove espaços e símbolo R$
        s = s.replace("R$", "").replace(" ", "").strip()
        # Formato BR: 1.234,56 → remove ponto de milhar, troca vírgula por ponto
        if "," in s and "." in s:
            # ex: 1.234,56
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            # ex: 1234,56
            s = s.replace(",", ".")
        # Remove caracteres não numéricos exceto ponto e sinal
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
    """Lê CSV, Excel ou OFX com detecção automática de encoding."""
    name = uploaded.name.lower()
    if name.endswith(".csv"):
        raw = uploaded.read()
        for enc in ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252"]:
            try:
                import io as _io
                return pd.read_csv(_io.BytesIO(raw), encoding=enc, sep=None, engine="python")
            except Exception:
                continue
        import io as _io
        return pd.read_csv(_io.BytesIO(raw), encoding="latin-1", sep=None, engine="python", on_bad_lines="skip")
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


def run_conciliacao(df_ext: pd.DataFrame, df_sis: pd.DataFrame,
                    col_val_ext: str, col_val_sis: str,
                    col_desc_ext: str, col_desc_sis: str,
                    col_data_ext: str, col_data_sis: str) -> pd.DataFrame:
    ext = df_ext[[col_data_ext, col_desc_ext, col_val_ext]].copy()
    sis = df_sis[[col_data_sis, col_desc_sis, col_val_sis]].copy()
    ext.columns = ["Data", "Descrição", "Valor_Extrato"]
    sis.columns = ["Data", "Descrição", "Valor_Sistema"]
    ext["Valor_Extrato"] = parse_numeric(ext["Valor_Extrato"])
    sis["Valor_Sistema"]  = parse_numeric(sis["Valor_Sistema"])
    ext["_key"] = ext["Valor_Extrato"].round(2).astype(str)
    sis["_key"] = sis["Valor_Sistema"].round(2).astype(str)

    merged = pd.merge(
        ext, sis, on="_key", how="outer", suffixes=("_ext", "_sis")
    ).drop(columns=["_key"])

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
                <div style="font-size:0.65rem;letter-spacing:.3em;color:#C9A84C;text-transform:uppercase;margin-bottom:8px;">
                    Identidade Profissional
                </div>
                <div class="hero-brand">C<span>R</span>S<br>Finance</div>
                <div class="hero-tagline">BPO · Gestão Financeira</div>
                <div class="hero-slogan">"Precisão que move o seu negócio."</div>
            </div>
            <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.2);border-radius:10px;padding:1rem 1.5rem;min-width:180px;">
                <div style="font-size:0.65rem;letter-spacing:.2em;color:#8899BB;text-transform:uppercase;margin-bottom:8px;">Especialidades</div>
                <div style="font-size:0.82rem;color:#C9A84C;line-height:2;">
                    ◆ Auditoria de Extrato<br>
                    ◆ Contas a Pagar/Receber<br>
                    ◆ Conciliação Bancária<br>
                    ◆ Relatórios Gerenciais
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

    col1, col2, col3, col4, col5 = st.columns(5)
    steps = [
        ("1", "Extrato\nBancário"),
        ("2", "Importação\nOFX/Excel"),
        ("3", "Cruzamento\ncom Sistema"),
        ("4", "Identifica\nDivergências"),
        ("5", "Relatório\nAuditado"),
    ]
    for col, (num, label) in zip([col1, col2, col3, col4, col5], steps):
        col.markdown(f"""
        <div style="text-align:center;">
            <div style="width:44px;height:44px;border-radius:50%;background:#1B2A4A;border:2px solid #C9A84C;
                        color:#C9A84C;font-size:1rem;font-weight:700;display:flex;align-items:center;
                        justify-content:center;margin:0 auto 8px;">{num}</div>
            <div style="font-size:0.75rem;color:#8899BB;line-height:1.4;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

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
# Foco: cada transação do extrato existe no sistema? (linha a linha)
# ════════════════════════════════════════════════════════════════════════════
elif page == "auditoria":
    st.markdown('<div class="page-title">Auditoria de Lançamentos</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-sub">Verifica se cada lançamento do extrato bancário está registrado no sistema de gestão
    — linha por linha, independente de período.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card" style="margin-bottom:1rem;">
        <div class="section-card-title">Como funciona</div>
        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;">
            <div style="flex:1;min-width:160px;font-size:0.82rem;color:#94a3b8;line-height:1.6;">
                <span style="color:#C9A84C;font-weight:600;">Entrada:</span> extrato bancário (OFX/CSV) 
                + exportação do seu sistema (Omie, Conta Azul, Nibo, Sienge, Excel próprio…)
            </div>
            <div style="flex:1;min-width:160px;font-size:0.82rem;color:#94a3b8;line-height:1.6;">
                <span style="color:#C9A84C;font-weight:600;">Processo:</span> cada lançamento do extrato 
                é buscado no sistema pelo valor + data
            </div>
            <div style="flex:1;min-width:160px;font-size:0.82rem;color:#94a3b8;line-height:1.6;">
                <span style="color:#C9A84C;font-weight:600;">Resultado:</span> lista com status individual 
                — conciliado, divergência, não lançado no sistema
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("**Extrato Bancário**")
        st.caption("OFX · CSV · Excel — exportado pelo banco")
        f_aud_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"],
                                     key="aud_ext2", label_visibility="collapsed")
    with col_u2:
        st.markdown("**Sistema de Gestão**")
        st.caption("CSV · Excel — exportado do Omie, Conta Azul, Nibo, Sienge ou Excel")
        f_aud_sis = st.file_uploader(" ", type=["csv","xlsx","xls"],
                                     key="aud_sis2", label_visibility="collapsed")

    if not f_aud_ext or not f_aud_sis:
        st.markdown("""
        <div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:.5rem;">🔎</div>
            <div style="color:#556688;font-size:0.85rem;">Carregue os dois arquivos para auditar os lançamentos</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Ver exemplo de resultado"):
            demo_ext = pd.DataFrame({
                "Data":      ["01/04/2025","03/04/2025","05/04/2025","07/04/2025","10/04/2025","12/04/2025","15/04/2025"],
                "Descrição": ["TEF Recebida - Alfa","Pagto Fornecedor","Tarifa Bancária","TEF - Beta","Pagto Aluguel","NF 0042","Folha"],
                "Valor":     [4800.00,-1250.00,-45.00,2300.00,-1800.00,3600.00,-5200.00],
            })
            demo_sis = pd.DataFrame({
                "Data":      ["01/04/2025","03/04/2025","05/04/2025","07/04/2025","10/04/2025","12/04/2025","17/04/2025"],
                "Descrição": ["Recebimento Alfa","Fornecedor","Tarifa","Recebimento Beta","Aluguel","NF 0042","Folha Abril"],
                "Valor":     [4800.00,-1250.00,-38.00,2300.00,-1800.00,3600.00,-5200.00],
            })
            demo_r = run_conciliacao(demo_ext, demo_sis, "Valor","Valor","Descrição","Descrição","Data","Data")
            st.dataframe(demo_r, use_container_width=True, hide_index=True)
        st.stop()

    try:
        df_aud_ext = load_file(f_aud_ext)
        df_aud_sis = load_file(f_aud_sis)
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
        st.stop()

    if df_aud_ext.empty or df_aud_sis.empty:
        st.warning("Um dos arquivos está vazio.")
        st.stop()

    # Aba Excel sistema
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
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Mapear colunas</div>', unsafe_allow_html=True)

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
        with st.spinner("Auditando lançamento por lançamento…"):
            result = run_conciliacao(df_aud_ext, df_aud_sis, ae_val, as_val, ae_desc, as_desc, ae_data, as_data)

        total  = len(result)
        ok     = (result["Status"] == "✅ Conciliado").sum()
        div    = (result["Status"] == "❌ Divergência").sum()
        only_e = (result["Status"] == "⚠️ Só no Extrato").sum()
        only_s = (result["Status"] == "ℹ️ Só no Sistema").sum()
        taxa   = round(ok / total * 100, 1) if total else 0

        st.markdown("---")
        m1,m2,m3,m4,m5,m6 = st.columns(6)
        for col,lbl,val,cls in [
            (m1,"Total lançamentos", str(total), ""),
            (m2,"Conciliados",       str(ok),    "green"),
            (m3,"Divergências",      str(div),   "red"),
            (m4,"Só no extrato",     str(only_e),"amber"),
            (m5,"Só no sistema",     str(only_s),"amber"),
            (m6,"Taxa conciliação",  f"{taxa}%", "green" if taxa>=95 else "amber"),
        ]:
            col.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{lbl}</div>
                <div class="metric-value {cls}">{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        filtro = st.selectbox("Filtrar por status",
            ["Todos","✅ Conciliado","❌ Divergência","⚠️ Só no Extrato","ℹ️ Só no Sistema"],
            key="aud_filter2")
        df_show = result if filtro=="Todos" else result[result["Status"]==filtro]

        for c in ["Valor_Extrato","Valor_Sistema","Diferença"]:
            if c in df_show.columns:
                df_show = df_show.copy()
                df_show[c] = df_show[c].apply(lambda v: fmt_brl(v) if not (isinstance(v,float) and np.isnan(v)) else "—")

        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.download_button("⬇️  Exportar Auditoria Excel",
            data=to_excel_bytes(result),
            file_name=f"auditoria_lancamentos_{datetime.today().strftime('%d%m%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")




# ════════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════════
# 3. CONCILIAÇÃO DE SALDO — 3 modos unificados
# Simples | Multi-Conta (CC + Aplicação) | Consolidado
# ════════════════════════════════════════════════════════════════════════════
elif page == "conciliacao":
    st.markdown('<div class="page-title">Conciliação de Saldo</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Escolha o modo conforme a estrutura de contas do cliente.</div>', unsafe_allow_html=True)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def get_clientes_salvos():
        return json.loads(st.session_state.get("_clientes_db","{}"))

    def carregar_config_cliente(nome):
        db = get_clientes_salvos()
        return db.get(nome, {})

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

    # ── Seletor de cliente salvo ───────────────────────────────────────────────
    clientes_db = get_clientes_salvos()
    nomes_clientes = list(clientes_db.keys())

    if nomes_clientes:
        col_cli, col_info = st.columns([2,3])
        with col_cli:
            cliente_sel = st.selectbox("Carregar configuração de cliente",
                ["— Sem cliente salvo —"] + nomes_clientes, key="conc_cliente_sel")
        with col_info:
            if cliente_sel != "— Sem cliente salvo —":
                cfg = carregar_config_cliente(cliente_sel)
                modo_default = cfg.get("modo_conc", "Simples")
                st.markdown(f"""
                <div style="background:#1B2A4A;border-radius:8px;padding:8px 14px;margin-top:20px;font-size:0.8rem;">
                    <span style="color:#C9A84C;font-weight:600;">{cliente_sel}</span>
                    <span style="color:#8899BB;margin-left:8px;">Modo: {modo_default}</span>
                    <span style="color:#8899BB;margin-left:8px;">Sistema: {cfg.get('sistema','—')}</span>
                </div>""", unsafe_allow_html=True)
            else:
                modo_default = "Simples"
    else:
        cliente_sel = "— Sem cliente salvo —"
        modo_default = "Simples"
        cfg = {}

    st.markdown("---")

    # ── Seletor de modo ───────────────────────────────────────────────────────
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Modo de conciliação</div>', unsafe_allow_html=True)

    m1,m2,m3 = st.columns(3)
    for col, titulo, desc, tag, key_val in [
        (m1, "Simples",
         "1 extrato + 1 sistema. Filtra transferências por palavra-chave. Para clientes sem conta de aplicação.",
         "1 OFX + 1 CSV", "Simples"),
        (m2, "Multi-Conta",
         "1 extrato + 2 sistemas (CC + Aplicação). O sistema já controla tudo — sem filtrar transferências.",
         "1 OFX + 2 CSV", "Multi-Conta"),
        (m3, "Consolidado",
         "2 extratos do banco (CC + Aplicação) + 1 sistema. Neutraliza internos automaticamente.",
         "2 OFX + 1 CSV", "Consolidado"),
    ]:
        ativo = (modo_default == key_val)
        borda = "2px solid #C9A84C" if ativo else "0.5px solid #253550"
        col.markdown(f"""
        <div style="background:#162236;border:{borda};border-radius:10px;padding:1rem;height:140px;">
            <div style="font-size:0.88rem;font-weight:600;color:{'#C9A84C' if ativo else '#f1f5f9'};margin-bottom:6px;">{titulo}</div>
            <div style="font-size:0.75rem;color:#8899BB;line-height:1.5;margin-bottom:8px;">{desc}</div>
            <span style="font-size:0.7rem;background:#253550;color:#8899BB;padding:2px 8px;border-radius:4px;">{tag}</span>
        </div>""", unsafe_allow_html=True)

    modo_idx = ["Simples","Multi-Conta","Consolidado"].index(modo_default)
    modo = st.radio(" ", ["Simples","Multi-Conta (CC + Aplicação)","Consolidado"],
                    index=modo_idx, horizontal=True, key="conc_modo", label_visibility="collapsed")
    modo_key = modo.split(" ")[0]  # "Simples", "Multi-Conta", "Consolidado"

    st.markdown("---")

    # ── Uploads dinâmicos por modo ────────────────────────────────────────────
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Carregar arquivos</div>', unsafe_allow_html=True)

    f_aplic_sis = None
    f_aplic_ofx = None

    if modo_key == "Simples":
        u1,u2 = st.columns(2)
        with u1:
            st.markdown("**Extrato Bancário**")
            st.caption("OFX · CSV · Excel — exportado pelo banco")
            f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Sistema de Gestão**")
            st.caption("CSV · Excel — qualquer sistema")
            f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")

    elif modo_key == "Multi-Conta":
        u1,u2,u3 = st.columns(3)
        with u1:
            st.markdown("**Extrato Bancário (OFX)**")
            st.caption("Extrato completo da conta corrente")
            f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Sistema — Conta Corrente (CSV)**")
            st.caption("Exportação da conta principal")
            f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")
        with u3:
            st.markdown("**Sistema — Conta Aplicação (CSV)**")
            st.caption("Exportação da conta de aplicação/reserva")
            f_aplic_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_aplic_sis", label_visibility="collapsed")
        st.markdown("""
        <div style="background:#162236;border-left:3px solid #C9A84C;border-radius:0 8px 8px 0;padding:8px 14px;font-size:0.8rem;color:#8899BB;margin-top:8px;">
            ℹ️ No Modo Multi-Conta o sistema já registra as transferências entre CC e Aplicação — 
            <strong style="color:#C9A84C;">não é necessário filtrar nada</strong>. O saldo bate diretamente.
        </div>""", unsafe_allow_html=True)

    else:  # Consolidado
        u1,u2,u3 = st.columns(3)
        with u1:
            st.markdown("**Extrato CC (OFX)**")
            st.caption("Extrato da conta corrente principal")
            f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Extrato Aplicação (XLS/CSV)**")
            st.caption("Formato XLS do Itaú ou CSV")
            f_aplic_ofx = st.file_uploader(" ", type=["xls","xlsx","csv","txt"], key="conc_aplic_ofx", label_visibility="collapsed")
        with u3:
            st.markdown("**Sistema de Gestão (CSV)**")
            st.caption("Exportação única do sistema")
            f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")

    # Verifica uploads obrigatórios
    arquivos_ok = f_c_ext and f_c_sis
    if modo_key == "Multi-Conta": arquivos_ok = arquivos_ok and f_aplic_sis
    if modo_key == "Consolidado": arquivos_ok = arquivos_ok and f_aplic_ofx

    if not arquivos_ok:
        msgs = {"Simples":"extrato OFX e o sistema","Multi-Conta":"extrato OFX, sistema CC e sistema Aplicação","Consolidado":"extrato CC, extrato Aplicação e o sistema"}
        st.markdown(f"""
        <div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:.5rem;">⚖️</div>
            <div style="color:#556688;font-size:0.85rem;">Carregue: {msgs[modo_key]}</div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Carrega dados ─────────────────────────────────────────────────────────
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
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-bottom:4px;">✓ Conta Aplicação: {len(df_aplic_sis_raw)} lançamentos</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Erro ao ler conta aplicação: {e}")

    df_aplic_ofx_raw = pd.DataFrame()
    if modo_key == "Consolidado" and f_aplic_ofx:
        try:
            df_aplic_ofx_raw = parse_aplic_xls(f_aplic_ofx)
            if not df_aplic_ofx_raw.empty:
                st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-bottom:4px;">✓ Extrato Aplicação: {len(df_aplic_ofx_raw)} movimentações</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Erro ao ler extrato aplicação: {e}")

    # ── Mapeamento de colunas ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Mapear colunas</div>', unsafe_allow_html=True)

    cols_ext = df_ext_raw.columns.tolist()
    cols_sis = df_sis_raw.columns.tolist()

    # Usa config salva do cliente se disponível
    cfg_data_e = cfg.get("col_data_e","")
    cfg_val_e  = cfg.get("col_val_e","")
    cfg_data_s = cfg.get("col_data_s","")
    cfg_val_s  = cfg.get("col_val_s","")
    idx_de = cols_ext.index(cfg_data_e) if cfg_data_e in cols_ext else 0
    idx_ve = cols_ext.index(cfg_val_e)  if cfg_val_e  in cols_ext else min(2,len(cols_ext)-1)
    idx_ds = cols_sis.index(cfg_data_s) if cfg_data_s in cols_sis else 0
    idx_vs = cols_sis.index(cfg_val_s)  if cfg_val_s  in cols_sis else min(2,len(cols_sis)-1)

    c1,c2,c3,c4 = st.columns(4)
    with c1: col_data_e = st.selectbox("Data (extrato)", cols_ext, index=idx_de, key="cce_d2")
    with c2: col_val_e  = st.selectbox("Valor (extrato)", cols_ext, index=idx_ve, key="cce_v2")
    with c3: col_data_s = st.selectbox("Data (sistema)", cols_sis, index=idx_ds, key="ccs_d2")
    with c4: col_val_s  = st.selectbox("Valor (sistema)", cols_sis, index=idx_vs, key="ccs_v2")

    col_val_aplic_sis = None
    col_data_aplic_sis = None
    if modo_key == "Multi-Conta" and not df_aplic_sis_raw.empty:
        cols_ap = df_aplic_sis_raw.columns.tolist()
        ca1,ca2 = st.columns(2)
        with ca1: col_data_aplic_sis = st.selectbox("Data (conta aplicação)", cols_ap, key="cap_d")
        with ca2: col_val_aplic_sis  = st.selectbox("Valor (conta aplicação)", cols_ap, index=min(2,len(cols_ap)-1), key="cap_v")

    # ── Filtros — só no modo Simples ──────────────────────────────────────────
    if modo_key == "Simples":
        st.markdown("---")
        st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.5rem;">Filtrar transferências internas</div>', unsafe_allow_html=True)

        palavras_padrao = ["APLIC AUT","RES APLIC","APL APLIC","RENDIMENTOS REND PAGO","TRANSF PROPRIA","TED PROPRIA"]
        fe1,fe2 = st.columns([1,2])
        with fe1:
            usar_filtro_ext = st.checkbox("Excluir do extrato", value=True, key="chk_ext_filtro")
        with fe2:
            if usar_filtro_ext:
                desc_cols_ext = [c for c in cols_ext if any(x in c.lower() for x in ["desc","memo","hist","nome","name"])]
                col_desc_filtro = st.selectbox("Coluna de descrição", cols_ext,
                    index=cols_ext.index(desc_cols_ext[0]) if desc_cols_ext else min(1,len(cols_ext)-1), key="cce_desc_f")
                palavras_excluir = st.multiselect("Palavras-chave", options=palavras_padrao, default=palavras_padrao, key="ext_palavras")
        if usar_filtro_ext and palavras_excluir:
            mask = df_ext_raw[col_desc_filtro].str.upper().str.contains("|".join([re.escape(p) for p in palavras_excluir]), na=False)
            n_antes = len(df_ext_raw)
            df_ext_raw = df_ext_raw[~mask].copy()
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;">✓ {n_antes-len(df_ext_raw)} excluídos · {len(df_ext_raw)} restantes</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#162236;border-left:3px solid #C9A84C;border-radius:0 8px 8px 0;
                    padding:8px 14px;font-size:0.8rem;color:#8899BB;margin-bottom:10px;">
            ⚠️ <strong style="color:#C9A84C;">Atenção:</strong> remova <u>somente</u> transferências internas
            entre contas do próprio banco (ex: CC ↔ Aplicação).
            Transferências da Caixinha para o Itaú <strong>devem ser mantidas</strong> — elas fazem parte do saldo real.
        </div>""", unsafe_allow_html=True)

        ft1, ft2, ft3 = st.columns(3)
        with ft1:
            # Coluna Tipo
            cols_sis_op = ["— Nenhum —"] + cols_sis
            col_tipo_sis = st.selectbox("Coluna Tipo (sistema)", cols_sis_op, key="ccs_tipo")
        with ft2:
            # Coluna Conta transferência — para filtrar por destino
            col_conta_transf_op = ["— Nenhum —"] + cols_sis
            col_conta_transf = st.selectbox("Coluna Conta destino", col_conta_transf_op,
                index=next((i+1 for i,c in enumerate(cols_sis) if "conta transfer" in c.lower() or "destino" in c.lower()), 0),
                key="ccs_conta_transf",
                help="Coluna que indica para qual conta foi a transferência. Ex: 'Conta transferência' no Meu Dinheiro.")
        with ft3:
            palavras_conta_aplic = st.multiselect(
                "Filtrar por conta destino (contém)",
                options=["Aplicação","Aplic","Auto Mais","Poupança","CDB","LCI","LCA","Reserva"],
                default=["Aplicação","Aplic","Auto Mais"],
                key="ccs_conta_palavras",
                help="Só transferências cujo destino contenha essas palavras serão removidas.")

        # Aplica filtro CIRÚRGICO: só remove quando é Transferência E conta destino contém palavras de aplicação
        n_antes = len(df_sis_raw)
        if col_tipo_sis != "— Nenhum —" and col_conta_transf != "— Nenhum —" and palavras_conta_aplic:
            mask_tipo = df_sis_raw[col_tipo_sis].astype(str).str.lower() == "transferência"
            mask_dest = df_sis_raw[col_conta_transf].astype(str).str.contains(
                "|".join([re.escape(p) for p in palavras_conta_aplic]), case=False, na=False)
            mask_remover = mask_tipo & mask_dest
            df_sis_raw = df_sis_raw[~mask_remover].copy()
            n_removidos = n_antes - len(df_sis_raw)
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-top:4px;">✓ {n_removidos} transferências CC↔Aplicação removidas · {len(df_sis_raw)} lançamentos restantes</div>', unsafe_allow_html=True)
        elif col_tipo_sis == "— Nenhum —":
            st.markdown('<div style="font-size:0.8rem;color:#8899BB;margin-top:4px;">Nenhuma coluna de tipo selecionada — usando todos os lançamentos.</div>', unsafe_allow_html=True)

    # ── Tipo análise + período ────────────────────────────────────────────────
    st.markdown("---")
    ca1,ca2 = st.columns([2,1])
    with ca1:
        tipo_analise = st.selectbox("Tipo de análise", [
            "Comparação de Valores por Dia",
            "Comparação de Movimentações por Dia",
            "Comparação por Chave Forte (Data+Valor)",
        ], key="conc_tipo")
    with ca2:
        data_range = st.text_input("Filtrar período (opcional)", placeholder="DD/MM/AAAA – DD/MM/AAAA", key="conc_range")

    # ── Salvar config do cliente ───────────────────────────────────────────────
    with st.expander("💾  Salvar configuração deste cliente"):
        nome_novo = st.text_input("Nome do cliente", value=cliente_sel if cliente_sel != "— Sem cliente salvo —" else "", key="conc_save_nome")
        sistema_novo = st.text_input("Sistema usado", value=cfg.get("sistema",""), placeholder="Ex: Meu Dinheiro, Omie, Conta Azul", key="conc_save_sistema")
        if st.button("Salvar configuração", key="btn_save_cfg"):
            if nome_novo.strip():
                db = get_clientes_salvos()
                db[nome_novo.strip()] = {
                    "modo_conc": modo_key,
                    "sistema": sistema_novo,
                    "col_data_e": col_data_e,
                    "col_val_e":  col_val_e,
                    "col_data_s": col_data_s,
                    "col_val_s":  col_val_s,
                }
                st.session_state["_clientes_db"] = json.dumps(db, ensure_ascii=False)
                st.success(f"✅ Configuração de '{nome_novo.strip()}' salva!")
            else:
                st.warning("Digite o nome do cliente.")

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.button("⚖️  Conciliar Saldo", key="btn_conc"):
        st.stop()

    # ── Processa ──────────────────────────────────────────────────────────────
    try:
        df_ext = df_ext_raw.copy()
        df_sis = df_sis_raw.copy()
        df_ext[col_val_e] = parse_numeric(df_ext[col_val_e])
        df_sis[col_val_s] = parse_numeric(df_sis[col_val_s])
        df_ext["_data"] = pd.to_datetime(df_ext[col_data_e], dayfirst=True, errors="coerce")
        df_sis["_data"] = pd.to_datetime(df_sis[col_data_s], dayfirst=True, errors="coerce")

        # Multi-Conta: soma CC + Aplicação do sistema
        saldo_aplic_info = None
        if modo_key == "Multi-Conta" and not df_aplic_sis_raw.empty and col_val_aplic_sis:
            df_ap = df_aplic_sis_raw.copy()
            df_ap[col_val_aplic_sis] = parse_numeric(df_ap[col_val_aplic_sis])
            df_ap["_data"] = pd.to_datetime(df_ap[col_data_aplic_sis], dayfirst=True, errors="coerce")
            saldo_aplic_info = df_ap[col_val_aplic_sis].sum()
            # Adiciona aplicação ao sistema para comparar com OFX
            df_ap_add = df_ap[["_data", col_val_aplic_sis]].rename(columns={col_val_aplic_sis: col_val_s})
            df_ap_add[col_data_s] = df_ap_add["_data"]
            df_sis = pd.concat([df_sis, df_ap_add], ignore_index=True)

        # Consolidado: adiciona OFX da aplicação ao extrato CC
        if modo_key == "Consolidado" and not df_aplic_ofx_raw.empty:
            df_ap_ofx = df_aplic_ofx_raw[["_data","Valor"]].copy()
            df_ap_ofx.columns = ["_data", col_val_e]
            df_ap_ofx[col_data_e] = df_ap_ofx["_data"]
            df_ext = pd.concat([df_ext, df_ap_ofx], ignore_index=True)

        dt_min = df_ext["_data"].min()
        dt_max = df_ext["_data"].max()
        if data_range and "–" in data_range:
            try:
                partes = [p.strip() for p in data_range.split("–")]
                dt_min = pd.to_datetime(partes[0], dayfirst=True)
                dt_max = pd.to_datetime(partes[1], dayfirst=True)
            except Exception: pass

        df_ext_f = df_ext[(df_ext["_data"]>=dt_min)&(df_ext["_data"]<=dt_max)].copy()
        df_sis_f = df_sis[(df_sis["_data"]>=dt_min)&(df_sis["_data"]<=dt_max)].copy()

        saldo_banco = df_ext_f[col_val_e].sum()
        saldo_erp   = df_sis_f[col_val_s].sum()
        diferenca   = saldo_banco - saldo_erp

        periodo_txt = f"{dt_min.strftime('%d/%m/%Y')} a {dt_max.strftime('%d/%m/%Y')}"
        modo_label  = {"Simples":"Modo Simples","Multi-Conta":"Modo Multi-Conta","Consolidado":"Modo Consolidado"}[modo_key]
        st.markdown("---")
        st.markdown(f'<div style="font-size:0.85rem;color:#8899BB;margin-bottom:1rem;">Período: <strong style="color:#C9A84C;">{periodo_txt}</strong> &nbsp;·&nbsp; <span style="color:#93c5fd;">{modo_label}</span></div>', unsafe_allow_html=True)

        # Métricas
        if modo_key == "Multi-Conta" and saldo_aplic_info is not None:
            m1,m2,m3,m4,m5 = st.columns(5)
            metricas = [
                (m1,"Saldo Banco (OFX)",   saldo_banco,       "OFX"),
                (m2,"Sistema CC",          df_sis_raw[col_val_s].apply(lambda v: parse_numeric(pd.Series([v])).iloc[0]).sum(), "CC"),
                (m3,"Sistema Aplicação",   saldo_aplic_info,  "APLIC"),
                (m4,"Sistema Total",       saldo_erp,         "ERP"),
                (m5,"Diferença",           diferenca,         "BRL"),
            ]
        else:
            m1,m2,m3 = st.columns(3)
            metricas = [
                (m1,"Saldo do Período no Banco",   saldo_banco,"OFX"),
                (m2,"Saldo do Período no Sistema", saldo_erp,  "ERP"),
                (m3,"Diferença",                   diferenca,  "BRL"),
            ]

        for col,lbl,val,origem in metricas:
            neg = val < 0 if lbl != "Diferença" else val != 0
            cor_val = "#f87171" if neg else "#4ade80"
            cor_brd = "#f87171" if (lbl=="Diferença" and diferenca!=0) else "#C9A84C"
            col.markdown(f"""
            <div style="background:#1B2A4A;border-radius:10px;padding:0.9rem 1rem;border-left:3px solid {cor_brd};margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
                    <span style="font-size:0.65rem;color:#8899BB;font-weight:600;letter-spacing:.05em;text-transform:uppercase;">{lbl}</span>
                    <span style="font-size:0.6rem;background:#253550;color:#8899BB;padding:1px 6px;border-radius:4px;">{origem}</span>
                </div>
                <div style="font-size:1.2rem;font-weight:700;color:{cor_val};">{fmt_brl(val)}</div>
            </div>""", unsafe_allow_html=True)

        # Info saldo preso na aplicação
        if modo_key == "Multi-Conta" and saldo_aplic_info is not None and abs(diferenca) < 0.05:
            st.markdown(f"""
            <div style="background:#162236;border-left:3px solid #4ade80;border-radius:0 8px 8px 0;padding:10px 14px;font-size:0.82rem;margin-top:4px;">
                ✅ <strong style="color:#4ade80;">Conciliação perfeita!</strong>
                Saldo em reserva na aplicação: <strong style="color:#C9A84C;">{fmt_brl(saldo_aplic_info)}</strong>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.8rem;color:#8899BB;margin-bottom:.75rem;">Análise: <strong style="color:#C9A84C;">{tipo_analise}</strong></div>', unsafe_allow_html=True)

        # Tabela de resultado
        if tipo_analise == "Comparação de Valores por Dia":
            grp_e = df_ext_f.groupby("_data")[col_val_e].sum().reset_index()
            grp_s = df_sis_f.groupby("_data")[col_val_s].sum().reset_index()
            grp_e.columns=["Data","Banco"]; grp_s.columns=["Data","Sistema"]
            result = pd.merge(grp_e,grp_s,on="Data",how="outer").fillna(0)
            result["Diferença"] = (result["Banco"]-result["Sistema"]).round(2)
            result["Status"] = result["Diferença"].apply(lambda v: "✅ OK" if abs(v)<0.01 else "❌ DIFF")
            result["Data"] = result["Data"].dt.strftime("%d/%m/%Y")
            for c in ["Banco","Sistema","Diferença"]:
                result[c] = result[c].apply(fmt_brl)
        elif tipo_analise == "Comparação de Movimentações por Dia":
            grp_e = df_ext_f.groupby("_data")[col_val_e].count().reset_index()
            grp_s = df_sis_f.groupby("_data")[col_val_s].count().reset_index()
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
            st.markdown("<br>",unsafe_allow_html=True)
            rows=[]
            for _,r in df_ext_f.iterrows():
                rows.append({"Data":r["_data"].strftime("%d/%m/%Y"),"Valor Banco":fmt_brl(r[col_val_e]),"Valor Sistema":"—","Status":"✅ Conciliado" if r["_chave"] in cs else "⚠️ Só no Banco"})
            for _,r in df_sis_f.iterrows():
                if r["_chave"] not in cb:
                    rows.append({"Data":r["_data"].strftime("%d/%m/%Y"),"Valor Banco":"—","Valor Sistema":fmt_brl(r[col_val_s]),"Status":"ℹ️ Só no Sistema"})
            result = pd.DataFrame(rows)

        st.dataframe(result, use_container_width=True, hide_index=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.download_button("⬇️  Baixar Relatório",
            data=to_excel_bytes(result),
            file_name=f"conciliacao_{modo_key.lower()}_{datetime.today().strftime('%d%m%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Erro ao processar: {e}")


# ════════════════════════════════════════════════════════════════════════════
# 3B. GESTÃO DE CLIENTES
# ════════════════════════════════════════════════════════════════════════════
elif page == "clientes":
    st.markdown('<div class="page-title">Gestão de Clientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Cadastre clientes, salve configurações de conciliação e evite reconfigurar a cada uso.</div>', unsafe_allow_html=True)

    def get_db():
        return json.loads(st.session_state.get("_clientes_db","{}"))
    def set_db(db):
        st.session_state["_clientes_db"] = json.dumps(db, ensure_ascii=False)

    db = get_db()
    tabs = st.tabs(["👥  Clientes cadastrados","➕  Novo cliente","✏️  Editar / Excluir"])

    # ── Tab: Listar ────────────────────────────────────────────────────────────
    with tabs[0]:
        if not db:
            st.info("Nenhum cliente cadastrado ainda. Use a aba 'Novo cliente' para adicionar.")
        else:
            st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin-bottom:1rem;">{len(db)} cliente(s) cadastrado(s)</div>', unsafe_allow_html=True)
            for nome, cfg in db.items():
                with st.expander(f"**{nome}** — {cfg.get('sistema','—')} · Modo {cfg.get('modo_conc','—')}"):
                    c1,c2,c3,c4 = st.columns(4)
                    for col,lbl,val in [
                        (c1,"Sistema",       cfg.get("sistema","—")),
                        (c2,"Modo Conc.",    cfg.get("modo_conc","—")),
                        (c3,"Col. Data",     cfg.get("col_data_s","—")),
                        (c4,"Col. Valor",    cfg.get("col_val_s","—")),
                    ]:
                        col.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{lbl}</div>
                            <div class="metric-value" style="font-size:0.9rem;">{val}</div>
                        </div>""", unsafe_allow_html=True)
                    if cfg.get("observacoes"):
                        st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin-top:8px;">📝 {cfg["observacoes"]}</div>', unsafe_allow_html=True)

    # ── Tab: Novo cliente ──────────────────────────────────────────────────────
    with tabs[1]:
        n1,n2 = st.columns(2)
        with n1:
            novo_nome    = st.text_input("Nome do cliente *", placeholder="Ex: Clínica Kids Pediatria", key="nc_nome")
            novo_sistema = st.text_input("Sistema de gestão *", placeholder="Ex: Meu Dinheiro Web, Omie, Conta Azul", key="nc_sistema")
            novo_modo    = st.selectbox("Modo de conciliação padrão", ["Simples","Multi-Conta","Consolidado"], key="nc_modo")
        with n2:
            novo_col_data_e = st.text_input("Coluna Data (extrato)", placeholder="Ex: Data", key="nc_de")
            novo_col_val_e  = st.text_input("Coluna Valor (extrato)", placeholder="Ex: Valor", key="nc_ve")
            novo_col_data_s = st.text_input("Coluna Data (sistema)",  placeholder="Ex: Data efetiva", key="nc_ds")
            novo_col_val_s  = st.text_input("Coluna Valor (sistema)", placeholder="Ex: Valor efetivo", key="nc_vs")

        novo_obs = st.text_area("Observações", placeholder="Ex: Filtrar transferências Caixinha, conta Aplic Aut Mais...", key="nc_obs", height=80)

        if st.button("➕  Cadastrar cliente", key="btn_add_cliente", use_container_width=False):
            if not novo_nome.strip():
                st.warning("Nome do cliente é obrigatório.")
            elif novo_nome.strip() in db:
                st.warning(f"Cliente '{novo_nome.strip()}' já existe. Use a aba Editar para atualizar.")
            else:
                db[novo_nome.strip()] = {
                    "sistema":     novo_sistema,
                    "modo_conc":   novo_modo,
                    "col_data_e":  novo_col_data_e,
                    "col_val_e":   novo_col_val_e,
                    "col_data_s":  novo_col_data_s,
                    "col_val_s":   novo_col_val_s,
                    "observacoes": novo_obs,
                }
                set_db(db)
                st.success(f"✅ Cliente '{novo_nome.strip()}' cadastrado!")
                st.rerun()

    # ── Tab: Editar / Excluir ─────────────────────────────────────────────────
    with tabs[2]:
        if not db:
            st.info("Nenhum cliente cadastrado ainda.")
        else:
            cliente_ed = st.selectbox("Selecione o cliente", list(db.keys()), key="ed_sel")
            cfg_ed = db[cliente_ed]

            e1,e2 = st.columns(2)
            with e1:
                ed_sistema  = st.text_input("Sistema",    value=cfg_ed.get("sistema",""),    key="ed_sis")
                ed_modo     = st.selectbox("Modo", ["Simples","Multi-Conta","Consolidado"],
                                          index=["Simples","Multi-Conta","Consolidado"].index(cfg_ed.get("modo_conc","Simples")), key="ed_modo")
                ed_col_de   = st.text_input("Col. Data extrato",   value=cfg_ed.get("col_data_e",""), key="ed_de")
                ed_col_ve   = st.text_input("Col. Valor extrato",  value=cfg_ed.get("col_val_e",""),  key="ed_ve")
            with e2:
                ed_col_ds   = st.text_input("Col. Data sistema",   value=cfg_ed.get("col_data_s",""), key="ed_ds")
                ed_col_vs   = st.text_input("Col. Valor sistema",  value=cfg_ed.get("col_val_s",""),  key="ed_vs")
                ed_obs      = st.text_area("Observações", value=cfg_ed.get("observacoes",""),         key="ed_obs", height=100)

            bc1,bc2 = st.columns(2)
            with bc1:
                if st.button("💾  Salvar alterações", key="btn_ed_save", use_container_width=True):
                    db[cliente_ed] = {
                        "sistema":     ed_sistema,
                        "modo_conc":   ed_modo,
                        "col_data_e":  ed_col_de,
                        "col_val_e":   ed_col_ve,
                        "col_data_s":  ed_col_ds,
                        "col_val_s":   ed_col_vs,
                        "observacoes": ed_obs,
                    }
                    set_db(db)
                    st.success("✅ Alterações salvas!")
                    st.rerun()
            with bc2:
                confirmar_del = st.checkbox(f"Confirmo exclusão de '{cliente_ed}'", key="confirm_del_cli")
                if st.button("🗑️  Excluir cliente", key="btn_del_cli", use_container_width=True):
                    if confirmar_del:
                        del db[cliente_ed]
                        set_db(db)
                        st.success(f"Cliente '{cliente_ed}' excluído.")
                        st.rerun()
                    else:
                        st.warning("Marque a confirmação para excluir.")

            st.markdown("---")
            col_exp, _ = st.columns([1,2])
            with col_exp:
                st.download_button("⬇️  Exportar cadastro JSON",
                    data=json.dumps(db, ensure_ascii=False, indent=2).encode("utf-8"),
                    file_name="clientes_crs.json", mime="application/json",
                    use_container_width=True)


elif page == "conversor":
    st.markdown('<div class="page-title">Conversor OFX → Excel</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Converta extratos bancários OFX em planilha Excel estruturada</div>', unsafe_allow_html=True)

    f_ofx = st.file_uploader("Selecione o arquivo OFX / OFC", type=["ofx","ofc","txt"], key="conv_ofx")

    if f_ofx:
        content = f_ofx.read().decode("utf-8", errors="replace")
        df_ofx = parse_ofx(content)

        if df_ofx.empty:
            st.warning("Nenhuma transação encontrada. Verifique se o arquivo é um OFX/SGML válido.")
        else:
            total_txn     = len(df_ofx)
            total_cred    = df_ofx[df_ofx["Valor"] > 0]["Valor"].sum()
            total_deb     = df_ofx[df_ofx["Valor"] < 0]["Valor"].sum()
            saldo         = total_cred + total_deb

            m1, m2, m3, m4 = st.columns(4)
            for col, lbl, val, cls in [
                (m1, "Transações",    str(total_txn),       ""),
                (m2, "Total créditos", fmt_brl(total_cred), "green"),
                (m3, "Total débitos",  fmt_brl(abs(total_deb)), "red"),
                (m4, "Saldo",          fmt_brl(saldo),      "green" if saldo >= 0 else "red"),
            ]:
                col.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{lbl}</div>
                    <div class="metric-value {cls}" style="font-size:1.1rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns([1, 2])
            with c1:
                tipo_opts = ["Todos"] + sorted(df_ofx["Valor"].apply(lambda v: "Crédito" if v > 0 else "Débito").unique().tolist())
                tipo_sel = st.selectbox("Tipo", tipo_opts)
            with c2:
                busca = st.text_input("Buscar descrição", placeholder="ex: pagamento, tarifa…")

            df_show = df_ofx.copy()
            if tipo_sel == "Crédito":
                df_show = df_show[df_show["Valor"] > 0]
            elif tipo_sel == "Débito":
                df_show = df_show[df_show["Valor"] < 0]
            if busca:
                df_show = df_show[df_show["Descrição"].str.contains(busca, case=False, na=False)]

            st.dataframe(df_show, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️  Baixar como Excel",
                data=to_excel_bytes(df_show),
                file_name=f"extrato_{f_ofx.name.split('.')[0]}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.markdown("""
        <div class="section-card" style="text-align:center;padding:2.5rem;">
            <div style="font-size:2rem;margin-bottom:.75rem;">📄</div>
            <div style="color:#556688;font-size:0.88rem;">Arraste um arquivo .ofx aqui</div>
        </div>
        """, unsafe_allow_html=True)




# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# 6. CLASSIFICADOR CAIXINHA — v2 · configuração persistente · fluxo direto
# ════════════════════════════════════════════════════════════════════════════
elif page == "classificador":
    st.markdown('<div class="page-title">Classificador Caixinha</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Processa dados brutos da caixinha e exporta no padrão do Meu Dinheiro Web.</div>', unsafe_allow_html=True)

    # ── Configuração persistente (módulo level — @st.cache_resource) ───────────
    cfg = _cfg_store()

    PLANO_PADRAO = {"2.1 IMPOSTOS E TAXAS":["2.101 - Simples Nacional (DAS)","2.102 - Parcelamentos de Impostos"],"2.2 DEDUCOES DE RECEITAS":["2.201 - Devolucao de vendas/Reembolso","2.202 - Descontos ","2.203 - Desembolso - Nota Fiscal","2.204 - Cancelamento/Glosas de Convenios"],"2.3 - CUSTO DIRETO COM PESSOAL (MOD)":[],"2.4 - CUSTOS DIRETOS COM INSUMOS (MAT)":["2.401 - Teste/Vacinas para Revenda","2.402 - Material de Consumo Clinico","2.403 - Material de Protecao (EPIs)"],"20 - SAIDAS OPERACIONAIS DE CAIXA - REPASSE (DFC)":["20.01 - Repasse Caixa - Medicos (% producao)","20.02 - Repasse Caixa - Terapeutas (% producao)","20.03 - Repasse Caixa - Medicos (valor fixo)","20.04 - Repasse Caixa - Terapeutas (valor fixo)"],"3.1 DESPESAS ADMINISTRATIVAS":["3.301 - Agua e Esgoto","3.302 - IPTU","3.303 - Aluguel","3.304 - Assessoria Financeira (BPO)","3.305 - Consultoria","3.306 - Cartorio","3.307 - Energia Eletrica","3.308 - Material de Escritorio","3.309 - Confraternizacao/Coffee break","3.310 - Material de Copa e Cozinha","3.311 - Material de Informatica","3.312 - Material de Limpeza","3.313 - Seguranca e Monitoramento","3.314 - Contabilidade","3.315 - Telefone e Internet","3.316 - Aluguel de Maquininha - Adquirente de Cartao","3.317 - Manutencao de Equipamento","3.318 - Softwares e Sistemas de Gestao","3.319 - Servicos de Terceiros - Montagem e instalacoes","3.320 - Pro-labore","3.321 - Manutencao de Informatica (contrato)","3.322 - Certificados Digitais","3.323 - Frete/Transportadora","3.324 - Seguro do Imovel","3.325 - Taxas de Adesao","3.326 - Manutencao e Conservacao","3.327 - Viagens - Passagem Aerea e outros","3.328 - Viagens - Servico de Hospedagem","3.329 - Viagens - Transporte e Locomocao","3.330 - Taxas, Licencas e Anuidades Regulatorias","3.331 - Servico de Limpeza","3.332 - Parcela Imovel Proprio (equiv. Aluguel)"],"3.2 - DESPESAS COM PESSOAL":["3.201 - Salario - Fonoaudiologia (C)","3.202 - Salario - Psicologa (C)","3.203 - Salarios (D)","3.204 - 13o Salario (D)","3.205 - Ferias (D)","3.206 - Vale Alimentacao (D)","3.207 - Vale Transporte (D)","3.208 - Uniforme (D)","3.209 - Cursos e Treinamentos (D)","3.210 - Exames Admissional/Demissional","3.211 - FGTS (D)","3.212 - Gratificacao (D)","3.213 - Vale Manicure (D)","3.214 - INSS/IRRF (D)","3.215 - Estagiarios (D)","3.216 - Rescisao","3.217 - Beneficios Exames-Medicos com Coparticipacao"],"3.3 - DESPESAS DE VENDAS E MARKETING":["3.301 - Jessica (Stories)","3.302 - Agencia Experience (Conteudo)","3.303 - Agencia Coqueiro Midia (CRM/IA)","3.304 - Mensalidade Chat OpenAI IA","3.305 - Ornamentacao/Eventos","3.306 - Brindes","3.307 - Patrocinios","3.308 - Publicidade - Meta Ads - Trafego","3.309 - Outdoors"],"3.4 - DESPESAS FINANCEIRAS":["3.402 - Juros sobre Emprestimos","3.403 - Tarifas Bancarias","3.404 - Taxas de Cartao de Credito/Debito","3.405 - Juros/Multa de atraso a Fornecedores","3.406 - Anuidade Cartao de Credito Empresarial","3.407 - IOF sobre operacoes de credito"],"4.1 - INVESTIMENTOS":["4.401 - Moveis e Utensilios","4.403 - Maquinas e Equipamentos","4.404 - Sistema de Energia Solar","4.405 - Obras/Projeto Arquitetonico","4.406 - Integralizacao Capital Unicred"],"5.1 - MOVIMENTACOES DE SOCIOS / FINANCIAMENTOS":["5.502 - Distribuicao de Lucros","5.503 - Quitacao Cheque Especial (Saida)","5.505 - Financiamento - Pronampe","5.506 - Pagamento de Mutuo a Socios"],"6.1 - OUTRAS DESPESAS OPERACIONAIS":["6.601 - Estornos Negativos","6.602 - Faltas de Caixa"],"7.1 - CUSTOS DE TERCEIROS - NAO OPERACIONAIS":["7.701 - Repasse de Valor - Medicos","7.702 - Repasse de Valor - Terapeutas"],"1.1 - RECEITAS OPERACIONAIS (DRE)":["1.101 - Honorarios Clinicos - Medicos","1.102 - Honorarios Clinicos - Terapeutas","1.103 - Receita Recebimento Notas Fiscais/Faturados","1.104 - Receita venda de Vacinas","1.105 - Receita Vendas Cartao - Rede Credito e Debito"],"1.2 - RECEITAS COMPLEMENTARES OPERACIONAIS":["1.201 - Exames e Teste - Laboratoriais","1.202 - Venda de Ativos","1.206 - Receitas Eventuais - Estagios"],"1.3 - RECUPERACAO E AJUSTE OPERACIONAIS":["1.301 - Reembolso de Valores Exames Medicos","1.302 - Valores Recebidos a Maior","1.303 - Estornos Positivos","1.304 - Creditos Recuperados"],"1.4 - RECEITAS FINANCEIRAS":["1.402 - Descontos obtidos","1.403 - Rendimentos de Aplicacoes","1.404 - Juros s/ duplicatas","1.405 - Multas"],"1.5 - MOVIMENTACOES DE SOCIOS / FINANCIAMENTOS":["1.501 - Aporte de Capital","1.502 - Uso de Cheque Especial (entrada)","1.503 - Mutuo de Socios"],"1.7 - MOVIMENTACOES TRANSITORIAS":["1.701 - Ajuste de Caixa a Regularizar","1.702 - Depositos nao Identificados","1.703 - Transferencias Transitorias","1.704 - Adiantamento a Regularizar"],"1.8 - OUTRAS RECEITAS OPERACIONAIS":["1.801 - Sobra de Caixa"],"1.9 - RECEITAS DE TERCEIROS - NAO OPERACIONAIS":["1.901 - Valores a Repassar - Medicos","1.902 - Valores a Repassar - Terapeutas"],"10 - RECEITAS OPERACIONAIS DE CAIXA (DFC)":["10.01 - Recebimento Pix/TED - Sinal de Consulta","10.02 - Recebimento Pix/TED - Consulta Final","10.03 - Recebimento Pix/TED - Terapias","10.04 - Recebimento Dinheiro Especie - Consultas/Terapias","10.05 - Recebimento Pix/TED - Convenios e Faturados","10.06 - Recebimento Cartao Liquido (Rede-Itau)","10.07 - Recebimento Pix/TED - Venda de Vacinas","10.08 - Recebimento Bruto Producao - Medicos","10.09 - Recebimento Bruto Producao - Terapeutas"]}

    import unicodedata as _ud, difflib, re as _re, io as _io, csv as _csv

    # ── Funções utilitárias ────────────────────────────────────────────────────

    def _plano_ativo():
        return cfg["plano"] if cfg["plano"] else PLANO_PADRAO

    def _norm(s):
        _TITULOS = {'dr','dra','prof','profa','mr','ms','sr','sra','me','pe','rev','seu','dona','d','s','st','sto','sta'}
        s = str(s).lower().strip().replace('/', ' ')
        tokens = [w.rstrip('.') for w in s.split() if w.rstrip('.') not in _TITULOS]
        return ''.join(c for c in _ud.normalize('NFD', ' '.join(tokens)) if _ud.category(c) != 'Mn')

    def _fragmentos(raw):
        raw = str(raw).strip()
        partes = [raw]
        for sep in [' - ', ' / ']:
            for p in _re.split(_re.escape(sep), raw):
                p = p.strip()
                if p and p not in partes:
                    partes.append(p)
        return partes

    def resolver_contato(contato_input):
        _STOP = {'das','dos','de','do','da','em','para','por','no','na','com','que','os','as','ao'}
        raw = str(contato_input).strip()
        if not raw:
            return raw, "sem_match"
        base_norm = [(_norm(n), n) for n in cfg["base_md"]]

        # Camada 1: dicionário manual
        for frag in _fragmentos(raw):
            fn = _norm(frag)
            for chave, nome_md in cfg["mapa"].items():
                if _norm(chave) in fn or fn in _norm(chave):
                    return nome_md, "mapa"

        def _match_str(cn):
            palavras = [w for w in cn.split() if len(w) >= 3 and w not in _STOP]
            if not palavras:
                return 0.0, None, None
            melhor_match, melhor_score = None, 0
            for nome_n, nome_orig in base_norm:
                palavras_md = set(w for w in nome_n.split() if w not in _STOP)
                score = sum(1 for p in palavras if p in palavras_md)
                if score > melhor_score:
                    melhor_score, melhor_match = score, nome_orig
            if melhor_score >= 1:
                return float(melhor_score) + 10, melhor_match, "auto"
            if len(palavras) > 3:
                return 0.0, None, None
            melhor_fuzzy, melhor_ratio = None, 0.0
            for nome_n, nome_orig in base_norm:
                ratio = 0.0
                if any(p in nome_n for p in palavras if len(p) >= 4):
                    ratio = 0.85
                else:
                    tokens_md = [w for w in nome_n.split() if w not in _STOP]
                    for p in palavras:
                        if len(p) >= 4 and difflib.get_close_matches(p, tokens_md, n=1, cutoff=0.85):
                            ratio = max(ratio, 0.78)
                            break
                    if ratio < 0.70:
                        ratio = max(ratio, difflib.SequenceMatcher(None, cn, nome_n).ratio())
                if ratio > melhor_ratio:
                    melhor_ratio, melhor_fuzzy = ratio, nome_orig
            if melhor_ratio >= 0.75:
                return melhor_ratio, melhor_fuzzy, "fuzzy"
            return 0.0, None, None

        best_s, best_n, best_t = 0.0, None, None
        for frag in _fragmentos(raw):
            s, n, t = _match_str(_norm(frag))
            if s > best_s:
                best_s, best_n, best_t = s, n, t
        if best_n:
            return best_n, best_t
        return raw, "sem_match"

    def buscar_categoria_matriz(contato_md, tipo_mov):
        if not cfg["matriz"]:
            return "", ""
        contato_n = _norm(contato_md)
        tipo_n = "entrada" if tipo_mov == "E" else "saida"
        GENERICOS = {'cliente variavel','variacao de terapeutas','variacao de medicos','contas da clinica',''}
        for reg in cfg["matriz"]:
            cf_raw = reg.get("cf", "")
            if tipo_n not in _norm(reg.get("tipo_es", "")):
                continue
            cf_variants = [_norm(v.strip()) for v in cf_raw.split(" ou ")]
            if any(v in GENERICOS for v in cf_variants):
                continue
            if contato_n in cf_variants:
                return reg.get("cat", ""), reg.get("sub", "")
        palavras_md = [w for w in contato_n.split() if len(w) >= 6]
        if palavras_md:
            for reg in cfg["matriz"]:
                cf_raw = reg.get("cf", "")
                if tipo_n not in _norm(reg.get("tipo_es", "")):
                    continue
                cf_variants = [_norm(v.strip()) for v in cf_raw.split(" ou ")]
                if any(v in GENERICOS for v in cf_variants):
                    continue
                for cf_v in cf_variants:
                    if sum(1 for p in palavras_md if p in set(cf_v.split())) >= 1:
                        return reg.get("cat", ""), reg.get("sub", "")
        return "", ""

    def is_transferencia(contato, descricao):
        c = _norm(contato)
        d = _norm(descricao)
        CONTATOS_T = ["mov entre contas","movimentacao entre contas","deposito bb",
                      "deposito itau","deposito bradesco","deposito banco","deposito bancario"]
        if any(p in c for p in CONTATOS_T):
            return True, "Fechamento de caixa 2025;2026"
        if any(p in d for p in ["fechamento cx","fechamento de cx"]):
            return True, "Fechamento de caixa 2025;2026"
        return False, ""

    def get_chave(row):
        return "|".join(str(row.get(c,"")).strip() for c in ["Data","Contato","Descricao","Entrada","Saida"])

    def fmt_num(v, neg=False):
        s = f"{abs(float(v)):.2f}".replace(".", ",")
        return f"-{s}" if neg else s

    def montar_csv_meu_dinheiro(df, conta_nome="Caixinha 2025;2026"):
        rows = []
        for _, r in df.iterrows():
            _pn = lambda x: (parse_numeric(pd.Series([x])).iloc[0] or 0.0)
            ent = _pn(r.get("Entrada",""))
            sai = _pn(r.get("Saida",""))
            tipo = str(r.get("Tipo","")).strip()
            conta_d = str(r.get("Conta Destino","")).strip()
            cat = str(r.get("Categoria","")).strip()
            sub = str(r.get("SubCategoria","")).strip()
            cmd = str(r.get("Contato MD","")).strip() or str(r.get("Contato","")).strip()
            desc = str(r.get("Descricao",""))[:100].strip()
            data = str(r.get("Data","")).strip()
            eh_saida = sai > 0 and ent == 0
            if tipo == "Transferência":
                v = fmt_num(sai, neg=True) if eh_saida else fmt_num(ent)
                rows.append({"Data":data,"Valor":v,"Descrição":desc,"Conta":conta_nome,
                    "Conta Transferência":conta_d or "Fechamento de caixa 2025;2026",
                    "Cartão":"","Categoria":"","Subcategoria":"","Contato":"",
                    "Centro":"","Projeto":"","Forma":"","N. Documento":"","Observações":"",
                    "Data Competência":data,"Tags":""})
            elif tipo == "Receita":
                rows.append({"Data":data,"Valor":fmt_num(ent),"Descrição":desc,"Conta":conta_nome,
                    "Conta Transferência":"","Cartão":"","Categoria":cat,"Subcategoria":sub,
                    "Contato":cmd,"Centro":"","Projeto":"","Forma":"","N. Documento":"","Observações":"",
                    "Data Competência":data,"Tags":""})
            else:
                rows.append({"Data":data,"Valor":fmt_num(sai,neg=True),"Descrição":desc,"Conta":conta_nome,
                    "Conta Transferência":"","Cartão":"","Categoria":cat,"Subcategoria":sub,
                    "Contato":cmd,"Centro":"","Projeto":"","Forma":"","N. Documento":"","Observações":"",
                    "Data Competência":data,"Tags":""})
        return pd.DataFrame(rows)

    def gerar_ofx(df, conta_nome="Caixinha"):
        _pn = lambda x: (parse_numeric(pd.Series([x])).iloc[0] or 0.0)
        lines_ofx = [
            "OFXHEADER:100","DATA:OFXSGML","VERSION:102","SECURITY:NONE",
            "ENCODING:UTF-8","CHARSET:1252","COMPRESSION:NONE","OLDFILEUID:NONE","NEWFILEUID:NONE",
            "<OFX><SIGNONMSGSRSV1><SONRS><STATUS><CODE>0</CODE><SEVERITY>INFO</SEVERITY></STATUS>",
            "<DTSERVER>20260101120000</DTSERVER><LANGUAGE>POR</LANGUAGE></SONRS></SIGNONMSGSRSV1>",
            "<BANKMSGSRSV1><STMTTRNRS><TRNUID>1</TRNUID><STMTRS>",
            "<CURDEF>BRL</CURDEF><BANKACCTFROM><BANKID>000</BANKID>",
            f"<ACCTID>{conta_nome}</ACCTID><ACCTTYPE>CHECKING</ACCTTYPE></BANKACCTFROM>",
            "<BANKTRANLIST>",
        ]
        for i, r in df.iterrows():
            ent = _pn(r.get("Entrada",""))
            sai = _pn(r.get("Saida",""))
            val = ent if ent > 0 else -sai
            data_raw = str(r.get("Data","")).replace("/","")
            if len(data_raw) == 8:
                data_ofx = data_raw[4:8] + data_raw[2:4] + data_raw[0:2] + "120000"
            else:
                data_ofx = "20260101120000"
            desc = str(r.get("Descricao",""))[:32].replace("&","e").replace("<","").replace(">","")
            lines_ofx += [
                "<STMTTRN>",
                f"<TRNTYPE>{'CREDIT' if val>=0 else 'DEBIT'}</TRNTYPE>",
                f"<DTPOSTED>{data_ofx}</DTPOSTED>",
                f"<TRNAMT>{val:.2f}</TRNAMT>",
                f"<FITID>{i+1:06d}</FITID>",
                f"<MEMO>{desc}</MEMO>",
                "</STMTTRN>",
            ]
        lines_ofx += ["</BANKTRANLIST>","</STMTRS></STMTTRNRS></BANKMSGSRSV1></OFX>"]
        return "\n".join(lines_ofx)

    # ── Tabs principais ────────────────────────────────────────────────────────
    tab_cfg_ui, tab_cls_ui = st.tabs(["⚙️  Configuração", "🤖  Classificar"])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1 — CONFIGURAÇÃO
    # ═════════════════════════════════════════════════════════════════════════
    with tab_cfg_ui:
        st.markdown('<div style="color:#8899BB;font-size:.85rem;margin-bottom:1rem;">Configure uma vez — os dados ficam salvos até você atualizar ou remover.</div>', unsafe_allow_html=True)

        # ── Plano de Contas ────────────────────────────────────────────────────
        st.markdown("#### 📋 Plano de Contas")
        plano_cur = _plano_ativo()
        n_cats_cur = len(plano_cur)
        n_subs_cur = sum(len(v) for v in plano_cur.values())
        fonte = "padrão embutido" if not cfg["plano"] else "importado"
        st.markdown(f'<span style="color:#4ade80;font-size:.82rem;">✅ Ativo: {n_cats_cur} categorias · {n_subs_cur} subcategorias ({fonte})</span>', unsafe_allow_html=True)

        f_plano = st.file_uploader("Importar Plano de Contas do Meu Dinheiro (Excel/CSV)", type=["xlsx","xls","csv"], key="cfg_plano_up")
        if f_plano:
            try:
                if f_plano.name.endswith(".csv"):
                    df_pl = pd.read_csv(f_plano, sep=None, engine="python", dtype=str).fillna("")
                else:
                    df_pl = pd.read_excel(f_plano, dtype=str).fillna("")
                df_pl.columns = [c.strip() for c in df_pl.columns]
                col_cat = next((c for c in df_pl.columns if "categ" in c.lower()), None)
                col_sub = next((c for c in df_pl.columns if "sub" in c.lower()), None)
                if col_cat and col_sub:
                    novo_plano = {}
                    for _, row in df_pl.iterrows():
                        cat = str(row[col_cat]).strip()
                        sub = str(row[col_sub]).strip()
                        if cat and cat != "nan":
                            novo_plano.setdefault(cat, [])
                            if sub and sub != "nan" and sub not in novo_plano[cat]:
                                novo_plano[cat].append(sub)
                    if novo_plano:
                        cfg["plano"] = novo_plano
                        st.success(f"✅ Plano carregado: {len(novo_plano)} categorias")
                        st.rerun()
                    else:
                        st.warning("Nenhuma categoria encontrada. Verifique o arquivo.")
                else:
                    st.warning(f"Colunas esperadas: Categoria / Subcategoria. Encontradas: {list(df_pl.columns)}")
            except Exception as e:
                st.error(f"Erro ao ler plano: {e}")

        if cfg["plano"]:
            if st.button("🔄 Voltar ao plano padrão embutido", key="cfg_reset_plano"):
                cfg["plano"] = {}
                st.rerun()

        st.markdown("---")

        # ── Base de Contatos ───────────────────────────────────────────────────
        st.markdown("#### 👤 Base de Contatos (PF + PJ)")
        n_base = len(cfg["base_md"])
        cor_base = "#4ade80" if n_base > 0 else "#f97316"
        st.markdown(f'<span style="color:{cor_base};font-size:.82rem;">{"✅" if n_base > 0 else "⚠️"} {n_base} contatos carregados</span>', unsafe_allow_html=True)

        col_pf, col_pj = st.columns(2)
        with col_pf:
            st.markdown("**Pessoa Física (PF)**")
            f_pf = st.file_uploader("Arquivo PF", type=["xlsx","xls"], key="cfg_pf_up", label_visibility="collapsed")
            if f_pf:
                try:
                    df_pf = pd.read_excel(f_pf, dtype=str).fillna("")
                    col_nome = next((c for c in df_pf.columns if "nome" in c.lower()), df_pf.columns[0])
                    nomes_pf = [str(v).strip() for v in df_pf[col_nome] if str(v).strip() and str(v).strip() != "nan"]
                    existentes = set(cfg["base_md"])
                    novos = [n for n in nomes_pf if n not in existentes]
                    cfg["base_md"].extend(novos)
                    st.success(f"✅ {len(novos)} contatos PF adicionados")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

        with col_pj:
            st.markdown("**Pessoa Jurídica (PJ)**")
            f_pj = st.file_uploader("Arquivo PJ", type=["xlsx","xls"], key="cfg_pj_up", label_visibility="collapsed")
            if f_pj:
                try:
                    df_pj = pd.read_excel(f_pj, dtype=str).fillna("")
                    nomes_pj = []
                    for col in df_pj.columns:
                        if any(k in col.lower() for k in ["razao","fantasia","nome"]):
                            nomes_pj += [str(v).strip() for v in df_pj[col] if str(v).strip() and str(v).strip() != "nan"]
                    existentes = set(cfg["base_md"])
                    novos = [n for n in nomes_pj if n not in existentes]
                    cfg["base_md"].extend(novos)
                    st.success(f"✅ {len(novos)} contatos PJ adicionados")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

        if cfg["base_md"]:
            if st.button("🗑️ Limpar base de contatos", key="cfg_reset_base"):
                cfg["base_md"] = []
                st.rerun()

        st.markdown("---")

        # ── Matriz do Plano de Contas ──────────────────────────────────────────
        st.markdown("#### 📊 Matriz do Plano de Contas")
        st.caption("Regras de classificação por contato — atualiza quando adicionar novos profissionais.")
        n_mtz = len(cfg["matriz"])
        cor_mtz = "#4ade80" if n_mtz > 0 else "#f97316"
        st.markdown(f'<span style="color:{cor_mtz};font-size:.82rem;">{"✅" if n_mtz > 0 else "⚠️"} {n_mtz} regras carregadas</span>', unsafe_allow_html=True)

        f_mtz = st.file_uploader("Arquivo Matriz (aba MATRIZ)", type=["xlsx","xls"], key="cfg_mtz_up")
        if f_mtz:
            try:
                df_mtz = pd.read_excel(f_mtz, sheet_name="MATRIZ", dtype=str).fillna("")
                df_mtz.columns = [c.strip() for c in df_mtz.columns]
                col_cf  = next((c for c in df_mtz.columns if "contato" in c.lower() or c.upper() == "CF"), None)
                col_cat = next((c for c in df_mtz.columns if "categ" in c.lower()), None)
                col_sub = next((c for c in df_mtz.columns if "sub" in c.lower()), None)
                col_tp  = next((c for c in df_mtz.columns if "tipo" in c.lower() or "e/s" in c.lower() or "es" == c.lower()), None)
                if not all([col_cf, col_cat, col_sub, col_tp]):
                    st.warning(f"Colunas esperadas: CF/Contato, Categoria, Subcategoria, Tipo E/S. Encontradas: {list(df_mtz.columns)}")
                else:
                    registros = []
                    for _, row in df_mtz.iterrows():
                        cf = str(row[col_cf]).strip()
                        if cf and cf != "nan":
                            registros.append({
                                "cf": cf,
                                "cat": str(row[col_cat]).strip(),
                                "sub": str(row[col_sub]).strip(),
                                "tipo_es": str(row[col_tp]).strip(),
                            })
                    cfg["matriz"] = registros
                    st.success(f"✅ Matriz carregada: {len(registros)} regras")
                    st.rerun()
            except Exception as e:
                st.error(f"Erro ao ler Matriz: {e}")

        if cfg["matriz"]:
            if st.button("🗑️ Limpar Matriz", key="cfg_reset_mtz"):
                cfg["matriz"] = []
                st.rerun()

        st.markdown("---")

        # ── Dicionário Manual ──────────────────────────────────────────────────
        st.markdown("#### 🔤 Dicionário de Contatos")
        st.caption("Associe apelidos da caixinha ao nome exato no Meu Dinheiro.")

        n_mapa = len(cfg["mapa"])
        if n_mapa > 0:
            df_mapa_show = pd.DataFrame([{"Apelido (Caixinha)": k, "Nome no MD": v} for k, v in cfg["mapa"].items()])
            st.dataframe(df_mapa_show, hide_index=True, use_container_width=True)

        with st.expander("➕ Adicionar entrada no dicionário"):
            m1, m2 = st.columns(2)
            with m1:
                alias_inp = st.text_input("Apelido da caixinha", key="dic_alias", placeholder="Ex: D. Catia")
            with m2:
                nome_inp  = st.text_input("Nome exato no Meu Dinheiro", key="dic_nome", placeholder="Ex: Catia Maria Silva")
            if st.button("Salvar no dicionário", key="dic_save"):
                if alias_inp.strip() and nome_inp.strip():
                    cfg["mapa"][alias_inp.strip()] = nome_inp.strip()
                    st.success(f"✅ '{alias_inp.strip()}' → '{nome_inp.strip()}' salvo!")
                    st.rerun()
                else:
                    st.warning("Preencha os dois campos.")

        if cfg["mapa"]:
            del_key = st.selectbox("Remover entrada", ["— selecione —"] + list(cfg["mapa"].keys()), key="dic_del_sel")
            if st.button("Remover", key="dic_del_btn") and del_key != "— selecione —":
                del cfg["mapa"][del_key]
                st.rerun()

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2 — CLASSIFICAR
    # ═════════════════════════════════════════════════════════════════════════
    with tab_cls_ui:

        plano_ativo  = _plano_ativo()
        PLANO_CATS   = list(plano_ativo.keys())
        subs_flat    = [""] + sorted(set(s for lst in plano_ativo.values() for s in lst))
        CONTAS_DISP  = ["","Fechamento de caixa 2025;2026","Itaú 2025;2026","Banco do Brasil","Caixinha 2025;2026"]
        CONTA_PADRAO = "Caixinha 2025;2026"

        # Avisos de configuração incompleta
        alertas = []
        if not cfg["base_md"]:
            alertas.append("Base de contatos não carregada — os nomes não serão resolvidos para o Meu Dinheiro.")
        if not cfg["matriz"]:
            alertas.append("Matriz do Plano de Contas não carregada — categorias não serão preenchidas automaticamente.")
        for alerta in alertas:
            st.warning(f"⚠️ {alerta} Configure na aba **⚙️ Configuração**.")

        # Upload do CSV da caixinha
        f_csv = st.file_uploader("📂 Planilha da Caixinha (Excel ou CSV)", type=["xlsx","xls","csv"], key="cls_csv_up")
        if not f_csv:
            st.info("⬆️ Faça o upload da planilha da caixinha para começar.")
            st.stop()

        # Carrega e normaliza
        try:
            df_raw = load_file(f_csv)
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")
            st.stop()

        col_map = {}
        for c in df_raw.columns:
            cl = c.strip().lower()
            if "data" in cl:                         col_map["Data"]     = c
            elif "contato" in cl or "fornec" in cl:  col_map["Contato"]  = c
            elif "descri" in cl or "hist" in cl:     col_map["Descricao"]= c
            elif "entrada" in cl:                    col_map["Entrada"]  = c
            elif "sa" in cl and "da" not in cl and "saldo" not in cl: col_map["Saida"] = c

        df_work = df_raw.rename(columns={v: k for k, v in col_map.items()})
        for c in ["Data","Contato","Descricao","Entrada","Saida"]:
            if c not in df_work.columns:
                df_work[c] = ""

        df_work = df_work[df_work["Contato"].astype(str).str.strip().str.len() > 0].copy()
        df_work = df_work[df_work["Data"].astype(str).str.strip().str.len() > 0].copy()
        df_work = df_work.reset_index(drop=True)

        if df_work.empty:
            st.warning("Nenhum lançamento válido encontrado no arquivo.")
            st.stop()

        n_total = len(df_work)
        nome_aba = f_csv.name.replace(".csv","").replace(".xlsx","").replace(".xls","")
        st.markdown(f'<div style="color:#8899BB;font-size:.82rem;margin-bottom:.5rem;">Arquivo: <strong style="color:#C9A84C;">{nome_aba}</strong> · {n_total} lançamentos</div>', unsafe_allow_html=True)

        # Lançamentos já exportados
        ja_exp_count = sum(1 for _, row in df_work.iterrows() if get_chave(row) in cfg["exportados"])
        if ja_exp_count > 0:
            st.markdown(f'<div style="background:#162236;border-left:3px solid #C9A84C;border-radius:0 8px 8px 0;padding:8px 14px;font-size:.82rem;margin-bottom:12px;">📋 <strong style="color:#C9A84C;">{ja_exp_count} lançamentos</strong> já foram exportados anteriormente. <strong style="color:#4ade80;">{n_total-ja_exp_count} novos</strong> para revisar.</div>', unsafe_allow_html=True)

        # ── Auto-processo: roda sempre que o arquivo mudar ───────────────────────
        _file_key = f"{f_csv.name}|{f_csv.size}"
        if st.session_state.get("_cls_file_key") != _file_key:
            with st.spinner("🤖 Classificando lançamentos…"):
                tipos, contas_dest, cats, subs, confs = [], [], [], [], []
                contatos_md, status_cts, ja_flags = [], [], []

                for _, row in df_work.iterrows():
                    contato   = str(row.get("Contato","")).strip()
                    descricao = str(row.get("Descricao","")).strip()
                    ja_exp    = get_chave(row) in cfg["exportados"]
                    ja_flags.append("✅ Sim" if ja_exp else "🆕 Novo")

                    _pn = lambda x: (parse_numeric(pd.Series([x])).iloc[0] or 0.0)
                    ent = _pn(row.get("Entrada",""))
                    tmov = "E" if ent > 0 else "S"

                    transf, conta_dest = is_transferencia(contato, descricao)
                    if transf:
                        tipos.append("Transferência")
                        contas_dest.append(conta_dest)
                        cats.append(""); subs.append(""); confs.append("Auto")
                        contatos_md.append(""); status_cts.append("transf")
                        continue

                    tipo_fin = "Receita" if tmov == "E" else "Despesa"
                    tipos.append(tipo_fin)
                    contas_dest.append("")

                    nome_md, st_res = resolver_contato(contato)
                    contatos_md.append(nome_md)
                    status_cts.append(st_res)

                    if ja_exp:
                        cats.append(""); subs.append(""); confs.append("✅ Exportado")
                        continue

                    cat, sub = buscar_categoria_matriz(nome_md, tmov)
                    conf = "Matriz" if cat else ""

                    if not cat:
                        for r in cfg["regras"]:
                            if r.get("mov","") != tmov:
                                continue
                            if r.get("tipo") == "contato" and r.get("contato","").lower() in contato.lower():
                                cat, sub, conf = r["categoria"], r["subcategoria"], "Aprendida"
                                break
                            if r.get("tipo") == "descricao":
                                for p in descricao.lower().split():
                                    if len(p) > 4 and p == r.get("palavra",""):
                                        cat, sub, conf = r["categoria"], r["subcategoria"], "Aprendida"
                                        break
                            if cat:
                                break

                    conf = conf or "Manual"
                    cats.append(cat); subs.append(sub); confs.append(conf)

                df_work["Tipo"]         = tipos
                df_work["Conta Destino"]= contas_dest
                df_work["Categoria"]    = cats
                df_work["SubCategoria"] = subs
                df_work["Confiança"]    = confs
                df_work["Status"]       = ja_flags
                df_work["Contato MD"]   = contatos_md
                df_work["_st_ct"]       = status_cts
                st.session_state["df_cls"]       = df_work.copy()
                st.session_state["_cls_file_key"] = _file_key

        df_cls = st.session_state["df_cls"].copy()

        # Métricas
        n_exp  = (df_cls["Status"]=="✅ Sim").sum()
        n_nov  = (df_cls["Status"]=="🆕 Novo").sum()
        n_rec  = (df_cls["Tipo"]=="Receita").sum()
        n_des  = (df_cls["Tipo"]=="Despesa").sum()
        n_tra  = (df_cls["Tipo"]=="Transferência").sum()
        n_mtz_c  = (df_cls["Confiança"]=="Matriz").sum()
        n_apr  = (df_cls["Confiança"]=="Aprendida").sum()
        n_man  = ((df_cls["Confiança"]=="Manual") & (df_cls["Status"]!="✅ Sim")).sum()

        m1,m2,m3,m4,m5,m6,m7,m8 = st.columns(8)
        for col,lbl,val,cls in [
            (m1,"Total",    n_total,      ""),
            (m2,"Exportados",n_exp,       "green"),
            (m3,"Novos",    n_nov,        "amber" if n_nov>0 else "green"),
            (m4,"Receitas", n_rec,        "green" if n_rec>0 else ""),
            (m5,"Despesas", n_des,        ""),
            (m6,"Transf.",  n_tra,        ""),
            (m7,"Matriz",   n_mtz_c,      "green" if n_mtz_c>0 else ""),
            (m8,"Manual",   n_man,        "red" if n_man>0 else "green"),
        ]:
            col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Alertas de resolução de contatos
        if "_st_ct" in df_cls.columns:
            sem_match = df_cls[df_cls["_st_ct"]=="sem_match"]["Contato MD"].tolist()
            fuzzy_lst = df_cls[df_cls["_st_ct"]=="fuzzy"]["Contato MD"].tolist()
            if sem_match:
                uniq_sm = list(dict.fromkeys(sem_match))[:5]
                st.markdown(f'<div style="background:#422006;border-left:3px solid #f97316;border-radius:0 8px 8px 0;padding:8px 14px;font-size:.82rem;margin-bottom:6px;">⚠️ <strong style="color:#fcd34d;">{len(sem_match)} lançamento(s) sem match</strong> na base — revise a coluna <strong>Contato MD</strong>:<br><span style="color:#fdba74;font-size:.78rem;">{" · ".join(str(n) for n in uniq_sm)}</span></div>', unsafe_allow_html=True)
            if fuzzy_lst:
                uniq_fz = list(dict.fromkeys(fuzzy_lst))[:5]
                st.markdown(f'<div style="background:#1c2a1c;border-left:3px solid #fcd34d;border-radius:0 8px 8px 0;padding:8px 14px;font-size:.82rem;margin-bottom:6px;">🔍 <strong style="color:#fcd34d;">{len(fuzzy_lst)} contato(s) com match heurístico</strong> — confirme se o nome está correto:<br><span style="color:#86efac;font-size:.78rem;">{" · ".join(str(n) for n in uniq_fz)}</span></div>', unsafe_allow_html=True)

        st.markdown('<div style="background:#1B2A4A;border-radius:8px;padding:8px 14px;margin-bottom:10px;font-size:.82rem;color:#C9A84C;">✏️ Edite <strong>Tipo</strong>, <strong>Categoria</strong>, <strong>SubCategoria</strong> e <strong>Contato MD</strong> diretamente na tabela.</div>', unsafe_allow_html=True)

        df_edit = st.data_editor(
            df_cls,
            column_config={
                "Tipo": st.column_config.SelectboxColumn("Tipo", options=["Receita","Despesa","Transferência"], width="small"),
                "Conta Destino": st.column_config.SelectboxColumn("Conta Destino", options=CONTAS_DISP, width="medium"),
                "Categoria":     st.column_config.SelectboxColumn("Categoria",    options=PLANO_CATS, width="large"),
                "SubCategoria":  st.column_config.SelectboxColumn("SubCategoria", options=subs_flat,  width="large"),
                "Contato MD":    st.column_config.TextColumn("Contato MD", width="medium"),
                "Status":        st.column_config.TextColumn("Status", disabled=True, width="small"),
                "Confiança":     st.column_config.TextColumn("Confiança", disabled=True, width="small"),
                "Contato":       st.column_config.TextColumn("Contato", width="medium"),
                "Descricao":     st.column_config.TextColumn("Descrição", disabled=True),
                "Data":          st.column_config.TextColumn("Data", disabled=True, width="small"),
                "Entrada":       st.column_config.TextColumn("Entrada", disabled=True, width="small"),
                "Saida":         st.column_config.TextColumn("Saída",   disabled=True, width="small"),
                "_st_ct":        st.column_config.TextColumn("_st_ct", disabled=True),
            },
            use_container_width=True, hide_index=True, key="editor_cls",
        )

        # Salvar correções como regras
        col_sv, _ = st.columns([1,3])
        with col_sv:
            if st.button("💾  Salvar correções", key="btn_salvar", use_container_width=True):
                orig = st.session_state["df_cls"]
                n_novas = 0
                for i, row in df_edit.iterrows():
                    orig_cat = orig.loc[i,"Categoria"] if i < len(orig) else ""
                    new_cat  = row.get("Categoria","")
                    new_sub  = row.get("SubCategoria","")
                    new_tipo = row.get("Tipo","")
                    if new_cat and new_cat != orig_cat:
                        contato = str(row.get("Contato","")).strip()
                        descricao = str(row.get("Descricao","")).strip()
                        _pn = lambda x: (parse_numeric(pd.Series([x])).iloc[0] or 0.0)
                        tmov = "E" if _pn(row.get("Entrada","")) > 0 else "S"
                        if contato and len(contato) > 2:
                            r = {"tipo":"contato","contato":contato.lower(),"palavra":"","mov":tmov,"categoria":new_cat,"subcategoria":new_sub}
                            if not any(x.get("contato","").lower()==r["contato"] and x.get("mov","")==tmov for x in cfg["regras"]):
                                cfg["regras"].insert(0, r); n_novas += 1
                        palavras = [p for p in descricao.lower().split() if len(p) > 4]
                        if palavras:
                            chave = palavras[0]
                            r2 = {"tipo":"descricao","contato":"","palavra":chave,"mov":tmov,"categoria":new_cat,"subcategoria":new_sub}
                            if not any(x.get("palavra","").lower()==chave and x.get("mov","")==tmov for x in cfg["regras"]):
                                cfg["regras"].insert(0, r2); n_novas += 1
                st.session_state["df_cls"] = df_edit.copy()
                st.success(f"✅ {n_novas} novas regras salvas!")
                st.rerun()

        st.markdown("---")

        # Exportar apenas novos
        df_novos = df_edit[df_edit["Status"] != "✅ Sim"].copy()
        n_novos_export = len(df_novos)
        n_skip = len(df_edit) - n_novos_export
        nome_base = f"caixinha_{nome_aba.replace(' ','_')}_{pd.Timestamp.today().strftime('%d%m%Y')}"

        st.markdown("**📤 Exportar**")
        if n_skip > 0:
            st.caption(f"{n_novos_export} novos para exportar · {n_skip} já exportados ignorados")

        dl1, dl2, dl3 = st.columns(3)
        with dl1:
            st.markdown("**CSV — Meu Dinheiro Web**")
            df_csv_md = montar_csv_meu_dinheiro(df_novos, conta_nome=CONTA_PADRAO)
            buf = _io.StringIO()
            df_csv_md.to_csv(buf, index=False, sep=",", quoting=_csv.QUOTE_MINIMAL)
            if st.download_button(f"⬇️ Baixar CSV ({n_novos_export} lançamentos)", data=buf.getvalue().encode("utf-8"),
                                   file_name=f"{nome_base}_meu_dinheiro.csv", mime="text/csv"):
                for _, row in df_novos.iterrows():
                    cfg["exportados"].add(get_chave(row))
                st.success(f"✅ {n_novos_export} marcados como exportados!")
                st.rerun()

        with dl2:
            st.markdown("**Excel — revisão**")
            st.download_button("⬇️ Baixar Excel", data=to_excel_bytes(df_edit),
                               file_name=f"{nome_base}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        with dl3:
            st.markdown("**OFX — extrato**")
            st.download_button("⬇️ Baixar OFX", data=gerar_ofx(df_edit, conta_nome=nome_aba).encode("utf-8"),
                               file_name=f"{nome_base}.ofx", mime="application/octet-stream")

        # Limpar exportados
        if cfg["exportados"]:
            with st.expander("🔧 Controle de exportações"):
                st.caption(f"{len(cfg['exportados'])} lançamentos marcados como exportados nesta sessão.")
                if st.button("🗑️ Limpar histórico de exportações", key="btn_clear_exp"):
                    cfg["exportados"] = set()
                    st.rerun()



# ════════════════════════════════════════════════════════════════════════════
elif page == "servicos":
    st.markdown('<div class="page-title">Serviços & Contato</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">CRS Finance · BPO Financeiro · Parnaíba, Piauí</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    servicos = [
        ("Auditoria de Extrato", "Cruzamento sistemático do extrato bancário com o sistema de gestão, identificando divergências, duplicidades e lançamentos não conciliados.", "A partir de R$ 490/mês"),
        ("Contas a Pagar/Receber", "Gestão completa do fluxo de pagamentos e recebimentos com conciliação diária e relatórios de inadimplência.", "A partir de R$ 690/mês"),
        ("Conciliação Bancária", "Conferência entre saldos bancários e registros do sistema de gestão com relatório de diferenças.", "A partir de R$ 390/mês"),
        ("Relatórios Gerenciais", "DRE simplificado, fluxo de caixa e painel financeiro para tomada de decisão do gestor.", "A partir de R$ 290/mês"),
    ]
    for i, (titulo, desc, preco) in enumerate(servicos):
        col = c1 if i % 2 == 0 else c2
        col.markdown(f"""
        <div class="svc-card" style="margin-bottom:12px;">
            <div class="svc-title">{titulo}</div>
            <div class="svc-desc">{desc}</div>
            <div class="svc-price">{preco}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card">
        <div class="section-card-title">Entre em contato</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;">
                <div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">WhatsApp</div>
                <div style="color:#94a3b8;">(86) 9 xxxx-xxxx</div>
            </div>
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;">
                <div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">Instagram</div>
                <div style="color:#94a3b8;">@crsfinance</div>
            </div>
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;">
                <div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">LinkedIn</div>
                <div style="color:#94a3b8;">Caio Rodrigues Silva</div>
            </div>
            <div style="background:#1B2A4A;border-radius:8px;padding:10px 16px;font-size:0.82rem;">
                <div style="color:#C9A84C;font-weight:600;margin-bottom:2px;">Localização</div>
                <div style="color:#94a3b8;">Parnaíba · PI · Brasil</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1B2A4A;border-radius:12px;padding:1.5rem 2rem;border-top:2px solid #C9A84C;text-align:center;margin-top:1rem;">
        <div style="font-size:0.65rem;letter-spacing:.25em;color:#C9A84C;text-transform:uppercase;margin-bottom:8px;">Posicionamento CRS Finance</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-style:italic;color:#fff;line-height:1.7;">
            "Precisão que move o seu negócio."
        </div>
    </div>
    """, unsafe_allow_html=True)
