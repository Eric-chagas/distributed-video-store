# Relatório de Projeto: Monitoramento e Observabilidade em Clusters K8S (PSPD)

| Item | Descrição |
| :--- | :--- |
| **Curso** | UnB/FCTE – Engenharia de Software |
| **Semestre** | 2025/2 |
| **Disciplina** | PSPD - Programação para Sistemas Paralelos e Distribuídos - Turma 02 |
| **Professor** | Prof. Fernando W. Cruz |
| **Grupo** | Eric Chagas de Oliveira - 180119508 |
|**Link do repositório**|[Repositório](https://github.com/Eric-chagas/distributed-video-store)|
|**Link do vídeo de apresentação**|`#TODO: Adicionar link do vídeo`|
|**Ferramenta de Teste de Carga**| [Locust](https://locust.io/) |


## 1. Introdução

Este relatório descreve o projeto de pesquisa focado na monitoramento e observabilidade da aplicação de microserviços gRPC "Distributed Video Store" em um cluster Kubernetes (K8S) multi-node. O objetivo principal é identificar o arranjo ideal da aplicação no K8S para otimizar desempenho e elasticidade, utilizando o [Prometheus](https://prometheus.io/) como ferramenta primária de coleta de métricas e análise.

## 2. Metodologia de Trabalho

### 2.1. Organização do Projeto

Esse projeto de pesquisa final foi desenvolvido individualmente, e consiste na evolução da aplicação **Distributed Video Store** desenvolvida no Trabalho 1 da disciplina para adicionar e atender os requisitos de observabilidade e teste de carga do projeto final.

Como o trabalho inicialmente era executado no ambiente kubernetes com o minikube que é uma ferramenta single-node por padrão, foi necessária a migração para um ambiente capaz de executar múltiplos nodes na máquina onde o cluster roda. A ferramenta escolhida foi o Kind cuja documentação oficial pode ser acessada [nesse link](https://kind.sigs.k8s.io/).

Na tabela abaixo, está a nova stack tecnologica para o projeto final:

|**Categoria**|**Componente**|**Propósito no Projeto**|
|---|---|---|
|**Aplicação Base**|Microserviços gRPC (P, A, B)|O código-fonte a ser instrumentado e testado.|
|**Orquestração K8S**|**Kind** (Kubernetes in Docker)|Criação de um **cluster K8s multi-node** de forma leve e rápida, simulando o ambiente de produção localmente.|
|**Elasticidade**|**HPA** (_Horizontal Pod Autoscaler_)|Mecanismo do K8s utilizado para **escalar automaticamente** os Pods da aplicação com base na métrica de CPU (ou outras).|
|**Monitoramento**|**Prometheus**|Sistema principal de coleta, armazenamento e consulta de métricas de desempenho da aplicação e do K8s.|
|**Visualização**|**Grafana**|Interface gráfica para criar _dashboards_ e visualizar as métricas coletadas pelo Prometheus.|
|**Teste de Carga**|**Locust**|Ferramenta de testes de estresse para simular alta demanda de requisições no API Gateway (Módulo P).|

###### Tabela 01 - Stack tecnologica do projeto final. Fonte: Autoria própria.



- Evolução da Aplicação:
  - Instrumentação: Implementação de código de instrumentação Prometheus nos microserviços Python (Módulo P - API Gateway) e Go (Módulos A e B - Catálogo/Estoque) para exposição de métricas gRPC e HTTP.
  - Containerização: Atualização dos Dockerfiles e da gestão de dependências.
- Infraestrutura e Observabilidade:
  - Cluster K8S: Configuração e gestão do cluster multi-node que antes executava no minikube.
  - Deployment: Ajustes e evolução dos manifestos Kubernetes (Deployments, Services, ConfigMaps).
  - Monitoramento: Instalação e configuração do stack Prometheus e Grafana, incluindo regras de scrape e dashboards para visualização das métricas.
- Testes e Análise:
  - Teste de Carga: Desenvolvimento e execução dos scripts de teste (Locust).
  - Análise de Desempenho: Coleta e consolidação dos dados (latência, vazão, autoscaling) obtidos via Prometheus/Grafana nos diferentes cenários.

### 2.2. Timeline de Implementação e Decisões de escopo do projeto

|**Etapa de Implementação**|**Decisões/Marcos Cruciais**|
|---|---|
|**Preparação do Ambiente**|**Escolha da Plataforma K8S:** Definido o uso do **Kind (Kubernetes in Docker)** para simular o cluster multi-node. **Definição da CNI:** O **Flannel** foi escolhido para criar a rede _overlay_ necessária para a comunicação entre os nodes.|
|**Instrumentação**|**Definição de Métricas:** Priorizadas as métricas de latência em requisições gRPC (Módulos A/B) e latência HTTP (Módulo P), essenciais para medir o desempenho distribuído e diagnosticar gargalos.|
|**Implantação e Monitoramento**|**Configuração do Prometheus:** Configurado o _ServiceMonitor_ para descoberta automática dos _endpoints_ `/metrics` dos microserviços. Instalação e _setup_ inicial do Grafana.|
|**Teste Base**|**Seleção da Ferramenta de Teste:** **Locust**. Estabelecimento da Linha de Base de Desempenho (RPS e Latência) para o cenário de 1 réplica sem _autoscaling_.|
|**Testes Comparativos**|**Desenho de Cenários:** Definidos [Número] cenários comparativos, focando na variação do **Horizontal Pod Autoscaler (HPA)** e [Ex: distribuição de Pods usando _Node Affinity_] para otimizar o uso dos _Worker Nodes_.|

###### Tabela 02 - Roadmap do projeto. Fonte: Autoria própria.

## 3. Experiência de Montagem do Kubernetes em Modo Cluster
### 3.1. Arquitetura do Cluster
## 4. Monitoramento e Observabilidade com Prometheus
### 4.1. Instrumentação da Aplicação (Módulos P, A e B)
### 4.2. Configuração e Uso do Prometheus
## 5. Aplicação Distributed Video Store - Versão Base

* **Arquitetura:** Aplicação baseada em microserviços gRPC (P, A e B) com Gateway REST (P).
* **Comunicação:** Chamadas **Unary gRPC** entre o Módulo P e os Módulos A/B.
* **Configuração Base:** A aplicação foi instanciada com **1 réplica de cada Pod (P, A, B)** e recursos mínimos, garantindo apenas a distribuição inerente ao gRPC e K8S.

## 6. Cenários de Teste, Resultados e Conclusões
### 6.1. Ferramenta de Teste de Carga
### 6.2. Cenário Base (Linha de Referência)
### 6.3. Cenários Variáveis e Análise Comparativa
#### Cenário A: nome cenario
## 7. Conclusão
### 7.1. Conclusão Final do Projeto
### 7.2. Dificuldades Encontradas e Soluções
### 7.3. Comentários Pessoais e Autoavaliação (Eric Chagas de Oliveira)
## 8. Referências Utilizadas

