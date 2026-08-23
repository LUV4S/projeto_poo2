## 📌 Decisões de Projeto (Capítulos 5 a 7)

### 1. No Fechamento, os lançamentos originais foram copiados ou referenciados? Por quê?
**Decisão:** Os lançamentos originais foram **referenciados**.

* **Justificativa:** Em Orientação a Objetos, duplicar ou copiar instâncias de entidades com estado mutável (como um `Lancamento`, que possui atributos como `status` e `data_pagamento`) cria problemas graves de inconsistência e sincronização (*dados obsoletos*). 
* Manter a referência direta garante a **fonte única da verdade**: se um lançamento tiver seu status alterado ou for cancelado, a alteração se reflete imediatamente nos cálculos do `Fechamento` e do `Orcamento`, sem necessidade de propagação manual de alterações entre cópias.

---

### 2. Conciliacao virou uma classe própria ou um método de Fechamento? Por quê?
**Decisão:** A `Conciliacao` foi modelada como uma **classe própria** (`financeiro/conciliacao.py`).

* **Justificativa:** Aplicação direta do **Princípio da Responsabilidade Única (SRP)**. 
* O `Fechamento` tem como responsabilidade consolidar e agregar dados contábeis (receitas, despesas e resultado do período). 
* A `Conciliacao` possui uma responsabilidade com lógica de negócio complexa e distinta: cruzar dados de fontes externas (como o extrato bancário/OFX em `ItemExtrato`) com lançamentos internos do sistema, aplicando regras de tolerância de valores e margem de datas. Misturar essa regra dentro do `Fechamento` causaria alto acoplamento e feriria a coesão.

---

### 3. O que acontece quando não há lançamentos no período, ou quando a conciliação não bate?

#### A) Quando não há lançamentos no período:
* **No Fechamento:** O método `gerar_resumo_mes` processa a lista (vazia ou sem correspondências para a data) de forma segura, retornando um objeto `ResumoMensal` com `total_receitas = Decimal('0.00')`, `total_despesas = Decimal('0.00')` e `resultado = Decimal('0.00')`. Isso evita erros de execução (*NullPointer* ou *IndexError*) e mantém o contrato da API consistente.
* **No Orçamento:** O método `calcular_executado` retorna `Decimal('0.00')`, indicando que 100% do limite orçamentário permanece disponível.

#### B) Quando a conciliação não bate:
* **Divergência de Valores:** A tentativa de efetuar `conciliacao.conciliar(item_extrato, lancamento)` dispara uma exceção explícita (`raise ValueError("Não é possível conciliar itens com valores divergentes.")`), impedindo que o saldo seja alterado ou efetivado incorretamente.
* **Ausência de Correspondência (Matches):** O método `sugerir_matches` simplesmente não inclui o par divergente na lista de sugestões, sinalizando ao sistema que aquele item do extrato permanece pendente de auditoria manual ou de criação de um novo lançamento.