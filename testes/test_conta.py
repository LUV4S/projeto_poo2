from decimal import Decimal
import pytest
from financeiro.conta import Conta, TipoConta, SaldoInsuficienteError

def test_depositar_e_sacar_sucesso():
    conta = Conta("1", "Banco A", TipoConta.CORRENTE, Decimal('1000.00'))
    conta.depositar(Decimal('500.00'))
    assert conta.saldo == Decimal('1500.00')

    conta.sacar(Decimal('300.00'))
    assert conta.saldo == Decimal('1200.00')

def test_sacar_saldo_insuficiente_erro():
    conta = Conta("1", "Banco A", TipoConta.CORRENTE, Decimal('100.00'))
    with pytest.raises(SaldoInsuficienteError):
        conta.sacar(Decimal('200.00'))

def test_depositar_valor_invalido_erro():
    conta = Conta("1", "Banco A", TipoConta.CORRENTE)
    with pytest.raises(ValueError, match="positivo"):
        conta.depositar(Decimal('0.00'))

def test_transferencia_entre_contas_sucesso():
    origem = Conta("1", "Origem", TipoConta.CORRENTE, Decimal('500.00'))
    destino = Conta("2", "Destino", TipoConta.CORRENTE, Decimal('100.00'))
    
    origem.transferir_para(destino, Decimal('300.00'))
    assert origem.saldo == Decimal('200.00')
    assert destino.saldo == Decimal('400.00')