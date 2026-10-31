# RotaMais

Sistema de gestão financeira para motoristas de aplicativo: cadastro de motoristas, veículos, registro de corridas, metas financeiras e relatório de lucratividade.

## Arquitetura

O projeto segue o fluxo obrigatório de ponta a ponta:

```
Interface/Tela → API Flask → Controller → Service → Model/Repository → Banco de Dados
```

Arquitetura cliente-servidor: são **dois servidores separados**.

```
Frontend (porta 5500)                          Backend / API (porta 5000)
HTML + CSS + JavaScript   --- fetch (JSON) --->  Flask → Controller → Service → Model/Repository → SQLite
python -m http.server 5500                     python backend/app.py
```

```
backend/
    app.py               # aplicação Flask (somente API JSON) + configuração do SQLAlchemy
    .env.example         # modelo do .env (SECRET_KEY etc.) — o .env real não vai para o Git
    schema.sql           # estrutura das tabelas, gerada a partir das Models (referência)
    controllers/          # Controllers (classes) — uma por recurso, herdam de BaseController
    services/              # Services (uma classe por caso de uso) + excecoes.py e validacoes.py
    models/                # Models (herdam de ModeloBase → db.Model): CRUD com ORM
    repositories/           # Repositories — consultas especiais em SQL escrito (SELECT, JOIN, GROUP BY...)
    utils/                 # login_required (token) e conversão de datas

frontend/
    index.html
    paginas/               # uma página HTML por recurso
    js/                    # um arquivo JS por página, consumindo a API
    css/
```

- **Controllers**: implementados como classes que herdam de `BaseController` (`flask.views.MethodView`), uma por recurso (`MotoristaController`, `VeiculoController`, `CorridaController`, `MetaController`, `GastoController`, `CofrinhoController`, `GuardarDinheiroController`, `RelatorioLucroController`, `AuthController`). Só recebem a requisição HTTP, interpretam o JSON, chamam o Service e devolvem a resposta (400 para dados inválidos, 404 para registro não encontrado); não têm regra de negócio.
- **Services**: uma classe por caso de uso (ex.: `CriarMotorista`, `AtualizarVeiculo`, `ExcluirCorrida`, `GuardarDinheiroNoObjetivo`, `GerarRelatorioLucro`, `RegistrarUsuario`, `AutenticarUsuario`), cada uma com um método `executar(...)`. Fazem as validações (campos obrigatórios, valores maiores que zero, datas coerentes, duplicidade de CPF/CNH/placa/e-mail) e coordenam a operação chamando a Model ou o Repository.
- **Models (CRUD com ORM)**: `Motorista`, `Veiculo`, `Corrida`, `Meta`, `Gasto` e `ObjetivoCofrinho` herdam de `ModeloBase`, que herda de `db.Model` (Flask-SQLAlchemy). O `ModeloBase` concentra as operações básicas de persistência: `salvar()`, `atualizar()`, `deletar()`, `listar_todos()`, `buscar_por_id()`. Os relacionamentos (`db.relationship`) definem a composição (cascade ao excluir) e a agregação (`Gasto` ↔ `Veiculo`).
- **Repositories (SQL escrito)**: guardam as consultas com filtro específico e os relatórios, escritas à mão em SQL (`SELECT ... WHERE`, `LEFT JOIN`, `GROUP BY`, `SUM`, `COALESCE`) e executadas por `BaseRepository` com parâmetros nomeados (`:cpf`), o que evita SQL injection: `MotoristaRepository` (busca por CPF, CNH, e-mail, telefone e token), `VeiculoRepository` (busca por placa), `GastoRepository` (gastos do motorista), `CofrinhoRepository` (objetivos do motorista e total guardado) e `RelatorioRepository` (lucro por motorista). O CRUD simples não usa Repository, conforme pedido no enunciado. Controllers e Services nunca escrevem SQL.
- **Banco de dados**: SQLite em `backend/instance/rotamais.db` (independente da pasta de onde o servidor é iniciado). As tabelas são criadas pelo `db.create_all()` a partir das Models ao iniciar a API; `backend/schema.sql` mostra a estrutura gerada.
- **Autenticação**: login por token (`Authorization: Bearer <token>`), gerado em `/auth/login` ou `/auth/registrar` e armazenado no `localStorage` do frontend. Optamos por token em vez de sessão/cookie porque o frontend roda em outro servidor (porta 5500) que a API (porta 5000) — evita as regras frágeis de cookie cross-origin entre navegadores. Todas as rotas, exceto `/auth/registrar` e `/auth/login`, exigem token válido. Gastos e Cofrinho sempre usam o motorista do token (`request.motorista_atual`), nunca um `motorista_id` enviado pelo cliente — evita que alguém manipule dados de outro motorista.
- **Informações sensíveis**: a `SECRET_KEY` do Flask é lida do arquivo `backend/.env` (variável de ambiente), que está no `.gitignore`. O repositório traz só o modelo `backend/.env.example`. Não há integração com IA/API externa nesta entrega.

