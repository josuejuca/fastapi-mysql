# API de Gerenciamento de Usuários

Esta API permite operações básicas de gerenciamento de usuários em um banco de dados.

## Autenticação

A API requer autenticação básica para acessar os endpoints. As credenciais de autenticação são:

- **Usuário:** user
- **Senha:** password

## Endpoints Disponíveis

### Verificação de Status

- **Método:** GET
- **URL:** `/`
- **Descrição:** Verifica o status da API.
- **Resposta de Exemplo:**
    ```json
    {
        "API Stats": "Online"
    }
    ```

### Listar Todos os Usuários

- **Método:** GET
- **URL:** `/users`
- **Descrição:** Retorna todos os usuários cadastrados.
- **Resposta de Exemplo:**
    ```json
    [
        {
            "idusuario": 1,
            "nome": "João",
            "senha": "********",
            "email": "joao@example.com"
        },
        {
            "idusuario": 2,
            "nome": "Maria",
            "senha": "********",
            "email": "maria@example.com"
        },
        ...
    ]
    ```

### Obter Detalhes de um Usuário Específico

- **Método:** GET
- **URL:** `/users/{user_id}`
- **Descrição:** Retorna os detalhes de um usuário específico.
- **Parâmetros:**
    - `{user_id}`: ID do usuário desejado.
- **Resposta de Exemplo:**
    ```json
    {
        "idusuario": 1,
        "nome": "João",
        "senha": "********",
        "email": "joao@example.com"
    }
    ```

### Criar um Novo Usuário

- **Método:** POST
- **URL:** `/users`
- **Descrição:** Cria um novo usuário.
- **Corpo da Requisição (JSON):**
    ```json
    {
        "nome": "Novo Usuário",
        "senha": "novasenha",
        "email": "novo@example.com"
    }
    ```
- **Resposta de Exemplo:**
    ```json
    {
        "message": "Usuário criado com sucesso"
    }
    ```

### Atualizar Detalhes de um Usuário

- **Método:** PUT
- **URL:** `/users/{user_id}`
- **Descrição:** Atualiza os detalhes de um usuário específico.
- **Parâmetros:**
    - `{user_id}`: ID do usuário a ser atualizado.
- **Corpo da Requisição (JSON):** (Campos opcionais)
    ```json
    {
        "nome": "Novo Nome",
        "senha": "novasenha",
        "email": "novoemail@example.com"
    }
    ```
- **Resposta de Exemplo:**
    ```json
    {
        "message": "Usuário atualizado com sucesso"
    }
    ```

### Excluir um Usuário

- **Método:** DELETE
- **URL:** `/users/{user_id}`
- **Descrição:** Exclui um usuário específico.
- **Parâmetros:**
    - `{user_id}`: ID do usuário a ser excluído.
- **Resposta de Exemplo:**
    ```json
    {
        "message": "Usuário excluído com sucesso"
    }
    ```

## Códigos de Status

- **200:** Requisição bem-sucedida.
- **401:** Não autorizado - Credenciais inválidas.
- **404:** Não encontrado - Usuário não encontrado.
- **500:** Erro interno do servidor - Detalhes adicionais no campo "detail".
