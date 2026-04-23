import streamlit as st

st.set_page_config(page_title="Mapeia Lead", page_icon="🎯")

st.title("🎯 MAPEIA LEAD")
st.markdown("### Sistema de Prospecção por CNAE")

# Filtros
cnae = st.text_input("CNAE", "5612")
uf = st.selectbox("UF", ["SP", "RJ", "MG", "BA", "PE", "PR", "RS", "SC"])

if st.button("BUSCAR"):
    # Dados embutidos (não precisa de pandas)
    empresas = {
        ("5612", "SP"): ["Gelato Sul Sorvetes - SP - (11) 98765-4321", "Sorveteria Kids - Campinas - (19) 98765-4322"],
        ("5612", "RJ"): ["Ice Mania - Rio - (21) 98765-4323"],
        ("5612", "MG"): ["Sorvete Bom - BH - (31) 98765-4324"],
        ("4721", "RJ"): ["Mercado Popular - Rio - (21) 98765-4325"],
    }
    
    resultados = empresas.get((cnae, uf), [])
    
    if resultados:
        st.success(f"✅ {len(resultados)} empresas encontradas")
        for r in resultados:
            st.write(f"- {r}")
        
        # Criar CSV manualmente
        csv = "\n".join(resultados)
        st.download_button("📥 Exportar CSV", csv, f"leads_{cnae}_{uf}.csv")
    else:
        st.warning("Nenhuma empresa encontrada")
