#Classifica os lancamentos financeiros em DESPESA ou RECEITA

from enum import Enum

class TipoCategoria(Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

class Categoria:
    def __init__(self, id_categoria: str, nome: str, tipo: TipoCategoria, categoria_pai: 'Categoria' = None):
        if not nome or not nome.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")
            
        self.id_categoria = id_categoria
        self.nome = nome.strip()
        self.tipo = tipo
        self.categoria_pai = categoria_pai

    @property
    def nome_completo(self) -> str:
        """Retorna o caminho hierárquico da categoria (ex: Moradia > Aluguel)."""
        if self.categoria_pai:
            return f"{self.categoria_pai.nome_completo} > {self.nome}"
        return self.nome