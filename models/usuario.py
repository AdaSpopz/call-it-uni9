from models.conexao import conectar


def buscar_usuario_por_login(matricula, senha):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            u.id,
            u.nome,
            u.matricula,
            u.email,
            u.senha,
            u.ativo,
            u.perfil_id,
            p.nome AS perfil
        FROM usuario u
        INNER JOIN perfil p ON p.id = u.perfil_id
        WHERE u.matricula = %s
          AND u.senha = %s
          AND u.ativo = TRUE
        LIMIT 1
    """

    cursor.execute(sql, (matricula, senha))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return usuario
def buscar_usuario_por_matricula(matricula):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT id, nome, matricula
        FROM usuario
        WHERE matricula = %s
        LIMIT 1
    """

    cursor.execute(sql, (matricula,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            u.id,
            u.nome,
            u.matricula,
            u.email,
            u.ativo,
            p.nome AS perfil
        FROM usuario u
        INNER JOIN perfil p ON p.id = u.perfil_id
        WHERE u.ativo = TRUE
        ORDER BY u.nome ASC
    """

    cursor.execute(sql)
    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()
    return usuarios

def buscar_usuario_por_id(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            u.id,
            u.nome,
            u.matricula,
            u.email,
            u.ativo,
            u.perfil_id,
            p.nome AS perfil
        FROM usuario u
        INNER JOIN perfil p ON p.id = u.perfil_id
        WHERE u.id = %s
        LIMIT 1
    """

    cursor.execute(sql, (usuario_id,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return usuario

def criar_usuario(nome, matricula, email, senha, perfil_id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO usuario (nome, matricula, email, senha, perfil_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, matricula, email, senha, perfil_id))
    conexao.commit()

    novo_id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return novo_id


def atualizar_usuario(usuario_id, nome, matricula, email, senha, perfil_id):
    conexao = conectar()
    cursor = conexao.cursor()

    if senha:
        sql = """
            UPDATE usuario
            SET nome = %s,
                matricula = %s,
                email = %s,
                senha = %s,
                perfil_id = %s
            WHERE id = %s
        """
        valores = (nome, matricula, email, senha, perfil_id, usuario_id)
    else:
        sql = """
            UPDATE usuario
            SET nome = %s,
                matricula = %s,
                email = %s,
                perfil_id = %s
            WHERE id = %s
        """
        valores = (nome, matricula, email, perfil_id, usuario_id)

    cursor.execute(sql, valores)
    conexao.commit()

    ok = cursor.rowcount > 0

    cursor.close()
    conexao.close()

    return ok


def excluir_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE usuario
        SET ativo = FALSE
        WHERE id = %s
    """

    cursor.execute(sql, (usuario_id,))
    conexao.commit()

    ok = cursor.rowcount > 0

    cursor.close()
    conexao.close()

    return ok