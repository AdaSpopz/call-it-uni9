# imports
import os
from functools import wraps

from flask import Flask, render_template, request, redirect, session
from controller.usuario_controller import login
from controller.prioridades_controller import listar_prioridade
from controller.motivo_solicitacao_controller import listar_motivos
from controller.chamados_controller import criar_chamado
from models.usuario import listar_usuarios,criar_usuario,excluir_usuario,atualizar_usuario,buscar_usuario_por_id,buscar_usuario_por_matricula
from models.perfil import listar_perfil
from models.chamados import (
    listar_chamados,
    listar_chamados_encerrados,
    buscar_chamado_por_id,
    atualizar_chamado,
    encerrar_chamado,
    salvar_comentario,
    buscar_comentarios,
    
)
from models.chamados import buscar_comentarios
from datetime import datetime, timedelta
from flask import flash, redirect


# base do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'views'),
    static_folder=os.path.join(BASE_DIR, 'views'),
    static_url_path='/static'
)

app.secret_key = "amouni9"

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def fazer_login():
    matricula = request.form.get("matricula")
    senha = request.form.get("senha")

    usuario = login(matricula, senha)

    if usuario:
        session["usuario"] = {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "perfil": usuario["perfil"],
            "perfil_id": usuario["perfil_id"]
        }
        print(usuario)
        return redirect("/chamados")
    return render_template("login.html", erro="Usuário ou senha inválidos")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/chamados")
