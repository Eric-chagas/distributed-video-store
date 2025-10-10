# Relatório de Atividade Extraclasse - Desenvolvimento de Aplicações Distribuídas com gRPC e Kubernetes

| Item | Descrição |
| :--- | :--- |
| **Curso** | UnB/FCTE – Engenharia de Software |
| **Semestre** | 2025/2 |
| **Disciplina** | PSPD - Programação para Sistemas Paralelos e Distribuídos - Turma 02 |
| **Professor** | Prof. Fernando W. Cruz |
| **Aluno** | Eric Chagas de Oliveira |
| **Matrícula** | 180119508 |
|**Link do repositório**|https://github.com/Eric-chagas/distributed-video-store|
|**Link do vídeo de apresentação**|#TODO: Adicionar vídeo|

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

## 2. O Framework gRPC e Tipos de Comunicação

### 2.1. Conceitos usados pelo gRPC

#### Protocol Buffers (Protobuf) 
  O Protobuf é usado pelo gRPC para a serialização dos dados enviados pela rede e como linguagem de definição de interface (IDL). Ele permite definir as mensagens e serviços em um arquivo `.proto`, a partir do qual são gerados os **stubs** para as diferentes linguagens de programação.

#### HTTP/2
  O gRPC também se baseia no protocolo HTTP/2, que oferece **multiplexação de streams**, **compressão de cabeçalhos** e **server push**, possibilitando comunicações simultâneas, menor latência e uso mais eficiente dos recursos de rede.

### 2.2. Estudo e simulação dos tipos de comunicação

