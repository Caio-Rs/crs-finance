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

/* ── Tabela ── */
.stDataFrame {
    border: 0.5px solid #253550 !important;
    border-radius: 10px !important;
    background: #162236 !important;
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
    name = uploaded.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded)
    elif name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded)
    elif name.endswith((".ofx", ".ofc", ".txt")):
        content = uploaded.read().decode("utf-8", errors="replace")
        return parse_ofx(content)
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
# 3. CONCILIAÇÃO DE SALDO — Modo Simples + Modo Consolidado
# ════════════════════════════════════════════════════════════════════════════
elif page == "conciliacao":
    st.markdown('<div class="page-title">Conciliação de Saldo</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Verifica se o saldo do banco bate com o sistema — com suporte a conta de aplicação automática (Itaú Aplic Aut Mais).</div>', unsafe_allow_html=True)

    # ── Parser extrato aplicação XLS (HTML disfarçado do Itaú) ───────────────
    def parse_aplic_xls(arquivo) -> pd.DataFrame:
        """Lê o extrato XLS da Aplic Aut Mais do Itaú (HTML disfarçado)."""
        from bs4 import BeautifulSoup
        import re
        try:
            conteudo = arquivo.read().decode("iso-8859-1", errors="replace")
        except Exception:
            arquivo.seek(0)
            conteudo = arquivo.read().decode("utf-8", errors="replace")

        soup = BeautifulSoup(conteudo, "html.parser")
        table = soup.find("table")
        if not table:
            return pd.DataFrame()

        rows = table.find_all("tr")
        transactions = []
        for row in rows:
            cells = [td.get_text(strip=True) for td in row.find_all(["td","th"])]
            cells = [c for c in cells if c != ""]
            if len(cells) < 2:
                continue
            data = cells[0]
            if not re.match(r"\d{2}/\d{2}/\d{4}", data):
                continue
            doc = cells[1] if len(cells) > 1 else ""
            if "Total" in str(cells):
                continue
            if doc.startswith("A") and len(cells) > 2:
                try:
                    valor = float(cells[2].replace(".","").replace(",","."))
                    transactions.append({"Data": data, "Valor": -valor, "Descrição": "APL APLIC AUT MAIS"})
                except Exception:
                    pass
            elif doc.startswith("R") and len(cells) > 7:
                try:
                    valor = float(cells[7].replace(".","").replace(",","."))
                    transactions.append({"Data": data, "Valor": valor, "Descrição": "RES APLIC AUT MAIS"})
                except Exception:
                    pass

        df = pd.DataFrame(transactions)
        if not df.empty:
            df["_data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
        return df

    # ── Modo de conciliação ───────────────────────────────────────────────────
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Modo de conciliação</div>', unsafe_allow_html=True)

    modo_col1, modo_col2 = st.columns(2)
    with modo_col1:
        modo_simples = st.container()
        modo_simples.markdown("""
        <div style="background:#162236;border:0.5px solid #253550;border-radius:10px;padding:1rem 1.25rem;cursor:pointer;">
            <div style="font-size:0.88rem;font-weight:600;color:#f1f5f9;margin-bottom:4px;">Modo Simples</div>
            <div style="font-size:0.78rem;color:#8899BB;line-height:1.5;">1 extrato OFX/CSV + sistema. Transferências internas filtradas por palavra-chave.</div>
            <div style="margin-top:8px;"><span style="background:#14532d;color:#86efac;font-size:0.7rem;padding:2px 8px;border-radius:4px;font-weight:600;">1 arquivo OFX</span></div>
        </div>""", unsafe_allow_html=True)
    with modo_col2:
        modo_consolidado = st.container()
        modo_consolidado.markdown("""
        <div style="background:#1B2A4A;border:2px solid #C9A84C;border-radius:10px;padding:1rem 1.25rem;cursor:pointer;">
            <div style="font-size:0.88rem;font-weight:600;color:#C9A84C;margin-bottom:4px;">Modo Consolidado ★</div>
            <div style="font-size:0.78rem;color:#8899BB;line-height:1.5;">CC + Aplicação + sistema. Consolida os saldos e neutraliza transferências internas automaticamente.</div>
            <div style="margin-top:8px;"><span style="background:#1e3a5f;color:#93c5fd;font-size:0.7rem;padding:2px 8px;border-radius:4px;font-weight:600;">2 OFX + sistema</span></div>
        </div>""", unsafe_allow_html=True)

    modo = st.radio(" ", ["Simples", "Consolidado"], horizontal=True,
                    key="conc_modo", label_visibility="collapsed")

    st.markdown("---")

    # ── UPLOADS ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Carregar arquivos</div>', unsafe_allow_html=True)

    if modo == "Simples":
        u1, u2 = st.columns(2)
        with u1:
            st.markdown("**Extrato Bancário**")
            st.caption("OFX · CSV · Excel — exportado pelo banco")
            f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Sistema de Gestão**")
            st.caption("CSV · Excel — Omie · Conta Azul · Nibo · Sienge · Meu Dinheiro")
            f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")
        f_aplic = None
    else:
        u1, u2, u3 = st.columns(3)
        with u1:
            st.markdown("**Conta Corrente (OFX)**")
            st.caption("Extrato principal do banco")
            f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"], key="conc_ext", label_visibility="collapsed")
        with u2:
            st.markdown("**Conta Aplicação (XLS/CSV)**")
            st.caption("Extrato Aplic Aut Mais — formato XLS do Itaú ou CSV")
            f_aplic = st.file_uploader(" ", type=["xls","xlsx","csv","txt"], key="conc_aplic", label_visibility="collapsed")
        with u3:
            st.markdown("**Sistema de Gestão**")
            st.caption("CSV · Excel — exportado do sistema")
            f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"], key="conc_sis", label_visibility="collapsed")

    arquivos_ok = f_c_ext and f_c_sis
    if modo == "Consolidado":
        arquivos_ok = arquivos_ok and f_aplic

    if not arquivos_ok:
        msg = "Carregue o extrato OFX e o sistema para iniciar." if modo == "Simples" else "Carregue os 3 arquivos (CC + Aplicação + Sistema) para iniciar."
        st.markdown(f"""
        <div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:.5rem;">⚖️</div>
            <div style="color:#556688;font-size:0.85rem;">{msg}</div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── CARREGA DADOS ─────────────────────────────────────────────────────────
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
        except Exception:
            pass

    try:
        df_sis_raw = pd.read_excel(f_c_sis, sheet_name=aba_sis) if aba_sis else load_file(f_c_sis)
    except Exception as e:
        st.error(f"Erro ao ler sistema: {e}"); st.stop()

    df_aplic = pd.DataFrame()
    if modo == "Consolidado" and f_aplic:
        try:
            df_aplic = parse_aplic_xls(f_aplic)
            if df_aplic.empty:
                st.warning("Não foi possível extrair transações do extrato de aplicação. Verifique se é o formato XLS do Itaú.")
            else:
                st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-bottom:8px;">✓ Extrato aplicação: {len(df_aplic)} movimentações carregadas</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Erro ao ler extrato de aplicação: {e}")

    if df_ext_raw.empty or df_sis_raw.empty:
        st.warning("Um dos arquivos está vazio."); st.stop()

    # ── MAPEAMENTO DE COLUNAS ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Mapear colunas</div>', unsafe_allow_html=True)

    cols_ext = df_ext_raw.columns.tolist()
    cols_sis = df_sis_raw.columns.tolist()
    c1,c2,c3,c4 = st.columns(4)
    with c1: col_data_e = st.selectbox("Data (extrato)", cols_ext, key="cce_d2")
    with c2: col_val_e  = st.selectbox("Valor (extrato)", cols_ext, index=min(2,len(cols_ext)-1), key="cce_v2")
    with c3: col_data_s = st.selectbox("Data (sistema)", cols_sis, key="ccs_d2")
    with c4: col_val_s  = st.selectbox("Valor (sistema)", cols_sis, index=min(2,len(cols_sis)-1), key="ccs_v2")

    # ── FILTROS TRANSFERÊNCIAS ────────────────────────────────────────────────
    st.markdown("---")

    if modo == "Simples":
        # Filtro extrato
        st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.5rem;">Filtrar transferências internas (extrato)</div>', unsafe_allow_html=True)
        st.caption("Aplicações automáticas e resgates se cancelam e zeram os totais.")
        palavras_padrao = ["APLIC AUT","RES APLIC","APL APLIC","RENDIMENTOS REND PAGO","TRANSF PROPRIA","TED PROPRIA"]
        fext1, fext2 = st.columns([1,2])
        with fext1:
            usar_filtro_ext = st.checkbox("Excluir transferências internas do extrato", value=True, key="chk_ext_filtro")
        with fext2:
            if usar_filtro_ext:
                desc_cols_ext = [c for c in cols_ext if any(x in c.lower() for x in ["desc","memo","hist","nome","name"])]
                col_desc_ext_filtro = st.selectbox("Coluna de descrição (extrato)", cols_ext,
                    index=cols_ext.index(desc_cols_ext[0]) if desc_cols_ext else min(1,len(cols_ext)-1), key="cce_desc_filtro")
                palavras_excluir_ext = st.multiselect("Palavras-chave para excluir", options=palavras_padrao,
                    default=palavras_padrao, key="ext_palavras")

        if usar_filtro_ext and palavras_excluir_ext:
            mask_ext = df_ext_raw[col_desc_ext_filtro].str.upper().str.contains(
                "|".join([re.escape(p) for p in palavras_excluir_ext]), na=False)
            n_antes = len(df_ext_raw)
            df_ext_raw = df_ext_raw[~mask_ext].copy()
            st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-top:4px;">✓ {n_antes-len(df_ext_raw)} lançamentos internos excluídos · {len(df_ext_raw)} restantes</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;font-size:0.82rem;color:#C9A84C;margin-bottom:12px;">
            ✓ <strong>Modo Consolidado:</strong> as transferências entre CC e Aplicação são neutralizadas automaticamente.
            O saldo final = CC + Aplicação, sem distorções.
        </div>""", unsafe_allow_html=True)

    # Filtro sistema
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.5rem;margin-top:.75rem;">Filtrar transferências internas (sistema)</div>', unsafe_allow_html=True)
    ft1, ft2 = st.columns(2)
    with ft1:
        cols_sis_opcoes = ["— Nenhum (usar todos os lançamentos) —"] + cols_sis
        col_tipo_sis = st.selectbox("Coluna de tipo (sistema)", cols_sis_opcoes, key="ccs_tipo")
    with ft2:
        tipos_excluir = []
        if col_tipo_sis != "— Nenhum (usar todos os lançamentos) —":
            tipos_unicos = df_sis_raw[col_tipo_sis].dropna().unique().tolist()
            tipos_excluir = st.multiselect("Excluir tipos", tipos_unicos,
                default=[t for t in tipos_unicos if "transfer" in str(t).lower()], key="ccs_excluir")

    if col_tipo_sis != "— Nenhum (usar todos os lançamentos) —" and tipos_excluir:
        n_antes = len(df_sis_raw)
        df_sis_raw = df_sis_raw[~df_sis_raw[col_tipo_sis].isin(tipos_excluir)].copy()
        st.markdown(f'<div style="font-size:0.8rem;color:#C9A84C;margin-top:4px;">✓ {n_antes-len(df_sis_raw)} transferências excluídas do sistema · {len(df_sis_raw)} restantes</div>', unsafe_allow_html=True)

    # ── TIPO ANÁLISE + PERÍODO ────────────────────────────────────────────────
    st.markdown("---")
    ca1, ca2 = st.columns([2,1])
    with ca1:
        tipo_analise = st.selectbox("Tipo de análise", [
            "Comparação de Valores por Dia",
            "Comparação de Movimentações por Dia",
            "Comparação por Chave Forte (Data+Valor)",
        ], key="conc_tipo")
    with ca2:
        data_range = st.text_input("Filtrar período (opcional)", placeholder="DD/MM/AAAA – DD/MM/AAAA", key="conc_range")

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.button("⚖️  Conciliar Saldo", key="btn_conc"):
        st.stop()

    # ── PROCESSA ──────────────────────────────────────────────────────────────
    try:
        df_ext = df_ext_raw.copy()
        df_sis = df_sis_raw.copy()
        df_ext[col_val_e] = parse_numeric(df_ext[col_val_e])
        df_sis[col_val_s] = parse_numeric(df_sis[col_val_s])
        df_ext["_data"] = pd.to_datetime(df_ext[col_data_e], dayfirst=True, errors="coerce")
        df_sis["_data"] = pd.to_datetime(df_sis[col_data_s], dayfirst=True, errors="coerce")

        # Modo consolidado: adiciona transações da aplicação ao extrato CC
        if modo == "Consolidado" and not df_aplic.empty:
            df_aplic_add = df_aplic[["_data","Valor","Descrição"]].copy()
            df_aplic_add.columns = ["_data", col_val_e, col_data_e]
            df_ext = pd.concat([df_ext, df_aplic_add], ignore_index=True)

        dt_min = df_ext["_data"].min()
        dt_max = df_ext["_data"].max()
        if data_range and "–" in data_range:
            try:
                partes = [p.strip() for p in data_range.split("–")]
                dt_min = pd.to_datetime(partes[0], dayfirst=True)
                dt_max = pd.to_datetime(partes[1], dayfirst=True)
            except Exception:
                pass

        df_ext_f = df_ext[(df_ext["_data"]>=dt_min)&(df_ext["_data"]<=dt_max)].copy()
        df_sis_f = df_sis[(df_sis["_data"]>=dt_min)&(df_sis["_data"]<=dt_max)].copy()

        saldo_banco = df_ext_f[col_val_e].sum()
        saldo_erp   = df_sis_f[col_val_s].sum()
        diferenca   = saldo_banco - saldo_erp

        periodo_txt = f"{dt_min.strftime('%d/%m/%Y')} a {dt_max.strftime('%d/%m/%Y')}"
        st.markdown("---")
        st.markdown(f'<div style="font-size:0.85rem;color:#8899BB;margin-bottom:1rem;">Período: <strong style="color:#C9A84C;">{periodo_txt}</strong>'
                    + (f' &nbsp;·&nbsp; <span style="color:#93c5fd;">Modo Consolidado (CC + Aplicação)</span>' if modo=="Consolidado" else '')
                    + '</div>', unsafe_allow_html=True)

        # Métricas
        if modo == "Consolidado" and not df_aplic.empty:
            # Mostra CC, Aplicação e Sistema separados + consolidado
            saldo_cc    = df_ext_raw.copy()
            saldo_cc[col_val_e] = parse_numeric(saldo_cc[col_val_e])
            saldo_cc["_data"] = pd.to_datetime(saldo_cc[col_data_e], dayfirst=True, errors="coerce")
            saldo_cc_val = saldo_cc[(saldo_cc["_data"]>=dt_min)&(saldo_cc["_data"]<=dt_max)][col_val_e].sum()
            saldo_ap_val = df_aplic[(df_aplic["_data"]>=dt_min)&(df_aplic["_data"]<=dt_max)]["Valor"].sum()

            m1,m2,m3,m4,m5 = st.columns(5)
            for col,lbl,val,origem,neg in [
                (m1,"Saldo CC (banco)",         saldo_cc_val, "CC",   saldo_cc_val<0),
                (m2,"Saldo Aplicação (banco)",   saldo_ap_val, "APLIC",saldo_ap_val<0),
                (m3,"Total banco consolidado",   saldo_banco,  "OFX",  saldo_banco<0),
                (m4,"Saldo no sistema",          saldo_erp,    "ERP",  saldo_erp<0),
                (m5,"Diferença",                 diferenca,    "BRL",  diferenca!=0),
            ]:
                cor_val = "#f87171" if neg else "#4ade80"
                cor_brd = "#f87171" if (neg and col==m5) else "#C9A84C"
                col.markdown(f"""
                <div style="background:#1B2A4A;border-radius:10px;padding:0.9rem 1rem;border-left:3px solid {cor_brd};margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
                        <span style="font-size:0.65rem;color:#8899BB;font-weight:600;letter-spacing:.05em;text-transform:uppercase;">{lbl}</span>
                        <span style="font-size:0.6rem;background:#253550;color:#8899BB;padding:1px 6px;border-radius:4px;">{origem}</span>
                    </div>
                    <div style="font-size:1.15rem;font-weight:700;color:{cor_val};">{fmt_brl(val)}</div>
                </div>""", unsafe_allow_html=True)
        else:
            c1,c2,c3 = st.columns(3)
            for col,lbl,val,origem,neg in [
                (c1,"Saldo do Período no Banco",   saldo_banco,"OFX",saldo_banco<0),
                (c2,"Saldo do Período no Sistema", saldo_erp,  "ERP",saldo_erp<0),
                (c3,"Diferença",                   diferenca,  "BRL",diferenca!=0),
            ]:
                cor_val = "#f87171" if neg else "#4ade80"
                cor_brd = "#f87171" if (diferenca!=0 and col==c3) else "#C9A84C"
                col.markdown(f"""
                <div style="background:#1B2A4A;border-radius:10px;padding:1rem 1.25rem;border-left:3px solid {cor_brd};margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <span style="font-size:0.68rem;color:#8899BB;font-weight:600;letter-spacing:.06em;text-transform:uppercase;">{lbl}</span>
                        <span style="font-size:0.65rem;background:#253550;color:#8899BB;padding:2px 7px;border-radius:4px;">{origem}</span>
                    </div>
                    <div style="font-size:1.4rem;font-weight:700;color:{cor_val};">{fmt_brl(val)}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.8rem;color:#8899BB;margin-bottom:.75rem;">Análise: <strong style="color:#C9A84C;">{tipo_analise}</strong></div>', unsafe_allow_html=True)

        # Tabela
        if tipo_analise == "Comparação de Valores por Dia":
            grp_e = df_ext_f.groupby("_data")[col_val_e].sum().reset_index()
            grp_s = df_sis_f.groupby("_data")[col_val_s].sum().reset_index()
            grp_e.columns=["Data","Banco"]; grp_s.columns=["Data","Sistema"]
            result = pd.merge(grp_e,grp_s,on="Data",how="outer").fillna(0)
            result["Diferença"] = result["Banco"]-result["Sistema"]
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

        else:  # Chave Forte
            df_ext_f["_chave"] = df_ext_f["_data"].dt.strftime("%Y%m%d")+"_"+df_ext_f[col_val_e].round(2).astype(str)
            df_sis_f["_chave"] = df_sis_f["_data"].dt.strftime("%Y%m%d")+"_"+df_sis_f[col_val_s].round(2).astype(str)
            cb=set(df_ext_f["_chave"]); cs=set(df_sis_f["_chave"])
            conc=cb&cs; so_b=cb-cs; so_s=cs-cb
            ck1,ck2,ck3=st.columns(3)
            for col,lbl,val,cls in [(ck1,"Conciliados",len(conc),"green"),(ck2,"Só no Banco",len(so_b),"amber"),(ck3,"Só no Sistema",len(so_s),"amber")]:
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
        st.download_button("⬇️  Baixar Relatório de Conciliação",
            data=to_excel_bytes(result),
            file_name=f"conciliacao_saldo_{datetime.today().strftime('%d%m%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Erro ao processar: {e}")


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
        (["retirada"],[],"S","5.1 - MOVIMENTAÇÕES DE SÓCIOS / FINANCIAMENTOS","5.502 - Distribuição de Lucros"),
        (["montagem","instalação","instalacao","montar"],[],"S","3.1 DESPESAS ADMINISTRATIVAS","3.319 - Serviços de Terceiros - Montagem e instalações"),
    ]

    # ── Storage persistente ───────────────────────────────────────────────────
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
    tab_class, tab_plano, tab_regras = st.tabs(["🤖  Classificar", "📋  Plano de Contas", "📚  Regras Aprendidas"])

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
            st.markdown("**Planilha da Caixinha (Excel)**")
            f_caixa = st.file_uploader(" ", type=["xlsx","xls"], key="class_file", label_visibility="collapsed")
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
                <div style="color:#556688;font-size:0.85rem;">Carregue a planilha Excel da Caixinha para iniciar</div>
            </div>""", unsafe_allow_html=True)
            st.stop()

        try:
            xl_caixa = pd.ExcelFile(f_caixa)
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")
            st.stop()

        abas_cx = [a for a in xl_caixa.sheet_names if "caixa" in a.lower()]
        aba_sel = st.selectbox("Selecione o mês", abas_cx if abas_cx else xl_caixa.sheet_names, key="class_aba")

        try:
            df_raw = xl_caixa.parse(aba_sel, header=None)
            header_row = 1
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
            df_work = df_work[df_work["Data"].notna() & (df_work["Data"].astype(str).str.strip() != "") & (df_work["Data"].astype(str) != "nan")]
            df_work["Data"] = pd.to_datetime(df_work["Data"], dayfirst=True, errors="coerce").dt.strftime("%d/%m/%Y")
            df_work = df_work[df_work["Data"].notna()].reset_index(drop=True)
        except Exception as e:
            st.error(f"Erro ao ler aba: {e}")
            st.stop()

        st.markdown(f'<div style="font-size:0.82rem;color:#8899BB;margin:.5rem 0 1rem;">Aba: <strong style="color:#C9A84C;">{aba_sel}</strong> · {len(df_work)} lançamentos</div>', unsafe_allow_html=True)

        if st.button("🤖  Classificar Automaticamente", key="btn_class"):
            cats, subs, confs = [], [], []
            for _, row in df_work.iterrows():
                entrada = parse_numeric(pd.Series([row.get("Entrada","")])).iloc[0]
                saida   = parse_numeric(pd.Series([row.get("Saida","")])).iloc[0]
                tmov    = "E" if (pd.notna(entrada) and entrada > 0) else "S"
                cat, sub, conf = classificar(str(row.get("Contato","")), str(row.get("Descricao","")), tmov, regras_aprendidas)
                cats.append(cat); subs.append(sub); confs.append(conf)
            df_work["Categoria"]    = cats
            df_work["SubCategoria"] = subs
            df_work["Confiança"]    = confs
            st.session_state["df_classificado"] = df_work.copy()

        if "df_classificado" not in st.session_state:
            st.stop()

        df_class = st.session_state["df_classificado"].copy()

        alta   = (df_class["Confiança"]=="Alta").sum()
        aprend = (df_class["Confiança"]=="Aprendida").sum()
        media  = (df_class["Confiança"]=="Média").sum()
        manual = (df_class["Confiança"]=="Manual").sum()

        m1,m2,m3,m4,m5 = st.columns(5)
        for col,lbl,val,cls in [
            (m1,"Total",str(len(df_class)),""),
            (m2,"Alta confiança",str(alta),"green"),
            (m3,"Aprendidas",str(aprend),"green"),
            (m4,"Média",str(media),"amber"),
            (m5,"Revisão manual",str(manual),"red" if manual>0 else "green"),
        ]:
            col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#1B2A4A;border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:0.82rem;color:#C9A84C;">
            ✏️ Edite <strong>Categoria</strong> e <strong>SubCategoria</strong> diretamente na tabela.
            Clique em <strong>Salvar correções</strong> para criar regras automáticas para os próximos meses.
        </div>""", unsafe_allow_html=True)

        df_edit = st.data_editor(
            df_class,
            column_config={
                "Categoria":    st.column_config.SelectboxColumn("Categoria",    options=PLANO_CATS_DIN, width="large"),
                "SubCategoria": st.column_config.SelectboxColumn("SubCategoria", options=subs_flat,      width="large"),
                "Confiança":    st.column_config.TextColumn("Confiança", disabled=True, width="small"),
                "Contato":      st.column_config.TextColumn("Contato",   disabled=True),
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
        dl1, dl2, dl3 = st.columns(3)
        with dl1:
            st.markdown("**CSV — Meu Dinheiro**")
            csv_cols = [c for c in ["Data","Contato","Descricao","Entrada","Saida","Categoria","SubCategoria"] if c in df_edit.columns]
            csv_df = df_edit[csv_cols].copy()
            csv_df.columns = ["Data","Contato/Fornecedor","Descrição","Entrada","Saída","Categoria","Subcategoria"][:len(csv_cols)]
            st.download_button("⬇️  Baixar CSV", data=csv_df.to_csv(index=False,sep=";",encoding="utf-8-sig").encode("utf-8-sig"), file_name=f"{nome_base}.csv", mime="text/csv")
        with dl2:
            st.markdown("**Excel — revisão**")
            st.download_button("⬇️  Baixar Excel", data=to_excel_bytes(df_edit), file_name=f"{nome_base}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with dl3:
            st.markdown("**OFX — extrato bancário**")
            st.download_button("⬇️  Baixar OFX", data=gerar_ofx(df_edit, conta_nome=aba_sel).encode("utf-8"), file_name=f"{nome_base}.ofx", mime="application/octet-stream")

    # ════════════════════════════
    with tab_regras:
        st.markdown('<div class="page-sub">Regras criadas pelas suas correções — prioridade máxima na classificação.</div>', unsafe_allow_html=True)
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

