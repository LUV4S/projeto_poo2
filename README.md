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

## 🧠 Decisões de Arquitetura e Modelagem

### 1. Referência vs. Cópia no `Fechamento`
No processo de geração de fechamento contábil, os lançamentos originais são **referenciados** e não clonados. Como o método `gerar_resumo_mes` opera de forma estática e em modo somente-leitura (calculando métricas sem mutar dados internos de transação), referenciar os objetos é a abordagem mais eficiente em memória e desempenho, preservando a imutabilidade dos lançamentos.

### 2. Separação entre `Conciliacao` e `Fechamento`
A **`Conciliacao`** foi modelada como uma classe própria e autônoma, e não como método de `Fechamento`, respeitando o **Princípio da Responsabilidade Única (SRP)**:
* **`Conciliacao`:** Lida com auditoria operacional e conferência de registros internos contra transações brutas externas (OFX/banco), mantendo estado histórico dos pares conciliados e efetuando liquidação.
* **`Fechamento`:** Atua na camada analítica de agregação contábil, apurando totais mensais com base exclusivamente em lançamentos já efetivados no período.

### 3. Comportamento em Casos de Borda e Falha
* **Períodos sem lançamentos:** Ao gerar fechamento para um mês/ano sem movimentações válidas, o sistema retorna um `ResumoMensal` preenchido de forma neutra (`total_receitas = 0.00`, `total_despesas = 0.00`, `resultado = 0.00`), sem estourar exceções.
* **Divergência na Conciliação:**
  * No matching preliminar (`sugerir_matches`), pares que divirjam de valor ou fujam da margem temporal de tolerância são simplesmente ignorados.
  * Na tentativa explícita de conciliação com valores absolutos divergentes (`conciliar`), o sistema lança um `ValueError`, barrando a operação antes de efetivar ou registrar o par.

---

## 🧪 Testes Automatizados

A suíte de testes foi construída com `pytest` e cobre fluxos de sucesso e tratamento de exceções.

Para executar todos os testes da raiz do projeto, utilize:

```powershell
python -m pytest