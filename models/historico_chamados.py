from models.conexao import conectar

def adicionar_historico(chamado_id, usuario_id, acao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
    """
        INSERT INTO historico_chamado (chamado_id, usuario_id, acao)    VALUES (%s, %s, %s)
    """, (chamado_id, usuario_id, acao))

    conexao.commit()

    inserido = cursor.lastrowid

    cursor.close()
    conexao.close()
    return inserido


def listar_historico_por_chamado(chamado_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT h.id, h.acao, h.data_acao, u.nome AS usuario FROM historico_chamado h JOIN usuario u ON u.id = h.usuario_id WHERE h.chamado_id = %s ORDER BY h.data_acao ASC
    """, (chamado_id,))

    historico = cursor.fetchall()

    cursor.close()
    conexao.close()

    return historico

