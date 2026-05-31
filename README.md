# Call It - Frontend (HTML/CSS/JS)

Este repositório contém **apenas o frontend** do sistema Call It.
Toda a lógica de negócio (autenticação, banco de dados, SLA, permissões,
persistência) deve ser implementada por um **backend em Python** (Flask, FastAPI,
Django ou similar).

## Estrutura

```
.
├── index.html            # Redireciona para login.html
├── login.html            # Tela de login
├── chamados.html         # Lista de chamados em aberto
├── abrir-chamado.html    # Formulário para abrir novo chamado
├── detalhes.html         # Detalhes de um chamado (comentários, ações)
├── encerrados.html       # Lista de chamados encerrados (com SLA)
├── admin.html            # Painel administrativo (usuários + chamados)
├── css/
│   └── estilos.css       # Design system (cores, layout, componentes)
└── js/
    └── interacoes.js     # APENAS interações visuais (dropdowns, abas, modal)
```

## O que o JavaScript faz

O arquivo `js/interacoes.js` cuida **exclusivamente** de comportamento visual:

- Abrir/fechar dropdowns customizados (filtros e seletores).
- Marcar a opção selecionada e atualizar o rótulo + bolinha de cor.
- Atualizar o `<input type="hidden">` correspondente, para que o `<form>` envie
  o valor escolhido ao backend.
- Mostrar o botão **Salvar Status** quando o usuário muda o status no detalhe
  do chamado (antes de salvar, nada é alterado).
- Alternar entre as abas "Usuários" / "Chamados" no painel admin.
- Abrir/fechar o diálogo de novo/editar usuário e popular os campos.

## O que o JavaScript **NÃO** faz

- Não autentica usuários.
- Não acessa banco de dados.
- Não calcula SLA, prioridade, ou qualquer regra de negócio.
- Não usa `sessionStorage`/`localStorage` para guardar usuário ou chamados.
- Não gera HTML dinamicamente para listas de chamados/usuários — esse HTML
  precisa ser produzido pelo backend (templating Python: Jinja2, Django
  templates, etc.).

## Endpoints esperados do backend

Os formulários do frontend já estão configurados com os `action`/`method`
abaixo. Adapte conforme o framework Python escolhido:

| Página             | Método | Rota                               | Descrição                                     |
| ------------------ | ------ | ---------------------------------- | --------------------------------------------- |
| `login.html`       | POST   | `/login`                           | Autentica e cria sessão                       |
| qualquer página    | GET    | `/logout`                          | Encerra sessão e redireciona para login       |
| `abrir-chamado`    | POST   | `/chamados`                        | Cria novo chamado                             |
| `chamados.html`    | GET    | `/chamados?prioridade=&status=`    | Lista chamados ativos (filtragem server-side) |
| `encerrados.html`  | GET    | `/chamados/encerrados?sla=`        | Lista encerrados                              |
| `detalhes.html`    | GET    | `/chamados/<id>`                   | Detalhe do chamado                            |
| `detalhes.html`    | POST   | `/chamados/<id>/atribuir`          | Atribui chamado ao técnico atual              |
| `detalhes.html`    | POST   | `/chamados/<id>/status`            | Altera status                                 |
| `detalhes.html`    | POST   | `/chamados/<id>/encerrar`          | Encerra o chamado                             |
| `detalhes.html`    | POST   | `/chamados/<id>/comentarios`       | Adiciona comentário                           |
| `admin.html`       | POST   | `/usuarios`                        | Cria usuário                                  |
| `admin.html`       | POST   | `/usuarios/<id>`                   | Atualiza usuário                              |
| `admin.html`       | POST   | `/usuarios/<id>/remover`           | Remove usuário                                |

## Pontos de injeção no HTML (templating)

Procure pelos comentários `<!-- ... -->` em cada arquivo HTML — eles indicam
exatamente onde o backend deve renderizar dados do banco. Os atributos
`data-usuario-nome`, `data-usuario-tipo` no cabeçalho também devem ser
preenchidos pelo backend a partir da sessão atual.

Os dados visíveis hoje (Pedro Costa, Impressora offline, etc.) são apenas
**exemplos estáticos** para preview do design — devem ser substituídos por
loops de templating no backend.

## Design

O design segue o protótipo do Figma:
<https://cinch-lean-77314197.figma.site/>

Todas as cores, espaçamentos e componentes vivem em `css/estilos.css` e usam
variáveis CSS (`--turquesa`, `--alta`, `--media`, `--baixa`, etc.).
