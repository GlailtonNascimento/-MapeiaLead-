import streamlit as st

st.set_page_config(page_title="Mapeia Lead", page_icon="🎯", layout="wide")

st.title("🎯 MAPEIA LEAD")
st.markdown("### Sistema de Prospecção por CNAE")

# ============================================================
# BALÃO EXPLICATIVO (Tooltip)
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
    
    ---
    
    ### ⚠️ **Aviso sobre os dados**
    - ✅ **CNAEs são REAIS** (códigos oficiais)
    - ⚠️ **CNPJs e empresas são EXEMPLOS**
    - 🔗 Para dados reais, adquira a versão completa
    """)

# ============================================================
# FILTROS COM BALÕES EXPLICATIVOS
# ============================================================
st.markdown("---")
st.subheader("🔍 Buscar empresas")

col1, col2 = st.columns(2)

with col1:
    # BALÃO 1: Explicação do CNAE
    cnae_ajuda = """
    **O que é CNAE?**
    
    CNAE = Classificação Nacional de Atividades Econômicas.
    
    **Exemplos:**
    - 5612 → Sorveterias
    - 4721 → Mercados
    - 4771 → Farmácias
    
    Digite os 4 primeiros dígitos.
    """
    cnae = st.text_input(
        "📌 CNAE", 
        value="5612",
        help=cnae_ajuda
    )

with col2:
    # BALÃO 2: Explicação da UF
    uf_ajuda = """
    **O que é UF?**
    
    UF = Unidade Federativa (estado brasileiro).
    
    **Siglas disponíveis:**
    SP, RJ, MG, BA, PE, PR, RS, SC, DF, GO, ES, CE, RN, PB, PI, MA, PA, AM, AC, RO, RR, TO, MT, MS, SE, AL, AP
    
    Selecione o estado onde deseja buscar empresas.
    """
    uf = st.selectbox(
        "📍 UF", 
        ["SP", "RJ", "MG", "BA", "PE", "PR", "RS", "SC", 
         "DF", "GO", "ES", "CE", "RN", "PB", "PI", "MA"],
        help=uf_ajuda
    )

# BALÃO 3: Explicação do botão
botao_ajuda = """
**O que acontece ao clicar aqui?**

O sistema vai:
1. Buscar empresas com o CNAE informado
2. Filtrar apenas empresas ATIVAS no estado selecionado
3. Exibir os resultados
4. Permitir exportar lista em CSV

**Tempo estimado:** 1-2 segundos
"""

if st.button("🔍 BUSCAR LEADS", type="primary", help=botao_ajuda):
    # Dados de exemplo
    empresas = {
        ("5612", "SP"): ["🍦 Gelato Sul Sorvetes - São Paulo/SP - (11) 98765-4321", "🍦 Sorveteria Kids - Campinas/SP - (19) 98765-4322"],
        ("5612", "RJ"): ["🍦 Ice Mania - Rio de Janeiro/RJ - (21) 98765-4323"],
        ("5612", "MG"): ["🍦 Sorvete Bom - Belo Horizonte/MG - (31) 98765-4324"],
        ("4721", "RJ"): ["🛒 Mercado Popular - Rio de Janeiro/RJ - (21) 98765-4325"],
        ("4721", "SP"): ["🛒 Supermercado Econômico - São Paulo/SP - (11) 98765-4326"],
        ("4771", "SP"): ["💊 Farmácia Popular - São Paulo/SP - (11) 98765-4327"],
        ("9312", "SP"): ["🏋️ Academia Corpo Livre - São Paulo/SP - (11) 98765-4328"],
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
        st.markdown("💡 **Sugestão:** Tente CNAE 5612 em SP ou 4721 em RJ")

# ============================================================
# RODAPÉ
# ============================================================
st.markdown("---")
st.markdown("### 👨‍💻 Desenvolvido por **Glailton Nascimento**")
st.caption("© 2025 Mapeia Lead - Todos os direitos reservados")
st.caption("🔬 Versão demonstrativa - Dados reais disponíveis na versão completa")
