#Define um limite de gastos do usuario para uma categoria especifica

from decimal import Decimal
from typing import List
from financeiro.categoria import Categoria
from financeiro.lancamento import Lancamento, StatusLancamento, TipoLancamento

class Orcamento:
    def __init__(self, id_orcamento: str, categoria: Categoria, valor_limite: Decimal, mes: int, ano: int):
        if valor_limite <= Decimal('0.00'):
            raise ValueError("O limite do orçamento deve ser maior que zero.")
            
        self.id_orcamento = id_orcamento
        self.categoria = categoria
        self.valor_limite = valor_limite
        self.mes = mes
        self.ano = ano

    def calcular_executado(self, lancamentos: List[Lancamento]) -> Decimal:
        total = Decimal('0.00')
        for l in lancamentos:
            if (
                l.categoria.id_categoria == self.categoria.id_categoria
                and l.tipo == TipoLancamento.DESPESA
                and l.status != StatusLancamento.CANCELADO
                and l.data_vencimento.month == self.mes
                and l.data_vencimento.year == self.ano
            ):
                total += l.valor
        return total

    def esta_estourado(self, lancamentos: List[Lancamento]) -> bool:
        return self.calcular_executado(lancamentos) > self.valor_limite

    def saldo_disponivel(self, lancamentos: List[Lancamento]) -> Decimal:
        return self.valor_limite - self.calcular_executado(lancamentos)