import streamlit as st
import pandas as pd
import numpy as np
import re
import io
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
# 3. CONCILIAÇÃO DE SALDO
# Foco: o saldo do banco bate com o saldo do sistema no período? (totais)
# ════════════════════════════════════════════════════════════════════════════
elif page == "conciliacao":
    st.markdown('<div class="page-title">Conciliação de Saldo</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-sub">Verifica se o saldo total do banco bate com o saldo do sistema no período
    — comparando totais diários, mensais e diferença acumulada.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card" style="margin-bottom:1rem;">
        <div class="section-card-title">Como funciona</div>
        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;">
            <div style="flex:1;min-width:160px;font-size:0.82rem;color:#94a3b8;line-height:1.6;">
                <span style="color:#C9A84C;font-weight:600;">Entrada:</span> extrato OFX/CSV do banco 
                + exportação do sistema de gestão para o mesmo período
            </div>
            <div style="flex:1;min-width:160px;font-size:0.82rem;color:#94a3b8;line-height:1.6;">
                <span style="color:#C9A84C;font-weight:600;">Processo:</span> soma os valores por dia 
                e compara banco vs sistema — ideal para fechamento mensal
            </div>
            <div style="flex:1;min-width:160px;font-size:0.82rem;color:#94a3b8;line-height:1.6;">
                <span style="color:#C9A84C;font-weight:600;">Resultado:</span> saldo do período no banco,
                saldo no sistema, diferença e tabela por dia
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("**Extrato Bancário**")
        st.caption("OFX · CSV · Excel — exportado pelo banco")
        f_c_ext = st.file_uploader(" ", type=["ofx","ofc","csv","xlsx","xls","txt"],
                                   key="conc_ext", label_visibility="collapsed")
    with col_u2:
        st.markdown("**Sistema de Gestão**")
        st.caption("CSV · Excel — Omie · Conta Azul · Nibo · Sienge · Excel próprio")
        f_c_sis = st.file_uploader(" ", type=["csv","xlsx","xls"],
                                   key="conc_sis", label_visibility="collapsed")

    if not f_c_ext or not f_c_sis:
        st.markdown("""
        <div class="section-card" style="text-align:center;padding:2rem;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:.5rem;">⚖️</div>
            <div style="color:#556688;font-size:0.85rem;">Carregue os dois arquivos para conciliar o saldo do período</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    try:
        df_ext_raw = load_file(f_c_ext)
    except Exception as e:
        st.error(f"Erro ao ler extrato: {e}")
        st.stop()

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
        st.error(f"Erro ao ler sistema: {e}")
        st.stop()

    if df_ext_raw.empty or df_sis_raw.empty:
        st.warning("Um dos arquivos está vazio.")
        st.stop()

    # Mapeamento
    st.markdown("---")
    st.markdown('<div class="section-card-title" style="font-size:.7rem;letter-spacing:.12em;color:#C9A84C;text-transform:uppercase;margin-bottom:.75rem;">Mapear colunas</div>', unsafe_allow_html=True)

    cols_ext = df_ext_raw.columns.tolist()
    cols_sis = df_sis_raw.columns.tolist()
    c1,c2,c3,c4 = st.columns(4)
    with c1: col_data_e = st.selectbox("Data (extrato)", cols_ext, key="cce_d2")
    with c2: col_val_e  = st.selectbox("Valor (extrato)", cols_ext, index=min(2,len(cols_ext)-1), key="cce_v2")
    with c3: col_data_s = st.selectbox("Data (sistema)", cols_sis, key="ccs_d2")
    with c4: col_val_s  = st.selectbox("Valor (sistema)", cols_sis, index=min(2,len(cols_sis)-1), key="ccs_v2")

    # Tipo análise + período
    st.markdown("<br>", unsafe_allow_html=True)
    ca1,ca2 = st.columns([2,1])
    with ca1:
        tipo_analise = st.selectbox("Tipo de análise", [
            "Comparação de Valores por Dia",
            "Comparação de Movimentações por Dia",
            "Comparação por Chave Forte (Data+Valor)",
        ], key="conc_tipo")
    with ca2:
        data_range = st.text_input("Filtrar período (opcional)",
                                   placeholder="DD/MM/AAAA – DD/MM/AAAA", key="conc_range")

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.button("⚖️  Conciliar Saldo", key="btn_conc"):
        st.stop()

    try:
        df_ext = df_ext_raw.copy()
        df_sis = df_sis_raw.copy()
        df_ext[col_val_e] = parse_numeric(df_ext[col_val_e])
        df_sis[col_val_s] = parse_numeric(df_sis[col_val_s])
        df_ext["_data"] = pd.to_datetime(df_ext[col_data_e], dayfirst=True, errors="coerce")
        df_sis["_data"] = pd.to_datetime(df_sis[col_data_s], dayfirst=True, errors="coerce")

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
        st.markdown(f'<div style="font-size:0.85rem;color:#8899BB;margin-bottom:1rem;">Período: <strong style="color:#C9A84C;">{periodo_txt}</strong></div>', unsafe_allow_html=True)

        # Saldos em destaque
        c1,c2,c3 = st.columns(3)
        for col,lbl,val,origem,neg in [
            (c1,"Saldo do Período no Banco",   saldo_banco,"OFX", saldo_banco<0),
            (c2,"Saldo do Período no Sistema", saldo_erp,  "ERP", saldo_erp<0),
            (c3,"Diferença",                   diferenca,  "BRL", diferenca!=0),
        ]:
            cor_val = "#f87171" if neg else "#4ade80"
            cor_brd = "#f87171" if diferenca!=0 and col==c3 else "#C9A84C"
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

        # Tabela por tipo
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
            chaves_b = set(df_ext_f["_chave"]); chaves_s = set(df_sis_f["_chave"])
            conc = chaves_b & chaves_s; so_b = chaves_b-chaves_s; so_s = chaves_s-chaves_b
            ck1,ck2,ck3 = st.columns(3)
            for col,lbl,val,cls in [(ck1,"Conciliados",len(conc),"green"),(ck2,"Só no Banco",len(so_b),"amber"),(ck3,"Só no Sistema",len(so_s),"amber")]:
                col.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value {cls}">{val}</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            rows=[]
            for _,r in df_ext_f.iterrows():
                rows.append({"Data":r["_data"].strftime("%d/%m/%Y"),"Valor Banco":fmt_brl(r[col_val_e]),"Valor Sistema":"—","Status":"✅ Conciliado" if r["_chave"] in chaves_s else "⚠️ Só no Banco"})
            for _,r in df_sis_f.iterrows():
                if r["_chave"] not in chaves_b:
                    rows.append({"Data":r["_data"].strftime("%d/%m/%Y"),"Valor Banco":"—","Valor Sistema":fmt_brl(r[col_val_s]),"Status":"ℹ️ Só no Sistema"})
            result = pd.DataFrame(rows)

        st.dataframe(result, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("⬇️  Baixar Relatório de Conciliação",
            data=to_excel_bytes(result),
            file_name=f"conciliacao_saldo_{datetime.today().strftime('%d%m%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Erro ao processar: {e}")


# ════════════════════════════════════════════════════════════════════════════
# 4. CONVERSOR OFX → EXCEL
# ════════════════════════════════════════════════════════════════════════════
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
# 5. SERVIÇOS & CONTATO
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

