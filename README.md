# Módulo Financeiro — POO II

Este repositório contém a implementação do pacote `financeiro`, desenvolvido como trabalho prático da disciplina de Programação Orientada a Objetos II.

---

## 🏗️ Estrutura do Pacote (`financeiro/`)

O projeto é composto pelas 6 classes solicitadas no escopo dos Capítulos 4 a 7:

* **`Conta` (`conta.py`):** Gerencia a conta bancária, saldos e operações de depósito, saque e transferência com tratamento de erros (ex: `SaldoInsuficienteError`).
* **`Categoria` (`categoria.py`):** Classifica movimentações financeiras em receitas ou despesas, oferecendo suporte à hierarquia de subcategorias.
* **`Lancamento` (`lancamento.py`):** Entidade central que registra entradas e saídas de valores, gerenciando estados (`PENDENTE`, `REALIZADO`, `CANCELADO`).
* **`Fechamento` (`fechamento.py`):** Consolida os lançamentos de um determinado mês e ano, gerando resumos de receitas, despesas e saldo líquido.
* **`Conciliacao` (`conciliacao.py`):** Realiza o cruzamento de lançamentos internos com itens de extrato bancário externo, aplicando regras de tolerância e conferência.
* **`Extrato` (`extrato.py`):** Gerencia a importação de transações bancárias (ex: OFX), utilizando o código `fitid` para evitar duplicidades no sistema.

---

## 🧪 Testes Automatizados

A suíte de testes foi construída com `pytest` e cobre fluxos de sucesso e tratamento de exceções.

Para executar todos os testes da raiz do projeto, utilize:

```powershell
python -m pytest