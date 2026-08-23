from datetime import date
from decimal import Decimal

from financeiro.categoria import Categoria, TipoCategoria
from financeiro.conta import Conta, TipoConta
from financeiro.fechamento import Fechamento
from financeiro.lancamento import Lancamento, TipoLancamento

def test_gerar_resumo_mensal():
    conta = Conta("1", "Banco", TipoConta.CORRENTE, Decimal('0.00'))
    cat = Categoria("C1", "Geral", TipoCategoria.RECEITA)
    
    r1 = Lancamento("L1", "Freelance", Decimal('1500.00'), date(2026, 8, 1), TipoLancamento.RECEITA, cat, conta)
    d1 = Lancamento("L2", "Internet", Decimal('150.00'), date(2026, 8, 5), TipoLancamento.DESPESA, cat, conta)
    
    r1.efetivar(data_pagamento=date(2026, 8, 1))
    d1.efetivar(data_pagamento=date(2026, 8, 5))
    
    resumo = Fechamento.gerar_resumo_mes(mes=8, ano=2026, lancamentos=[r1, d1])
    
    assert resumo.total_receitas == Decimal('1500.00')
    assert resumo.total_despesas == Decimal('150.00')
    assert resumo.resultado == Decimal('1350.00')