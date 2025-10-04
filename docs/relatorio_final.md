# Relatório de Atividade Extraclasse - Desenvolvimento de Aplicações Distribuídas com gRPC e Kubernetes

| Item | Descrição |
| :--- | :--- |
| **Curso** | UnB/FCTE – Engenharia de Software |
| **Semestre** | 2025/2 |
| **Disciplina** | PSPD - Programação para Sistemas Paralelos e Distribuídos - Turma 02 |
| **Professor** | Prof. Fernando W. Cruz |
| **Aluno** | Eric Chagas de Oliveira |
| **Matrícula** | 180119508 |

---

## 1. Introdução

Esse relatório descreve o desenvolvimento de um sistema distribuído de uma loja e locadora de filmes virtual. A aplicação “Distributed Video Store” desenvolvida para o trabalho, é baseada em microserviços e foi utilizado o framework gRPC, com posterior empacotamento em contêineres e deploy em um ambiente de Kubernetes simulado localmente com o Minikube.

### Objetivos
1. Estudo do gRPC, seus componentes e os quatro tipos de comunicação.
2. Implementação da aplicação cliente/servidor Distributed Video Store
3. Implementação de uma versão alternativa baseada em Rest-API para comparação de desempenho com a versão gRPC.
4. Simulação de um ambiente Cloud Native com k8s localmente usando o Minikube.

### Escopo do trabalho e observações

Em geral, é comum utilizar ambientes com múltiplos repositórios para aplicações baseadas em microsserviços, especialmente quando o time de desenvolvimento é dividido em sub-times que podem trabalhar em serviços diferentes paralelamente. 

No entanto, para o escopo desse trabalho, que é uma simulação desenvolvida apenas por uma pessoa, será adotada uma estratégia de monorepo, ou seja, o projeto será organizado em um único repositório, e o deploy de cada componente da arquitetura no kubernetes será feito de maneira distribuída através dos manifestos de configuração.

#TODO: Adicionar outras seções pedidas pelo professor
