import pytest
from financeiro.categoria import Categoria, TipoCategoria


def test_criar_categoria_com_sucesso():
    cat = Categoria("C1", "Alimentação", TipoCategoria.DESPESA)
    assert cat.id_categoria == "C1"
    assert cat.nome == "Alimentação"
    assert cat.nome_completo == "Alimentação"

def test_categoria_hierarquica_nome_completo():
    pai = Categoria("C1", "Moradia", TipoCategoria.DESPESA)
    filha = Categoria("C2", "Aluguel", TipoCategoria.DESPESA, categoria_pai=pai)
    assert filha.nome_completo == "Moradia > Aluguel"

def test_criar_categoria_nome_vazio_erro():
    with pytest.raises(ValueError, match="O nome da categoria não pode ser vazio."):
        Categoria("C1", "   ", TipoCategoria.DESPESA)