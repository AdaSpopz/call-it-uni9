from models.conexao import conectar

def listar_perfil():

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
       SELECT id, nome FROM perfil ORDER BY id
    """
    )

    status = cursor.fetchall()

    cursor.close()
    conexao.close()
    return status


def buscar_prioridade_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT id, nome FROM perfil WHERE id = %s
    """, (id,)
    )

    status = cursor.fetchall()

    cursor.close()
    conexao.close()
    return status