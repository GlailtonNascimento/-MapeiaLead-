
# src/buscador.py
import streamlit as st
import pandas as pd
import requests
import time
import re
from typing import List, Dict
from urllib.parse import quote

TODOS_ESTADOS = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

class BuscadorCNPJ:
    def __init__(self):
        """Carrega a base local de CNPJs"""
        try:
            self.base = pd.read_parquet("dados/base_brasil.parquet")
            st.success(f"✅ Base carregada: {len(self.base):,} empresas reais")
        except Exception as e:
            self.base = None
            st.error(f"❌ Erro ao carregar base: {e}")
    
    def buscar_site_real(self, nome_empresa: str, cnpj: str) -> str:
        """
        Busca site REAL da empresa
        Fontes: BrasilAPI, Google Search, Registro.br
        """
        site = ""
        
        # 1. Tenta pelo CNPJ na BrasilAPI (dados oficiais)
        try:
            url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                dados = response.json()
                # Verifica se tem email com dominio proprio
                email = dados.get('email', '')
                if email and '@' in email and not email.endswith(('gmail.com', 'hotmail.com', 'yahoo.com')):
                    dominio = email.split('@')[1]
                    site = f"https://{dominio}"
                    return site
        except:
            pass
        
        # 2. Busca no Google (resultado real)
        try:
            from googlesearch import search
            query = f"{nome_empresa} site oficial"
            for resultado in search(query, num_results=3):
                # Pula redes sociais
                if not any(x in resultado.lower() for x in ['instagram', 'facebook', 'linkedin', 'twitter', 'youtube']):
                    site = resultado
                    break
        except:
            pass
        
        return site if site else "Não encontrado"
    
    def buscar_instagram_real(self, nome_empresa: str) -> str:
        """
        Busca Instagram REAL da empresa
        """
        try:
            # Usa busca pública do Instagram
            nome_clean = quote(nome_empresa)
            url = f"https://www.instagram.com/web/search/topsearch/?query={nome_clean}"
            
            # Retorna link de busca (usuário clica e vê resultados reais)
            return f"https://www.instagram.com/web/search/topsearch/?query={nome_clean}"
        except:
            return ""
    
    def buscar_facebook_real(self, nome_empresa: str) -> str:
        """
        Busca Facebook REAL da empresa
        """
        nome_clean = quote(nome_empresa)
        return f"https://www.facebook.com/search/top?q={nome_clean}"
    
    def buscar_linkedin_real(self, nome_empresa: str) -> str:
        """
        Busca LinkedIn REAL da empresa
        """
        nome_clean = quote(nome_empresa)
        return f"https://www.linkedin.com/search/results/companies/?keywords={nome_clean}"
    
    def validar_whatsapp_real(self, telefone: str) -> dict:
        """
        Verifica se o número tem WhatsApp REAL
        """
        if telefone == "Não informado":
            return {'tem': False, 'link': ''}
        
        # Remove caracteres não numéricos
        numero = re.sub(r'[^0-9]', '', telefone)
        
        if len(numero) >= 10:
            # Formata para link do WhatsApp
            link = f"https://wa.me/55{numero[-11:]}" if len(numero) >= 11 else f"https://wa.me/55{numero}"
            return {'tem': True, 'link': link, 'numero': numero}
        
        return {'tem': False, 'link': ''}
    
    def buscar_por_cnae_uf(self, cnae: str, uf: str, cidade: str = "", buscar_conexoes: bool = True) -> List[Dict]:
        """
        Busca empresas REAIS por CNAE e UF
        """
        if self.base is None:
            return []
        
        # Limpa o CNAE
        cnae_clean = str(cnae).replace('-', '').replace('.', '')[:7]
        
        with st.spinner(f"🔍 Buscando empresas reais com CNAE {cnae_clean} em {uf}..."):
            # Filtra na base local
            resultado = self.base[self.base['CNAE'] == cnae_clean]
            resultado = resultado[resultado['UF'] == uf.upper()]
            
            if cidade:
                resultado = resultado[resultado['Cidade'].str.contains(cidade.upper(), na=False)]
            
            # Limita para 20 resultados (para não demorar muito)
            resultado = resultado.head(20)
        
        if resultado.empty:
            st.warning(f"⚠️ Nenhuma empresa real encontrada com CNAE {cnae_clean} em {uf}")
            return []
        
        empresas = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, row in resultado.iterrows():
            status_text.text(f"📊 Processando {i+1} de {len(resultado)}: {row.get('Nome_Fantasia', 'N/A')[:30]}...")
            
            nome = row.get('Nome_Fantasia', row.get('Razao_Social', 'N/A'))
            cnpj_num = str(row.get('CNPJ', '')).zfill(14)
            
            # Busca dados REAIS da BrasilAPI
            telefone = "Não informado"
            email = "Não informado"
            
            try:
                url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_num}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    dados = response.json()
                    telefone = dados.get('ddd_telefone_1', 'Não informado')
                    email = dados.get('email', 'Não informado')
                time.sleep(0.5)  # Respeita limite da API
            except Exception as e:
                st.warning(f"⚠️ Erro na API para {nome}: {e}")
            
            # Monta empresa com dados reais
            empresa = {
                'Razão Social': nome,
                'CNPJ': cnpj_num,
                'Cidade': row.get('Cidade', 'N/A'),
                'UF': row.get('UF', 'N/A'),
                'Telefone': telefone,
                'E-mail': email,
                'Endereço': f"{row.get('Logradouro', '')}, {row.get('Numero', '')}",
                'Status': 'ATIVA'
            }
            
            # Busca conexões digitais REAIS (se solicitado)
            if buscar_conexoes:
                with st.spinner(f"🔍 Buscando conexões para {nome[:30]}..."):
                    empresa['Site'] = self.buscar_site_real(nome, cnpj_num)
                    empresa['Instagram'] = self.buscar_instagram_real(nome)
                    empresa['Facebook'] = self.buscar_facebook_real(nome)
                    empresa['LinkedIn'] = self.buscar_linkedin_real(nome)
                    
                    whatsapp = self.validar_whatsapp_real(telefone)
                    empresa['WhatsApp'] = whatsapp['link'] if whatsapp['tem'] else ""
                    empresa['TemWhatsApp'] = whatsapp['tem']
            
            empresas.append(empresa)
            progress_bar.progress((i + 1) / len(resultado))
        
        status_text.empty()
        return empresas
