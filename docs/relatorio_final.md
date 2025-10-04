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

## 2. O Framework gRPC e Tipos de Comunicação (B.1)

### 2.1. Conceitos usados pelo gRPC

#### Protocol Buffers (Protobuf) 
  O Protobuf é usado pelo gRPC para a serialização dos dados enviados pela rede e como linguagem de definição de interface (IDL). Ele permite definir as mensagens e serviços em um arquivo `.proto`, a partir do qual são gerados os **stubs** para as diferentes linguagens de programação.

#### HTTP/2
  O gRPC também se baseia no protocolo HTTP/2, que oferece **multiplexação de streams**, **compressão de cabeçalhos** e **server push**, possibilitando comunicações simultâneas, menor latência e uso mais eficiente dos recursos de rede.

### 2.2. Estudo e simulação dos tipos de comunicação

O gRPC possui 4 tipos de comunicação, que são bem descritos na página [Core concepts, architecture and lifecycle](https://grpc.io/docs/what-is-grpc/core-concepts/) da documentação oficial.

Para esse trabalho foram construídos 4 pequenas aplicações cliente-servidor implementando cada um dos tipos de chamada mostrados na **Tabela 01**. 

Também foram linkados na **Tabela 01** os diretórios no github onde foram armazenados os arquivos de teste, em que foram criados 4 diretórios, um para cada tipo de chamada:

- `estudo-gRPC/unary-call`
- `estudo-gRPC/server-streaming`
- `estudo-gRPC/client-streaming`
- `estudo-gRPC/bidirectional-streaming`

Dentro de cada diretório listado acima, estão os arquivos `.proto`, e os arquivos python do cliente e do servidor.


###### Tabela 01 - Tipos de chamada gRPC. Fonte: Autoria própria com base na documentação oficial do gRPC

| Tipo de Comunicação | Funcionamento | Arquivo Protobuf e Código de Teste | Conclusão e Cenários de Uso Recomendados |
| :--- | :--- | :--- | :--- |
| **Unary Call** | Cliente envia uma requisição e recebe uma resposta única. | [`unary-call/movie_info.proto`](#TODO:Adicionar_link_direto_arquivo_github) | Ideal para operações simples de consulta ou cadastro. |
| **Server-Streaming Call** | Cliente envia uma requisição e recebe múltiplas respostas em *stream*. | [`server-streaming/movie_info.proto`](#TODO:Adicionar_link_direto_arquivo_github) | Útil para relatórios, logs contínuos ou notificações. |
| **Client-Streaming Call** | Cliente envia múltiplas requisições e recebe uma resposta única consolidada. | [`client-streaming/movie_info.proto`](#TODO:Adicionar_link_direto_arquivo_github) | Adequado para upload de arquivos ou envio de lotes de dados. |
| **Bidirectional Streaming Call** | Cliente e servidor trocam múltiplas mensagens simultaneamente. | [`bidirectional-streaming/movie_info.proto`](#TODO:Adicionar_link_direto_arquivo_github) | Perfeito para chats em tempo real ou monitoramento contínuo. |

### 2.3 Aplicações de exemplo para os tipos de chamada

Para as demonstrações dos tipo de chamada, foram desenvolvidos quatro programas simples, em python, e que implementam o gRPC usando as bibliotecas `grpcio` e `grpcio-tools`. 

O contexto é o mesmo para as quatro: O servidor contém uma lista de filmes com as seguintes informações para cada um:
1. movie_id: "chave primária" do filme (int32) 
2. movie_name: nome do filme (string)
3. movie_release_year: ano de lançamento do filme (int32)
4. movie_genre: Gênero do filme (string)

O que muda para cada experimento é o tipo de chamada, o cliente pode enviar requisições pedindo por filmes, usando o movie_id como chave de busca.

#### 2.3.1 Método de reprodução dos testes

Os nomes dos arquivos foram mantidos de maneira que para reproduzir qualquer um dos testes descritos nesse relatório. A título de exemplo, o passo a passo a seguir demonstra como executar o teste de unary calls, para executar os demais testes, basta seguir os mesmos passos substituindo o nome do diretório pelo do teste desejado.

> Requisitos:
> 
> 1. Estar em um ambiente linux
> 2. Possuir o Python3 instalado. Versão usada nesse trabalho: 3.12.3  

1. Clonar o repositório, acessa-lo

```bash
git clone git@github.com:Eric-chagas/distributed-video-store.git
cd distributed-video-store

# Criar ambiente virtual python para posteriormente instalar as dependencias
python3 -m venv .venv
source .venv/bin/activate
```
2. Instalar as dependências do python

```bash
cd estudo-gRPC/
pip install -r requirements.txt
```

3. Acessar o diretório do teste e gerar os arquivos do gRPC com o protoc

```bash
cd unary-call/
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./movie_info.proto
```
Serão criados os arquivos `movie_info_pb2_grpc.py` e `movie_info_pb2.py` 

4. Agora execute o servidor

```bash
python3 movie_info_server.py 
```
O output deve ser "gRPC server online and listening on port 70001...". Agora é necessário abrir um novo terminal para executar a chamada do cliente.

5. Em um novo terminal, acesse o diretório `estudo-gRPC/unary-call/` novamente e execute o cliente:

```bash
# É necessário iniciar o virtualenv do python no novo terminal também. Na raiz do repositório:
cd estudo-gRPC/
source .venv/bin/activate

# Em seguida, basta executar o cliente
python3 movie_info_client.py
```

O resultado deve se ser o da Figura 01, na seção a seguir. Para executar os testes de client streaming, server streaming e bidirectional streaming, basta seguir os mesmos passos, para o diretório específico de cada um.

#### 2.3.2 Unary Call

Para a demonstração do tipo de chamada unary call, o cliente deve chamar o stub de `GetMovieInfo(movie_id)` passando como argumento o `movie_id` do filme desejado. Por se tratar de **unary call** o cliente envia apenas um id, e aguarda o retorno do servidor, que consiste em um único filme.

O arquivo `movie_info.proto` foi construído da seguinte forma:

```
syntax = "proto3";

package movie_info;

// gRPC service
service MovieInfo {
    rpc GetMovieInfo (MovieRequest) returns (MovieReply);
}

// Message client request
message MovieRequest {
    int32 movie_id = 1;
}

// Message Server response
message MovieReply {
    int32 movie_id = 1;
    string movie_name = 2;
    int32 movie_release_year = 3;
    string movie_genre = 4;
}
```

Os códigos do cliente e servidor estão no mesmo diretório, no repositório e são acessíveis por [esse link](https://github.com/Eric-chagas/distributed-video-store/tree/main/estudo-gRPC/unary-call).

Na Figura 01, está ilustrado o resultado da execução do programa.

###### Figura 01 - Execução do exemplo de unary call. Fonte: Autoria própria

![Unary call execution result](../assets/estudo-gRPC/unary_call.png)