## Princípios SOLID aplicados

- **S — Single Responsibility**: cada Service resolve um único caso de uso (`CriarGasto`, `GuardarDinheiroNoObjetivo`, `ExcluirCorrida`...); Controllers só traduzem HTTP ↔ Service; Models só sabem persistir a si mesmos.
- **O — Open/Closed**: novos casos de uso (ex.: "guardar dinheiro no cofrinho") viram uma nova classe de Service, sem alterar as classes existentes de CRUD.
- **L — Liskov Substitution**: todo Model herda de `ModeloBase` (que herda de `db.Model`) e pode ser usado por qualquer código que espere um `ModeloBase` (`salvar()`, `atualizar()`, `deletar()`, `listar_todos()`, `buscar_por_id()` funcionam igual para todos).
- **I — Interface Segregation**: cada Controller expõe só os métodos HTTP que faz sentido para aquele recurso (ex.: `Auth` não tem `delete`, `Relatório` só tem `get`), em vez de uma interface genérica única.
- **D — Dependency Inversion**: os Controllers dependem da "forma" dos Services (todos expõem `.executar(...)`), não dos detalhes internos de acesso a dados — quem fala com o banco é o Model (CRUD básico) ou o Repository (consultas com filtro e relatórios).

## Funcionalidades Implementadas

1. Cadastrar conta (com login automático)
2. Fazer login
3. Fazer logout
4. Cadastrar motorista
5. Listar motoristas
6. Editar motorista
7. Excluir motorista
8. Cadastrar veículo
9. Listar veículos
10. Editar veículo
11. Excluir veículo
12. Registrar corrida
13. Editar corrida
14. Excluir corrida
15. Cadastrar meta financeira
16. Listar metas
17. Editar meta
18. Excluir meta
19. Registrar gasto (combustível/manutenção/outro)
20. Listar gastos
21. Editar gasto
22. Excluir gasto
23. Criar objetivo de cofrinho
24. Listar objetivos de cofrinho (com total guardado)
25. Guardar dinheiro em um objetivo
26. Editar objetivo de cofrinho
27. Excluir objetivo de cofrinho
28. Relatório de lucro por motorista (consulta agregada via Repository)

Todas passam pelo fluxo completo Tela → API → Controller → Service → Model/Repository → Banco.

## Diagrama de classes

O diagrama de classes do domínio (Models, atributos, herança, composição e agregação) está em [`docs/diagrama-de-classes.md`](docs/diagrama-de-classes.md). O GitHub renderiza o diagrama direto na página.

## Tecnologias

- Python 3 + Flask (API REST em JSON)
- Flask-SQLAlchemy / SQLAlchemy: CRUD com ORM nas Models; conexão usada pelos Repositories para executar SQL escrito à mão
- SQLite
- Flask-CORS: o frontend (porta 5500) chama a API (porta 5000)
- Werkzeug (hash de senha) · python-dotenv (`.env`)
- HTML, CSS e JavaScript puro no frontend (`fetch`)

## Como rodar

São **dois processos**: a API (porta 5000) e o frontend (porta 5500).

### Configuração (uma vez)

Copie `backend/.env.example` para `backend/.env` e troque o valor de `SECRET_KEY` (sem o `.env` a API funciona, mas usa uma chave temporária e avisa no terminal).

### Opção 1 — Windows (um clique)

Dê dois cliques em `iniciar.bat` (na raiz do projeto). Ele instala as dependências, abre uma janela com a API (porta 5000), outra com o frontend (porta 5500) e abre o navegador em `http://127.0.0.1:5500`.

### Opção 2 — Pelo terminal (dois terminais, na raiz do projeto)

```bash
pip install -r requirements.txt
python backend/app.py                                     # terminal 1: API em http://127.0.0.1:5000
python -m http.server 5500 --directory frontend           # terminal 2: site em http://127.0.0.1:5500
```

Depois abra **http://127.0.0.1:5500** no navegador (também funciona com o Live Server do VS Code). O banco é sempre criado em `backend/instance/rotamais.db`.

- A API fica nas rotas `/auth`, `/motoristas`, `/veiculos`, `/corridas`, `/metas`, `/gastos`, `/cofrinho` e `/relatorios`. Um resumo está em `http://127.0.0.1:5000/`.
- Se aparecer "não foi possível falar com a API", a API não está rodando: confira o terminal/janela da porta 5000.
