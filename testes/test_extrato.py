from datetime import date
from decimal import Decimal
from financeiro.extrato import Extrato, ItemExtrato

def test_carregar_itens_extrato_evitando_duplicados():
    extrato = Extrato(conta_id="C1", data_inicio=date(2026, 8, 1), data_fim=date(2026, 8, 31))
    
    item1 = ItemExtrato(fitid="TX001", data=date(2026, 8, 10), descricao="Pix", valor=Decimal('-50.00'))
    item2 = ItemExtrato(fitid="TX001", data=date(2026, 8, 10), descricao="Pix Duplicado", valor=Decimal('-50.00'))
    item3 = ItemExtrato(fitid="TX002", data=date(2026, 8, 11), descricao="Padaria", valor=Decimal('-15.00'))
    
    extrato.carregar_itens([item1, item2, item3])
    
    assert len(extrato.itens) == 2
    assert extrato.itens[0].fitid == "TX001"
    assert extrato.itens[1].fitid == "TX002"