from dataclasses import dataclass
from typing import List, Tuple
from financeiro.extrato import ItemExtrato
from financeiro.lancamento import Lancamento, StatusLancamento

@dataclass
class ParConciliado:
    item_extrato: ItemExtrato
    lancamento: Lancamento

class Conciliacao:
    def __init__(self, conta_id: str):
        self.conta_id = conta_id
        self.pares_conciliados: List[ParConciliado] = []

    def sugerir_matches(
        self, itens_extrato: List[ItemExtrato], lancamentos: List[Lancamento], margem_dias: int = 2
    ) -> List[Tuple[ItemExtrato, Lancamento]]:
        sugestoes = []
        for item in itens_extrato:
            for lancamento in lancamentos:
                if lancamento.status == StatusLancamento.CANCELADO:
                    continue
                
                mesmo_valor = abs(item.valor) == abs(lancamento.valor)
                diferenca_dias = abs((item.data - lancamento.data_vencimento).days)
                
                if mesmo_valor and diferenca_dias <= margem_dias:
                    sugestoes.append((item, lancamento))
        return sugestoes

    def conciliar(self, item_extrato: ItemExtrato, lancamento: Lancamento) -> None:
        if abs(item_extrato.valor) != abs(lancamento.valor):
            raise ValueError("Não é possível conciliar itens com valores divergentes.")
            
        if lancamento.status != StatusLancamento.REALIZADO:
            lancamento.efetivar(data_pagamento=item_extrato.data)
            
        self.pares_conciliados.append(ParConciliado(item_extrato=item_extrato, lancamento=lancamento))