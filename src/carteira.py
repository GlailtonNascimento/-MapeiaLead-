
from datetime import datetime
from typing import List, Dict

class CarteiraProspector:
    def __init__(self, arquivo_json: str = "data/carteira.json"):
        self.arquivo = arquivo_json
        self.carteira = {'leads': []}
    
    def adicionar_lead(self, empresa: Dict, observacao: str = ""):
        lead = {
            'id': len(self.carteira['leads']) + 1,
            'empresa': empresa.get('Razão Social', 'N/A'),
            'cnpj': empresa.get('CNPJ', 'N/A'),
            'cidade': empresa.get('Cidade', 'N/A'),
            'telefone': empresa.get('Telefone', 'N/A'),
            'data_adicao': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'status': 'Novo',
            'observacao': observacao
        }
        self.carteira['leads'].append(lead)
        return lead
    
    def listar_leads(self, status_filter: str = None) -> List[Dict]:
        if status_filter:
            return [l for l in self.carteira['leads'] if l['status'] == status_filter]
        return self.carteira['leads']
