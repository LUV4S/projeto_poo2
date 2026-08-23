from datetime import date
from decimal import Decimal
import pytest

from financeiro.categoria import Categoria, TipoCategoria
from financeiro.conta import Conta, TipoConta
from financeiro.fatura import Fatura, StatusFatura
from financeiro.lancamento import Lancamento, TipoLancamento

@pytest.fixture
def setup_fatura():
    conta = Conta("1", "Banco", TipoConta.CORRENTE, Decimal('1000.00'))
    categoria = Categoria("C1", "Mercado", TipoCategoria.DESPESA)
    fatura = Fatura("F1", mes=8, ano=2026, limite=Decimal('500.00'))
    return conta, categoria, fatura

def test_adicionar_item_e_pagar_fatura(setup_fatura):
    conta, categoria, fatura = setup_fatura
    item = Lancamento("L1", "Compras", Decimal('200.00'), date(2026, 8, 10), TipoLancamento.DESPESA, categoria, conta)
    
    fatura.adicionar_item(item)
    assert fatura.valor_total == Decimal('200.00')
    
    fatura.fechar_fatura()
    assert fatura.status == StatusFatura.FECHADA
    
    fatura.pagar(conta, date(2026, 8, 15))
    assert fatura.status == StatusFatura.PAGA
    assert conta.saldo == Decimal('800.00')

def test_adicionar_item_excedendo_limite_erro(setup_fatura):
    conta, categoria, fatura = setup_fatura
    item = Lancamento("L1", "TV 4K", Decimal('600.00'), date(2026, 8, 10), TipoLancamento.DESPESA, categoria, conta)
    
    with pytest.raises(ValueError, match="limite do cartão excedido"):
        fatura.adicionar_item(item)

def test_pagar_fatura_ainda_aberta_erro(setup_fatura):
    conta, _, fatura = setup_fatura
    with pytest.raises(ValueError, match="precisa estar FECHADA"):
        fatura.pagar(conta, date.today())