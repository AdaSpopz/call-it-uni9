from models.conexao import conectar

def listar_prioridade():

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
       SELECT id, nome, sla_horas FROM prioridade ORDER BY id
    """
    )

    prioridades = cursor.fetchall()

    cursor.close()
    conexao.close()
    return prioridades

def buscar_prioridade_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT id, nome, sla_horas FROM prioridade WHERE id = %s
    """, (id,)
    )

    prioridades = cursor.fetchall()

    cursor.close()
    conexao.close()
    return prioridades