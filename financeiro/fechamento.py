#Gera relatorios e consolidacoes contabeis de um determinado mes/ano

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List
from financeiro.lancamento import Lancamento, StatusLancamento, TipoLancamento

@dataclass
class ResumoMensal:
    mes: int
    ano: int
    total_receitas: Decimal
    total_despesas: Decimal
    resultado: Decimal

class Fechamento:
    @staticmethod
    def gerar_resumo_mes(mes: int, ano: int, lancamentos: List[Lancamento]) -> ResumoMensal:
        receitas = Decimal('0.00')
        despesas = Decimal('0.00')

        for l in lancamentos:
            if l.status == StatusLancamento.REALIZADO and l.data_pagamento:
                if l.data_pagamento.month == mes and l.data_pagamento.year == ano:
                    if l.tipo == TipoLancamento.RECEITA:
                        receitas += l.valor
                    elif l.tipo == TipoLancamento.DESPESA:
                        despesas += l.valor

        return ResumoMensal(
            mes=mes,
            ano=ano,
            total_receitas=receitas,
            total_despesas=despesas,
            resultado=receitas - despesas
        )