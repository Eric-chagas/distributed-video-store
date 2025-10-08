# Distributed Video Store

Projeto de locadora e loja virtual de filmes utilizando conceitos de computação distribuida, gRPC e Kubernetes. Desenvolvido para a disciplina **PSPD - Programação para Sistemas Paralelos e Distribuídos (Turma 02)** – **UnB/FCTE – Engenharia de Software** 

- **Professor:** Prof. Fernando W. Cruz  
- **Aluno:** Eric Chagas de Oliveira  
- **Matrícula:** 180119508

## Descrição do Projeto

O **Distributed Video Store** é uma aplicação simples de aluguel e compra de filmes online. 

O sistema será distribuído e baseado em **microserviços**, será utilizado o **framework gRPC** para comunicação entre serviços e **Kubernetes (Minikube)** para orquestração e deploy em contêineres.

### Objetivos

1. Estudo do gRPC, seus componentes e os quatro tipos de comunicação.
2. Implementação da aplicação cliente/servidor Distributed Video Store
3. Implementação de uma versão alternativa baseada em Rest-API para comparação de desempenho com a versão gRPC.
4. Simulação de um ambiente Cloud Native com k8s localmente usando o Minikube.

## Estrutura da Aplicação

| Módulo | Função | Tecnologia | Linguagem |
| :--- | :--- | :--- | :--- |
| **frontend** | Implementação do front-end que realiza chamadas HTTP para o API Gateway | VueJs | Typescript |
| **API Gateway** | Recebe requisições REST, traduz para gRPC e agrega respostas. É a implementação do serviço **P** | FastAPI | Python |
| **Catalogue Service (Microserviço 1)** | É a implementação do microsserviço **A**, que gerencia catálogo de vídeos | Go gRPC server | Go lang |
| **Rent Service (Microserviço 2)** | É a implementação do microsserviço **B**, que  gerencia informações de clientes e pedidos | Go gRPC server | Go lang |

### Desenho de Arquitetura

TODO: Elaborar e adicionar desenho

## Stack tecnológica do projeto

| Tecnologia | Função | Versão |
| :--- | :--- | :--- |
| **gRPC** | Comunicação entre microserviços | TODO |
| **Protocol Buffers (Protobuf)** | Serialização de dados | TODO |
| **HTTP/2** | Transporte de dados binários | TODO |
| **Docker** | Contêineres para cada módulo | TODO |
| **Minikube (K8s)** | Orquestração e deploy local | TODO |
| **Go lang** | Implementação do microserviço A | TODO |
|**Fast API**| Implementação do API gateway| TODO |
| **Go lang** | Implementação do microserviço B | TODO |
| **VueJs** | Implementação dos front-end | TODO |



## Funcionalidades Principais

- Comunicação **Unary**, **Server Streaming**, **Client Streaming** e **Bidirectional Streaming** com gRPC  
- API Gateway REST conectando múltiplos microserviços gRPC  
- Deploy automatizado com Minikube  
- Testes de performance comparando **gRPC vs REST/JSON**

### Escopo do trabalho e observações

Em geral, é comum utilizar ambientes com múltiplos repositórios para aplicações baseadas em microsserviços, especialmente quando o time de desenvolvimento é dividido em sub-times que podem trabalhar em serviços diferentes paralelamente. No entanto, para o escopo desse trabalho, que é uma simulação desenvolvida apenas por uma pessoa, será adotada uma estratégia de monorepo, ou seja, o projeto será organizado em um único repositório, e o deploy de cada componente da arquitetura no kubernetes será feito de maneira distribuída através dos manifestos de configuração.

## Como Executar 

TODO: instruções de setup e reprodução
