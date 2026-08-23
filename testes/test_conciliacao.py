from datetime import date
from decimal import Decimal
import pytest

from financeiro.categoria import Categoria, TipoCategoria
from financeiro.conta import Conta, TipoConta
from financeiro.conciliacao import Conciliacao
from financeiro.extrato import ItemExtrato
from financeiro.lancamento import Lancamento, TipoLancamento, StatusLancamento

def test_sugerir_e_conciliar_transacao():
    conta = Conta("C1", "Banco", TipoConta.CORRENTE, Decimal('500.00'))
    cat = Categoria("CAT1", "Saúde", TipoCategoria.DESPESA)
    
    item_extrato = ItemExtrato(fitid="FIT100", data=date(2026, 8, 10), descricao="Farmacia", valor=Decimal('-80.00'))
    lancamento = Lancamento("L1", "Farmacia Droga", Decimal('80.00'), date(2026, 8, 11), TipoLancamento.DESPESA, cat, conta)
    
    conciliacao = Conciliacao(conta_id="C1")
    sugestoes = conciliacao.sugerir_matches([item_extrato], [lancamento])
    
    assert len(sugestoes) == 1
    
    conciliacao.conciliar(item_extrato, lancamento)
    assert lancamento.status == StatusLancamento.REALIZADO
    assert conta.saldo == Decimal('420.00')

def test_conciliar_valores_divergentes_erro():
    conta = Conta("C1", "Banco", TipoConta.CORRENTE)
    cat = Categoria("CAT1", "Saúde", TipoCategoria.DESPESA)
    
    item = ItemExtrato("FIT1", date.today(), "Teste", Decimal('-100.00'))
    lancamento = Lancamento("L1", "Teste", Decimal('80.00'), date.today(), TipoLancamento.DESPESA, cat, conta)
    
    conciliacao = Conciliacao(conta_id="C1")
    with pytest.raises(ValueError, match="valores divergentes"):
        conciliacao.conciliar(item, lancamento)