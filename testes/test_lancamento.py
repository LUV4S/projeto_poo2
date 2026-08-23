from datetime import date
from decimal import Decimal
import pytest

from financeiro.categoria import Categoria, TipoCategoria
from financeiro.conta import Conta, TipoConta
from financeiro.lancamento import Lancamento, TipoLancamento, StatusLancamento

@pytest.fixture
def setup_lancamento():
    conta = Conta("1", "Banco", TipoConta.CORRENTE, Decimal('1000.00'))
    categoria = Categoria("C1", "Lazer", TipoCategoria.DESPESA)
    return conta, categoria

def test_efetivar_lancamento_despesa(setup_lancamento):
    conta, categoria = setup_lancamento
    lancamento = Lancamento("L1", "Cinema", Decimal('50.00'), date.today(), TipoLancamento.DESPESA, categoria, conta)
    
    assert lancamento.status == StatusLancamento.PENDENTE
    lancamento.efetivar()
    
    assert lancamento.status == StatusLancamento.REALIZADO
    assert conta.saldo == Decimal('950.00')

def test_efetivar_lancamento_ja_efetivado_erro(setup_lancamento):
    conta, categoria = setup_lancamento
    lancamento = Lancamento("L1", "Cinema", Decimal('50.00'), date.today(), TipoLancamento.DESPESA, categoria, conta)
    lancamento.efetivar()
    
    with pytest.raises(ValueError, match="já foi efetivado"):
        lancamento.efetivar()

def test_cancelar_lancamento_estorna_saldo(setup_lancamento):
    conta, categoria = setup_lancamento
    lancamento = Lancamento("L1", "Salário Extra", Decimal('200.00'), date.today(), TipoLancamento.RECEITA, categoria, conta)
    
    lancamento.efetivar()
    assert conta.saldo == Decimal('1200.00')
    
    lancamento.cancelar()
    assert lancamento.status == StatusLancamento.CANCELADO
    assert conta.saldo == Decimal('1000.00')