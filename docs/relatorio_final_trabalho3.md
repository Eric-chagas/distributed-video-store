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

- **Plataforma de Execução:** O cluster foi implantado localmente utilizando **Kind (Kubernetes in Docker)**, aproveitando a infraestrutura de contêineres para executar o ambiente multi-node.
- **Estrutura:** O cluster foi configurado com 1 Nó Mestre (Control Plane) e 2 Nós Escravos (Worker Nodes). 
- **Passos da Instalação:** Conforme já era feito no projeto inicial do distributed video store, o provisionamento do ambiente completo é automático via shell script. Para a evolução do projeto de observabilidade, foi criado um novo script [setup_kind.sh](/setup_kind.sh), com base no script anterior para minikube, porém que agora executa o ambiente no Kind com os 3 nodes citados acima. O passo a passo do provisionamento do cluster é:
  1. Criar o cluster: `kind create cluster --name $CLUSTER_NAME --config kind-config.yaml --wait 2m`
  2. Realizar build das imagens do back normalmente
  3. Carregar as imagens no cluster, distribuidas nos 2 nodes workers
  ```bash
  kind load docker-image api-gateway:latest --name $CLUSTER_NAME
  kind load docker-image catalogue-service:latest --name $CLUSTER_NAME
  kind load docker-image catalogue-rest-service:latest --name $CLUSTER_NAME
  kind load docker-image rent-service:latest --name $CLUSTER_NAME
  ```
  4. Aplicar os manifestos no cluster
Após isso o script segue como era antes, expondo um port-forward na porta 8000 para que o api-gateway esteja acessível fora do cluster.  
- **Configuração do kind**: Foi adicionado o [kind-config.yaml](/kind-config.yaml) para configuração do Kind, definindo as portas de acesso aos nodes e os próprios nodes que serão criados:
```bash
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: video-store-kind-cluster
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: 30000
    listenAddress: "127.0.0.1"
    protocol: tcp
- role: worker
- role: worker
```
- **Recursos de Elasticidade**: O recurso principal utilizado para conferir elasticidade e resiliência à aplicação foi o Horizontal Pod Autoscaler (HPA).
  - Serviços: O HPA foi aplicado aos Deployments dos serviços do back API Gateway, Catalogue Service (grpc), catalogue service (rest) e Rent Service.
  - Métricas: A métrica primária utilizada para acionamento do autoscaling foi a Utilização Média da CPU, com um alvo de 50%.
  - Configuração: O HPA foi configurado para permitir que o número de réplicas escalasse de 1 (mínimo) a 5 (máximo) Pods para cada um dos módulos alvos, para que o sistema consiga responder a picos de carga. 

Já com os serviços em execução, é possível verificar a distribuição dos pods nos nodes e o status do autoscaling com os comandos mostrados abaixo:

![Cluster status](/assets/trab3/autoscaling_and_pods.png)

## 4. Monitoramento e Observabilidade com Prometheus

### 4.1. Instrumentação da Aplicação (Módulos P, A, B e REST)

A aplicação foi instrumentada para expor métricas críticas via endpoint `/metrics` nas portas listadas abaixo.

| Serviço | Ferramenta | Tipo de Instrumentação | Porta do `/metrics` |
| :--- | :--- | :--- | :--- |
| **P** (API Gateway) | `fastapi-instrumentator` | HTTP e **Latência gRPC Cliente** (`8000`) | `8000` |
| **A/B** (gRPC Servers) | `go-grpc-prometheus` | Interceptors gRPC (Latência/Volume) | `9090` / `9091` |
| **REST** (Catalogue) | `go-gin-prometheus` | Middleware HTTP | `8080` |

###### Tabela 03 - Instrumentação do prometheus e scraping de métricas. Fonte: Autoria própria

As métricas escolhidas como foco do teste de carga estão na seção 6.

### 4.2. Configuração do Scraping e Observabilidade

A stack de monitoramento foi implantada utilizando o **Helm chart `kube-prometheus-stack`**.

#### Ativação do Scraping (ServiceMonitor e Prometheus)

O Service Discovery do Prometheus foi configurado através de **ServiceMonitors** (CRDs), que buscam Services pelos labels. Foram necessárias algumas correções de mapeamento nos manifests para a ativação completa do scraping:

1.  **Timing:** Adição de um delay de 60 segundos no script de setup após a instalação do Helm para garantir o registro dos CRDs de **`ServiceMonitor`** no Kubernetes.
2.  **Mapeamento de Service:** Foi necessária a adição da label **`metadata.labels: app: [nome-do-app]`** nos manifestos de **Service** K8s, pois o ServiceMonitor usa essa label para localizar os serviços de target.

#### Visualização (Grafana)

O **Grafana** foi configurado automaticamente pelo stack do Helm, usando o Prometheus como fonte de dados. A instrumentação no Grafana focou em:

* **Validação do HPA:** Dashboards para monitorar o uso de **CPU** por Deployment para verificar o autoscaling.
* **Análise de Desempenho:** Painéis customizados para rastrear a latência distribuída (`grpc_client_call_duration_seconds` e `grpc_server_handling_seconds`) sob estresse.

Na imagem abaixo pode ser visualizado o painel web do prometheus, já dentro do cluster, com todos os serviços tendo as métricas sondadas pelo prometheus (frequencia é a cada 10s).

![Targets prometheus](/assets/trab3/targets_prometheus.png)

## 5. Aplicação Base e Evolução

### Comparativo da Arquitetura: Versão Base vs. Versão Evoluída

| Característica | 5.1 Versão Base (Setup Inicial) | 5.2 Versão Evoluída (Multinode e Observabilidade) |
| :--- | :--- | :--- |
| **Ambiente K8s** | 1 nó (Setup de Desenvolvimento) | **Múltiplos Nós** (1 Control Plane, 2 Workers) |
| **Escalabilidade** | Configuração estática: **1 réplica por Pod (P, A, B)**. | **Horizontal Pod Autoscaler (HPA)** no **API Gateway (Módulo P)**. |
| **Mecanismo HPA** | N/A | Alvo de **Utilização de CPU** para escalonamento automático de réplicas. |
| **Monitoramento** | N/A (Apenas logs e status K8s) | **Prometheus** (Instalado via `kube-prometheus-stack`). |
| **Observabilidade** | N/A | **Grafana** (Integrado ao Prometheus) para visualização de métricas em tempo real e análise de desempenho. |
| **Comunicação** | Chamadas Unary gRPC entre Módulo P e Módulos A/B. | Chamadas Unary gRPC, mantendo o mesmo padrão de comunicação. |

###### Tabela 04 - Comparação pré e pós evolução da infra do projeto. Fonte: Autoria própria

## 6. Cenários de Teste e Resultados

### 6.1. Métricas

Para a análise foram escolhidas **Métricas do Sistema** (para validar o autoscaling) e **Métricas de Desempenho** (para avaliar a experiência do usuário e gargalos).

### 6.1.1. Métricas de Escalonamento e Sistema (HPA)

Metricas avaliadas por serviço no dashboard padrão do grafana `Kubernetes / Compute Resources / Namespace (Workloads)` para analisar o comportamento dentro do node para cada serviço, e como os pods escalam e de-escalam com o teste de carga do locust.

| Métrica | Localização | Propósito da Análise |
| :--- | :--- | :--- |
| **`kube_horizontalpodautoscaler_status_current_replicas`** | Grafana / Prometheus | Mostrar a transição do número de réplicas do **API Gateway** (Módulo P) durante o teste. **Essencial para provar o *scaling***. |
| **`container_cpu_usage_seconds_total`** | Grafana / Prometheus | Mostrar o uso de CPU atingindo o limite na **Fase 1 (Sem HPA)** (100%) e estabilizando no alvo (ex: 50%) na **Fase 2 (Com HPA)**. |
| **RPS (Requests per Second)** | Locust | Medir a taxa máxima de requisições que o sistema conseguiu processar em cada fase, provando o **ganho de capacidade**. |

### 6.1.2. Métricas de Latência e Desempenho (gRPC)

Métricas do dashboard `go gRPC1` no grafana que analisam status das métricas dos servers gRPC dos quais a api-gateway é cliente.

