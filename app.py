import streamlit as st
import pandas as pd
import numpy as np
import re
import io
import json
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
# 6. CLASSIFICADOR CAIXINHA — com plano de contas dinâmico + aprendizado
# ════════════════════════════════════════════════════════════════════════════
elif page == "classificador":
    st.markdown('<div class="page-title">Classificador Caixinha</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Classifica automaticamente os lançamentos, aprende com suas correções e aceita atualizações do plano de contas.</div>', unsafe_allow_html=True)

    # ── Plano de contas padrão embutido (fallback) ────────────────────────────
    PLANO_PADRAO = {"2.1 IMPOSTOS E TAXAS":["2.101 - Simples Nacional (DAS)","2.102 - IOF"],"2.2 DEDUCOES DE RECEITAS":["2.201 - Devolucao de vendas/Reembolso","2.202 - Descontos ","2.203 - Desembolso - Nota Fiscal"],"2.3 - CUSTO DIRETO COM PESSOAL (MOD)":["2.301 - Salario - Fonoaudiologia (C)","2.302 - Salario - Psicologa (C)","2.303 - Adiantamento (C)"],"2.4 - CUSTOS DIRETOS COM INSUMOS (MAT)":["2.401 - Teste/Vacinas para Revenda","2.402 - Material de Consumo Clinico"],"3.1 DESPESAS ADMINISTRATIVAS":["3.301 - Água e Esgoto","3.302 - IPTU","3.303 - Aluguel","3.304 - Assessoria Financeira (BPO)","3.305 - Consultoria ","3.306 - Cartorio","3.307 - Energia Elétrica","3.308 - Material de Escritório ","3.309 - Confraternizacao/Coffee break","3.310 - Material de Copa e Cozinha","3.311 - Material de informatica","3.312 - Material de Limpeza","3.313 - Segurança e Monitoramento","3.314 - Contabilidade","3.315 - Telefone e Internet","3.316 - Aluguel de Maquinhinha - Adquirente de Cartão","3.317 - Manutenção de Equipamento ","3.318 - Softwares e Sistemas de Gestao","3.319 - Serviços de Terceiros - Montagem e instalações","3.320 - Pró-labore","3.321 - Manutenção de Informática (contrato)","3.322 - Certificados Digitais","3.323 - Frete/Transportadora","3.324 - Seguro do Imóvel","3.325 - Taxas de Adesao","3.326 - Manutencao e Conservacao","3.327 - Viagens - Passagem Aérea e outros","3.328 - Viagens - Serviço de Hospedagem","3.329 - Viagens - Transporte e Locomoção","3.330 - Alvará, Vistoria, Taxas Municipais","3.331 - Serviço de Limpeza "],"3.2 - DESPESAS COM PESSOAL":["3.301 - Salarios (D)","3.302 - 13º Salario (D)","3.303 - Férias (D)","3.304 - Vale Alimentacao (D)","3.305 - Vale Transporte (D)","3.306 - Uniforme (D)","3.307 - Cursos e Treinamentos (D)","3.308 - Exames Admissional/Demissional","3.309 - Vale Manicure (D)","3.310 - Gratificação (D)","3.311 - FGTS (D)","3.312 - INSS/IRRF (D)","3.313 - Estagiários (D)","3.314 - Rescisão"],"3.3 - DESPESAS DE VENDAS E MARKETING":["3.301 - Website/Redes Sociais","3.302 - Feiras e Eventos","3.303 - Propaganda e publicidade","3.304 - Brindes","3.305 - Patrocínios"],"3.4 - DESPESAS FINANCEIRAS":["3.401 - Estornos","3.402 - Juros sobre emprestimos","3.403 - Tarifas Bancárias","3.404 - Taxa de Vendas - Rede cartao Credito/Debito","3.405 - Juros Fornecedores","3.406 - Anuidade Cartão de Crédito"],"4.1 - INVESTIMENTOS":["4.401 - Móveis e Utensílios ","4.402 - Imóveis","4.403 - Máquinas e Equipamentos","4.404 - Sistema de Energia Solar","4.405 - Obras/Projeto Arquitetonico"],"5.1 - MOVIMENTAÇÕES DE SÓCIOS / FINANCIAMENTOS":["5.501 - Parcelamentos de Impostos","5.502 - Distribuição de Lucros","5.503 - Quitação Cheque Especial","5.504 - Multas Sobre Empréstimos Bancários","5.505 - Financiamento - Pronampe","5.506 - Movimentação Mútuo do Socio"],"6.1 - CUSTOS DE TERCEIROS - NAO OPERACIONAIS":["6.601 - Repasse de Valor - Médicos","6.602 - Repasse de Valor - Terapeutas"],"1.1 - RECEITAS OPERACIONAIS":["1.101 - Honorários Clínicos - Medicos","1.102 - Honorários Clínicos - Terapeutas","1.103 - Receita Vendas Cartao - Rede Credito e Debito","1.104 - Receita Recebimento Notas Fiscais","1.105 - Receita venda de Vacinas"],"1.2 - RECEITAS NÃO OPERACIONAIS":["1.201 - Exames e Teste - Laboratoriais ","1.202 - Venda de Ativos","1.203 - Reembolso de despesas","1.206 - Receitas Eventuais – Estagios"],"1.3 - DEVOLUÇÕES DE COMPRAS":["1.301 - Devoluções de Compra de Serviços","1.302 -  Devoluções de Compra de ativo"],"1.4 - RECEITAS FINANCEIRAS":["1.401 - Ajuste de Caixa","1.402 - Descontos obtidos","1.403 - Rendimentos de Aplicacoes","1.404 - Juros s/ duplicatas","1.405 - Multas"],"1.5 - MOVIMENTAÇÕES DE SÓCIOS / FINANCIAMENTOS":["1.501 - Aporte de Capital","1.502 - Cheque Especial Utilizado/Emprestimos","1.503 - Mútuo de Sócios"],"1.6 - RECEITAS DE TERCEIROS - NAO OPERACIONAIS":["1.601 - Valores a Repassar - Médicos","1.602 - Valores a Repassar - Terapeutas"],"Ajuste de Caixa 2026 - Inicio":[]}

    # ── Função para carregar plano de contas de arquivo ───────────────────────
    def carregar_plano(arquivo=None):
        """Lê arquivo Excel/CSV do plano de contas e retorna {cat: [subcats]}."""
        if arquivo is None:
            return PLANO_PADRAO.copy()
        try:
            if arquivo.name.endswith(".csv"):
                df = pd.read_csv(arquivo)
            else:
                df = pd.read_excel(arquivo, header=0)
            df.columns = [str(c).strip() for c in df.columns]
            # Detecta colunas
            col_cat = next((c for c in df.columns if "categ" in c.lower()), df.columns[0])
            col_sub = next((c for c in df.columns if "sub" in c.lower()), df.columns[1] if len(df.columns) > 1 else None)
            plano = {}
            for _, row in df.iterrows():
                cat = str(row[col_cat]).strip()
                if cat == "nan" or not cat:
                    continue
                sub = str(row[col_sub]).strip() if col_sub and pd.notna(row[col_sub]) else ""
                if cat not in plano:
                    plano[cat] = []
                if sub and sub != "nan":
                    plano[cat].append(sub)
            return plano if plano else PLANO_PADRAO.copy()
        except Exception as e:
            st.warning(f"Não foi possível ler o plano de contas: {e}. Usando o padrão embutido.")
            return PLANO_PADRAO.copy()

    # ── Contatos embutidos ────────────────────────────────────────────────────
    MEDICOS    = ["luciany","rossania","marilia","sarita","isadora","priscila","juliana","deodato","marcelo","marcello","airton","tarcizio","tarcízio","eulalio","raquel","nahara","paloma","sandra","carlos eduardo","isabela lima","ana camila","gisa"]
    TERAPEUTAS = ["andrezza","andressa","antonio clayton","marcia karina","jussara","dayrla","ceciane","wanderson","iasmim","katrine","norla","rosario","alessia","leticia","narllyanna","brenda","maria stheffany","sara micaela","vitorugo","rondinara","edilene","ana karolina"]
    PESSOAL    = ["cacilene","kacilene","iara","jessica pinto","simone","vanderlene","gleicyelle","gleycyelle","maria cacilene"]

    # ── Regras base ───────────────────────────────────────────────────────────
    REGRAS_BASE = [
        (["cx do dia","honorários","repasse","honorarios"],MEDICOS,"E","1.6 - RECEITAS DE TERCEIROS - NAO OPERACIONAIS","1.601 - Valores a Repassar - Médicos"),
        (["cx do dia","honorários","repasse","honorarios"],TERAPEUTAS,"E","1.6 - RECEITAS DE TERCEIROS - NAO OPERACIONAIS","1.602 - Valores a Repassar - Terapeutas"),
        (["repasse","honorários","honorarios","cx do dia"],MEDICOS,"S","6.1 - CUSTOS DE TERCEIROS - NAO OPERACIONAIS","6.601 - Repasse de Valor - Médicos"),
        (["repasse","honorários","honorarios","cx do dia","fusma"],TERAPEUTAS,"S","6.1 - CUSTOS DE TERCEIROS - NAO OPERACIONAIS","6.602 - Repasse de Valor - Terapeutas"),
        (["folha","salario","salário"],PESSOAL+["cacilene","kacilene"],"S","3.2 - DESPESAS COM PESSOAL","3.301 - Salarios (D)"),
        (["gratificação","gratificacao"],[],  "S","3.2 - DESPESAS COM PESSOAL","3.310 - Gratificação (D)"),
        (["agua","água","galão","galoes","galões","mineral"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.301 - Água e Esgoto"),
        (["energia","luz"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.307 - Energia Elétrica"),
        (["internet","telefone"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.315 - Telefone e Internet"),
        (["aluguel"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.303 - Aluguel"),
        (["limpeza","faxina"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.331 - Serviço de Limpeza "),
        (["manutenção","manut","refriger","ar condic"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.317 - Manutenção de Equipamento "),
        (["escritorio","impressora","tinta","papel","caneta"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.308 - Material de Escritório "),
        (["copa","cozinha","cafe","café","marmita","lanche","restaurante","bolo","pipoca","toureiro","atacarejo"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.310 - Material de Copa e Cozinha"),
        (["material de limpeza","detergente","sabao","sabão"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.312 - Material de Limpeza"),
        (["segurança","monitoramento","camera"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.313 - Segurança e Monitoramento"),
        (["marketing","publicidade","propaganda"],[],"S","3.3 - DESPESAS DE VENDAS E MARKETING","3.303 - Propaganda e publicidade"),
        (["detetizacao","detetização"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.326 - Manutencao e Conservacao"),
        (["armario","armário","movel","móvel","cadeira","mesa","gancho"],[],"S","4.1 - INVESTIMENTOS","4.401 - Móveis e Utensílios "),
        (["iof","juros limite"],[],"S","2.1 IMPOSTOS E TAXAS","2.102 - IOF"),
        (["simples","das "],[],"S","2.1 IMPOSTOS E TAXAS","2.101 - Simples Nacional (DAS)"),
        (["vacina","teste","exame","laborat"],[],"S","2.4 - CUSTOS DIRETOS COM INSUMOS (MAT)","2.401 - Teste/Vacinas para Revenda"),
        (["ajuste","troco"],[],"E","1.4 - RECEITAS FINANCEIRAS","1.401 - Ajuste de Caixa"),
        (["pró-labore","pro labore","prolabore"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.320 - Pró-labore"),
        (["prestação de serviço","prestacao","bpo"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.304 - Assessoria Financeira (BPO)"),
        (["devolução","devolveu","deposito","depósito"],[],"S","1.2 - RECEITAS NÃO OPERACIONAIS","1.203 - Reembolso de despesas"),
        (["retirada","retiradas"],[],"S","5.1 - MOVIMENTAÇÕES DE SÓCIOS / FINANCIAMENTOS","5.502 - Distribuição de Lucros"),
        (["montagem","instalação","instalacao","montar"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.319 - Serviços de Terceiros - Montagem e instalações"),
    ]

    # ── Storage persistente ───────────────────────────────────────────────────
    # ── Storage de mapeamento de contatos ──────────────────────────────────
    def carregar_mapa_contatos():
        """Retorna dict {palavra_chave_lower: nome_exato_md}"""
        try:
            dados = st.session_state.get("_contatos_mapa", None)
            if dados:
                return json.loads(dados)
        except Exception:
            pass
        return {}

    def salvar_mapa_contatos(mapa):
        st.session_state["_contatos_mapa"] = json.dumps(mapa, ensure_ascii=False)

    def carregar_base_md():
        """Retorna lista de nomes do Meu Dinheiro (salva no storage)."""
        try:
            dados = st.session_state.get("_base_contatos_md", None)
            if dados:
                return json.loads(dados)
        except Exception:
            pass
        return []

    def salvar_base_md(nomes):
        st.session_state["_base_contatos_md"] = json.dumps(nomes, ensure_ascii=False)

    def resolver_contato(contato_input, mapa, base_md):
        """
        Resolve contato do input para nome exato do Meu Dinheiro.
        Retorna (nome_resolvido, status):
          status = "mapa"    → encontrado no dicionário manual
          status = "auto"    → encontrado na base MD por match de palavra inteira
          status = "sem_match" → não encontrou, retorna original com ⚠️
        """
        import unicodedata as _ud
        def _n(s):
            return ''.join(c for c in _ud.normalize('NFD', str(s).lower().strip()) if _ud.category(c) != 'Mn')

        cn = _n(contato_input)

        # Camada 1: dicionário manual (match por palavra-chave)
        for chave, nome_md in mapa.items():
            if _n(chave) in cn or cn in _n(chave):
                return nome_md, "mapa"

        # Camada 2: auto-match na base MD
        # Usa match de palavra INTEIRA para evitar "iara" dentro de "naiara"
        palavras_input = [w for w in cn.split() if len(w) > 3]
        melhor_match = None
        melhor_score = 0
        for nome_md in base_md:
            nome_md_n = _n(nome_md)
            palavras_md = set(nome_md_n.split())
            score = sum(1 for p in palavras_input if p in palavras_md)  # match de palavra EXATA
            if score > melhor_score:
                melhor_score = score
                melhor_match = nome_md

        if melhor_score >= 1 and melhor_match:
            return melhor_match, "auto"

        # Camada 3: sem match
        return contato_input, "sem_match"

    def carregar_regras_aprendidas():
        try:
            dados = st.session_state.get("_regras_storage", None)
            if dados:
                return json.loads(dados)
        except Exception:
            pass
        return []

    def salvar_regras_aprendidas(regras):
        st.session_state["_regras_storage"] = json.dumps(regras, ensure_ascii=False)

    def get_chave(row):
        """Chave única por lançamento: data + contato + descrição + valor."""
        data  = str(row.get("Data","")).strip()
        cont  = str(row.get("Contato","")).strip().lower()
        desc  = str(row.get("Descricao","")).strip().lower()
        ent   = str(row.get("Entrada","")).strip()
        sai   = str(row.get("Saida","")).strip()
        return f"{data}|{cont}|{desc}|{ent}|{sai}"

    def carregar_exportados():
        try:
            dados = st.session_state.get("_exportados_storage", None)
            if dados:
                return set(json.loads(dados))
        except Exception:
            pass
        return set()

    def salvar_exportados(chaves: set):
        st.session_state["_exportados_storage"] = json.dumps(list(chaves), ensure_ascii=False)

    def classificar(contato, descricao, tipo_mov, regras_aprendidas):
        c = str(contato).lower().strip()
        d = str(descricao).lower().strip()
        t = tipo_mov
        for r in regras_aprendidas:
            if r.get("contato","") and r["contato"].lower() in c:
                if r.get("mov","") in ("", t):
                    return r["categoria"], r["subcategoria"], "Aprendida"
            if r.get("palavra",""):
                if r["palavra"].lower() in d or r["palavra"].lower() in c:
                    if r.get("mov","") in ("", t):
                        return r["categoria"], r["subcategoria"], "Aprendida"
        for palavras_desc, palavras_contato, mov, cat, sub in REGRAS_BASE:
            if mov != "" and mov != t:
                continue
            desc_match = any(p in d for p in palavras_desc) or any(p in c for p in palavras_desc)
            if palavras_contato:
                contato_match = any(p in c for p in palavras_contato)
                if desc_match and contato_match:
                    return cat, sub, "Alta"
                if contato_match:
                    return cat, sub, "Média"
            else:
                if desc_match:
                    return cat, sub, "Alta"
        return "", "", "Manual"

    def gerar_ofx(df_class, conta_nome="Caixinha"):
        linhas = ["OFXHEADER:100","DATA:OFSGML","VERSION:102","SECURITY:NONE",
                  "ENCODING:UTF-8","CHARSET:1252","COMPRESSION:NONE",
                  "OLDFILEUID:NONE","NEWFILEUID:NONE","",
                  "<OFX>","<BANKMSGSRSV1>","<STMTTRNRS>","<TRNUID>1001",
                  "<STATUS><CODE>0<SEVERITY>INFO</STATUS>","<STMTRS>",
                  "<CURDEF>BRL",
                  f"<BANKACCTFROM><BANKID>0000<ACCTID>{conta_nome}<ACCTTYPE>CHECKING</BANKACCTFROM>",
                  "<BANKTRANLIST>"]
        for i, row in df_class.iterrows():
            try:
                dt = pd.to_datetime(row["Data"], dayfirst=True, errors="coerce")
                dt_str = dt.strftime("%Y%m%d") if pd.notna(dt) else "20260101"
            except Exception:
                dt_str = "20260101"
            entrada = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
            saida   = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
            valor   = (entrada if pd.notna(entrada) and entrada > 0 else 0) - (saida if pd.notna(saida) and saida > 0 else 0)
            trntype = "CREDIT" if valor >= 0 else "DEBIT"
            memo    = str(row.get("Descricao",""))[:60].replace("<","").replace(">","")
            contato = str(row.get("Contato",""))[:40].replace("<","").replace(">","")
            linhas += ["<STMTTRN>",f"<TRNTYPE>{trntype}",f"<DTPOSTED>{dt_str}",
                       f"<TRNAMT>{valor:.2f}",f"<FITID>CX{dt_str}{i:04d}",
                       f"<n>{contato}",f"<MEMO>{memo}","</STMTTRN>"]
        linhas += ["</BANKTRANLIST>","</STMTRS>","</STMTTRNRS>","</BANKMSGSRSV1>","</OFX>"]
        return "\n".join(linhas)

    regras_aprendidas = carregar_regras_aprendidas()

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab_class, tab_plano, tab_contatos, tab_regras = st.tabs(["🤖  Classificar", "📋  Plano de Contas", "👤  Contatos", "📚  Regras Aprendidas"])

    # ════════════════════════════
    with tab_plano:
        st.markdown('<div class="page-sub">Gerencie categorias (mãe) e subcategorias (filhas) do plano de contas.</div>', unsafe_allow_html=True)

        # ── Helpers para carregar/salvar plano no session_state ───────────────
        def get_plano():
            if "_plano_carregado" in st.session_state:
                return json.loads(st.session_state["_plano_carregado"])
            return PLANO_PADRAO.copy()

        def set_plano(p):
            st.session_state["_plano_carregado"] = json.dumps(p, ensure_ascii=False)

        # ── Upload de arquivo ─────────────────────────────────────────────────
        st.markdown("**Carregar plano do Meu Dinheiro**")
        st.caption("Envie o arquivo exportado (Excel ou CSV). Deixe vazio para usar o padrão embutido.")
        f_plano = st.file_uploader(" ", type=["xlsx","xls","csv"], key="plano_file", label_visibility="collapsed")
        if f_plano:
            plano_importado = carregar_plano(f_plano)
            set_plano(plano_importado)
            st.success(f"Plano carregado: {len(plano_importado)} categorias, {sum(len(v) for v in plano_importado.values())} subcategorias.")
            st.rerun()

        plano = get_plano()
        cats_list = list(plano.keys())
        n_subs_total = sum(len(v) for v in plano.values())
        st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin:.5rem 0 1rem;">{len(cats_list)} categorias · {n_subs_total} subcategorias</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ════════════════════════════════════════════
        # SEÇÃO 1 — ADICIONAR
        # ════════════════════════════════════════════
        st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Adicionar</div>', unsafe_allow_html=True)

        add1, add2 = st.columns(2)
        with add1:
            st.markdown("**Nova categoria (mãe)**")
            nova_cat_nome = st.text_input(" ", placeholder="Ex: 7.1 - NOVA CATEGORIA", key="nova_cat_inp", label_visibility="collapsed")
            if st.button("➕  Adicionar categoria", key="btn_add_cat", use_container_width=True):
                if nova_cat_nome.strip():
                    p = get_plano()
                    if nova_cat_nome.strip() not in p:
                        p[nova_cat_nome.strip()] = []
                        set_plano(p)
                        st.success(f"Categoria '{nova_cat_nome.strip()}' adicionada!")
                        st.rerun()
                    else:
                        st.warning("Essa categoria já existe.")
                else:
                    st.warning("Digite o nome da categoria.")

        with add2:
            st.markdown("**Nova subcategoria (filha)**")
            cat_mae = st.selectbox("Vincular à categoria", ["— selecione —"] + cats_list, key="sub_cat_mae")
            nova_sub_nome = st.text_input(" ", placeholder="Ex: 7.101 - Descrição da subcategoria", key="nova_sub_inp", label_visibility="collapsed")
            if st.button("➕  Adicionar subcategoria", key="btn_add_sub", use_container_width=True):
                if cat_mae == "— selecione —":
                    st.warning("Selecione a categoria mãe.")
                elif not nova_sub_nome.strip():
                    st.warning("Digite o nome da subcategoria.")
                else:
                    p = get_plano()
                    if nova_sub_nome.strip() not in p[cat_mae]:
                        p[cat_mae].append(nova_sub_nome.strip())
                        set_plano(p)
                        st.success(f"Subcategoria adicionada em '{cat_mae}'!")
                        st.rerun()
                    else:
                        st.warning("Essa subcategoria já existe nesta categoria.")

        st.markdown("---")

        # ════════════════════════════════════════════
        # SEÇÃO 2 — EDITAR
        # ════════════════════════════════════════════
        st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Editar</div>', unsafe_allow_html=True)

        ed1, ed2 = st.columns(2)
        with ed1:
            st.markdown("**Renomear categoria (mãe)**")
            cat_renomear = st.selectbox("Categoria a renomear", ["— selecione —"] + cats_list, key="cat_renomear_sel")
            novo_nome_cat = st.text_input(" ", placeholder="Novo nome", key="novo_nome_cat_inp", label_visibility="collapsed")
            if st.button("✏️  Renomear categoria", key="btn_rename_cat", use_container_width=True):
                if cat_renomear == "— selecione —":
                    st.warning("Selecione a categoria.")
                elif not novo_nome_cat.strip():
                    st.warning("Digite o novo nome.")
                elif novo_nome_cat.strip() == cat_renomear:
                    st.warning("O nome é igual ao atual.")
                else:
                    p = get_plano()
                    # Reconstrói dict preservando a ordem
                    p_novo = {}
                    for k, v in p.items():
                        if k == cat_renomear:
                            p_novo[novo_nome_cat.strip()] = v
                        else:
                            p_novo[k] = v
                    set_plano(p_novo)
                    st.success(f"'{cat_renomear}' → '{novo_nome_cat.strip()}'")
                    st.rerun()

        with ed2:
            st.markdown("**Renomear subcategoria (filha)**")
            cat_mae_ed = st.selectbox("Categoria mãe", ["— selecione —"] + cats_list, key="sub_ed_mae")
            if cat_mae_ed != "— selecione —":
                subs_da_cat = plano.get(cat_mae_ed, [])
                sub_renomear = st.selectbox("Subcategoria a renomear", ["— selecione —"] + subs_da_cat, key="sub_renomear_sel")
                novo_nome_sub = st.text_input(" ", placeholder="Novo nome", key="novo_nome_sub_inp", label_visibility="collapsed")
                if st.button("✏️  Renomear subcategoria", key="btn_rename_sub", use_container_width=True):
                    if sub_renomear == "— selecione —":
                        st.warning("Selecione a subcategoria.")
                    elif not novo_nome_sub.strip():
                        st.warning("Digite o novo nome.")
                    else:
                        p = get_plano()
                        idx = p[cat_mae_ed].index(sub_renomear)
                        p[cat_mae_ed][idx] = novo_nome_sub.strip()
                        set_plano(p)
                        st.success(f"'{sub_renomear}' → '{novo_nome_sub.strip()}'")
                        st.rerun()
            else:
                st.caption("Selecione a categoria mãe primeiro.")

        st.markdown("---")

        # ════════════════════════════════════════════
        # SEÇÃO 3 — EXCLUIR
        # ════════════════════════════════════════════
        st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Excluir</div>', unsafe_allow_html=True)

        ex1, ex2 = st.columns(2)
        with ex1:
            st.markdown("**Excluir categoria (mãe)**")
            st.caption("⚠️ Remove a categoria e todas as subcategorias vinculadas.")
            cat_excluir = st.selectbox("Categoria a excluir", ["— selecione —"] + cats_list, key="cat_excluir_sel")
            if cat_excluir != "— selecione —":
                n_filhas = len(plano.get(cat_excluir, []))
                if n_filhas > 0:
                    st.markdown(f'<div style="font-size:0.8rem;color:#f87171;margin-bottom:6px;">Esta categoria tem {n_filhas} subcategoria(s) que serão removidas junto.</div>', unsafe_allow_html=True)
                confirmar_cat = st.checkbox(f"Confirmo a exclusão de '{cat_excluir}'", key="confirm_del_cat")
                if st.button("🗑️  Excluir categoria", key="btn_del_cat", use_container_width=True):
                    if confirmar_cat:
                        p = get_plano()
                        del p[cat_excluir]
                        set_plano(p)
                        st.success(f"Categoria '{cat_excluir}' excluída!")
                        st.rerun()
                    else:
                        st.warning("Marque a caixa de confirmação para excluir.")

        with ex2:
            st.markdown("**Excluir subcategoria (filha)**")
            st.caption("Remove apenas a subcategoria. A categoria mãe permanece intacta.")
            cat_mae_ex = st.selectbox("Categoria mãe", ["— selecione —"] + cats_list, key="sub_ex_mae")
            if cat_mae_ex != "— selecione —":
                subs_ex = plano.get(cat_mae_ex, [])
                if subs_ex:
                    sub_excluir = st.selectbox("Subcategoria a excluir", ["— selecione —"] + subs_ex, key="sub_excluir_sel")
                    if sub_excluir != "— selecione —":
                        confirmar_sub = st.checkbox(f"Confirmo a exclusão de '{sub_excluir}'", key="confirm_del_sub")
                        if st.button("🗑️  Excluir subcategoria", key="btn_del_sub", use_container_width=True):
                            if confirmar_sub:
                                p = get_plano()
                                p[cat_mae_ex].remove(sub_excluir)
                                set_plano(p)
                                st.success(f"Subcategoria '{sub_excluir}' excluída. Categoria '{cat_mae_ex}' mantida.")
                                st.rerun()
                            else:
                                st.warning("Marque a caixa de confirmação para excluir.")
                else:
                    st.caption("Esta categoria não tem subcategorias.")
            else:
                st.caption("Selecione a categoria mãe primeiro.")

        st.markdown("---")

        # ════════════════════════════════════════════
        # SEÇÃO 4 — VISUALIZAR E EXPORTAR
        # ════════════════════════════════════════════
        st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Visualizar plano atual</div>', unsafe_allow_html=True)

        for cat, subs in plano.items():
            with st.expander(f"**{cat}** — {len(subs)} subcategoria(s)"):
                if subs:
                    for s in subs:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;↳ {s}")
                else:
                    st.caption("Sem subcategorias cadastradas.")

        st.markdown("<br>", unsafe_allow_html=True)
        rows_dl = []
        for cat, subs in plano.items():
            if subs:
                for s in subs:
                    rows_dl.append({"Categoria": cat, "Subcategoria": s})
            else:
                rows_dl.append({"Categoria": cat, "Subcategoria": ""})
        st.download_button(
            "⬇️  Baixar plano atualizado (Excel)",
            data=to_excel_bytes(pd.DataFrame(rows_dl)),
            file_name=f"plano_contas_crs_{datetime.today().strftime('%d%m%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


    # ════════════════════════════
    with tab_class:
        # Carrega plano vigente
        if "_plano_carregado" in st.session_state:
            PLANO_CATS_DIN  = list(json.loads(st.session_state["_plano_carregado"]).keys())
            PLANO_SUBS_DIN  = json.loads(st.session_state["_plano_carregado"])
        else:
            PLANO_CATS_DIN  = list(PLANO_PADRAO.keys())
            PLANO_SUBS_DIN  = PLANO_PADRAO

        subs_flat = [""] + sorted(set(s for lst in PLANO_SUBS_DIN.values() for s in lst))

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown("**Planilha da Caixinha (Excel ou CSV)**")
            st.caption("Excel com abas mensais · ou CSV exportado diretamente")
            f_caixa = st.file_uploader(" ", type=["xlsx","xls","csv"], key="class_file", label_visibility="collapsed")
        with col_u2:
            st.markdown("**Cadastro de Contatos (opcional)**")
            f_contatos = st.file_uploader(" ", type=["xlsx","xls"], key="class_contatos", label_visibility="collapsed")

        if f_contatos:
            try:
                df_con_up = pd.ExcelFile(f_contatos).parse(0, header=0)
                extra_med = df_con_up[df_con_up["Categoria"].astype(str).str.contains("iatria|édico|eciatra|Pediatra", na=False, case=False)]["Nome"].str.lower().tolist()
                extra_ter = df_con_up[df_con_up["Categoria"].astype(str).str.contains("terapia|psicol|fono|nutri|fisio|musico|neuropsico|psicoped", na=False, case=False)]["Nome"].str.lower().tolist()
                MEDICOS    += extra_med
                TERAPEUTAS += extra_ter
                st.success(f"Cadastro atualizado: +{len(extra_med)} médicos, +{len(extra_ter)} terapeutas")
            except Exception as e:
                st.warning(f"Não foi possível ler o cadastro: {e}")

        if not f_caixa:
            st.markdown("""
            <div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;">
                <div style="font-size:2rem;margin-bottom:.5rem;">🤖</div>
                <div style="color:#556688;font-size:0.85rem;">Carregue a planilha Excel ou CSV da Caixinha para iniciar</div>
            </div>""", unsafe_allow_html=True)
            st.stop()

        def parse_caixinha_df(df_raw):
            """Normaliza colunas do DataFrame da Caixinha (Excel ou CSV)."""
            # Detecta linha de cabeçalho buscando pela palavra DATA
            header_row = 0
            for i, row in df_raw.iterrows():
                if "DATA" in [str(v).upper().strip() for v in row.values]:
                    header_row = i
                    break
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
                elif "SA" in cu and "DO" not in cu and len(c) < 10: col_map[c] = "Saida"
                elif "SALDO" in cu: col_map[c] = "Saldo"
            df_raw = df_raw.rename(columns=col_map)
            needed = [c for c in ["Data","Contato","Descricao","Entrada","Saida"] if c in df_raw.columns]
            df_work = df_raw[needed].copy()
            df_work = df_work[
                df_work["Data"].notna() &
                (df_work["Data"].astype(str).str.strip() != "") &
                (df_work["Data"].astype(str) != "nan")
            ]
            df_work["Data"] = pd.to_datetime(
                df_work["Data"], dayfirst=True, errors="coerce"
            ).dt.strftime("%d/%m/%Y")
            return df_work[df_work["Data"].notna()].reset_index(drop=True)

        # ── Carrega Excel ou CSV ───────────────────────────────────────────
        nome_arquivo = f_caixa.name.lower()
        aba_sel = None

        if nome_arquivo.endswith(".csv"):
            # CSV — lê com detecção de encoding e separador
            raw_bytes = f_caixa.read()
            df_csv_raw = None
            for enc in ["latin-1","cp1252","iso-8859-1","utf-8","utf-8-sig"]:
                for sep in [";",",","\t"]:
                    try:
                        import io as _io
                        df_csv_raw = pd.read_csv(
                            _io.BytesIO(raw_bytes), encoding=enc, sep=sep,
                            header=None, on_bad_lines="skip", engine="python"
                        )
                        if len(df_csv_raw.columns) > 3:
                            break
                    except Exception:
                        continue
                if df_csv_raw is not None and len(df_csv_raw.columns) > 3:
                    break

            if df_csv_raw is None or df_csv_raw.empty:
                st.error("Não foi possível ler o CSV. Verifique o formato.")
                st.stop()

            # Nome do arquivo sem extensão como identificador
            aba_sel = f_caixa.name.replace(".csv","").replace("_"," ")
            try:
                df_work = parse_caixinha_df(df_csv_raw)
            except Exception as e:
                st.error(f"Erro ao processar CSV: {e}")
                st.stop()

        else:
            # Excel — seleciona aba
            try:
                xl_caixa = pd.ExcelFile(f_caixa)
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
                st.stop()

            abas_cx = [a for a in xl_caixa.sheet_names if "caixa" in a.lower()]
            aba_sel = st.selectbox(
                "Selecione o mês", abas_cx if abas_cx else xl_caixa.sheet_names, key="class_aba"
            )
            try:
                df_raw = xl_caixa.parse(aba_sel, header=None)
                df_work = parse_caixinha_df(df_raw)
            except Exception as e:
                st.error(f"Erro ao ler aba: {e}")
                st.stop()

        st.markdown(
            f'<div style="font-size:0.82rem;color:#8899BB;margin:.5rem 0 1rem;">' +
            (f'Arquivo: <strong style="color:#C9A84C;">{aba_sel}</strong>' if nome_arquivo.endswith(".csv") else f'Aba: <strong style="color:#C9A84C;">{aba_sel}</strong>') +
            f' · {len(df_work)} lançamentos</div>',
            unsafe_allow_html=True
        )

        # ── Contas disponíveis para transferência ────────────────────────────
        CONTAS_DISPONIVEIS = [
            "",
            "Fechamento de caixa 2025;2026",
            "Itaú 2025;2026",
            "Banco do Brasil",
            "Caixinha 2025;2026",
        ]
        CONTA_PADRAO_CAIXINHA = "Caixinha 2025;2026"

        # ── Detecta se lançamento é Transferência entre contas ────────────────
        TODOS_PROFISSIONAIS = MEDICOS + TERAPEUTAS + PESSOAL

        # Palavras que indicam DESPESA/MOVIMENTAÇÃO direta mesmo com profissional no contato
        # Normalizadas sem acento para comparação robusta
        PALAVRAS_DESPESA_DIRETA = [
            # Marketing / pessoal
            "instagram","facebook","marketing","publicidade","propaganda",
            "gratificacao","salario","vale","uniforme","ferias",
            "curso","treinamento","adiantamento","inss","fgts","rescisao",
            # Retiradas de sócios / movimentações (5.1)
            "retirada","retiradas","pro labore","prolabore","distribuicao",
            # Repasses externos (Fusma = repasse de terceiros)
            "repasse externo",
            # Despesas diversas
            "reembolso","material","limpeza","compra","nota fiscal","servico",
            "remedio","medicamento","farmacia","lampada","toner","copia",
            "energia","agua","internet","telefone","aluguel","condominio",
            "manutencao","conserto","reparo","instalacao","montagem",
            "salgado","bolo","cafe","lanche","marmita","restaurante",
            "camiseta","brinde","aniversario","evento","joia","joias",
            "papelaria","viagem","passagem","hospedagem","capa",
            "protestada","energia protestada",
        ]

        def detectar_tipo_lancamento(contato, descricao):
            """
            Retorna (tipo, conta_destino):
            - "Transferência" + "Fechamento de caixa 2025;2026"  → Cx do dia / fechamento
            - "Receita" / "Despesa" + ""                          → lançamento direto

            Regras em ordem de prioridade:
            1. "Cx do dia" ou "Fechamento Cx" na descrição → sempre Transferência
            2. Profissional no contato + descrição NÃO é despesa direta → Transferência
            3. Qualquer outra coisa → Receita ou Despesa por sinal
            """
            import unicodedata as _ud
            def _norm(s): return ''.join(c for c in _ud.normalize('NFD', str(s).lower().strip()) if _ud.category(c) != 'Mn')

            c = _norm(contato)
            d = _norm(descricao)

            # Regra 1: palavras-chave de transferência na descrição
            palavras_transf = ["cx do dia","fechamento cx","fechamento de cx","cx dia"]
            if any(p in d for p in palavras_transf):
                return "Transferência", "Fechamento de caixa 2025;2026"

            # Regra 2: profissional no contato mas SEM palavras de despesa direta
            eh_profissional   = any(_norm(p) in c for p in TODOS_PROFISSIONAIS)
            eh_despesa_direta = any(_norm(p) in d for p in PALAVRAS_DESPESA_DIRETA)
            if eh_profissional and not eh_despesa_direta:
                return "Transferência", "Fechamento de caixa 2025;2026"

            return None, ""  # será definido por sinal (E/S)

        exportados = carregar_exportados()
        n_ja_exportados = sum(1 for _, row in df_work.iterrows() if get_chave(row) in exportados)

        # Banner informativo se houver lançamentos já exportados
        if n_ja_exportados > 0:
            n_novos = len(df_work) - n_ja_exportados
            st.markdown(f"""
            <div style="background:#162236;border-left:3px solid #C9A84C;border-radius:0 8px 8px 0;
                        padding:8px 14px;font-size:0.82rem;margin-bottom:12px;">
                📋 <strong style="color:#C9A84C;">{n_ja_exportados} lançamentos</strong>
                <span style="color:#8899BB;">já foram exportados para o Meu Dinheiro anteriormente.</span>
                <strong style="color:#4ade80;">{n_novos} novos</strong>
                <span style="color:#8899BB;">para revisar.</span>
            </div>""", unsafe_allow_html=True)

        mapa_contatos = carregar_mapa_contatos()
        base_md       = carregar_base_md()

        if st.button("🤖  Classificar Automaticamente", key="btn_class"):
            cats, subs, confs, tipos, contas_dest, ja_exp_flags, contatos_md, status_contatos = [], [], [], [], [], [], [], []
            for _, row in df_work.iterrows():
                entrada = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
                saida   = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
                tmov    = "E" if (pd.notna(entrada) and entrada > 0) else "S"
                contato   = str(row.get("Contato",""))
                descricao = str(row.get("Descricao",""))
                chave     = get_chave(row)
                ja_exp    = chave in exportados

                # Detecta tipo
                tipo_det, conta_det = detectar_tipo_lancamento(contato, descricao)
                if tipo_det == "Transferência":
                    tipos.append("Transferência")
                    contas_dest.append(conta_det)
                    cats.append("")
                    subs.append("")
                    confs.append("Auto" if not ja_exp else "✅ Exportado")
                else:
                    tipo_fin = "Receita" if tmov == "E" else "Despesa"
                    tipos.append(tipo_fin)
                    contas_dest.append("")
                    if ja_exp:
                        cats.append(""); subs.append(""); confs.append("✅ Exportado")
                    else:
                        cat, sub, conf = classificar(contato, descricao, tmov, regras_aprendidas)
                        cats.append(cat); subs.append(sub); confs.append(conf)
                ja_exp_flags.append("✅ Sim" if ja_exp else "🆕 Novo")

                # Resolve contato — só para Receita/Despesa
                tipo_final = tipos[-1]
                if tipo_final == "Transferência":
                    contatos_md.append("")
                    status_contatos.append("transf")
                else:
                    nome_res, status_res = resolver_contato(
                        str(row.get("Contato","")), mapa_contatos, base_md
                    )
                    contatos_md.append(nome_res)
                    status_contatos.append(status_res)

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

        # Garante coluna Status Export
        if "Status Export" not in df_class.columns:
            df_class["Status Export"] = "🆕 Novo"

        total_exp = (df_class["Status Export"]=="✅ Sim").sum()
        total_nov = (df_class["Status Export"]=="🆕 Novo").sum()
        alta      = (df_class["Confiança"]=="Alta").sum()
        aprend    = (df_class["Confiança"]=="Aprendida").sum()
        manual    = (df_class[~df_class["Status Export"].str.contains("Sim")]["Confiança"]=="Manual").sum()

        m1,m2,m3,m4,m5 = st.columns(5)
        for col,lbl,val,cls in [
            (m1,"Total",str(len(df_class)),""),
            (m2,"Já exportados",str(total_exp),"green"),
            (m3,"Novos",str(total_nov),"amber" if total_nov>0 else "green"),
            (m4,"Aprendidas",str(aprend),"green"),
            (m5,"Revisão manual",str(manual),"red" if manual>0 else "green"),
        ]:
            col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # ── Alerta de contatos sem match ─────────────────────────────────────
        if "_status_contato" in df_class.columns:
            n_sem_match = (df_class["_status_contato"] == "sem_match").sum()
            if n_sem_match > 0:
                nomes_sem = df_class[df_class["_status_contato"]=="sem_match"]["Contato MD"].tolist()
                nomes_uniq = list(dict.fromkeys(nomes_sem))[:5]
                st.markdown(f"""
                <div style="background:#422006;border-left:3px solid #f97316;border-radius:0 8px 8px 0;
                            padding:10px 14px;font-size:0.82rem;margin-bottom:12px;">
                    ⚠️ <strong style="color:#fcd34d;">{n_sem_match} contato(s) sem match</strong>
                    <span style="color:#fed7aa;"> na base do Meu Dinheiro — revise na coluna <strong>Contato MD</strong>
                    ou cadastre no dicionário (aba Contatos):</span><br>
                    <span style="color:#fdba74;font-size:0.78rem;">{" · ".join(str(n) for n in nomes_uniq if n and str(n) != "nan")}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:0.82rem;color:#C9A84C;">
            ✏️ Edite <strong>Categoria</strong>, <strong>SubCategoria</strong> e <strong>Contato MD</strong> diretamente na tabela.
            Clique em <strong>Salvar correções</strong> para criar regras automáticas para os próximos meses.
        </div>""", unsafe_allow_html=True)

        # Garante colunas existem mesmo se recarregado sem reclassificar
        for col_init, val_init in [("Tipo Lançamento",""), ("Conta Destino",""),
                                   ("Contato MD",""), ("_status_contato","sem_match")]:
            if col_init not in df_class.columns:
                df_class[col_init] = val_init

        df_edit = st.data_editor(
            df_class,
            column_config={
                "Tipo Lançamento": st.column_config.SelectboxColumn(
                    "Tipo Lançamento",
                    options=["Receita","Despesa","Transferência"],
                    width="medium",
                    help="Transferência = entre contas internas (sem Categoria). Receita/Despesa = lançamento direto com Categoria."
                ),
                "Conta Destino":   st.column_config.SelectboxColumn(
                    "Conta Destino",
                    options=CONTAS_DISPONIVEIS,
                    width="large",
                    help="Preencha só quando Tipo = Transferência"
                ),
                "Categoria":    st.column_config.SelectboxColumn("Categoria",    options=PLANO_CATS_DIN, width="large"),
                "SubCategoria": st.column_config.SelectboxColumn("SubCategoria", options=subs_flat,      width="large"),
                "Status Export":st.column_config.TextColumn("Export", disabled=True, width="small"),
                "Contato MD":   st.column_config.TextColumn("Contato MD", width="medium",
                    help="Nome exato no Meu Dinheiro. ⚠️ = sem match na base — edite antes de exportar."),
                "Confiança":    st.column_config.TextColumn("Confiança", disabled=True, width="small"),
                "Contato":      st.column_config.TextColumn("Contato"),
                "Descricao":    st.column_config.TextColumn("Descrição", disabled=True),
                "Data":         st.column_config.TextColumn("Data",      disabled=True, width="small"),
                "Entrada":      st.column_config.TextColumn("Entrada",   disabled=True, width="small"),
                "Saida":        st.column_config.TextColumn("Saída",     disabled=True, width="small"),
            },
            use_container_width=True, hide_index=True, key="editor_class",
        )

        col_sv, _ = st.columns([1,2])
        with col_sv:
            if st.button("💾  Salvar correções e criar regras", key="btn_salvar_regras", use_container_width=True):
                novas_regras = list(regras_aprendidas)
                n_novas = 0
                orig = st.session_state["df_classificado"]
                for i, row in df_edit.iterrows():
                    orig_cat = orig.loc[i,"Categoria"] if i < len(orig) else ""
                    new_cat  = row.get("Categoria","")
                    new_sub  = row.get("SubCategoria","")
                    if (new_cat != orig_cat) and new_cat:
                        contato   = str(row.get("Contato","")).strip()
                        descricao = str(row.get("Descricao","")).strip()
                        entrada   = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
                        saida     = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
                        mov       = "E" if (pd.notna(entrada) and entrada > 0) else "S"
                        if contato and len(contato) > 2:
                            r = {"tipo":"contato","contato":contato.lower(),"palavra":"","mov":mov,"categoria":new_cat,"subcategoria":new_sub,"origem":f"{aba_sel}"}
                            if not any(x.get("contato","").lower()==r["contato"] and x.get("mov","")==mov for x in novas_regras):
                                novas_regras.insert(0, r); n_novas += 1
                        palavras = [p for p in descricao.lower().split() if len(p) > 4]
                        if palavras:
                            chave = palavras[0]
                            r2 = {"tipo":"descricao","contato":"","palavra":chave,"mov":mov,"categoria":new_cat,"subcategoria":new_sub,"origem":f"{aba_sel}"}
                            if not any(x.get("palavra","").lower()==chave and x.get("mov","")==mov for x in novas_regras):
                                novas_regras.insert(0, r2); n_novas += 1
                salvar_regras_aprendidas(novas_regras)
                st.session_state["df_classificado"] = df_edit.copy()
                st.success(f"✅ {n_novas} novas regras criadas!")
                st.rerun()

        st.markdown("---")
        nome_base = f"caixinha_{aba_sel.replace(' ','_').replace('$','').strip()}_{datetime.today().strftime('%d%m%Y')}"

        # ── Monta CSV no formato EXATO do Meu Dinheiro (16 colunas) ─────────
        def montar_csv_meu_dinheiro(df, conta_nome="Caixinha 2025;2026"):
            """
            Gera CSV no formato de importação do Meu Dinheiro Web — 16 colunas.
            Valor: negativo = saída/despesa, positivo = entrada/receita (sem aspas, sem R$).
            Transferência: valor positivo quando entrada, negativo quando saída.
            Separador: vírgula. Encoding: utf-8.
            """
            def fmt_num(v, negativo=False):
                """
                Formata número no padrão do Meu Dinheiro:
                vírgula como decimal, sem ponto milhar — ex: -4,00 ou 300,00
                Pandas coloca aspas quando o valor contém vírgula e o separador é vírgula,
                o que é aceito pelo Meu Dinheiro Web.
                """
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
                # Remove prefixo ⚠️ se presente (sem match — usa original)
                contato_md_clean = contato_md.lstrip("⚠️ ").strip() if contato_md else contato
                descricao  = str(r.get("Descricao",""))[:100].strip()
                data       = str(r.get("Data","")).strip()

                val_e = entrada if (pd.notna(entrada) and entrada > 0) else 0.0
                val_s = saida   if (pd.notna(saida)   and saida   > 0) else 0.0
                eh_saida = val_s > 0 and val_e == 0

                # Nome limpo — remove título Dra/Dr
                nome_limpo = " ".join(w for w in contato.split() if w.lower().rstrip(".") not in ("dra","dr")).strip()

                if tipo == "Transferência":
                    # Descrição: "Cx Luciany 01/04/2026" / "Fusma Norla fevereiro"
                    desc_lower = descricao.lower()
                    if "cx do dia" in desc_lower or "cx dia" in desc_lower:
                        prefixo = "Cx"
                    elif "fechamento cx" in desc_lower or "fechamento de cx" in desc_lower:
                        prefixo = "Fechamento Cx"
                    elif "fusma" in desc_lower:
                        prefixo = "Fusma"
                    else:
                        prefixo = descricao.split()[0] if descricao else "Cx"
                    desc_export    = f"{prefixo} {nome_limpo} {data}".strip() if nome_limpo else descricao
                    valor_str      = fmt_num(val_s, negativo=True) if eh_saida else fmt_num(val_e)
                    conta_transf   = conta_dest if conta_dest else "Fechamento de caixa 2025;2026"
                    cat_export     = ""
                    sub_export     = ""
                    contato_export = ""  # vazio nas transferências
                elif tipo == "Receita":
                    desc_export    = descricao
                    valor_str      = fmt_num(val_e, negativo=False)
                    conta_transf   = ""
                    cat_export     = cat
                    sub_export     = sub
                    contato_export = contato_md_clean or contato
                else:  # Despesa
                    desc_export    = descricao
                    valor_str      = fmt_num(val_s, negativo=True)
                    conta_transf   = ""
                    cat_export     = cat
                    sub_export     = sub
                    contato_export = contato_md_clean or contato

                rows.append({
                    "Data":                data,
                    "Valor":               valor_str,
                    "Descrição":           desc_export,
                    "Conta":               conta_nome,
                    "Conta Transferência": conta_transf,
                    "Cartão":              "",
                    "Categoria":           cat_export,
                    "Subcategoria":        sub_export,
                    "Contato":             contato_export,
                    "Centro":              "",
                    "Projeto":             "",
                    "Forma":               "",
                    "N. Documento":        "",
                    "Observações":         "",
                    "Data Competência":    data,
                    "Tags":                "",
                })
            return pd.DataFrame(rows)

        # Filtra só os NOVOS para exportar (exclui já exportados)
        status_col = "Status Export" if "Status Export" in df_edit.columns else None
        if status_col:
            df_novos = df_edit[df_edit[status_col] != "✅ Sim"].copy()
        else:
            df_novos = df_edit.copy()

        df_csv_md = montar_csv_meu_dinheiro(df_novos, conta_nome=CONTA_PADRAO_CAIXINHA)

        n_novos_export = len(df_novos)
        n_ja_exp_edit  = len(df_edit) - n_novos_export

        dl1, dl2, dl3 = st.columns(3)
        with dl1:
            st.markdown("**CSV — Importar no Meu Dinheiro**")
            if n_ja_exp_edit > 0:
                st.caption(f"Apenas os {n_novos_export} novos · {n_ja_exp_edit} já exportados ignorados")
            else:
                st.caption("16 colunas · Transferências com Conta Destino · Receitas/Despesas com Categoria")

            import io as _io, csv as _csv
            buf = _io.StringIO()
            df_csv_md.to_csv(buf, index=False, sep=",", quoting=_csv.QUOTE_MINIMAL)
            csv_bytes = buf.getvalue().encode("utf-8")

            if st.download_button(
                f"⬇️  Baixar CSV ({n_novos_export} lançamentos)",
                data=csv_bytes,
                file_name=f"{nome_base}_meu_dinheiro.csv",
                mime="text/csv"
            ):
                # Marca os novos como exportados no storage
                exportados_atual = carregar_exportados()
                for _, row in df_novos.iterrows():
                    exportados_atual.add(get_chave(row))
                salvar_exportados(exportados_atual)
                st.success(f"✅ {n_novos_export} lançamentos marcados como exportados!")
                st.rerun()
        with dl2:
            st.markdown("**Excel — revisão**")
            st.caption("Planilha completa com coluna de confiança")
            st.download_button("⬇️  Baixar Excel", data=to_excel_bytes(df_edit), file_name=f"{nome_base}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with dl3:
            st.markdown("**OFX — extrato bancário**")
            st.caption("Para conciliação — requer classificação manual no sistema")
            st.download_button("⬇️  Baixar OFX", data=gerar_ofx(df_edit, conta_nome=aba_sel).encode("utf-8"), file_name=f"{nome_base}.ofx", mime="application/octet-stream")

        st.markdown("""
        <div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;margin-top:8px;font-size:0.8rem;color:#8899BB;">
            💡 <strong style="color:#C9A84C;">Dica de importação no Meu Dinheiro:</strong>
            Vá em <strong>Lançamentos → Importar → selecione o CSV</strong>.
            Transferências já chegam com <strong>Conta Destino</strong> preenchida — o sistema cria os dois lados automaticamente.
            Receitas e Despesas já chegam com <strong>Categoria</strong> — sem retrabalho.
        </div>""", unsafe_allow_html=True)

    # ════════════════════════════
    # ════════════════════════════════════════════════════════════════
    with tab_contatos:
        st.markdown('<div class="page-sub">Mapeie contatos do input para os nomes exatos do Meu Dinheiro. Salvo permanentemente no app.</div>', unsafe_allow_html=True)

        mapa_atual = carregar_mapa_contatos()
        base_atual = carregar_base_md()

        # ── Upload base de contatos do Meu Dinheiro ───────────────────────
        st.markdown("**Carregar base de contatos do Meu Dinheiro**")
        st.caption("Upload do arquivo exportado em Cadastros → Contatos (Excel). Salvo automaticamente para os próximos meses.")
        f_base_md = st.file_uploader(" ", type=["xlsx","xls","csv"], key="base_md_upload", label_visibility="collapsed")
        if f_base_md:
            try:
                df_base = pd.read_excel(f_base_md) if f_base_md.name.endswith((".xlsx",".xls")) else pd.read_csv(f_base_md)
                col_nome = next((c for c in df_base.columns if "nome" in c.lower()), df_base.columns[0])
                nomes_base = [str(n).strip() for n in df_base[col_nome].dropna() if str(n).strip()]
                salvar_base_md(nomes_base)
                base_atual = nomes_base
                st.success(f"✅ {len(nomes_base)} contatos carregados e salvos!")
            except Exception as e:
                st.warning(f"Erro ao ler base: {e}")

        if base_atual:
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-bottom:12px;">📋 {len(base_atual)} contatos na base — auto-match ativo</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:0.8rem;color:#8899BB;margin-bottom:12px;">Nenhuma base carregada — apenas dicionário manual será usado.</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Dicionário manual ─────────────────────────────────────────────
        st.markdown("**Dicionário manual de contatos**")
        st.caption("Palavra-chave do input → Nome exato no Meu Dinheiro. Tem prioridade máxima sobre o auto-match.")

        # Adicionar novo mapeamento
        ma1, ma2, ma3 = st.columns([2,3,1])
        with ma1:
            nova_chave = st.text_input(" ", placeholder="Palavra-chave (ex: agua mineral)", key="novo_map_chave", label_visibility="collapsed")
        with ma2:
            if base_atual:
                novo_nome = st.selectbox(" ", ["— Digite ou selecione —"] + sorted(base_atual), key="novo_map_nome_sel", label_visibility="collapsed")
                if novo_nome == "— Digite ou selecione —":
                    novo_nome = st.text_input(" ", placeholder="Ou digite o nome exato", key="novo_map_nome_txt", label_visibility="collapsed")
            else:
                novo_nome = st.text_input(" ", placeholder="Nome exato no Meu Dinheiro", key="novo_map_nome_txt", label_visibility="collapsed")
        with ma3:
            if st.button("➕ Adicionar", key="btn_add_mapa", use_container_width=True):
                if nova_chave.strip() and novo_nome and novo_nome not in ("— Digite ou selecione —",""):
                    mapa_edit = carregar_mapa_contatos()
                    mapa_edit[nova_chave.strip().lower()] = novo_nome.strip()
                    salvar_mapa_contatos(mapa_edit)
                    st.success(f"Mapeamento adicionado: '{nova_chave}' → '{novo_nome}'")
                    st.rerun()
                else:
                    st.warning("Preencha os dois campos.")

        # Tabela do dicionário atual
        st.markdown("<br>", unsafe_allow_html=True)
        if mapa_atual:
            st.markdown(f'<div style="font-size:0.8rem;color:#8899BB;margin-bottom:8px;">{len(mapa_atual)} mapeamentos salvos</div>', unsafe_allow_html=True)
            df_mapa = pd.DataFrame([{"Palavra-chave (input)": k, "Nome no Meu Dinheiro": v} for k,v in mapa_atual.items()])
            df_mapa_edit = st.data_editor(
                df_mapa,
                column_config={
                    "Palavra-chave (input)": st.column_config.TextColumn("Palavra-chave (input)", width="medium"),
                    "Nome no Meu Dinheiro":  st.column_config.TextColumn("Nome no Meu Dinheiro",  width="large"),
                },
                num_rows="dynamic", use_container_width=True, hide_index=True, key="editor_mapa"
            )
            mc1, mc2 = st.columns(2)
            with mc1:
                if st.button("💾  Salvar alterações", key="btn_save_mapa", use_container_width=True):
                    novo_mapa = {str(r["Palavra-chave (input)"]).strip().lower(): str(r["Nome no Meu Dinheiro"]).strip()
                                 for _, r in df_mapa_edit.iterrows()
                                 if str(r.get("Palavra-chave (input)","")).strip()}
                    salvar_mapa_contatos(novo_mapa)
                    st.success("Dicionário salvo!")
                    st.rerun()
            with mc2:
                st.download_button("⬇️  Exportar dicionário JSON",
                    data=json.dumps(mapa_atual, ensure_ascii=False, indent=2).encode("utf-8"),
                    file_name="contatos_mapa_crs.json", mime="application/json",
                    use_container_width=True)
        else:
            st.info("Nenhum mapeamento manual ainda. Adicione acima para começar.")

        # ── Preview auto-match ────────────────────────────────────────────
        if base_atual:
            st.markdown("---")
            st.markdown("**Testar resolução de contato**")
            st.caption("Simule como um contato do input será resolvido.")
            tc1, tc2 = st.columns(2)
            with tc1:
                teste_contato = st.text_input(" ", placeholder="Digite um nome do input (ex: agua mineral)", key="teste_contato_inp", label_visibility="collapsed")
            with tc2:
                if teste_contato:
                    nome_res, status_res = resolver_contato(teste_contato, carregar_mapa_contatos(), base_atual)
                    cores = {"mapa":"#4ade80","auto":"#93c5fd","sem_match":"#f97316"}
                    labels = {"mapa":"Dicionário manual","auto":"Auto-match base MD","sem_match":"⚠️ Sem match"}
                    st.markdown(f'''
                    <div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;margin-top:4px;font-size:0.85rem;">
                        <span style="color:{cores[status_res]};font-weight:600;">{labels[status_res]}</span><br>
                        <span style="color:#e2e8f0;">→ {nome_res}</span>
                    </div>''', unsafe_allow_html=True)

    with tab_regras:
        st.markdown('<div class="page-sub">Regras criadas pelas suas correções — prioridade máxima na classificação.</div>', unsafe_allow_html=True)

        # ── Controle de exportados ────────────────────────────────────────────
        exportados_hist = carregar_exportados()
        if exportados_hist:
            st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin-bottom:8px;">📋 <strong style="color:#C9A84C;">{len(exportados_hist)}</strong> lançamentos marcados como já exportados para o Meu Dinheiro.</div>', unsafe_allow_html=True)
            if st.button("🗑️  Limpar histórico de exportados", key="btn_clear_exp"):
                salvar_exportados(set())
                st.success("Histórico limpo — todos os lançamentos serão tratados como novos.")
                st.rerun()
        else:
            st.info("Nenhum lançamento marcado como exportado ainda.")
        st.markdown("---")
        regras_atual = carregar_regras_aprendidas()

        if "_plano_carregado" in st.session_state:
            PLANO_CATS_R = list(json.loads(st.session_state["_plano_carregado"]).keys())
            subs_flat_r  = [""] + sorted(set(s for lst in json.loads(st.session_state["_plano_carregado"]).values() for s in lst))
        else:
            PLANO_CATS_R = list(PLANO_PADRAO.keys())
            subs_flat_r  = [""] + sorted(set(s for lst in PLANO_PADRAO.values() for s in lst))

        if not regras_atual:
            st.info("Nenhuma regra aprendida ainda. Corrija classificações na aba Classificar e salve.")
        else:
            st.markdown(f'<div style="font-size:0.82rem;color:#C9A84C;margin-bottom:1rem;">{len(regras_atual)} regras salvas</div>', unsafe_allow_html=True)
            df_regras = pd.DataFrame(regras_atual)
            df_regras_edit = st.data_editor(
                df_regras,
                column_config={
                    "tipo":         st.column_config.TextColumn("Tipo",          disabled=True, width="small"),
                    "contato":      st.column_config.TextColumn("Contato",       width="medium"),
                    "palavra":      st.column_config.TextColumn("Palavra-chave", width="medium"),
                    "mov":          st.column_config.SelectboxColumn("Mov",      options=["E","S",""], width="small"),
                    "categoria":    st.column_config.SelectboxColumn("Categoria",    options=PLANO_CATS_R,  width="large"),
                    "subcategoria": st.column_config.SelectboxColumn("Subcategoria", options=subs_flat_r,   width="large"),
                    "origem":       st.column_config.TextColumn("Origem",        disabled=True, width="medium"),
                },
                num_rows="dynamic", use_container_width=True, hide_index=True, key="editor_regras",
            )
            r1, r2, r3 = st.columns(3)
            with r1:
                if st.button("💾  Salvar alterações", key="btn_salvar_r2", use_container_width=True):
                    salvar_regras_aprendidas(df_regras_edit.to_dict("records"))
                    st.success("Regras salvas!"); st.rerun()
            with r2:
                st.download_button("⬇️  Exportar JSON", data=json.dumps(regras_atual, ensure_ascii=False, indent=2).encode("utf-8"),
                    file_name="regras_caixinha.json", mime="application/json", use_container_width=True)
            with r3:
                if st.button("🗑️  Apagar todas", key="btn_del_r", use_container_width=True):
                    salvar_regras_aprendidas([])
                    st.warning("Regras apagadas."); st.rerun()


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

