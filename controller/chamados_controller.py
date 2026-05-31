from models.chamados import criar_chamado,  buscar_chamado_por_id, listar_chamados

def salvar_chamado(titulo, descricao, prioridade_id, motivo_id, solicitante_id):
    return criar_chamado(
        titulo,
        descricao,
        prioridade_id,
        motivo_id,
        solicitante_id
    )

def get_chamado(id):
    return buscar_chamado_por_id(id)

def get_chamados():
    return listar_chamados()