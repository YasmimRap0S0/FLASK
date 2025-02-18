## **Trabalho Prático de Desenvolvimento de Software com Flask e ORM**

### **Objetivo**
O objetivo deste trabalho prático é desenvolver uma aplicação para gerenciar usuários, posts e comentários, utilizando o **Flask** como framework para criação de uma API REST e **SQLAlchemy** como ORM para persistência de dados. A aplicação deve permitir a criação, leitura, atualização e exclusão de registros no banco de dados, garantindo a integridade e consistência das informações.

### **Descrição**
A aplicação será um sistema de gerenciamento de posts e comentários, onde:

- Cada **Usuário** pode criar vários **Posts** e **Comentários**;
- Cada **Post** pertence a um **Usuário** e pode ter vários **Comentários**;
- Cada **Comentário** pertence a um **Usuário** e a um **Post**.

A API REST deve permitir interações para gerenciar usuários, posts e comentários, e seguir boas práticas de desenvolvimento utilizando Flask e SQLAlchemy.

### **Requisitos de Entrega do Trabalho Prático**

---

#### **1. Modelagem do Banco de Dados**

Crie o modelo de dados que atenda à descrição acima, contendo as seguintes entidades:

##### **Entidades e Atributos**

| **Entidade** | **Atributo**   | **Tipo**               | **Descrição**                                          |
|--------------|----------------|------------------------|--------------------------------------------------------|
| **Usuário**  | id             | Integer (Chave Primária)| Identificador único do usuário                        |
|              | nome           | String (100)            | Nome do usuário                                        |
|              | email          | String (100, único)     | Endereço de e-mail único do usuário                    |
| **Post**     | id             | Integer (Chave Primária)| Identificador único do post                           |
|              | titulo         | String (100)            | Título do post                                         |
|              | conteudo       | Text                    | Conteúdo do post                                       |
|              | usuario_id     | Integer (Foreign Key)   | Identificador do usuário que criou o post             |
| **Comentário**| id             | Integer (Chave Primária)| Identificador único do comentário                      |
|              | conteudo       | Text                    | Texto do comentário                                    |
|              | usuario_id     | Integer (Foreign Key)   | Identificador do usuário que fez o comentário          |
|              | post_id        | Integer (Foreign Key)   | Identificador do post ao qual o comentário pertence    |

##### **Relacionamentos**:
- **Usuário -> Posts**: Um **Usuário** pode criar vários **Posts**.
- **Usuário -> Comentários**: Um **Usuário** pode criar vários **Comentários**.
- **Post -> Comentários**: Um **Post** pode ter vários **Comentários**, e cada **Comentário** está associado a um **Post**.
- **Comentário -> Usuário e Post**: Cada **Comentário** pertence a um **Usuário** e a um **Post**.

---

#### **2. Implementação da API REST**

Desenvolver uma API REST para gerenciar os dados, garantindo as seguintes funcionalidades:

##### **Endpoints**

###### **Usuário**
- Criar um usuário: `POST /usuarios`
- Listar todos os usuários: `GET /usuarios`
- Buscar um usuário pelo ID: `GET /usuarios/:id`
- Atualizar dados de um usuário: `PUT /usuarios/:id`
- Excluir um usuário: `DELETE /usuarios/:id`

###### **Post**
- Criar um post: `POST /posts`
- Listar todos os posts: `GET /posts`
- Buscar um post pelo ID: `GET /posts/:id`

###### **Comentário**
- Criar um comentário: `POST /comentarios`
- Listar todos os comentários: `GET /comentarios`
- Excluir um comentário: `DELETE /comentarios/:id`

---

#### **3. Tecnologias Utilizadas**

- **Python** com **Flask** para a criação da API.
- **SQLAlchemy** como ORM para comunicação com o banco de dados relacional (pode ser PostgreSQL, MySQL ou SQLite).
- **Flasgger** para documentação da API (Swagger).

--- 

