# Gerenciador de Produtos (Desktop)

Aplicação desktop em Java Swing para cadastro e gerenciamento de produtos, com tela de login, seguindo o padrão **MVC** com camada de acesso a dados isolada (DAO).

## Tecnologias

- **Java** (Swing para interface gráfica)
- **Maven**
- Padrão **MVC** (Model-View-Controller) + **DAO**

## Funcionalidades

- Tela de login
- Cadastro, listagem, edição e exclusão de produtos (nome, categoria, preço e quantidade)

## Arquitetura

```
gerenciador-produtos-desktop/
├── src/main/java/model/       # entidades (Produto, Usuario)
├── src/main/java/dao/         # acesso a dados
├── src/main/java/controller/  # regras de aplicação (LoginController, ProdutoControlle)
├── src/main/java/view/        # telas Swing (TelaLogin, TelaProduto)
└── src/main/java/main/        # ponto de entrada
```

> Nesta versão, a camada DAO mantém os dados em memória (`ArrayList`), o que facilita rodar o projeto sem depender de um banco de dados configurado. A estrutura já separa as responsabilidades de forma que trocar por persistência em banco relacional (JDBC) exige apenas reimplementar a camada DAO.

## Como rodar

### Pré-requisitos
- Java JDK 22+
- Maven (ou uma IDE com suporte a projetos Maven, como NetBeans ou IntelliJ)

### Passos

```bash
mvn compile
mvn exec:java -Dexec.mainClass="view.TelaLogin"
```

Ou importe o projeto em uma IDE Java e execute a classe `view.TelaLogin`.
