from decimal import Decimal
import pytest

from financeiro.conta import Conta, TipoConta
from financeiro.investimento import Investimento, TipoInvestimento

def test_aporte_e_rentabilidade():
    conta = Conta("1", "Banco", TipoConta.CORRENTE, Decimal('1000.00'))
    invest = Investimento("I1", "Tesouro Selic", TipoInvestimento.RENDA_FIXA)
    
    invest.aportar(Decimal('400.00'), conta_origem=conta)
    assert conta.saldo == Decimal('600.00')
    assert invest.valor_atual_mercado == Decimal('400.00')

    invest.atualizar_cotacao(Decimal('420.00'))
    assert invest.rentabilidade_absoluta == Decimal('20.00')

def test_resgate_acima_do_disponivel_erro():
    conta = Conta("1", "Banco", TipoConta.CORRENTE, Decimal('1000.00'))
    invest = Investimento("I1", "Ações", TipoInvestimento.ACAO)
    invest.aportar(Decimal('100.00'), conta_origem=conta)
    
    with pytest.raises(ValueError, match="superior ao valor disponível"):
        invest.resgatar(Decimal('200.00'), conta_destino=conta)