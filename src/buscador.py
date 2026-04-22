
# src/buscador.py
import streamlit as st
import pandas as pd
import requests
import time
from typing import List, Dict

class BuscadorCNPJ:
    def __init__(self):
        """Carrega a base local de CNPJs"""
        try:
            # Tenta carregar a base do Brasil completo
            self.base = pd.read_parquet("dados/base_brasil.parquet")
            st.success(f"✅ Base carregada: {len(self.base):,} empresas ativas em todo Brasil")
        except FileNotFoundError:
            try:
                # Fallback: tenta carregar estado por estado
                self.base = self._carregar_estados()
            except:
                self.base = None
                st.error("""
                ❌ Base de dados não encontrada!
                
                Execute os scripts na seguinte ordem:
                1. python baixar_base.py
                2. python processar_base.py
                
                Ou aguarde o processamento na nuvem.
                """)
    
    def _carregar_estados(self):
        """Carrega bases de estados individuais"""
        import os
        estados = ['SP', 'RJ', 'MG']  # Adicione mais conforme baixar
        dfs = []
        
        for uf in estados:
            arquivo = f"dados/base_{uf}.parquet"
            if os.path.exists(arquivo):
                df = pd.read_parquet(arquivo)
                dfs.append(df)
                print(f"✅ Carregado {uf}: {len(df):,} empresas")
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return None
    
    def buscar_por_cnae_uf(self, cnae: str, uf: str, cidade: str = "") -> List[Dict]:
        """
        Busca empresas por CNAE e UF na base local
        """
        if self.base is None:
            return []
        
        # Limpa o CNAE (7 dígitos)
        cnae_clean = str(cnae).replace('-', '').replace('.', '')[:7]
        
        with st.spinner(f"🔍 Buscando empresas com CNAE {cnae_clean} em {uf}..."):
            # Filtra por CNAE
            resultado = self.base[self.base['CNAE'] == cnae_clean]
            
            # Filtra por UF
            resultado = resultado[resultado['UF'] == uf.upper()]
            
            # Filtra por cidade (se informada)
            if cidade:
                resultado = resultado[resultado['Cidade'].str.contains(cidade.upper(), na=False)]
            
            # Limita resultados para performance
            resultado = resultado.head(100)
        
        if resultado.empty:
            return []
        
        # Converte para lista de dicionários
        empresas = []
        for _, row in resultado.iterrows():
            empresas.append({
                'Razão Social': row.get('Nome_Fantasia', 'N/A'),
                'CNPJ': row.get('CNPJ', 'N/A'),
                'Cidade': row.get('Cidade', 'N/A'),
                'UF': row.get('UF', 'N/A'),
                'Telefone': 'Consultar na API',
                'E-mail': 'Consultar na API',
                'Endereço': f"{row.get('Logradouro', '')}, {row.get('Numero', '')}",
                'Status': 'ATIVA'
            })
        
        return empresas
    
    def enriquecer_com_api(self, empresas: List[Dict]) -> List[Dict]:
        """
        Opcional: Busca telefone e e-mail na BrasilAPI
        """
        for i, empresa in enumerate(empresas[:10]):  # Limita a 10 para não travar
            cnpj = ''.join(filter(str.isdigit, empresa['CNPJ']))
            
            try:
                url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    dados = response.json()
                    empresa['Telefone'] = dados.get('ddd_telefone_1', 'Não informado')
                    empresa['E-mail'] = dados.get('email', 'Não informado')
                
                time.sleep(0.5)  # Evita bloqueio
            except:
                pass
            
            empresas[i] = empresa
        
        return empresas
