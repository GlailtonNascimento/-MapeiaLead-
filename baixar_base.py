
%%writefile baixar_base.py
import os
import requests
from tqdm import tqdm

print("="*60)
print("📥 MAPEIA LEAD - Download da Base de CNPJs")
print("="*60)

# Criar pasta para os dados
os.makedirs("dados_brutos", exist_ok=True)

# Estados para download (comece com 1 para testar)
estados = ["SP"]

print(f"\n📌 Estados para download: {', '.join(estados)}")
print("⚠️  Atenção: Cada estado leva ~15-30 minutos")
print()

def baixar_estado(uf):
    """Baixa os dados de um estado"""
    url = f"https://data.brasil.io/dataset/cnpj/data/cnpj_completo_{uf.lower()}.zip"
    
    print(f"📥 Baixando {uf}...")
    
    try:
        response = requests.get(url, stream=True, timeout=120)
        
        if response.status_code == 200:
            tamanho = int(response.headers.get('content-length', 0))
            tamanho_mb = tamanho / (1024 * 1024)
            print(f"   Tamanho: {tamanho_mb:.1f} MB")
            
            zip_path = f"dados_brutos/cnpj_{uf}.zip"
            
            with open(zip_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192), 
                                 total=tamanho/8192, 
                                 unit='chunk',
                                 desc=f"   {uf}"):
                    f.write(chunk)
            
            print(f"   ✅ {uf} baixado com sucesso!")
            return True
        else:
            print(f"   ❌ Erro HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

# Baixar cada estado
for uf in estados:
    baixar_estado(uf)

print("\n" + "="*60)
print("✅ DOWNLOAD CONCLUÍDO!")
print("="*60)
