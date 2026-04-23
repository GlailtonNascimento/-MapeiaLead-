import pandas as pd
import os

def gerar_lista_prospeccao(caminho_base, cnae_alvo, uf_alvo=None):
    """
    Gera lista de leads por CNAE e UF
    """
    print("="*50)
    print(f"🎯 MAPEIA LEAD - Buscando CNAE {cnae_alvo} em {uf_alvo if uf_alvo else 'BRASIL'}")
    print("="*50)
    
    arquivo_saida = 'leads_ativos_prontos.csv'
    
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)
    
    total_leads = 0
    
    for chunk in pd.read_csv(caminho_base, chunksize=100000, dtype=str):
        mask = chunk['cnae_fiscal_principal'].str.startswith(cnae_alvo, na=False)
        
        if 'situacao_cadastral' in chunk.columns:
            mask = mask & (chunk['situacao_cadastral'].isin(['02', 'ATIVA']))
        
        if uf_alvo:
            mask = mask & (chunk['uf'] == uf_alvo.upper())
        
        leads = chunk[mask]
        
        if not leads.empty:
            leads.to_csv(arquivo_saida, mode='a', index=False, header=not os.path.exists(arquivo_saida))
            total_leads += len(leads)
            print(f"✅ {len(leads)} leads encontrados")
    
    print("="*50)
    print(f"🎯 TOTAL DE LEADS: {total_leads}")
    print(f"📁 Arquivo salvo: {arquivo_saida}")
    print("="*50)
    
    return total_leads

if __name__ == "__main__":
    print("\n📋 Exemplos de busca:")
    print("1 - Sorveterias em SP (CNAE 5612)")
    print("2 - Mercados no RJ (CNAE 4721)")
    print("3 - Farmácias em MG (CNAE 4771)")
    
    opcao = input("\nEscolha uma opção (1/2/3) ou digite o CNAE desejado: ")
    
    if opcao == "1":
        gerar_lista_prospeccao('dados/base_brasil.csv', '5612', 'SP')
    elif opcao == "2":
        gerar_lista_prospeccao('dados/base_brasil.csv', '4721', 'RJ')
    elif opcao == "3":
        gerar_lista_prospeccao('dados/base_brasil.csv', '4771', 'MG')
    else:
        cnae = opcao
        uf = input("Digite a UF (ex: SP): ")
        gerar_lista_prospeccao('dados/base_brasil.csv', cnae, uf)
