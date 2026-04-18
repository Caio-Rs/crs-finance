# CRS Finance — Sistema de Auditoria Bancária

**Caio Rodrigues Silva · Especialista BPO Financeiro · Parnaíba, PI**

---

## Funcionalidades

- **Marca & Apresentação** — Identidade visual CRS Finance
- **Auditoria Bancária** — Cruza extrato bancário vs sistema de gestão
- **Conciliação** — Visão lado a lado com cálculo de diferença
- **Conversor OFX → Excel** — Transforma extrato OFX em planilha
- **Serviços & Contato** — Portfólio de serviços BPO

---

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Deploy no Streamlit Cloud (gratuito)

1. Crie conta em github.com
2. Crie um repositório e suba os arquivos:
   - app.py
   - requirements.txt
   - .streamlit/config.toml
3. Acesse share.streamlit.io
4. Conecte o GitHub → selecione o repositório → Deploy
5. URL pública: crsfinance.streamlit.app

---

## Estrutura de arquivos

```
crs_finance/
├── app.py                  ← arquivo principal
├── requirements.txt        ← dependências
└── .streamlit/
    └── config.toml         ← tema e configurações
```

---

## Formatos aceitos

| Tipo de arquivo | Extrato bancário | Sistema de gestão |
|-----------------|:---:|:---:|
| OFX / OFC       | ✅  | —   |
| CSV             | ✅  | ✅  |
| Excel (.xlsx)   | ✅  | ✅  |
