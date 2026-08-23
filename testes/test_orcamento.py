from datetime import date
from decimal import Decimal
import pytest

from financeiro.categoria import Categoria, TipoCategoria
from financeiro.conta import Conta, TipoConta
from financeiro.lancamento import Lancamento, TipoLancamento
from financeiro.orcamento import Orcamento

def test_calculo_executado_e_estouro_orcamento():
    cat = Categoria("C1", "Transporte", TipoCategoria.DESPESA)
    conta = Conta("1", "Banco", TipoConta.CORRENTE)
    orcamento = Orcamento("O1", categoria=cat, valor_limite=Decimal('300.00'), mes=8, ano=2026)
    
    despesa1 = Lancamento("L1", "Gasolina", Decimal('200.00'), date(2026, 8, 5), TipoLancamento.DESPESA, cat, conta)
    despesa2 = Lancamento("L2", "Uber", Decimal('150.00'), date(2026, 8, 12), TipoLancamento.DESPESA, cat, conta)
    
    lancamentos = [despesa1, despesa2]
    
    assert orcamento.calcular_executado(lancamentos) == Decimal('350.00')
    assert orcamento.esta_estourado(lancamentos) is True
    assert orcamento.saldo_disponivel(lancamentos) == Decimal('-50.00')

def test_orcamento_limite_invalido_erro():
    cat = Categoria("C1", "Transporte", TipoCategoria.DESPESA)
    with pytest.raises(ValueError, match="maior que zero"):
        Orcamento("O1", categoria=cat, valor_limite=Decimal('0.00'), mes=8, ano=2026)

def test_calculo_executado_e_estouro_orcamento():
    cat = Categoria("C1", "Transporte", TipoCategoria.DESPESA)
    conta = Conta("1", "Banco", TipoConta.CORRENTE)
    orcamento = Orcamento("O1", categoria=cat, valor_limite=Decimal('300.00'), mes=8, ano=2026)
    
    despesa1 = Lancamento("L1", "Gasolina", Decimal('200.00'), date(2026, 8, 5), TipoLancamento.DESPESA, cat, conta)
    despesa2 = Lancamento("L2", "Uber", Decimal('150.00'), date(2026, 8, 12), TipoLancamento.DESPESA, cat, conta)
    
    lancamentos = [despesa1, despesa2]
    
    assert orcamento.calcular_executado(lancamentos) == Decimal('350.00')
    assert orcamento.esta_estourado(lancamentos) is True
    assert orcamento.saldo_disponivel(lancamentos) == Decimal('-50.00')

def test_orcamento_limite_invalido_erro():
    cat = Categoria("C1", "Transporte", TipoCategoria.DESPESA)
    with pytest.raises(ValueError, match="maior que zero"):
        Orcamento("O1", categoria=cat, valor_limite=Decimal('0.00'), mes=8, ano=2026)