| Categoria | Métrica (PromQL) | Painel Principal | O que Mede |
| :--- | :--- | :--- | :--- |
| **Saúde Básica** | `up` | Up (Painel 15) | Indica se o endpoint Prometheus do trabalho (`$job`) está acessível e respondendo (1 = UP, 0 = DOWN). |
| **QoS / Latência** | `grpc_server_handling_seconds_bucket` | 99%-tile latency (Painel 8) | Utilizada com `histogram_quantile(0.99, ...)` para calcular a Latência P99 das requisições gRPC. |
| **QoS / Latência** | `grpc_server_handling_seconds_sum` | Average handling time (Painel 16) | Usada para calcular o tempo **médio** de processamento de requisições gRPC. |
| **Taxa de Erro** | `grpc_server_handled_total` | Global Success Rate, gRPC request code (Painéis 12, 26) | Contador de requisições **finalizadas**, discriminado por `grpc_code` (OK, NotFound, etc.), usado para calcular taxas de sucesso e erro. |
| **QPS / Carga** | `grpc_server_started_total` | QPS (Painéis 14, 2) | Contador de requisições gRPC **iniciadas**. Usado com `rate()` ou `irate()` para calcular o QPS (Queries Per Second). |
| **Go Runtime** | `go_goroutines` | Goroutines (Painel 32) | Número de *goroutines* ativas. Ajuda a identificar vazamentos (*leaks*) de concorrência. |
| **Go Runtime** | `go_gc_duration_seconds` | GC duration quantiles (Painel 30) | Tempo gasto em Coleta de Lixo (GC), geralmente em percentis. Valores altos indicam pausas na aplicação. |
| **Memória (SO)** | `process_resident_memory_bytes` | process memory (Painel 28) | Memória RAM física (ou swap) usada pelo processo Go (RSS). |
| **Memória (SO)** | `process_virtual_memory_bytes` | process memory (Painel 28) | Memória virtual total alocada pelo processo. |
| **Memória (Go)** | `go_memstats_alloc_bytes` | go memstats (Painel 34) | Bytes de memória alocados no heap (montanha) para objetos Go. |
| **Memória (Go)** | `go_memstats_alloc_bytes_total` | go memstats (Painel 34) | Usado com `rate()` para calcular a **Taxa de Alocação** de memória. |
| **Memória (Go)** | `go_memstats_stack_inuse_bytes` | go memstats (Painel 34) | Memória usada para as pilhas (*stacks*) das goroutines. |
| **Memória (Go)** | `go_memstats_heap_inuse_bytes` | go memstats (Painel 34) | Memória do heap atualmente em uso para objetos Go. |


### 6.2. Ferramenta de Teste de Carga Locust

O Locust é uma ferramenta de teste de carga de código aberto escrita em Python. Sua principal vantagem é permitir que os cenários de teste sejam definidos usando código Python padrão, o que oferece alta flexibilidade e expressividade.

* **Definição de Carga:** Os cenários de teste são modelados através de classes que herdam de `HttpUser`. Estas classes definem o comportamento dos usuários simulados, as rotas (endpoints) que serão acessadas e a **ponderação** (probabilidade de execução) de cada tarefa.
* **Interface Web:** O Locust fornece uma interface web que permite controlar o teste em tempo real, especificando o número total de usuários (swarms) e a taxa de inicialização (spawn rate). 
* **Resultados:** Durante e após a execução, o Locust gera relatórios detalhados com métricas essenciais, como a taxa de requisições por segundo (RPS), a taxa de falha e a **latência**, com foco nos percentis (como P95 e P99), que são cruciais para a análise de desempenho em ambientes distribuídos.

No contexto deste projeto, o Locust é usado para gerar uma carga de estresse controlada no **API Gateway**, servindo como o **gatilho** para a ativação do Horizontal Pod Autoscaler (HPA), enquanto o Prometheus/Grafana monitora a reação do sistema.

### 6.3. Cenário Base (Linha de Referência)

A abordagem para os testes de estresse com o Locust será focada na validação da escalabilidade dinâmica do sistema sob diferentes padrões de carga e todos os cenários de teste serão executados sob a mesma configuração do Kubernetes, com o HPA ativo e configurado.

O objetivo principal será **isolar e medir o impacto do aumento da carga** na capacidade de resposta do sistema. Para isso, os únicos parâmetros que serão variados no Locust, mantendo-se o restante da configuração fixa, serão:

1.  **Número Máximo de Usuários (*Peak Users*)**
2.  **Taxa de Ramp-Up (*Users Started/Second*)**

Todos os testes terão duração de 4-5 minutos para que os resultados fiquem aparentes nos dashboards do grafana.

### 6.4. Execução dos Cenários

#### Cenário A: Baseline (Rampa Lenta)

Este cenário estabelece a linha de base de desempenho e verifica o acionamento suave e sustentado do HPA.

