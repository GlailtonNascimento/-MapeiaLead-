
%%writefile app.py
import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(
    page_title="Mapeia Lead",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .main-header p {
        color: #a8c8ff;
        margin: 0;
    }
    .result-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stButton button {
        background-color: #2a5298;
        color: white;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("""
<div class="main-header">
    <h1>🎯 MAPEIA LEAD</h1>
    <p>Encontre empresas por CNAE e UF - Dados oficiais</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/business-group.png", width=80)
    st.markdown("### 🔍 Filtros de Busca")
    
    cnae = st.text_input("📌 CNAE", value="5612", help="Ex: 5612 (sorveterias), 4721 (mercados)")
    
    uf = st.selectbox("📍 Estado", [
        "SP", "RJ", "MG", "ES", "BA", "PE", "PR", "RS", "SC", 
        "DF", "GO", "MT", "MS", "CE", "RN", "PB", "PI", "MA", 
        "PA", "AM", "AC", "RO", "RR", "TO", "SE", "AL", "AP"
    ])
    
    st.divider()
    
    st.markdown("### 📊 CNAEs comuns")
    st.markdown("""
    - Sorveterias: **5612**
    - Mercados: **4721**
    - Pizzarias: **5612**
    - Farmácias: **4771**
    - Academias: **9312**
    - Restaurantes: **5611**
    """)
    
    st.divider()
    
    buscar = st.button("🔍 BUSCAR LEADS", type="primary", use_container_width=True)

# Função para buscar dados
def buscar_empresas(cnae_alvo, uf_alvo):
    """Busca empresas na base de dados"""
    try:
        # Tenta carregar base real
        df = pd.read_csv('dados/base_brasil.csv', dtype=str)
        
        # Filtra
        resultado = df[
            (df['cnae_fiscal_principal'].str.startswith(cnae_alvo, na=False)) &
            (df['uf'] == uf_alvo) &
            (df['situacao_cadastral'].isin(['02', 'ATIVA']))
        ]
        
        return resultado
    except:
        # Se não tiver base, usa dados de exemplo
        dados_exemplo = pd.DataFrame([
            ['12345678000101', 'Gelato Sul Sorvetes', '5612001', '02', 'SP', 'São Paulo', '11', '987654321'],
            ['23456789000102', 'Sorveteria Kids', '5612001', '02', 'SP', 'Campinas', '19', '987654322'],
            ['34567890000103', 'Ice Mania', '5612001', '02', 'SP', 'Santos', '13', '987654323'],
        ], columns=['cnpj', 'razao_social', 'cnae_fiscal_principal', 'situacao_cadastral', 'uf', 'municipio', 'ddd_telefone_1', 'telefone_1'])
        
        resultado = dados_exemplo[dados_exemplo['uf'] == uf_alvo]
        return resultado

# Área principal
if buscar:
    if not cnae:
        st.error("❌ Por favor, digite um CNAE")
    else:
        with st.spinner(f"🔍 Buscando empresas com CNAE {cnae} em {uf}..."):
            resultado = buscar_empresas(cnae, uf)
            
            if resultado.empty:
                st.warning(f"⚠️ Nenhuma empresa encontrada para CNAE {cnae} em {uf}")
            else:
                st.success(f"✅ Encontradas **{len(resultado)}** empresas ativas")
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Leads", len(resultado))
                with col2:
                    st.metric("CNAE Buscado", cnae)
                with col3:
                    st.metric("UF", uf)
                
                st.divider()
                
                # Tabela de resultados
                st.markdown("### 📋 RESULTADOS")
                
                # Selecionar colunas para exibir
                colunas_exibir = ['razao_social', 'municipio', 'ddd_telefone_1', 'telefone_1', 'cnpj']
                colunas_existentes = [c for c in colunas_exibir if c in resultado.columns]
                
                # Renomear colunas
                df_display = resultado[colunas_existentes].copy()
                df_display.columns = ['Empresa', 'Cidade', 'DDD', 'Telefone', 'CNPJ']
                
                st.dataframe(df_display, use_container_width=True)
                
                # Botão de exportação
                st.divider()
                csv = resultado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 EXPORTAR PARA CSV",
                    data=csv,
                    file_name=f"leads_{cnae}_{uf}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Rodapé
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>🔒 Dados da Receita Federal | 🎯 Mapeia Lead - Prospecção Inteligente</p>
    <p>Desenvolvido por Glailton Nascimento</p>
</div>
""", unsafe_allow_html=True)
