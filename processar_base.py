
# processar_base.py
import pandas as pd
import zipfile
import os
from tqdm import tqdm

print("=" * 60)
print("🔄 MAPEIA LEAD - Processamento da Base de CNPJs")
print("=" * 60)

# Criar pasta para dados processados
os.makedirs("dados", exist_ok=True)

# Estados que foram baixados (mesmos do baixar_base.py)
estados = ["SP", "RJ", "MG"]  # Altere conforme os estados baixados

def processar_estado(uf):
    """Processa o arquivo de um estado"""
    
    zip_path = f"dados_brutos/cnpj_{uf}.zip"
    
    if not os.path.exists(zip_path):
        print(f"⚠️ Arquivo não encontrado: {zip_path}")
        return None
    
    print(f"\n📂 Processando {uf}...")
    
    try:
        # Abre o ZIP e lê o CSV
        with zipfile.ZipFile(zip_path, 'r') as z:
            csv_file = [f for f in z.namelist() if f.endswith('.csv')][0]
            
            # Lê em partes para não pesar
            chunks = []
            for chunk in tqdm(pd.read_csv(z.open(csv_file), 
                                         sep=';', 
                                         encoding='utf-8', 
                                         dtype=str,
                                         chunksize=100000),
                             desc=f"   Lendo {uf}"):
                chunks.append(chunk)
            
            df = pd.concat(chunks, ignore_index=True)
        
        # Seleciona apenas colunas necessárias
        colunas = ['cnpj', 'cnae_fiscal_principal', 'uf', 'municipio', 
                   'situacao_cadastral', 'nome_fantasia', 'logradouro', 'numero']
        
        colunas_existentes = [c for c in colunas if c in df.columns]
        df = df[colunas_existentes]
        
        # Renomeia para português
        df = df.rename(columns={
            'cnpj': 'CNPJ',
            'cnae_fiscal_principal': 'CNAE',
            'uf': 'UF',
            'municipio': 'Cidade',
            'situacao_cadastral': 'Situacao',
            'nome_fantasia': 'Nome_Fantasia',
            'logradouro': 'Logradouro',
            'numero': 'Numero'
        })
        
        # Filtra apenas ATIVAS
        df = df[df['Situacao'].isin(['ATIVA', '02'])]
        
        # Salva em Parquet
        output_file = f"dados/base_{uf}.parquet"
        df.to_parquet(output_file, index=False)
        
        print(f"   ✅ {uf}: {len(df):,} empresas ativas salvas")
        return df
        
    except Exception as e:
        print(f"   ❌ Erro em {uf}: {e}")
        return None

# Processar cada estado
todas = []
for uf in estados:
    df = processar_estado(uf)
    if df is not None:
        todas.append(df)

# Unificar todos
if todas:
    print("\n🔗 Unificando todos os estados...")
    df_brasil = pd.concat(todas, ignore_index=True)
    
    # Salvar base única
    df_brasil.to_parquet("dados/base_brasil.parquet", index=False)
    
    print("\n" + "=" * 60)
    print("✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"📊 Total de empresas ativas: {len(df_brasil):,}")
    print(f"📁 Arquivo: dados/base_brasil.parquet")
    print("=" * 60)
    print("\n▶️ Próximo passo: streamlit run app.py")
else:
    print("\n❌ Nenhum estado processado com sucesso!")