1.  **Número Máximo de Usuários (*Peak Users*)**: 300
2.  **Taxa de Ramp-Up (*Users Started/Second*)**: 5

##### K8s e HPA

![Relatório A hpa](/assets/trab3/locust-tests/grafana-a-1.png)

O uso de CPU Rápidamente atingiu mais de 50% para o serviço api-gateway, e o serviço escalou para 5 pods.

##### Go gRPC

![Relatório A grpc](/assets/trab3/locust-tests/grafana-a-2.png)

A métrica foco de handling time das requisições no servidor chegou próxima de 0.6ms para o catalogue-service e 0.3 para o rent-service.

##### Relatório Locust

![Relatório A locust](/assets/trab3/locust-tests/locust-a-1.png)

---

#### Cenário B: Estresse Moderado

Este cenário testa a capacidade de reação do HPA e a latência de aquecimento sob um aumento de demanda mais agressivo.

1.  **Número Máximo de Usuários (*Peak Users*)**: 700
2.  **Taxa de Ramp-Up (*Users Started/Second*)**: 30

##### K8s e HPA

![Relatório B hpa](/assets/trab3/locust-tests/grafana-b-1.png)

O uso de CPU Rápidamente atingiu mais de 50% para o serviço api-gateway, e o serviço escalou para 5 pods. Os outros serviços gRPC não chegaram a 50% da capacidade mesmo com o aumento do estresse de requisições, provavelmente devido ao scale-up da api-gateway.

##### Go gRPC

![Relatório B grpc](/assets/trab3/locust-tests/grafana-b-2.png)

A métrica foco de handling time das requisições no servidor chegou próxima de 0.6ms para o catalogue-service e 0.4 para o rent-service. Tempos maiores que no cenário A.

##### Relatório Locust

![Relatório B locust](/assets/trab3/locust-tests/locust-b-1.png)

---

#### Cenário C: Stress Extremo

Visa forçar o *scaling out* ao máximo (`maxReplicas` no HPA) e registrar o desempenho no limite máximo do sistema.

1.  **Número Máximo de Usuários (*Peak Users*)**: 1500
2.  **Taxa de Ramp-Up (*Users Started/Second*)**: 100

##### K8s e HPA

![Relatório C hpa](/assets/trab3/locust-tests/grafana-c-1.png)

Mais uma vez a api-gateway foi o principal "gargalo" chegando rápidamente a mais de 100% da capacidade e escalando para o máximo de pods, que eram 5. Os serviços gRPC ainda permaneceram com uma réplica apenas por não terem atingido 50% de cpu em uso, apesar de ter aumentado o consumo e tempo de resposta.

##### Go gRPC

![Relatório C grpc](/assets/trab3/locust-tests/grafana-c-2.png)

A métrica foco de handling time das requisições no servidor chegou próxima de 0.6ms para o catalogue-service e 0.4 para o rent-service. Cenário quase idêntico ao cenário C mesmo com o rápido aumento de requisições e usuários simulados do locust.

##### Relatório Locust

![Relatório C locust](/assets/trab3/locust-tests/locust-c-1.png)

---

#### Cenário D: Sobrecarga Súbita e stress extremo

Foco em verificar os serviços gRPC também atingindo 50% de CPU e escalando os pods dos serviços gRPC também.

1.  **Número Máximo de Usuários (*Peak Users*)**: 10000
2.  **Taxa de Ramp-Up (*Users Started/Second*)**: 90

##### K8s e HPA

![Relatório D hpa](/assets/trab3/locust-tests/grafana-d-1.png)

Aqui o cenário de mais de 100% de uso de CPU na api-gateway e scale-up pra 5 pods permaneceu, porém o serviço catalogue chegou a 50% de CPU e também escalou, para 2 pods de um máximo de 5. A api gateway ainda foi gargalo, e dessa vez, com o número elevado de requisições e usuários simulados, o port-forward do k8s caiu 4 vezes, e foi necessário recria-lo para que os testes continuassem. Isso explica os picos e vales dos gráficos do locust.

##### Go gRPC

![Relatório D grpc](/assets/trab3/locust-tests/grafana-d-2.png)

Os tempos de resposta foram relativamente menores nesse caso de teste, o catalogue service chegou a pouco mais de 0.3ms e o rent-service também a 0.3ms.

##### Relatório Locust

![Relatório D locust](/assets/trab3/locust-tests/locust-d-1.png)

