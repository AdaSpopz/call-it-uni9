from models.conexao import conectar

def listar_motivos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome 
        FROM motivo_solicitacao 
        ORDER BY id
    """)

    motivos = cursor.fetchall()

    cursor.close()
    conexao.close()
    return motivos


def buscar_motivos_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome 
        FROM motivo_solicitacao 
        WHERE id = %s
    """, (id,))

    motivo = cursor.fetchone()

    cursor.close()
    conexao.close()
    return motivo