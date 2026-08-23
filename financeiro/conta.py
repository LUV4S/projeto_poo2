from decimal import Decimal
from enum import Enum
from typing import Optional

class TipoConta(Enum):
    CORRENTE = "CORRENTE"
    POUPANCA = "POUPANCA"
    INVESTIMENTO = "INVESTIMENTO"

class SaldoInsuficienteError(Exception):
    pass

class Conta:
    def __init__(self, id_conta: str, nome: str, tipo: TipoConta, saldo_inicial: Decimal = Decimal('0.00')):
        self.id_conta = id_conta
        self.nome = nome
        self.tipo = tipo
        self._saldo: Decimal = saldo_inicial
        self.ativa: bool = True

    @property
    def saldo(self) -> Decimal:
        return self._saldo

    def depositar(self, valor: Decimal) -> None:
        if not self.ativa:
            raise ValueError("Não é possível depositar em uma conta inativa.")
        if valor <= Decimal('0.00'):
            raise ValueError("O valor do depósito deve ser positivo.")
        
        self._saldo += valor

    def sacar(self, valor: Decimal) -> None:
        if not self.ativa:
            raise ValueError("Não é possível sacar de uma conta inativa.")
        if valor <= Decimal('0.00'):
            raise ValueError("O valor do saque deve ser positivo.")
        if self._saldo < valor:
            raise SaldoInsuficienteError(f"Saldo insuficiente na conta '{self.nome}'. Saldo atual: {self._saldo}")

        self._saldo -= valor

    def transferir_para(self, conta_destino: 'Conta', valor: Decimal) -> None:
        self.sacar(valor)
        conta_destino.depositar(valor)