@login_required
def chamados():

    from datetime import datetime, timedelta

    usuario = session.get("usuario")

    prioridade_filtro = request.args.get("prioridade")
    status_filtro = request.args.get("status")

    chamados_filtrados = listar_chamados(prioridade_filtro, status_filtro)

    if usuario["perfil"] == "Usuário":
        chamados_filtrados = [
            chamado for chamado in chamados_filtrados
            if chamado["solicitante"] == usuario["nome"]
        ]

    total_chamados = len(chamados_filtrados)

    for chamado in chamados_filtrados:

        status = (chamado["status"] or "").strip().lower()
        prioridade = (chamado["prioridade"] or "").strip().lower()

        if prioridade == "alta":
            sla_total = timedelta(hours=1)
        elif prioridade == "média":
            sla_total = timedelta(hours=6)
        else:
            sla_total = timedelta(hours=24)

        prazo_final = chamado["data_abertura"] + sla_total
        agora = datetime.now()

        if status in ["encerrado", "encerrados"]:

            data_encerramento = chamado.get("data_encerramento")

            if not data_encerramento:
                chamado["sla_restante"] = "Encerrado"
                continue

            if data_encerramento <= prazo_final:
                chamado["sla_restante"] = "Atendido no Prazo"
            else:
                chamado["sla_restante"] = "Atendido Fora do Prazo"

            continue

        restante = prazo_final - agora

        if restante.total_seconds() <= 0:
            chamado["sla_restante"] = "ATRASADO"
        else:
            horas = int(restante.total_seconds() // 3600)
            minutos = int((restante.total_seconds() % 3600) // 60)

            chamado["sla_restante"] = (
                f"{horas}h {minutos}min" if horas > 0 else f"{minutos}min"
            )

    return render_template(
        "chamados.html",
        usuario=usuario,
        chamados=chamados_filtrados,
        usuario_tipo=usuario["perfil_id"],
        total_chamados=total_chamados
    )





@app.route("/abrir-chamado", methods=["GET", "POST"])
@login_required
def abrir_chamado():

    usuario = session.get("usuario")
    if usuario["perfil_id"] == 2 or usuario["perfil_id"] == 1:
        if request.method == "GET":
            prioridades = listar_prioridade()
            motivos = listar_motivos()

            return render_template(
                "abrir-chamado.html",
                usuario=usuario,
                prioridades=prioridades,
                motivos=motivos
            )

        if request.method == "POST":
            titulo = request.form["titulo"]
            descricao = request.form["descricao"]
            prioridade_id = request.form.get("prioridade")
            motivo_id = request.form.get("motivo")
            solicitante_id = session["usuario"]["id"]
            if not prioridade_id or not motivo_id:
                return "Campos obrigatórios não preenchidos", 400

            criar_chamado(
                titulo,
                descricao,
                prioridade_id,
                motivo_id,
                solicitante_id
            )

            return redirect("/chamados")
    else:
        return redirect("/chamados")
    
@app.route("/detalhes/<int:id>")
@login_required
def detalhes(id):

    usuario = session.get("usuario")

    chamado = buscar_chamado_por_id(id)

    # comentários
    chamado["comentarios"] = buscar_comentarios(id)
    chamado["qtd_comentarios"] = len(chamado["comentarios"])

    status = (chamado["status"] or "").strip().lower()
    prioridade = (chamado["prioridade"] or "").strip().lower()

    # remove acento (média → media)
    prioridade = prioridade.replace("média", "media")

    if prioridade == "alta":
        sla_total = timedelta(hours=1)
    elif prioridade == "media":
        sla_total = timedelta(hours=6)
    else:
        sla_total = timedelta(hours=24)

    sla_final = chamado["data_abertura"] + sla_total
    agora = datetime.now()

    chamado["sla_final"] = sla_final

    if status in ["encerrado", "encerrados"]:

        data_fechamento = chamado.get("data_encerramento")

        if not data_fechamento:
            chamado["sla_restante"] = "Encerrado"
            chamado["atrasado"] = False
        else:

            if data_fechamento <= sla_final:
                chamado["sla_restante"] = "SLA: Atendido no Prazo"
                chamado["atrasado"] = False
            else:
                chamado["sla_restante"] = "SLA: Atendido Fora do Prazo"
                chamado["atrasado"] = True
    else:

        chamado["atrasado"] = agora > sla_final

        if chamado["atrasado"]:
            chamado["sla_restante"] = "ATRASADO"
        else:

            restante = sla_final - agora

            horas = int(restante.total_seconds() // 3600)
            minutos = int((restante.total_seconds() % 3600) // 60)

            chamado["sla_restante"] = (
                f"{horas}h {minutos}min" if horas > 0 else f"{minutos}min"
            )

    return render_template(
        "detalhes.html",
        usuario=usuario,
        chamado=chamado
    )

@app.route("/encerrados")
@login_required
def encerrados():

    usuario = session.get("usuario")
    filtro_sla = request.args.get("sla", "todos")

    chamados = listar_chamados_encerrados()

    if usuario["perfil_id"] == 1:
        chamados = [
            c for c in chamados
            if c["solicitante"] == usuario["nome"]
        ]

    total = len(chamados)
    no_prazo = 0
    em_atraso = 0

    filtrados = []

    for c in chamados:
        # resto do seu código continua igual

        prioridade = (c.get("prioridade") or "").strip().lower()
        prioridade = prioridade.replace("média", "media")

        if prioridade == "alta":
            sla_total = timedelta(hours=1)
        elif prioridade == "media":
            sla_total = timedelta(hours=6)
        else:
            sla_total = timedelta(hours=24)

        data_abertura = c.get("data_abertura")
        data_encerramento = c.get("data_encerramento")

        if not data_abertura or not data_encerramento:
            continue

        sla_final = data_abertura + sla_total

        if data_encerramento <= sla_final:
            c["sla_status"] = "NO PRAZO"
            no_prazo += 1
        else:
            c["sla_status"] = "EM ATRASO"
            em_atraso += 1

        if filtro_sla == "no_prazo" and c["sla_status"] != "NO PRAZO":
            continue
        if filtro_sla == "em_atraso" and c["sla_status"] != "EM ATRASO":
            continue

        filtrados.append(c)

    # Mapear filtro para texto legível
    filtro_sla_label = {
        "todos": "Todos",
        "no_prazo": "No Prazo",
        "em_atraso": "Em Atraso"
    }.get(filtro_sla, "Todos")

    return render_template(
        "encerrados.html",
        usuario=usuario,
        chamados=filtrados,
        total=total,
        no_prazo=no_prazo,
        em_atraso=em_atraso,
        filtro_sla=filtro_sla,
        filtro_sla_label=filtro_sla_label
    )
@app.route("/administrar")
@login_required
def administrar():

    usuario = session.get("usuario")

    usuarios = listar_usuarios()

    total_tecnicos = sum(
        1 for u in usuarios
        if u["perfil"] == 'Técnico'
    )
    chamados = listar_chamados(
        prioridade=None,
        status=None
    )

    status_filtrado = ['aberto', 'em andamento']

    chamados_em_abertos = sum(
        1 for c in chamados
        if c["status"].strip().lower() in status_filtrado
    )


    chamados_encerrados = listar_chamados_encerrados()

    total_chamados = len(chamados) + len(chamados_encerrados)

    if usuario["perfil"] == 'Administrador':

        return render_template(
            "admin.html",
            usuario=usuario,
            usuarios=usuarios,
            total_tecnicos=total_tecnicos,
            chamados_em_abertos=chamados_em_abertos,
            total_chamados=total_chamados
        )

    else:
        return redirect("/chamados")
    

@app.route("/usuarios_listar")
@login_required
def usuarios_listar():
    usuario_logado = session.get("usuario")

    usuarios = listar_usuarios()
    print("Lista de usuários:", usuarios)

    return render_template("admin.html", usuario=usuario_logado, usuarios=usuarios)

@app.route("/gerenciar-chamados")
@login_required
def gerencia_chamados():

    usuario = session.get("usuario")

    usuarios = listar_usuarios()

    total_tecnicos = sum(
        1 for u in usuarios
        if u["perfil"] == 'Técnico'
    )
    chamados = listar_chamados(
        prioridade=None,
        status=None
    )

    status_filtrado = ['aberto', 'em andamento']

    chamados_em_abertos = sum(
        1 for c in chamados
        if c["status"].strip().lower() in status_filtrado
    )

    chamados_encerrados = listar_chamados_encerrados()

    total_chamados = len(chamados) + len(chamados_encerrados)

    todos_chamados = chamados + chamados_encerrados

    total_alta = sum(
        1 for c in todos_chamados
        if c["prioridade"].strip().lower() == 'alta'
    )

    total_media = sum(
        1 for c in todos_chamados
        if c["prioridade"].strip().lower() == 'média'
    )

    total_baixa = sum(
        1 for c in todos_chamados
        if c["prioridade"].strip().lower() == 'baixa'
    )

    if usuario["perfil"] == 'Administrador':

        return render_template(
            "gerenciar-chamados.html",
            usuario=usuario,
            usuarios=usuarios,
            total_tecnicos=total_tecnicos,
            chamados_em_abertos=chamados_em_abertos,
            total_chamados=total_chamados,
            total_alta=total_alta,
            total_media=total_media,
            total_baixa=total_baixa
        )

    else:
        return redirect("/chamados")
    
@app.route("/chamados/<int:id>/atribuir", methods=["POST"])
@login_required
def atribuir_chamado(id):

    usuario = session.get("usuario")

    atualizar_chamado(
        id,
        status_id=2,  
        tecnico_id=usuario["id"]
    )

    return redirect(f"/detalhes/{id}")

@app.route("/chamados/<int:id>/status", methods=["POST"])
@login_required
def alterar_status(id):

    status = request.form.get("status")

    mapa_status = {
        "Aberto": 1,
        "Em andamento": 2,
        "Encerrado": 3
    }

    status_id = mapa_status.get(status)

    atualizar_chamado(
        id,
        status_id=status_id
    )

    return redirect(f"/detalhes/{id}")


@app.route("/chamados/<int:id>/encerrar", methods=["POST"])
@login_required
def fechar_chamado(id):

    encerrar_chamado(id)

    return redirect("/encerrados")

@app.route("/chamados/<int:id>/comentarios", methods=["POST"])
@login_required
def adicionar_comentario(id):

    usuario = session.get("usuario")
    texto = request.form.get("conteudo")

    salvar_comentario(id, usuario["id"], texto)

    return redirect(f"/detalhes/{id}")

@app.route("/adicionar-usuario", methods=["GET", "POST"])
@login_required
def adicionar_usuario():
    usuario_logado = session.get("usuario")

    # somente administrador
    if usuario_logado["perfil_id"] != 2:
        return redirect("/chamados")

    perfis = listar_perfil()

    if request.method == "GET":
        usuario_id = request.args.get("id")  # se existir, modo editar
        usuario_editar = None
        modo = "novo"

        if usuario_id:
            usuario_editar = buscar_usuario_por_id(usuario_id)
            if usuario_editar:
                modo = "editar"
            else:
                flash("Usuário não encontrado.", "erro")
                return redirect("/administrar")

        return render_template(
            "adicionar-usuario.html",
            usuario=usuario_logado,
            perfis=perfis,
            modo=modo,
            usuario_editar=usuario_editar
        )

    usuario_id = request.form.get("usuario_id")  # hidden input opcional no HTML para edição
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    email = request.form.get("email")
    senha = request.form.get("senha")
    perfil_id = request.form.get("perfil_id")
   

    if not nome or not matricula or not perfil_id or (not senha and not usuario_id):
        flash("Preencha todos os campos obrigatórios!", "erro")
        return redirect(request.url)

    # valida matrícula duplicada
    usuario_existente = buscar_usuario_por_matricula(matricula)
    if usuario_existente:
        # se for edição, ignora se o ID é o mesmo
        if not usuario_id or int(usuario_id) != usuario_existente["id"]:
            flash("Já existe um usuário com essa matrícula!", "erro")
            return redirect(request.url)

    if usuario_id:  # modo editar
        atualizar_usuario(usuario_id, nome, matricula, email, senha, perfil_id)
        flash("Usuário atualizado com sucesso!", "sucesso")
    else:  # modo novo
        criar_usuario(nome, matricula, email, senha, perfil_id)
        flash("Usuário criado com sucesso!", "sucesso")

    return redirect("/administrar")


@app.route("/usuarios/<int:id>/remover", methods=["POST"])
@login_required
def remover_usuario(id):

    print("🔴 ROTA CHAMADA - ID:", id)

    sucesso = excluir_usuario(id)

    print("🔵 RESULTADO EXCLUIR:", sucesso)

    return redirect("/administrar", )

@app.route("/usuarios/<int:id>/editar", methods=["POST"])
@login_required
def atualizar_usuario_route(id):

    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    email = request.form.get("email")
    senha = request.form.get("senha")
    perfil_id = request.form.get("perfil_id")

    atualizar_usuario(id, nome, matricula, email, senha, perfil_id)

    # atualiza dados da sessão
    if session["usuario"]["id"] == id:

        session["usuario"]["nome"] = nome

        # atualiza perfil também
        if perfil_id == "1":
            session["usuario"]["perfil"] = "Usuário"
        elif perfil_id == "2":
            session["usuario"]["perfil"] = "Administrador"
        elif perfil_id == "3":
            session["usuario"]["perfil"] = "Técnico"

        session.modified = True

    return redirect("/administrar")