#### Cenário Final: Teste com novas configurações de hpa

O último teste foi feito após a alteração da configuração de autoscale dos pods gRPC, que antes escalavam com 50% de CPU (cenário que quase não foi atingido nos últimos testes) para **20% de CPU** e aumento do número máximo de réplicas da api-gateway **de 5 para 8**.

1.  **Número Máximo de Usuários (*Peak Users*)**: 10000
2.  **Taxa de Ramp-Up (*Users Started/Second*)**: 90

Nova configuração do HPA:

![Nova config de HPA](/assets/trab3/locust-tests/new_hpa.png)

##### K8s e HPA

![Relatório E hpa](/assets/trab3/locust-tests/grafana-e-1.png)

Aqui com as novas alterações os serviços gRPC finalmente escalaram para 2 no caso do rent-service e 3 no caso do catalogue. Isso também melhorou a saúde da aplicação, diminuindo a carga do api-gateway (com certeza aliado ao maior número de 8 réplicas) e o port-forward que caiu 4 vezes no último teste, caiu apenas 1 vez. 

##### Go gRPC

![Relatório E grpc](/assets/trab3/locust-tests/grafana-e-2.png)

Os tempos de resposta diminuiram significativamente com o scale-up dos serviços gRPC ficando para o catalogue service em torno de 0.25ms e 0.15ms para o rent-service.

##### Relatório Locust

![Relatório E locust](/assets/trab3/locust-tests/locust-e-1.png)

## 7. Conclusão
### 7.1. Conclusão Final do Projeto

Com base nos testes da seção 6, fica claro que a implementação e configuração do HPA no k8s é extremamente importante, especialmente em projetos grandes e com grande tráfego, para aumentar o throughput de requisições e respostas no sistema. Inicialmente limitado pela API Gateway, a otimização do target de CPU para 20% nos serviços gRPC e o aumento das réplicas da API Gateway permitiu que os serviços de backend (Catalogue e Rent) escalassem mais eficientemente, assim como a api-gateway, resultando em uma melhora significativa da Latência e maior estabilidade com uma carga mais alta de requisições.

### 7.2. Dificuldades Encontradas e Soluções

As minhas dificuldades principais foram na configuração da stack de monitoramento e fazer com que o prometheus fizesse o scrape da api, e dos dois serviços gRPC para que o grafana pudesse receber na conexão de dados. Mesmo após a instrumentação do código GO para expor as métricas, ainda precisei voltar algumas vezes e re-configurar a exposição das métricas pra que todas chegassem até o grafana.

A configuração do locust foi relativamente simples, e o cluster kubernetes no kind também, já que meus manifests já estavam prontos para os serviços e a configuração do Kind foi também relativamente simples. O ajuste dos novos manifests que precisei criar para o HPA, e o servicemonitor (para o scrape do prometheus) me deram muita "dor de cabeça" pela necessidade de ajustar as labels e nomes entre os manifestos de deployment e service que já estavam criados com o que o service monitor esperava, além de ter encontrado uma porta que eu estava expondo incorretamente no inicio do projeto para o serviço de catalogue-rest no GO.

A outra dificuldade grande que tive foi configurar o grafana, pois nunca tinha tido contato com a ferramenta, e tive a oportunidade agora de entender melhor como criar dashboards e interagir com as métricas que o prometheus coleta da aplicação para mostrar tudo visualmente, como fiz no meu relatório de testes.

### 7.3. Comentários Pessoais e Autoavaliação (Eric Chagas de Oliveira)

Foi uma experiência também trabalhosa, assim como o trabalho 1, porém considero muito engrandecedora pra minha carreira, especialmente pois já trabalho com provisionamento e devops de aplicações em nuvem no kubernetes (aws eks) porém com uma stack levemente diferente, e aqui pude ter contato com essas ferramentas de observabilidade que pretendo inclusive introduzir nas aplicações que estou envolvido na empresa onde trabalho.

**Auto-avaliação:** Por ter feito o trabalho individualmente, porém com o entendimento que estou entregando um dia atrasado, me auto-avalio com nota 8 (devido ao atraso na entrega) por ter considerado a experiência enriquecedora e achar ter feito um bom trabalho, apesar do atraso.

## 8. Referências Utilizadas
- https://locust.io/
- https://prometheus.io/
- https://kind.sigs.k8s.io/
- https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- https://grafana.com/
- https://go.dev/