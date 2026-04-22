
%%writefile baixar_base.py
import os
import requests
from tqdm import tqdm

print("="*60)
print("📥 MAPEIA LEAD - Download da Base Oficial da Receita")
print("="*60)

os.makedirs("dados_brutos", exist_ok=True)

# URL OFICIAL da Receita Federal (janeiro/2025)
# Para outros meses, mude o "2025-01" na URL
url_base = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-01"

estados = ["SP"]

print(f"\n📌 Estados: {estados}")
print(f"📌 Fonte: Receita Federal (oficial)")
print()

def baixar_estado(uf):
    nome_arquivo = f"Estabelecimentos_{uf}.zip"
    url = f"{url_base}/{nome_arquivo}"
    
    print(f"📥 Baixando {uf}...")
    print(f"   URL: {url}")
    
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

for uf in estados:
    baixar_estado(uf)

print("\n" + "="*60)
print("✅ DOWNLOAD CONCLUÍDO!")
print("="*60)
