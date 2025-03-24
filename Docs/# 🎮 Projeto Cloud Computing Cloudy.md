# 🎮 Projeto Cloud Computing: CloudyMovies

## 📌 Functional Requirements  

---

## **1. Criar Conta no Jogo**  
**ID:** FR-001  
**Descrição:** O sistema deve permitir que um usuário crie uma conta.  

### **Requisitos Funcionais:**  
- **FR-001.1** O usuário deve poder registrar-se com e-mail e senha.   
- **FR-001.2** A conta do usuário deve armazenar o **high score**.  
- **FR-001.3** A conta do usuário deve conter um **estado de conta** (premium/grátis).  
- **FR-001.4** O sistema deve verificar se o e-mail já está registrado antes de permitir a criação da conta.  

---

## **2. Consultar Conta**  
**ID:** FR-002  
**Descrição:** O usuário pode visualizar suas informações de conta.  

### **Requisitos Funcionais:**  
- **FR-002.1** O usuário deve poder visualizar seu nome, e-mail, high score e estado da conta.  
- **FR-002.2** O usuário deve poder alterar sua senha.  
- **FR-002.3** O usuário deve poder atualizar informações básicas do perfil.  
- **FR-002.4** Caso seja premium, o usuário deve poder gerir sua assinatura (renovar/cancelar).  

---

## **3. Jogar**  
**ID:** FR-003  
**Descrição:** O usuário pode jogar tentando adivinhar se a classificação de um filme é maior ou menor.  

### **Requisitos Funcionais:**  
- **FR-003.1** O sistema deve exibir dois filmes: um com rating visível (esquerda) e outro oculto (direita).  
- **FR-003.2** O usuário deve poder escolher se o rating do filme oculto é maior ou menor.  
- **FR-003.3** Se o usuário acertar, o filme da direita substitui o da esquerda e um novo filme é carregado.  
- **FR-003.4** Se o usuário errar, o jogo termina e exibe o score final.  

---

## **4. Criar Torneio (Premium)**  
**ID:** FR-004  
**Descrição:** Usuários premium podem criar torneios pagos para outros jogadores participarem.  

### **Requisitos Funcionais:**  
- **FR-004.1** Apenas contas premium podem criar torneios.  
- **FR-004.2** O criador do torneio deve definir o valor da inscrição e a premiação.  
- **FR-004.3** O torneio deve ter um tempo de duração pré-definido.  
- **FR-004.4** Os jogadores competem para obter a maior pontuação dentro do torneio.  
- **FR-004.5** Ao fim do torneio, os prêmios devem ser distribuídos automaticamente.  

---

## **5. Inscrever-se em Torneios Pagos**  
**ID:** FR-005  
**Descrição:** Qualquer usuário pode se inscrever em torneios pagos, desde que pague a taxa de inscrição.  

### **Requisitos Funcionais:**  
- **FR-005.1** O usuário deve visualizar a lista de torneios disponíveis.  
- **FR-005.2** O usuário deve pagar a taxa de inscrição antes de entrar no torneio.  
- **FR-005.3** Após a inscrição, o usuário pode competir para obter a maior pontuação.  
- **FR-005.4** O sistema deve exibir o ranking dos jogadores em tempo real.  

---

## **6. Empresa/Parceiro (Anúncios e Patrocínio)**  
**ID:** FR-006  
**Descrição:** Empresas podem exibir anúncios e patrocinar torneios.  

### **Requisitos Funcionais:**  
- **FR-006.1** O sistema deve exibir anúncios entre as rodadas do jogo para contas gratuitas.  
- **FR-006.2** Empresas podem pagar para exibir anúncios personalizados no jogo.  
- **FR-006.3** Empresas podem patrocinar torneios, oferecendo prêmios adicionais.  

---

## **7. Ver Detalhes do Filme**  
**ID:** FR-007  
**Descrição:** O usuário pode obter mais informações sobre um filme exibido no jogo.  

### **Requisitos Funcionais:**  
- **FR-007.1** Durante o jogo, o usuário pode clicar no filme para abrir uma aba com detalhes.  
- **FR-007.2** O sistema deve exibir título, data de lançamento, elenco principal, sinopse.