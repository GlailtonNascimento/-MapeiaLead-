
import re

def validar_cnae(cnae):
    if not cnae:
        return False, "CNAE é obrigatório"
    
    cnae_limpo = re.sub(r'[^0-9]', '', cnae)
    
    if len(cnae_limpo) != 7:
        return False, "CNAE deve ter 7 dígitos"
    
    return True, cnae_limpo

def validar_uf(uf):
    if not uf:
        return True, None
    
    uf = uf.upper().strip()
    ufs_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                   'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                   'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    
    if uf not in ufs_validas:
        return False, "UF inválida"
    
    return True, uf

def validar_cidade(cidade):
    if cidade and len(cidade.strip()) < 2:
        return False, "Cidade muito curta"
    return True, cidade.strip().upper() if cidade else ""
