
# prospector.py
import pandas as pd
import os

def gerar_lista_prospeccao(caminho_base, cnae_alvo, uf_alvo=None):
    """
    Filtra a base de CNPJs por CNAE, apenas empresas ATIVAS.
    
    Parâmetros:
    - caminho_base: caminho do arquivo CSV/Parquet com os dados
    - cnae_alvo: código CNAE (ex: '5612' para sorveterias)
    - uf_alvo: (opcional) sigla do estado (ex: 'SP')
    """
    print(f"🚀 Iniciando Mapeamento: CNAE {cnae_alvo}")
    arquivo_saida = 'leads_ativos_prontos.csv'
    
    # Remove arquivo anterior se existir
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)
    
    total_leads = 0
    
    # Chunking para não travar o PC
    for i, chunk in enumerate(pd.read_csv(caminho_base, chunksize=100000, dtype=str, encoding='utf-8')):
        
        print(f"\n📦 Processando lote {i+1}...")
        
        # 1. Filtro por CNAE
        mask = chunk['cnae_fiscal_principal'].str.startswith(cnae_alvo, na=False)
        
        # 2. Filtro por Situação Ativa (código '02' ou 'ATIVA')
        if 'situacao_cadastral' in chunk.columns:
            mask = mask & (chunk['situacao_cadastral'].isin(['02', 'ATIVA']))
        elif 'situacao' in chunk.columns:
            mask = mask & (chunk['situacao'].isin(['02', 'ATIVA']))
            
        # 3. Filtro Opcional por Estado (UF)
        if uf_alvo:
            mask = mask & (chunk['uf'] == uf_alvo.upper())
        
        leads = chunk[mask]
        
        # Selecionar apenas o que interessa para o prospector
        colunas_contato = [
            'cnpj', 'razao_social', 'nome_fantasia', 'ddd_telefone_1', 
            'telefone_1', 'email', 'logradouro', 'numero', 'municipio', 'uf'
        ]
        
        # Ajusta as colunas caso o nome varie na base
        cols_presentes = [c for c in colunas_contato if c in leads.columns]
        
        if not leads.empty:
            leads[cols_presentes].to_csv(arquivo_saida, mode='a', index=False, header=not os.path.exists(arquivo_saida))
            total_leads += len(leads)
            print(f"   ✅ {len(leads)} novos leads ativos encontrados...")

    print(f"\n" + "="*60)
    print(f"🎯 SUCESSO! Lista pronta para o comercial!")
    print(f"📊 Total de leads encontrados: {total_leads}")
    print(f"📁 Arquivo salvo em: {arquivo_saida}")
    print("="*60)

# Exemplo de uso direto (se executar o arquivo)
if __name__ == "__main__":
    # Altere o caminho conforme sua base
    gerar_lista_prospeccao(
        caminho_base='dados/base_brasil.csv',  # ou .parquet
        cnae_alvo='5612',  # Sorveterias
        uf_alvo='SP'       # São Paulo
  )
