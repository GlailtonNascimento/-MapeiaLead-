
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.validadores import validar_cnae, validar_uf, validar_cidade

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mapeia Lead",
    page_icon="🎯",
    layout="wide"
)

# CABEÇALHO
st.title("🎯 Mapeia Lead")
st.caption("Encontre seu cliente ideal por CNAE e região")

# DESENVOLVEDOR
st.markdown("---")
st.markdown("👨‍💻 **Desenvolvedor: Glailton Nascimento**")
st.markdown("---")

# SIDEBAR COM FILTROS
with st.sidebar:
    st.header("🔍 Filtros de Busca")
    
    cnae = st.text_input(
        "CNAE *",
        placeholder="Ex: 56120 (sorveteria) ou 47211 (mercado)",
        help="Digite os 7 dígitos do CNAE"
    )
    
    uf = st.selectbox(
        "Estado *",
        options=["SP", "RJ", "MG", "ES", "PR", "SC", "RS", "BA", "PE", "CE", "GO", "DF", "Outro"],
        help="Selecione o estado para buscar"
    )
    
    if uf == "Outro":
        uf = st.text_input("Digite a UF", max_chars=2, placeholder="Ex: AM")
    
    cidade = st.text_input(
        "Cidade (opcional)",
        placeholder="Deixe em branco para todo o estado"
    )
    
    buscar = st.button("🔍 Buscar Leads", type="primary", use_container_width=True)

# ÁREA DE RESULTADOS
if buscar:
    if not cnae:
        st.error("❌ Digite um CNAE")
    else:
        # Valida CNAE
        valido, resultado = validar_cnae(cnae)
        if not valido:
            st.error(f"❌ {resultado}")
        else:
            # Valida UF
            valido, resultado_uf = validar_uf(uf)
            if not valido:
                st.error(f"❌ {resultado_uf}")
            else:
                # Valida cidade
                valido, resultado_cidade = validar_cidade(cidade)
                if not valido:
                    st.error(f"❌ {resultado_cidade}")
                else:
                    with st.spinner("🔄 Buscando empresas ativas..."):
                        # DADOS DE EXEMPLO (enquanto não tem base real)
                        empresas = [
                            {
                                'Razão Social': 'Gelato Sul Sorvetes Ltda',
                                'CNPJ': '12.345.678/0001-90',
                                'Cidade': 'São Paulo',
                                'UF': resultado_uf,
                                'Telefone': '(11) 98765-4321',
                                'Endereço': 'Av. Paulista, 1000',
                                'Status': 'ATIVA'
                            },
                            {
                                'Razão Social': 'Sorveteria Kids Feliz',
                                'CNPJ': '23.456.789/0001-01',
                                'Cidade': 'Campinas',
                                'UF': resultado_uf,
                                'Telefone': '(19) 3456-7890',
                                'Endereço': 'Rua das Flores, 500',
                                'Status': 'ATIVA'
                            },
                            {
                                'Razão Social': 'Ice Mania Sorvetes',
                                'CNPJ': '34.567.890/0001-12',
                                'Cidade': 'Santos',
                                'UF': resultado_uf,
                                'Telefone': '(13) 98765-1234',
                                'Endereço': 'Av. da Praia, 200',
                                'Status': 'ATIVA'
                            },
                            {
                                'Razão Social': 'Sorvete Bom Demais',
                                'CNPJ': '45.678.901/0001-23',
                                'Cidade': 'Ribeirão Preto',
                                'UF': resultado_uf,
                                'Telefone': '(16) 98765-4321',
                                'Endereço': 'Rua São Sebastião, 300',
                                'Status': 'ATIVA'
                            },
                            {
                                'Razão Social': 'Gelato Artesanal',
                                'CNPJ': '56.789.012/0001-34',
                                'Cidade': 'Sorocaba',
                                'UF': resultado_uf,
                                'Telefone': '(15) 3456-7890',
                                'Endereço': 'Av. Independência, 150',
                                'Status': 'ATIVA'
                            }
                        ]
                        
                        # Filtra por cidade se informada
                        if resultado_cidade:
                            empresas = [e for e in empresas if resultado_cidade.upper() in e['Cidade'].upper()]
                        
                        if not empresas:
                            st.warning("⚠️ Nenhuma empresa encontrada com esses critérios.")
                        else:
                            st.success(f"✅ Encontradas **{len(empresas)}** empresas ativas")
                            
                            # Converte para DataFrame
                            df = pd.DataFrame(empresas)
                            
                            # Exibe tabela
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            # Botão de exportação
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Exportar para CSV",
                                data=csv,
                                file_name=f"leads_{resultado}_{resultado_uf}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

# RODAPÉ
st.divider()
st.caption("🔒 Dados consultados em tempo real. Sistema de prospecção inteligente.")
st.caption(f"© 2025 Mapeia Lead - Desenvolvido por Glailton Nascimento")
