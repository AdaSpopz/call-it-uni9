from models.conexao import conectar
from flask import render_template


def criar_chamado(titulo, descricao, prioridade_id, motivo_id, solicitante_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
    """
        INSERT INTO chamado (
            titulo,
            descricao,
            prioridade_id,
            motivo_id,
            status_id,
            solicitante_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        titulo,
        descricao,
        prioridade_id,
        motivo_id,
        1,
        solicitante_id
    ))

    conexao.commit()

    chamado_id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return chamado_id


def listar_chamados(prioridade=None, status=None):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            c.*,
            p.nome AS prioridade,
            s.nome AS status,
            m.nome AS motivo,
            u.nome AS solicitante,
            t.nome AS tecnico
        FROM chamado c

        JOIN prioridade p
            ON c.prioridade_id = p.id

        JOIN status_chamado s
            ON c.status_id = s.id

        JOIN motivo_solicitacao m
            ON c.motivo_id = m.id

        JOIN usuario u
            ON c.solicitante_id = u.id

        LEFT JOIN usuario t
            ON c.tecnico_id = t.id

        WHERE c.ativo = TRUE
        AND s.nome != 'Encerrados'
    """
    valores = []


    if prioridade:
        sql += " AND p.nome = %s"
        valores.append(prioridade)


    if status:
        sql += " AND s.nome = %s"
        valores.append(status)

    sql += " ORDER BY c.data_abertura DESC"

    cursor.execute(sql, valores)

    chamados = cursor.fetchall()

    

    cursor.close()
    conexao.close()

    return chamados

def atualizar_chamado(id, status_id=None, tecnico_id=None):

    conexao = conectar()
    cursor = conexao.cursor()

    if status_id and tecnico_id:

        cursor.execute(
        """
            UPDATE chamado
            SET status_id = %s,
                tecnico_id = %s
            WHERE id = %s
        """, (status_id, tecnico_id, id))

    elif status_id:

        cursor.execute(
        """
            UPDATE chamado
            SET status_id = %s
            WHERE id = %s
        """, (status_id, id))

    elif tecnico_id:

        cursor.execute(
        """
            UPDATE chamado
            SET tecnico_id = %s
            WHERE id = %s
        """, (tecnico_id, id))

    conexao.commit()

    atualizado = cursor.rowcount > 0

    cursor.close()
    conexao.close()

    return atualizado


def encerrar_chamado(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
    """
        UPDATE chamado
        SET status_id = 3,
            data_encerramento = NOW()
        WHERE id = %s
    """, (id,))

    conexao.commit()

    fechado = cursor.rowcount > 0

    cursor.close()
    conexao.close()

    return fechado


def buscar_chamado_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT
            c.id,
            c.titulo,
            c.descricao,
            c.data_abertura,
            c.data_encerramento,

            p.nome AS prioridade,
            m.nome AS motivo,
            s.nome AS status,

            u.nome AS solicitante,

            t.nome AS tecnico

        FROM chamado c

        JOIN prioridade p
            ON p.id = c.prioridade_id

        JOIN motivo_solicitacao m
            ON m.id = c.motivo_id

        JOIN status_chamado s
            ON s.id = c.status_id

        JOIN usuario u
            ON u.id = c.solicitante_id

        LEFT JOIN usuario t
            ON t.id = c.tecnico_id

        WHERE c.id = %s
    """, (id,))

    chamado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return chamado

def salvar_comentario(chamado_id, usuario_id, texto):

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO historico_chamado (chamado_id, usuario_id, acao)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (chamado_id, usuario_id, texto))
    conn.commit()

    cursor.close()
    conn.close()

def buscar_comentarios(chamado_id):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT h.acao AS texto,
               h.data_acao AS data,
               u.nome AS autor
        FROM historico_chamado h
        JOIN usuario u ON u.id = h.usuario_id
        WHERE h.chamado_id = %s
        ORDER BY h.data_acao DESC
    """

    cursor.execute(sql, (chamado_id,))
    comentarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return comentarios

def listar_chamados_encerrados():

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id,
            c.titulo,
            c.descricao,
            c.data_abertura,
            c.data_encerramento,

            p.nome AS prioridade,
            s.nome AS status,

            u.nome AS solicitante,

            t.nome AS tecnico

        FROM chamado c

        JOIN prioridade p
            ON p.id = c.prioridade_id

        JOIN status_chamado s
            ON s.id = c.status_id

        JOIN usuario u
            ON u.id = c.solicitante_id

        LEFT JOIN usuario t
            ON t.id = c.tecnico_id

        WHERE c.status_id = 3

        ORDER BY c.data_encerramento DESC
    """)

    chamados = cursor.fetchall()

    cursor.close()
    conexao.close()

    for chamado in chamados:

        if chamado["prioridade"] == "alta":
            sla_horas = 1

        elif chamado["prioridade"] == "media":
            sla_horas = 6

        else:
            sla_horas = 24
     
        tempo_total = chamado["data_encerramento"] - chamado["data_abertura"]

        sla_segundos = sla_horas * 3600

        if tempo_total.total_seconds() <= sla_segundos:
            chamado["sla_status"] = "NO PRAZO"
        else:
            chamado["sla_status"] = "EM ATRASO"

    return chamados