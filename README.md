# Sistema de Automação de Conciliação Financeira

## 📌 Visão Geral

Este projeto foi desenvolvido com o objetivo de simular e automatizar processos bancários relacionados à conciliação financeira, processamento fiscal e integração de lançamentos contábeis.

A proposta central é reduzir atividades manuais, minimizar erros operacionais e estruturar um fluxo organizado para tratamento de dados financeiros, inspirado em rotinas reais de backoffice bancário.

O sistema realiza:

* Importação de dados via CSV
* Persistência em banco de dados (SQLite)
* Validação de dados fiscais e financeiros
* Automação de conciliação entre notas fiscais e lançamentos
* Atualização automática de status
* Uso de triggers para automatização de regras no banco

---

## 🎯 Objetivo do Projeto

Este projeto foi construído visando:

* Simular automação de processos bancários
* Reduzir tarefas operacionais manuais
* Estruturar regras de negócio em camadas organizadas
* Implementar validações financeiras automatizadas
* Aplicar boas práticas de arquitetura (separação de responsabilidades)
* Demonstrar como triggers podem automatizar comportamentos diretamente no banco

A ideia central foi criar um sistema que representasse uma esteira de processamento financeiro automatizada.

---

## 🏗️ Arquitetura do Projeto

O sistema foi estruturado seguindo uma organização modular inspirada em padrões como Service Layer e Repository Pattern.

### Estrutura de Pastas

```
db/
repositories/
services/
views/
interfaces/
main/
```

### 🔹 Camadas

**db/**
Responsável por:

* Conexão com banco de dados
* Inicialização das tabelas
* Definição de triggers

**repositories/**
Responsável pelo acesso ao banco de dados:

* Execução de queries SQL
* Inserções
* Atualizações
* Consultas específicas

**services/**
Contém a regra de negócio:

* Validação de dados
* Regras de conciliação
* Processamento de CSV
* Controle de fluxo

**views/**
Responsável pela apresentação das informações no terminal.

**interfaces/**
Gerenciamento de menus e interação com o usuário.

**main/**
Ponto de entrada do sistema.

---

## 🗄️ Banco de Dados

O sistema utiliza SQLite para persistência dos dados.

### Principais Tabelas

* notas_fiscais
* lancamentos
* conciliacoes

---

## ⚙️ Automação com Triggers

Foram implementadas triggers no SQLite para automatizar a conciliação e garantir integridade operacional diretamente na camada do banco de dados.

### 🔹 1. trigger_validar_antes_de_lancar (BEFORE INSERT)

Executada antes da inserção em `lancamento_contabil`.

Função:

* Impede a inserção de um lançamento caso a nota fiscal não exista.
* Impede a inserção caso a nota exista, mas não possua valor definido.
* Utiliza `RAISE(ABORT, ...)` para cancelar a operação e garantir integridade referencial.

Isso evita inconsistências operacionais e simula validações comuns em sistemas financeiros reais.

---

### 🔹 2. trigger_conciliacao_pos_lancamento (AFTER INSERT)

Executada após a inserção de um lançamento contábil.

Função:

* Busca automaticamente a nota fiscal vinculada.
* Compara `lc_valor` com `nf_valor`.
* Gera automaticamente um registro na tabela `conciliacao`.
* Classifica o resultado como:

  * `EM CONFORMIDADE` (valores iguais)
  * `DIVERGENCIA` (valores diferentes)
* Registra descrição detalhando se o valor lançado foi maior, menor ou igual ao da nota.
* Registra data automática com `datetime('now')`.

Essa trigger transforma a conciliação em um processo automático e imediato após o lançamento.

---

### 🔹 3. trigger_conciliacao_pos_nota (AFTER INSERT)

Executada após a inserção de uma nova nota fiscal.

Função:

* Verifica se já existem lançamentos vinculados à nota.
* Caso existam, gera automaticamente os registros de conciliação.
* Aplica a mesma lógica de comparação de valores.

Essa abordagem garante que a ordem de inserção (nota → lançamento ou lançamento → nota) não impacte o processo de conciliação.

---

### 🎯 Benefícios da Estratégia com Triggers

* Conciliação automática em tempo real.
* Garantia de integridade antes da persistência do dado.
* Independência da camada de aplicação para execução da regra crítica.
* Simulação de comportamento encontrado em ambientes bancários e sistemas de backoffice financeiro.

O uso de triggers mostra que o banco de dados pode atuar como parte ativa da automação, reduzindo dependência da aplicação.

---

## 🔄 Fluxo de Processamento

1. Importação de arquivo CSV
2. Validação dos dados
3. Persistência no banco
4. Execução de regras de conciliação
5. Atualização automática de status
6. Exibição dos resultados

Esse fluxo representa uma esteira de processamento financeiro automatizada.

---

## 📊 Regras de Conciliação

A lógica de conciliação verifica:

* Correspondência de valores
* Compatibilidade entre nota fiscal e lançamento
* Atualização de status para:

  * Em conformidade
  * Divergente

---

## 🧠 Conceitos Aplicados

* Separação de responsabilidades
* Repository Pattern
* Service Layer
* Validação de dados
* Tratamento de exceções
* Organização modular
* Automação de processos
* Triggers em banco de dados

---

## 🚀 Possíveis Evoluções

* Métricas de performance
* Interface gráfica
* Integração com APIs bancárias simuladas

---

