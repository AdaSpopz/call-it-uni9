from models.conexao import conectar

def status_chamado(id,nome):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
       SELECT id, nome FROM status ORDER BY id
    """
    )

    status = cursor.fetchall()

    cursor.close()
    conexao.close()
    return status

def buscar_status_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT id, nome FROM status WHERE id = %s
    """, (id,)
    )

    status = cursor.fetchall()

    cursor.close()
    conexao.close()
    return status