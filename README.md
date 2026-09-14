# Módulo Financeiro — POO II

Este repositório contém a implementação do pacote `financeiro`, desenvolvido como trabalho prático da disciplina de Programação Orientada a Objetos II.

---

## 🏗️ Estrutura do Pacote (`financeiro/`)

O projeto é composto por 6 classes principais:

* **`Conta` (`conta.py`):** Gerencia saldo, saques, depósitos e transferências, tratando erros de saldo insuficiente.
* **`Categoria` (`categoria.py`):** Classifica lançamentos em receita ou despesa e permite categorias hierárquicas (subcategorias).
* **`Lancamento` (`lancamento.py`):** Representa cada movimentação financeira com controle de status (`PENDENTE`, `REALIZADO`, `CANCELADO`).
* **`Fechamento` (`fechamento.py`):** Consolida os totais de receitas, despesas e resultado de um mês/ano específico.
* **`Conciliacao` (`conciliacao.py`):** Cruza lançamentos do sistema com transações de extrato externo.
* **`Extrato` (`extrato.py`):** Armazena itens importados do banco, evitando duplicatas pelo identificador (`fitid`).

---

## ❓ Perguntas de Projeto

### No Fechamento, os lançamentos originais foram copiados ou referenciados? Por quê?
**Foram referenciados.**  
O método de fechamento apenas percorre a lista para somar os valores das transações realizadas no período. Como não há nenhuma modificação nos dados dos lançamentos, criar cópias seria um desperdício desnecessário de memória e processamento.

### Conciliacao virou uma classe própria ou um método de Fechamento? Por quê?
**Virou uma classe própria.**  
Por responsabilidade única: **Conciliação** serve para auditar e bater registros internos com extrato bancário externo (guardando histórico de pares conciliados), enquanto **Fechamento** serve apenas para gerar relatórios e balanços contábeis de um período. São propósitos diferentes.

### O que acontece quando não há lançamentos no período, ou quando a conciliação não bate?
* **Sem lançamentos no período:** O fechamento retorna normalmente um resumo com todos os valores zerados (`0.00`), sem disparar nenhum erro.
* **Conciliação não bate:**
  * Na sugestão (`sugerir_matches`): se a data estiver fora da margem permitida ou os valores forem diferentes, o par simplesmente não aparece na lista de sugestões.
  * Ao tentar forçar a conciliação (`conciliar`): se os valores forem diferentes, o sistema lança um erro (`ValueError`) e cancela a operação.

---

## 🧪 Testes Automatizados

A suíte de testes foi desenvolvida com `pytest`.

Para rodar todos os testes a partir da raiz do projeto:

```powershell
python -m pytest