O gRPC possui 4 tipos de comunicação, que são bem descritos na página [Core concepts, architecture and lifecycle](https://grpc.io/docs/what-is-grpc/core-concepts/) da documentação oficial.

Para esse trabalho foi construida uma pequena aplicações cliente-servidor, com um servidor e quarto clientes implementando cada um dos tipos de chamada mostrados na **Tabela 01**. 

###### Tabela 01 - Tipos de chamada gRPC. Fonte: Autoria própria com base na documentação oficial do gRPC

| Tipo de Comunicação | Funcionamento | Arquivo Protobuf e Código de Teste | Conclusão e Cenários de Uso Recomendados |
| :--- | :--- | :--- | :--- |
| **Unary Call** | Cliente envia uma requisição e recebe uma resposta única. | `unary-call/movie_info.proto` | Ideal para operações simples de consulta ou cadastro. |
| **Server-Streaming Call** | Cliente envia uma requisição e recebe múltiplas respostas em *stream*. | `server-streaming/movie_info.proto` | Útil para relatórios, logs contínuos ou notificações. |
| **Client-Streaming Call** | Cliente envia múltiplas requisições e recebe uma resposta única consolidada. | `client-streaming/movie_info.proto` | Adequado para upload de arquivos ou envio de lotes de dados. |
| **Bidirectional Streaming Call** | Cliente e servidor trocam múltiplas mensagens simultaneamente. | `bidirectional-streaming/movie_info.proto` | Perfeito para chats em tempo real ou monitoramento contínuo. |

Também linkado na **Tabela 01** está o endereço no github onde foram armazenados os arquivos de da demonstração. Os arquivos são os seguintes:

- `movie_info.proto`: Arquivo para definição de interface do serviço gRPC
- `estudo-gRPC/server.py`: Arquivo do servidor com 4 métodos, cada um com a lógica de resposta implementando um dos tipos de chamada do gRPC
- `estudo-gRPC/client_stream_client.py`: Arquivo de cliente que realiza chamadas **client stream**, enviando um id de filme por vez e processa a resposta única do servidor após ter terminado de enviar todos os IDs
- `estudo-gRPC/server_stream_client.py`: Arquivo de cliente que realiza uma única chamada para o servidor, passando uma lista de ids de filmes separados por vírgula, e processa acada id recebido como resposta no **server stream** à medida que recebe, também um por vez
- `estudo-gRPC/unary_call_client.py`: Arquivo de cliente que realiza uma única chamada para o servidor com um id de filme, e recebe uma única resposta com os dados do filme
- `estudo-gRPC/bidirectional_stream_client.py`: Arquivo de cliente que realiza chamadas **client stream**, enviando um id de filme por vez e processa a resposta **server stream** à medida que recebe, também um por vez

Os códigos de teste e o método para reproduzir o teste no seu ambiente local está melhor descrito no repositório do github, [nessa página](https://github.com/Eric-chagas/distributed-video-store/tree/main/estudo-gRPC).

#### 2.3.2 Unary Call

Para a demonstração do tipo de chamada unary call, o cliente deve chamar o stub de `GetMovieInfo(movie_id)` passando como argumento o `movie_id` do filme desejado. Por se tratar de **unary call** o cliente envia apenas um id, e aguarda o retorno do servidor, que consiste em um único filme.

O arquivo `unary_call_client.py` implementa a chamada ao stub de unary call do servidor.

```python
def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server
        response = stub.GetMovieInfo(movie_info_pb2.MovieRequest(movie_id=4)) # sending request for movie with id 4 and wating response
        print(response) # Printing single movie response

```

Na Figura 01, está ilustrado o resultado da execução desse cliente.

###### Figura 01 - Execução do exemplo de unary call. Fonte: Autoria própria

![Unary call execution result](../assets/estudo-gRPC/unary_call.png)

#### 2.3.3 Server streaming

Para a demonstração do tipo de chamada Server Streaming, o cliente deve chamar o stub de `GetMoviesServerStream(movie_id_list)` passando como argumento o a lista de movie_ids separados por vírgula dos filmes desejados. Por se tratar de **server stream call** o cliente envia apenas uma lista de ids de uma vez, e aguarda o retorno do servidor, que consiste nos vários filmes requisitados, um por vez.

O arquivo `server_stream_client.py` implementa a chamada ao stub de service streaming do servidor.

```python
def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server
        request = movie_info_pb2.MovieListRequest(movie_ids=[1, 3, 5, 9])
        
        # Calling server streaming sending list of ids
        responses = stub.GetMoviesServerStream(request)
        
        for movie in responses:
            print("Movie ID: ", movie.movie_id)
            print("Movie name: ", movie.movie_name)
            print("Movie year: ", movie.movie_release_year)
            print("Movie genre: ", movie.movie_genre)
            print()

```

Na Figura 02, está ilustrado o resultado da execução desse cliente.

###### Figura 02 - Execução do exemplo de server stream call. Fonte: Autoria própria

![Unary call execution result](../assets/estudo-gRPC/server_stream.png)

#### 2.3.4 Client streaming

Para a demonstração do tipo de chamada Client Streaming, o cliente deve chamar o stub de `GetMoviesClientStream(movie_id)` passando como argumento um movie_id por vez no formato de stream do cliente. Por se tratar de **client stream call** o cliente envia um id por vez, o servidor aguarda receber todos, e enfim processa e responde com a lista de filmes pedidos, de uma só vez.

O arquivo `client_stream_client.py` implementa a chamada ao stub de client streaming do servidor.

```python
def generate_movie_requests():
    for movie_id in [1, 4, 6, 9]:
        print(f"Client: Now sending movie_id {movie_id}")
        yield movie_info_pb2.MovieRequest(movie_id=movie_id)
        time.sleep(0.5) 

def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server        
        # Calling server streaming sending list of ids
        response = stub.GetMoviesClientStream(generate_movie_requests())
                
        for movie in response.movies:
            print("Movie ID: ", movie.movie_id)
            print("Movie name: ", movie.movie_name)
            print("Movie year: ", movie.movie_release_year)
            print("Movie genre: ", movie.movie_genre)
            print()

```

Na Figura 03, está ilustrado o resultado da execução desse cliente.

###### Figura 03 - Execução do exemplo de client stream call. Fonte: Autoria própria

![Unary call execution result](../assets/estudo-gRPC/client_stream.png)

#### 2.3.5 Bidirectional streaming

Para a demonstração do tipo de chamada Bidirectional Streaming, o cliente deve chamar o stub de `GetMoviesBidirectionalStream(movie_id)` passando como argumento um movie_id por vez no formato de stream do cliente. Por se tratar de **bidirectional stream call** o cliente envia um id por vez, e o servidor responde à medida que recebe, respondendo também um filme por vez ao cliente, no formato de server stream.

O arquivo `bidirectional_stream_client.py` implementa a chamada ao stub de bidirectional streaming do servidor.

```python
def generate_movie_requests():
    for movie_id in [1, 4, 6, 9]:
        print(f"Client: Now sending movie_id {movie_id}")
        yield movie_info_pb2.MovieRequest(movie_id=movie_id)
        time.sleep(1) 

def run():
    with grpc.insecure_channel('localhost:70001') as channel:
        stub = movie_info_pb2_grpc.MovieInfoStub(channel) # using created channel to server        
        
        # Calling server streaming sending list of ids
        response = stub.GetMoviesBidirectionalStream(generate_movie_requests())
                
        for movie in response:
            print("Movie ID: ", movie.movie_id)
            print("Movie name: ", movie.movie_name)
            print("Movie year: ", movie.movie_release_year)
            print("Movie genre: ", movie.movie_genre)
            print()
```

Na Figura 04, está ilustrado o resultado da execução desse cliente.

###### Figura 04 - Execução do exemplo de client stream call. Fonte: Autoria própria

![Unary call execution result](../assets/estudo-gRPC/client_stream.png)

#### 2.3.6 Discussão do estudo

Ao implementar os métodos acima, percebo que assim como em outros temas da computação como arquitetura de microsserviços e monolito, polirepo e monorepo, orientado a eventos e orientado a chamadas, entre outros assuntos, não existe bala de prata com relação a qual tipo de chamada gRPC utilizar. 

Fica claro que cada situação pode demandar um tipo diferente de chamada, minha percepção após esse experimento é:

1. **Unary calls**: Pode ser melhor utilizada em chamadas nas quais o processamento paralelo de chamadas não é algo crucial, para extrações pontuais ou consultas mais simples
2. **Server stream**: Acredito que possa ser bem empregado em situações onde o cliente está ativamente aguardando por resposta do servidor por exemplo, mas os dados recebidos podem ser entregues em partes. No caso da locadora por exemplo, não é um problema mostrar os filmes à medida que o cliente às recebe na tela, e manter um "loading" para o que ainda não foi carregado. O mesmo não pode ser dito de um sistema bancário por exemplo, em que se o cliente recebe um nome, ou valor monetário "quebrado" isso pode ter consequências graves.
3. **Client stream**: Esse aparenta se adequar melhor a situações opostas à que citei no server stream, por exemplo, quando não se tem problema em aguardar pela resposta do servidor do lado do cliente, e é importante receber os dados completos, de uma vez só para que a consistência das regras de negócio não sejam prejudicadas. Acredito que também se comporte bem quando a conexão do lado do cliente é lenta, os dados são enviados em partes e o servidor responde após receber todos.
4. **Bidirectional stream**: O bidirectional stream, pode se comportar bem quando empregado em comunicações como chats online por exemplo, onde se requer uma sincronia maior mas não é possível prever quantos pacotes serão enviados em um período de tempo.

## 3. Construção da Aplicação Cliente/Servidor com gRPC

### 3.1. Detalhes da Aplicação Distributed Video Store

  O sistema simula uma loja de vídeos distribuída, permitindo consultar informações sobre filmes, combinando dados provenientes de dois microserviços independentes:  
  - **Serviço A (Catálogo):** fornece metadados de filmes (título, gênero, duração, ano).  
  - **Serviço B (Estoque):** retorna informações de disponibilidade e preço de aluguel.  
  O **Gateway (P)** atua como ponto de entrada REST, recebendo requisições HTTP do cliente web, convertendo-as em chamadas gRPC para os microserviços e consolidando as respostas em um único JSON.
  
- **Linguagens Utilizadas:**
  - **Módulo P (Gateway/API):** Python (FastAPI + gRPC client)  
  - **Módulo A (Catálogo):** Go (gRPC server)  
  - **Módulo B (Estoque):** Go (gRPC server)  
  - **Frontend:** VueJs consumindo a API REST do gateway  

### 3.2. Estrutura dos Módulos Backend (P, A e B)

- **Módulo P (API Gateway / gRPC Stub):**  
  Recebe requisições HTTP (`GET /api/movies/:id` e `GET /api/rent/consult/:id`), chama os serviços A e B via gRPC, consolida os dados (metadados + disponibilidade/preço) e retorna a resposta em JSON.  
  - **Framework:** FastAPI  
  - **Exemplos de rota:**
    - `http://localhost:8000/api/movies/1`
    - `http://localhost:8000/api/rent/consult/1`  

- **Módulo A (gRPC Server - Catálogo):**  
  Implementado em Go. Retorna informações estáticas de filmes (título, gênero, ano de lançamento, duração).

- **Módulo B (gRPC Server - Estoque):**  
  Também implementado em Go. Retorna disponibilidade (em estoque ou não), preço de aluguel e possíveis promoções.


## 4. Comparativo de Performance entre gRPC e Rest

Para avaliar o desempenho da aplicação Distributed Video Store por meio de um "teste de estresse" foi implementada uma API rest em Go no serviço catalogue-service, e dois métodos novos no servidor gRPC do catalogue-service.  

- **API REST/JSON:** comunicação entre o API Gateway (P) e o microsserviço `catalogue-service` via HTTP/JSON.  
- **Versão gRPC:** comunicação via gRPC, testando dois modos:
  - **Unary Call:** retorno de todos os filmes em uma única resposta.
  - **Server Streaming:** envio dos filmes um a um através de stream.

### 4.1. Cenário de Teste

- Quantidade de filmes solicitados: **100000** e **500000**  
- Mesma infraestrutura local (Minikube/localhost)  
- Medição do **tempo de resposta total** para cada abordagem na ferramenta postman.

### 4.2. Resultados

#### Testes com 100000 resultados
| Versão / Protocolo        | Tempo de Resposta | Nº de Resultados |
|----------------------------|-----------------------|-----------------|
| REST/JSON                  | 1.05 s                  | 100000         |
| gRPC Unary                 | 0.918 s                | 100000         |
| gRPC Server Stream         | 4.45 s                  | 100000         |


#### Testes com 500000 resultados
| Versão / Protocolo        | Tempo de Resposta | Nº de Resultados |
|----------------------------|-----------------------|-----------------|
| REST/JSON                  | 5.26 s                  | 500000         |
| gRPC Unary                 | 4.39 s                | 500000         |
| gRPC Server Stream         | 25.24 s                  | 500000         |

> Observação: os valores são aproximados, representando a tendência observada nos testes.  

### 4.3. Análise e Conclusão

- O **gRPC Unary** apresentou desempenho muito próximo do REST/JSON, com apenas uma leve diferença devido à serialização binária do Protobuf.  
- O **Server Streaming** demonstrou maior tempo de resposta, principalmente pelo envio individual de cada registro, que introduz overhead de chamadas repetidas no transporte.  
- Conclui-se que para grandes volumes de dados, se a aplicação não precisa processar cada item em tempo real, a **chamada Unary gRPC** ou **REST/JSON** são mais eficientes. O **Streaming** é útil quando há necessidade de processamento progressivo ou transmissão contínua de dados.

Os testes possuem o viés de serem executados no ambiente local do desenvolvedor, por mais que tenha sido utilizado o kubernetes. É notável pelos testes que o gRPC em geral, quando usado corretamente, performa melhor, a tendência é que à medida que crescem as distâncias percorridas na rede e a quantidade de dados trafegados, a otimização da serialização do protobuffer torne-se mais perceptível.

## 5. Implantação e Orquestração com Kubernetes

Para garantir escalabilidade, isolamento e facilidade de gerenciamento dos microserviços desenvolvidos, o ambiente foi orquestrado utilizando o **Kubernetes**, executado localmente através do **Minikube**.

A arquitetura foi estruturada em três componentes principais: **API Gateway**, **Catalogue Service** e **Rent Service** cada um executando em um contêiner independente, gerenciado por um **Deployment** e exposto por um **Service**. Também foi utilizado um **ConfigMap** para centralizar as variáveis de ambiente responsáveis por definir os hosts e portas de comunicação entre os serviços.

### 5.1. Arquitetura do Ambiente

- **API Gateway**  
  - Responsável por receber as requisições REST externas e orquestrar chamadas gRPC para os serviços internos.  
  - Implantado via `Deployment` com **1 réplica** e exposto através de um **Service do tipo NodePort**, permitindo acesso externo ao cluster.  
  - Configurado com variáveis de ambiente definidas pelo **ConfigMap**.

- **Catalogue Service**  
  - Serviço gRPC responsável por fornecer os metadados dos filmes.  
  - Exposto apenas internamente por meio de um **Service do tipo ClusterIP**, garantindo comunicação restrita dentro do cluster.  

- **Catalogue Rest Service**  
  - Serviço gRPC responsável pelos testes de estresse rest.  
  - Exposto apenas internamente por meio de um **Service do tipo ClusterIP**, garantindo comunicação restrita dentro do cluster.  

- **Rent Service**  
  - Serviço gRPC responsável pelas informações de disponibilidade e locação.  
  - Também acessível apenas internamente via **ClusterIP**.  

- **ConfigMap**  
  - Contém as variáveis de ambiente que definem os endereços dos serviços internos:  
    ```yaml
    CATALOGUE_SERVICE_HOST: "catalogue-service"
    CATALOGUE_SERVICE_PORT: "50051"
    RENT_SERVICE_HOST: "rent-service"
    RENT_SERVICE_PORT: "50052"
    CATALOGUE_REST_SERVICE_HOST: "catalogue-rest-service"
    CATALOGUE_REST_SERVICE_PORT: "8080"
    ```
  - Compartilhado entre os contêineres que necessitam dessas informações.

### 6.2. Arquivos de Configuração

Os arquivos YAML definem os recursos do cluster:
- **Deployments**: especificam as imagens dos contêineres, número de réplicas, recursos de CPU/memória e variáveis de ambiente.  
- **Services**: configuram as portas de comunicação entre os módulos.  
- **ConfigMap**: centraliza parâmetros reutilizados pelos serviços.  

### 6.3. Resultados e Observações

- O **API Gateway** é acessível externamente via port forward, tornando possível consumir a API REST pela máquina local.
- Os serviços **Catalogue** e **Rent** se comunicam internamente com o gateway por meio dos nomes e portas presentes no **ConfigMap**.
- O script `setup.sh` e o script `destroy.sh`, permitem respectivamente subir e destruir o ambiente local completo com apenas um comando

## 7. Conclusão e relato do desenvolvedor: Eric

A experiência de desenvolver esse trabalho foi bem cansativa, porém muito enriquecedora. Havia algum tempo que não desenvolvia um sistema como esse "do zero" sozinho, e tive a oportunidade de construir todas as etapas, tanto da infra-estrutura quanto dos serviços em si, e me sinto satisfeito com o resultado.

Quanto ao gRPC, iniciei o projeto com conhecimento básico e absolutamente nenhuma experiência prática, e foi muito interessante entender como cada parte do protocolo funciona, e ver isso funcionando depois de implementar, é um recurso que não utilizo hoje no dia-a-dia e nunca tinha tido contato com no mercado de trabalho, porém vejo um potêncial grande quando usado corretamente, como exemplifiquei na seção de teste de estresse.

Me sinto gratificado com essa experiência, que foi extremamente trabalhosa, mas de enorme valor para mim como programador. Por ter feito o trabalho sozinho, sentir que consegui cumprir todos os requisitos pedidos e ter dedicado um enorme esforço, minha auto-avaliação é nota 10.