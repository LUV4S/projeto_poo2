from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List
from financeiro.lancamento import Lancamento, TipoLancamento
from financeiro.conta import Conta

class StatusFatura(Enum):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    PAGA = "PAGA"

class Fatura:
    def __init__(self, id_fatura: str, mes: int, ano: int, limite: Decimal):
        self.id_fatura = id_fatura
        self.mes = mes
        self.ano = ano
        self.limite = limite
        self.status = StatusFatura.ABERTA
        self.itens: List[Lancamento] = []

    @property
    def valor_total(self) -> Decimal:
        return sum((item.valor for item in self.itens), Decimal('0.00'))

    def adicionar_item(self, item: Lancamento) -> None:
        if self.status != StatusFatura.ABERTA:
            raise ValueError("Não é possível adicionar compras em uma fatura que não esteja ABERTA.")
            
        if self.valor_total + item.valor > self.limite:
            raise ValueError("Operação negada: limite do cartão excedido para esta fatura.")
            
        self.itens.append(item)

    def fechar_fatura(self) -> None:
        if self.status != StatusFatura.ABERTA:
            raise ValueError("Apenas faturas abertas podem ser fechadas.")
        self.status = StatusFatura.FECHADA

    def pagar(self, conta_pagamento: Conta, data_pagamento: date) -> Lancamento:
        if self.status != StatusFatura.FECHADA:
            raise ValueError("A fatura precisa estar FECHADA para ser paga.")
            
        lancamento_pagamento = Lancamento(
            id_lancamento=f"PAG-FAT-{self.id_fatura}",
            descricao=f"Pagamento Fatura {self.mes}/{self.ano}",
            valor=self.valor_total,
            data_vencimento=data_pagamento,
            tipo=TipoLancamento.DESPESA,
            categoria=None,
            conta=conta_pagamento
        )
        lancamento_pagamento.efetivar(data_pagamento)
        self.status = StatusFatura.PAGA
        return lancamento_pagamento