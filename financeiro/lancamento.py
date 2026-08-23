from datetime import date
from decimal import Decimal
from enum import Enum
from financeiro.categoria import Categoria
from financeiro.conta import Conta

class TipoLancamento(Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

class StatusLancamento(Enum):
    PENDENTE = "PENDENTE"
    REALIZADO = "REALIZADO"
    CANCELADO = "CANCELADO"

class Lancamento:
    def __init__(
        self,
        id_lancamento: str,
        descricao: str,
        valor: Decimal,
        data_vencimento: date,
        tipo: TipoLancamento,
        categoria: Categoria,
        conta: Conta
    ):
        if valor <= Decimal('0.00'):
            raise ValueError("O valor do lançamento deve ser maior que zero.")
            
        self.id_lancamento = id_lancamento
        self.descricao = descricao
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.tipo = tipo
        self.categoria = categoria
        self.conta = conta
        self.status = StatusLancamento.PENDENTE
        self.data_pagamento: date = None

    def efetivar(self, data_pagamento: date = None) -> None:
        if self.status == StatusLancamento.REALIZADO:
            raise ValueError("Lançamento já foi efetivado.")
            
        self.data_pagamento = data_pagamento or date.today()
        
        if self.tipo == TipoLancamento.RECEITA:
            self.conta.depositar(self.valor)
        elif self.tipo == TipoLancamento.DESPESA:
            self.conta.sacar(self.valor)
            
        self.status = StatusLancamento.REALIZADO

    def cancelar(self) -> None:
        if self.status == StatusLancamento.CANCELADO:
            return
            
        if self.status == StatusLancamento.REALIZADO:
            if self.tipo == TipoLancamento.RECEITA:
                self.conta.sacar(self.valor)
            elif self.tipo == TipoLancamento.DESPESA:
                self.conta.depositar(self.valor)
                
        self.status = StatusLancamento.CANCELADO

    def eh_atrasado(self) -> bool:
        return self.status == StatusLancamento.PENDENTE and date.today() > self.data_vencimento