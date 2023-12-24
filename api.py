from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import pymysql

# Inicialização do aplicativo FastAPI
app = FastAPI()

# Configuração da segurança para autenticação básica
security = HTTPBasic()

# Função para verificar as credenciais do usuário
def verify_user(credentials: HTTPBasicCredentials = Security(security)):
    correct_username = "juca"
    correct_password = "juca@juca"
    # Verifica se as credenciais são válidas
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return credentials.username

# Conexão com o banco de dados MySQL
conn = pymysql.connect(
    host='roundhouse.proxy.rlwy.net',
    port=15555,
    user='root',
    password='Ce3Ea6c1aA4C1A1df5dgeBeACEcE5AH2',
    database='railway'
)

# Endpoint para verificar o status da API
@app.get('/', tags=['Página inicial'])
def root():
    return {"API Stats": "Online"}

# Endpoint para obter todos os usuários
@app.get("/users", tags=['Lista os usuários'])
async def get_users(username: str = Depends(verify_user)):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.close()
        return users
    except Exception as e:
        # Em caso de exceção, retorna um erro interno do servidor
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter um usuário específico por ID
@app.get("/users/{user_id}", tags=['Usuário específico por ID'])
async def get_user(user_id: int, username: str = Depends(verify_user)):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user where idusuario=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            # Se o usuário não existir, retorna um erro 404
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return user
    except Exception as e:
        # Em caso de exceção, retorna um erro interno do servidor
        raise HTTPException(status_code=500, detail=str(e))

# Classe para definir a estrutura do novo usuário a ser criado
class CreateUser(BaseModel):
    nome: str
    senha: str
    email: str
    # Outros campos podem ser adicionados conforme necessário

# Endpoint para criar um novo usuário
@app.post("/users",tags=['Criar um novo usuário'])
async def create_user(user: CreateUser, username: str = Depends(verify_user)):    
    try:
        cursor = conn.cursor()
        query = "INSERT INTO user (nome, senha, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.nome, user.senha, user.email))
        conn.commit()
        cursor.close()

        return {"message": "Usuário criado com sucesso"}
    except Exception as e:
        # Em caso de exceção, retorna um erro interno do servidor
        raise HTTPException(status_code=500, detail=str(e))

# Classe para definir a estrutura dos dados a serem atualizados no usuário
class UpdateUser(BaseModel):
    nome: Optional[str] = None
    senha: Optional[str] = None
    email: Optional[str] = None
    # Outros campos podem ser adicionados conforme necessário

# Endpoint para atualizar os dados de um usuário existente
@app.put("/users/{user_id}", tags=['Atualizar o usuário'])
async def update_user(user_id: int, user_data: UpdateUser, username: str = Depends(verify_user)):
    try:
        cursor = conn.cursor()
        user_values = user_data.dict(exclude_unset=True)
        if user_values:
            query = "UPDATE user SET " + ", ".join([f"{key} = %s" for key in user_values.keys()]) + " WHERE idusuario = %s"
            cursor.execute(query, (*user_values.values(), user_id))
            conn.commit()
        cursor.close()

        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        # Em caso de exceção, retorna um erro interno do servidor
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para excluir um usuário existente
@app.delete("/users/{user_id}", tags=['Excluir o usuário'])
async def delete_user(user_id: int, username: str = Depends(verify_user)):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE idusuario = %s", (user_id,))
        conn.commit()
        cursor.close()

        return {"message": "Usuário excluído com sucesso"}
    except Exception as e:
        # Em caso de exceção, retorna um erro interno do servidor
        raise HTTPException(status_code=500, detail=str(e))

# Add login 
