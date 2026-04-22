
import pandas as pd
from typing import List, Dict

class BuscadorCNPJ:
    def __init__(self, caminho_base: str = "dados/base_cnpjs.parquet"):
        self.caminho_base = caminho_base
        self.base = None
    
    def buscar_por_cnae_uf(self, cnae: str, uf: str, cidade: str = "") -> List[Dict]:
        empresas_exemplo = {
            "SP": [
                {'Razão Social': 'Gelato Sul Sorvetes', 'CNPJ': '12.345.678/0001-90', 'Cidade': 'São Paulo', 'Telefone': '(11) 98765-4321', 'Endereço': 'Av. Paulista, 1000'},
                {'Razão Social': 'Sorveteria Kids', 'CNPJ': '23.456.789/0001-01', 'Cidade': 'Campinas', 'Telefone': '(19) 3456-7890', 'Endereço': 'Rua das Flores, 500'},
                {'Razão Social': 'Ice Mania', 'CNPJ': '34.567.890/0001-12', 'Cidade': 'Santos', 'Telefone': '(13) 98765-1234', 'Endereço': 'Av. da Praia, 200'},
                {'Razão Social': 'Sorvete Bom Demais', 'CNPJ': '45.678.901/0001-23', 'Cidade': 'Ribeirão Preto', 'Telefone': '(16) 98765-4321', 'Endereço': 'Rua São Sebastião, 300'},
                {'Razão Social': 'Gelato Artesanal', 'CNPJ': '56.789.012/0001-34', 'Cidade': 'Sorocaba', 'Telefone': '(15) 3456-7890', 'Endereço': 'Av. Independência, 150'},
            ],
            "RJ": [
                {'Razão Social': 'Sorvete Carioca', 'CNPJ': '45.678.901/0001-23', 'Cidade': 'Rio de Janeiro', 'Telefone': '(21) 98765-4321', 'Endereço': 'Av. Atlântica, 500'},
                {'Razão Social': 'Gelato Copacabana', 'CNPJ': '56.789.012/0001-34', 'Cidade': 'Rio de Janeiro', 'Telefone': '(21) 3456-7890', 'Endereço': 'Rua Santa Clara, 100'},
            ],
            "MG": [
                {'Razão Social': 'Sorveteria Mineira', 'CNPJ': '67.890.123/0001-45', 'Cidade': 'Belo Horizonte', 'Telefone': '(31) 98765-4321', 'Endereço': 'Av. Afonso Pena, 1000'},
            ]
        }
        
        empresas = empresas_exemplo.get(uf.upper(), [])
        
        if cidade:
            empresas = [e for e in empresas if cidade.upper() in e['Cidade'].upper()]
        
        for e in empresas:
            e['UF'] = uf.upper()
            e['Status'] = 'ATIVA'
        
        return empresas
