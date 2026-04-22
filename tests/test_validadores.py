
import sys
import os

# Adiciona a pasta raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validadores import validar_cnae, validar_uf, validar_cidade

def test_validar_cnae():
    # Testes com CNAE válido
    valido, resultado = validar_cnae("56120")
    assert valido == True
    assert resultado == "56120"
    
    valido, resultado = validar_cnae("5612-0")
    assert valido == True
    assert resultado == "56120"
    
    # Testes com CNAE inválido
    valido, erro = validar_cnae("")
    assert valido == False
    
    valido, erro = validar_cnae("123")
    assert valido == False
    
    valido, erro = validar_cnae("12345678")
    assert valido == False

def test_validar_uf():
    # Testes com UF válida
    valido, resultado = validar_uf("SP")
    assert valido == True
    assert resultado == "SP"
    
    valido, resultado = validar_uf("RJ")
    assert valido == True
    
    # Teste com UF vazia (opcional)
    valido, resultado = validar_uf("")
    assert valido == True
    
    # Teste com UF inválida
    valido, erro = validar_uf("XX")
    assert valido == False

def test_validar_cidade():
    # Testes com cidade válida
    valido, resultado = validar_cidade("São Paulo")
    assert valido == True
    assert resultado == "SÃO PAULO"
    
    # Teste com cidade vazia (opcional)
    valido, resultado = validar_cidade("")
    assert valido == True
    assert resultado == ""
    
    # Teste com cidade muito curta
    valido, erro = validar_cidade("A")
    assert valido == False

def test_integracao_busca():
    # Teste de integração com o buscador
    from src.buscador import BuscadorCNPJ
    
    buscador = BuscadorCNPJ()
    resultados = buscador.buscar_por_cnae_uf("56120", "SP")
    
    assert isinstance(resultados, list)
    if len(resultados) > 0:
        assert 'Razão Social' in resultados[0]
        assert 'CNPJ' in resultados[0]
        assert 'Telefone' in resultados[0]

if __name__ == "__main__":
    test_validar_cnae()
    test_validar_uf()
    test_validar_cidade()
    test_integracao_busca()
    print("✅ Todos os testes passaram!")
