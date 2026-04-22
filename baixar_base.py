
%%writefile baixar_base.py
import os
import requests
from tqdm import tqdm

print("="*60)
print("📥 MAPEIA LEAD - Download da Base Oficial da Receita")
print("="*60)

os.makedirs("dados_brutos", exist_ok=True)

# URL oficial da Receita Federal (janeiro/2025)
url_base = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-01"

# TODOS OS 27 ESTADOS DO BRASIL
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
           'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
           'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

print(f"\n📌 Estados para download: {len(estados)} estados")
print(f"   {', '.join(estados)}")
print(f"📌 Fonte: Receita Federal (oficial)")
print("⚠️  Atenção: Este processo pode levar de 6 a 8 horas")
print()

def baixar_estado(uf):
    nome_arquivo = f"Estabelecimentos_{uf}.zip"
    url = f"{url_base}/{nome_arquivo}"
    
    print(f"📥 Baixando {uf}...")
    
    try:
        response = requests.get(url, stream=True, timeout=120)
        
        if response.status_code == 200:
            tamanho = int(response.headers.get('content-length', 0))
            tamanho_mb = tamanho / (1024 * 1024)
            print(f"   Tamanho: {tamanho_mb:.1f} MB")
            
            zip_path = f"dados_brutos/{nome_arquivo}"
            
            with open(zip_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192), 
                                 total=tamanho/8192, 
                                 unit='chunk',
                                 desc=f"   {uf}"):
                    f.write(chunk)
            
            print(f"   ✅ {uf} baixado com sucesso!")
            return True
        else:
            print(f"   ❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

# Baixar cada estado
sucessos = 0
for uf in estados:
    if baixar_estado(uf):
        sucessos += 1

print("\n" + "="*60)
print("✅ DOWNLOAD CONCLUÍDO!")
print(f"📊 Resumo: {sucessos}/{len(estados)} estados baixados com sucesso")
print("📁 Arquivos salvos em: dados_brutos/")
print("="*60)
print("\n▶️ Próximo passo: python processar_base.py")
