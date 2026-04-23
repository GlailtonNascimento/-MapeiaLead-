import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mapeia Lead", page_icon="🎯")

st.title("🎯 MAPEIA LEAD")
st.markdown("### Sistema de Prospecção por CNAE")

# Filtros
cnae = st.text_input("CNAE", value="5612", help="Ex: 5612 (sorveterias)")
uf = st.selectbox("UF", ["SP", "RJ", "MG", "PE", "BA", "PR", "RS", "SC", "DF"])

if st.button("🔍 BUSCAR"):
    with st.spinner("Buscando empresas..."):
        try:
            df = pd.read_csv("dados/base_brasil.csv", dtype=str)
            resultado = df[df["cnae_fiscal_principal"].str.startswith(cnae, na=False)]
            resultado = resultado[resultado["uf"] == uf]
            resultado = resultado[resultado["situacao_cadastral"] == "02"]
            
            if resultado.empty:
                st.warning("Nenhuma empresa encontrada")
            else:
                st.success(f"✅ {len(resultado)} empresas encontradas")
                st.dataframe(resultado[["razao_social", "municipio", "telefone_1"]])
                
                csv = resultado.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Exportar CSV", csv, f"leads_{cnae}_{uf}.csv", "text/csv")
        except Exception as e:
            st.error(f"Erro: {e}")

st.markdown("---")
st.caption("Desenvolvido por Glailton Nascimento")
