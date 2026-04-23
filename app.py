import streamlit as st

st.set_page_config(page_title="Mapeia Lead", page_icon="🎯", layout="wide")

st.title("🎯 MAPEIA LEAD")
st.markdown("### Sistema de Prospecção por CNAE")

# ============================================================
# AVISO DE DADOS FICTÍCIOS (DESTAQUE)
# ============================================================
st.warning("""
⚠️ **ATENÇÃO:** Esta é uma **VERSÃO DEMONSTRATIVA** com dados FICTÍCIOS.

- ✅ Os **CNAEs são REAIS** (códigos oficiais da Receita Federal)
- ⚠️ As **empresas e CNPJs são EXEMPLOS** (não são dados reais)
- 🔗 Para dados REAIS de empresas, adquira a versão completa do sistema
""")

# ============================================================
# TEXTO EXPLICATIVO
# ============================================================
with st.expander("📖 Sobre o Mapeia Lead", expanded=False):
    st.markdown("""
    ### 💡 **Qual é a ideia?**
    O **Mapeia Lead** é uma ferramenta de prospecção comercial que permite encontrar empresas por **CNAE** e por **estado (UF)**.
    
    ---
    
    ### 🎯 **Para quem serve?**
    - Franqueadoras (ex: Oggi Sorvetes)
    - Vendedores B2B
    - Profissionais de marketing
    - Consultores de negócios
    
    ---
    
    ### ⚡ **Qual problema resolve?**
    | Problema | Solução |
    |----------|---------|
    | Dias perdidos no Google | Resultado em **5 segundos** |
    | Listas incompletas | TODAS as empresas ativas |
    | Contatos desatualizados | Filtro por empresa ATIVA |
    
    ---
    
    ### ⏱️ **Estatísticas de tempo**
    - Busca manual: **2 a 3 dias**
    - Mapeia Lead: **5 segundos**
    - **Economia:** 40 horas → 1 minuto
    """)

# ============================================================
# FILTROS
# ============================================================
st.markdown("---")
st.subheader("🔍 Buscar empresas")

col1, col2 = st.columns(2)

with col1:
    cnae_ajuda = """
    **O que é CNAE?**
    
    CNAE = Classificação Nacional de Atividades Econômicas.
    
    **Exemplos:**
    - 5612 → Sorveterias
    - 4721 → Mercados
    - 4771 → Farmácias
    """
    cnae = st.text_input("📌 CNAE", value="5612", help=cnae_ajuda)

with col2:
    uf_ajuda = """
    **Siglas disponíveis:**
    SP, RJ, MG, BA, PE, PR, RS, SC, DF, GO, ES, CE, RN, PB, PI, MA
    """
    uf = st.selectbox("📍 UF", ["SP", "RJ", "MG", "BA", "PE", "PR", "RS", "SC", "DF", "GO"], help=uf_ajuda)

if st.button("🔍 BUSCAR LEADS", type="primary"):
    # Dados FICTÍCIOS (exemplo)
    empresas_ficticias = {
        ("5612", "SP"): ["🍦 Empresa Fictícia A - São Paulo/SP - (11) 99999-1111", "🍦 Empresa Fictícia B - Campinas/SP - (19) 99999-2222"],
        ("5612", "RJ"): ["🍦 Empresa Fictícia C - Rio de Janeiro/RJ - (21) 99999-3333"],
        ("5612", "MG"): ["🍦 Empresa Fictícia D - Belo Horizonte/MG - (31) 99999-4444"],
        ("4721", "RJ"): ["🛒 Empresa Fictícia E - Rio de Janeiro/RJ - (21) 99999-5555"],
        ("4721", "SP"): ["🛒 Empresa Fictícia F - São Paulo/SP - (11) 99999-6666"],
    }
    
    resultados = empresas_ficticias.get((cnae, uf), [])
    
    if resultados:
        # AVISO DENTRO DO RESULTADO
        st.info("📌 **Lembrete:** Os dados exibidos são FICTÍCIOS (apenas demonstração)")
        st.success(f"✅ {len(resultados)} empresas encontradas")
        
        for r in resultados:
            st.write(r)
        
        csv = "\n".join(resultados)
        st.download_button("📥 Exportar CSV (demonstração)", csv, f"leads_{cnae}_{uf}.csv")
    else:
        st.warning(f"⚠️ Nenhuma empresa fictícia encontrada para CNAE {cnae} em {uf}")
        st.info("💡 **Sugestão:** Tente CNAE 5612 em SP ou CNAE 4721 em RJ")

# ============================================================
# RODAPÉ
# ============================================================
st.markdown("---")
st.markdown("### 👨‍💻 Desenvolvido por **Glailton Nascimento**")
st.caption("© 2025 Mapeia Lead - Todos os direitos reservados")
st.caption("🔬 VERSÃO DEMONSTRATIVA - Dados fictícios para apresentação")
