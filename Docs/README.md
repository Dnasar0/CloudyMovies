# 🚀 Projeto Cloud Computing: Jogo de Adivinhação de Ratings de Filmes  

## 🕴️ Membros 
- Diogo Sargaço 58252
- Francisco Papoula 58206
- Henrique Vale 58168

---


## 🎯 Descrição  
O objetivo principal é criar um jogo onde o jogador tenta adivinhar se o rating de um filme do **Letterboxd**, apresentado no lado esquerdo da tela, é maior ou menor que o do filme apresentado à direita.  

- O filme da direita tem a classificação oculta e só é revelada após a decisão do jogador.  
- Se errar, o jogo termina e recomeça com novos filmes gerados aleatoriamente.  
- Se acertar, o jogo continua, movendo o filme da direita para a esquerda e adicionando um novo filme à direita, com a classificação oculta.  
- Inspirado no jogo [Higher or Lower](http://www.higherlowergame.com).  

---

## 📂 Dataset
- **Movies Dataset:** 783 MB (CSV)  | https://www.kaggle.com/datasets/gsimonx37/letterboxd/data
- **Imagens:** 18 GB (fotos extraídas da Internet)  
- **Date of Release:** 2024

---

## 💼 Business Capabilities  
- 📢 **Anúncios**: Monetização via anúncios entre rondas.  
- 💎 **Versão Premium**: Remove anúncios e adiciona funcionalidades extras.
- ❤️ **Doações**: Possibilidade de apoio voluntário dos jogadores.  
- 🏆 **Torneios Pagos**: Competição entre jogadores com prémios.  

---

## 📌 Casos de Uso

### 1. Criar conta no jogo - Francisco Papoula
- Conta vai ter high score.
- Conta vai ter estado de conta (premium / grátis)

### 2. Consultar conta - Francisco Papoula

### 3. Jogar -  Diogo Sargaço, Francisco Papoula, Henrique Vale

### 4. Criar torneio (caso seja premium) - Henrique Vale
- Conta premium vai ter possibilidade de criar torneio pago
- Recompensa por 1º lugar

### 4. Inscrever em torneios pagos. - Henrique Vale
- Qualquer conta pode-se inscrever desde que pague a inscrição inicial no torneio.

### 5. Empresa / Parceiro - Diogo Sargaço
- Exibe anúncios dentro do jogo.
- Pode patrocinar torneios ou eventos especiais.

### 6. Ver detalhes do filme - Diogo Sargaço
- Durante o jogo, se o utilizador quiser obter mais detalhes dos filmes exibidos, pode clicar no filme e ver numa nova tab as informações relacionadas com o filme

---

## 🌐 Tecnologias Sugeridas  
- **Back-end**: Node.js / Java
- **Front-end**: Angular
- **Banco de Dados**: MongoDB
- **Hospedagem**: Google Cloud


--------------------------
INSTRUÇÕES CORRER FICHEIRO 
--------------------------

Para correr o projeto, no diretório com o ficheiro docker, escreve-se "docker compose up". Depois correr o script (script.py) para popular DB. E abrir link que aparece quando docker compose up acabar de correr.



Nós para correr isto no wsl tivemos que instalar o kompose, para gerar os ficheiros yaml kubernets a partir do ficheiro docker, fizemos: 

- kompose convert

Tem de se ter o docker desktop ligado. Para iniciar o minikube, faz-se:

- minikube start

Para parar o minikube e apagar os containers:

- monikube stop; minikube delete

Para correr os ficheiros kubernets (atenção, tem de se apagar o ficheiro docker compose para fazermos isto):

- Editar frontend-service.yaml para ter isto: 
spec:
  type: LoadBalancer
  selector:
    io.kompose.service: frontend
  ports:
    - port: 80            # Publicly exposed port (HTTP)
      targetPort: 5000    # Your frontend app’s internal port

- Inserir comando kubectl apply -f .

Para verificar o estado de cada serviço:

- watch -n 2 kubectl get pods

Para dar expose do mongodb para depois editar o ficheiro script.py, e alterar o porto para popular db fazer:

- minikube service mongodb

Para dar expose do frontend, fazer:

- minikube service frontend

Depois é entrar no frontend e testar as cenas. Por agora falta o account

Caso se queira verificar algum log, por exemplo o do frontend, faz-se:

- kubectl logs <nome do pod>

