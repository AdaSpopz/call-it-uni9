from models.usuario import (
    buscar_usuario_por_login,
    criar_usuario
)

def obter_perfil_id_por_tipo(tipo):
    tipo = tipo.lower().strip()

    if tipo in ["usuário", "usuario"]:
        return 1
    elif tipo == "administrador":
        return 2
    elif tipo in ["técnico", "tecnico"]:
        return 3
    else:
        return None

def login(matricula, senha):
    return buscar_usuario_por_login(matricula, senha)

def criar(nome, matricula, email, senha, tipo):
    perfil_id = obter_perfil_id_por_tipo(tipo)

    if not perfil_id:
        return None

    return criar_usuario(nome, matricula, email, senha, perfil_id)