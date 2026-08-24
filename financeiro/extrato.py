#Armazena os dados brutos do banco de dados

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List

@dataclass
class ItemExtrato:
    fitid: str
    data: date
    descricao: str
    valor: Decimal

class Extrato:
    def __init__(self, conta_id: str, data_inicio: date, data_fim: date):
        self.conta_id = conta_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.itens: List[ItemExtrato] = []

    def carregar_itens(self, novos_itens: List[ItemExtrato]) -> None:
        # Mantém controle dos IDs existentes para evitar duplicações
        fitids_existentes = {item.fitid for item in self.itens}
        
        for item in novos_itens:
            if item.fitid not in fitids_existentes:
                self.itens.append(item)
                fitids_existentes.add(item.fitid)