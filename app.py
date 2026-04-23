import streamlit as st

st.set_page_config(page_title="Mapeia Lead", page_icon="🎯")

st.title("🎯 MAPEIA LEAD")
st.markdown("### Sistema de Prospecção por CNAE")

# Filtros
cnae = st.text_input("CNAE", "5612")
uf = st.selectbox("UF", ["SP", "RJ", "MG", "BA", "PE", "PR", "RS", "SC"])

if st.button("BUSCAR"):
    # Dados embutidos
    empresas = {
        ("5612", "SP"): ["Gelato Sul Sorvetes - SP", "Sorveteria Kids - Campinas"],
        ("5612", "RJ"): ["Ice Mania - Rio de Janeiro"],
        ("5612", "MG"): ["Sorvete Bom - Belo Horizonte"],
        ("4721", "RJ"): ["Mercado Popular - Rio de Janeiro"],
    }
    
    resultados = empresas.get((cnae, uf), [])
    
    if resultados:
        st.success(f"✅ {len(resultados)} empresas encontradas")
        for r in resultados:
            st.write(f"- {r}")
        
        csv = "\n".join(resultados)
        st.download_button("📥 Exportar CSV", csv, f"leads_{cnae}_{uf}.csv")
    else:
        st.warning("Nenhuma empresa encontrada")

# Rodapé com o nome do desenvolvedor
st.markdown("---")
st.markdown("### 👨‍💻 Desenvolvido por **Glailton Nascimento**")
st.caption("© 2025 Mapeia Lead - Todos os direitos reservados")
