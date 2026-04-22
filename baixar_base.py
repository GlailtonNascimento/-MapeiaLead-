
# Google Colab - MAPEIA LEAD
# Baixar base de CNPJs do BRASIL COMPLETO

import os
import requests
from tqdm import tqdm

print("=" * 60)
print("📥 MAPEIA LEAD - Download da Base de CNPJs do BRASIL TODO")
print("=" * 60)

# Montar Google Drive para salvar os dados
from google.colab import drive
drive.mount('/content/drive')

# Criar pasta no Drive
os.makedirs("/content/drive/MyDrive/mapeia_lead_dados", exist_ok=True)

# TODOS OS 27 ESTADOS DO BRASIL (corrigido)
estados = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

print(f"\n📌 Estados para download: {len(estados)} estados")
print(f"   {', '.join(estados)}")
print("⚠️  Atenção: Cada estado leva ~10-30 minutos")
print("⏱️  Tempo total estimado: 2-4 horas")
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
            
            # Salva no Google Drive
            zip_path = f"/content/drive/MyDrive/mapeia_lead_dados/cnpj_{uf}.zip"
            
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
sucessos = 0
falhas = 0

for uf in estados:
    if baixar_estado(uf):
        sucessos += 1
    else:
        falhas += 1

print("\n" + "=" * 60)
print("✅ DOWNLOAD CONCLUÍDO!")
print(f"📊 Resumo: {sucessos} estados baixados, {falhas} falhas")
print(f"📁 Arquivos salvos em: /content/drive/MyDrive/mapeia_lead_dados/")
print("=" * 60)
print("\n▶️ Próximo passo: Executar o processar_base.py no Colab")
