from models.motivo_solicitacao import listar_motivos, buscar_motivos_por_id

def listar_prioridades():
    return listar_motivos()

def buscar_prioridade(id):
    return buscar_motivos_por_id(id)