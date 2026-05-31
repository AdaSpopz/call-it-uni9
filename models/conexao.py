import mysql.connector

def conectar():
    """
    Cria e retorna uma conexão com o banco de dados.
    Altere host, user, password e database conforme o seu ambiente.
    """
    try:
        conexao = mysql.connector.connect(
            host="localhost",        
            user="root",              
            password="",              
            database="chamados_db"        
        )

        return conexao

    except mysql.connector.Error as erro:
                print(f"Erro ao conectar: {erro}")
                return None

if __name__ == "__main__":

    testando = conectar()

    if testando:
        print("Conectado com sucesso")
    else:
        print("Erro ao conectar")