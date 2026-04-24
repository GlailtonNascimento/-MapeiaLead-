import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mapeia Lead", page_icon="🎯", layout="wide")

# ============================================================
# AVISO DE SEGURANÇA (Para quem ver o aviso do navegador)
# ============================================================
st.info("""
🔒 **Sobre o aviso de segurança:**  
Se aparecer uma mensagem de certificado, clique em "Avançadas" → "Prosseguir".  
É apenas um detalhe técnico do Streamlit Cloud. O site é **100% seguro** e seus dados estão protegidos.
""")

st.title("🎯 MAPEIA LEAD")
st.markdown("### Sistema de Prospecção por CNAE")

st.warning("""
⚠️ **ATENÇÃO:** Esta é uma **VERSÃO DEMONSTRATIVA** com dados FICTÍCIOS.
- ✅ **CNAEs são REAIS** (códigos oficiais da Receita Federal)
- ⚠️ **As empresas e CNPJs são EXEMPLOS** (não são dados reais)
- 🔗 Para dados REAIS de empresas, adquira a versão completa do sistema
""")

with st.expander("📖 Sobre o Mapeia Lead", expanded=False):
    st.markdown("""
    ### 💡 **O que faz?**
    Busca empresas por CNAE e estado em segundos.
    
    ### 🎯 **Para quem?**
    - Franqueadoras
    - Vendedores B2B
    - Profissionais de marketing
    
    ### ⚡ **Problema que resolve**
    - Busca manual: 2-3 dias
    - Mapeia Lead: 5 segundos
    """)

# Filtros
col1, col2 = st.columns(2)
with col1:
    cnae = st.text_input("📌 CNAE", value="5612", help="Ex: 5612 (sorveterias)")
with col2:
    uf = st.selectbox("📍 UF", ["SP", "RJ", "MG", "BA", "PE", "PR", "RS", "SC", "DF", "GO"])

if st.button("🔍 BUSCAR LEADS", type="primary"):
    empresas = {
        ("5612", "SP"): ["🍦 Gelato Sul Sorvetes - São Paulo/SP - (11) 98765-4321", "🍦 Sorveteria Kids - Campinas/SP - (19) 98765-4322"],
        ("5612", "RJ"): ["🍦 Ice Mania - Rio de Janeiro/RJ - (21) 98765-4323"],
        ("4721", "RJ"): ["🛒 Mercado Popular - Rio de Janeiro/RJ - (21) 98765-4325"],
    }
    
    resultados = empresas.get((cnae, uf), [])
    
    if resultados:
        st.success(f"✅ {len(resultados)} empresas encontradas")
        for r in resultados:
            st.write(r)
        csv = "\n".join(resultados)
        st.download_button("📥 Exportar CSV", csv, f"leads_{cnae}_{uf}.csv")
    else:
        st.info(f"ℹ️ Nenhuma empresa encontrada para CNAE {cnae} em {uf}")

st.markdown("---")
st.markdown("### 👨‍💻 Desenvolvido por **Glailton Nascimento**")
st.caption("© 2025 Mapeia Lead - Todos os direitos reservados")
