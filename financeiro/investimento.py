#Controla a carteira de ativos

from datetime import date
from decimal import Decimal
from enum import Enum
from financeiro.conta import Conta

class TipoInvestimento(Enum):
    RENDA_FIXA = "RENDA_FIXA"
    ACAO = "ACAO"
    FII = "FII"
    CRIPTO = "CRIPTO"

class Investimento:
    def __init__(self, id_investimento: str, nome: str, tipo: TipoInvestimento):
        self.id_investimento = id_investimento
        self.nome = nome
        self.tipo = tipo
        self.saldo_aplicado = Decimal('0.00')
        self.valor_atual_mercado = Decimal('0.00')

    def aportar(self, valor: Decimal, conta_origem: Conta) -> None:
        conta_origem.sacar(valor)
        self.saldo_aplicado += valor
        self.valor_atual_mercado += valor

    def resgatar(self, valor: Decimal, conta_destino: Conta) -> None:
        if valor > self.valor_atual_mercado:
            raise ValueError("Valor do resgate superior ao valor disponível de mercado.")
            
        proporcao = valor / self.valor_atual_mercado
        self.saldo_aplicado -= (self.saldo_aplicado * proporcao)
        self.valor_atual_mercado -= valor
        conta_destino.depositar(valor)

    def atualizar_cotacao(self, novo_valor_mercado: Decimal) -> None:
        if novo_valor_mercado < Decimal('0.00'):
            raise ValueError("Valor de mercado não pode ser negativo.")
        self.valor_atual_mercado = novo_valor_mercado

    @property
    def rentabilidade_absoluta(self) -> Decimal:
        return self.valor_atual_mercado - self.saldo_aplicado