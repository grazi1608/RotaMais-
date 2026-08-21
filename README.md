# RotaMais

Sistema de gestão financeira para motoristas de aplicativo: cadastro de motoristas, veículos, registro de corridas, metas financeiras e relatório de lucratividade.

## Arquitetura

O projeto segue o fluxo obrigatório de ponta a ponta:

```
Interface/Tela → API Flask → Controller → Service → Model/Repository → Banco de Dados
```

```
backend/
    app.py               # criação e configuração da aplicação Flask
    controllers/          # Controllers (classes MethodView) — uma por recurso
    services/              # Services (uma classe por caso de uso)
    models/                # Models (herdam de ModeloBase / db.Model)
    repositories/           # Repository — consultas agregadas/especiais

frontend/
    index.html
    paginas/               # uma página HTML por recurso
    js/                    # um arquivo JS por página, consumindo a API
    css/
```

- **Controllers**: implementados como classes (`flask.views.MethodView`), uma por recurso (`MotoristaController`, `VeiculoController`, `CorridaController`, `MetaController`, `RelatorioLucroController`). Só traduzem request → chamada ao Service → response; não têm regra de negócio.
- **Services**: uma classe por caso de uso (ex.: `CriarMotorista`, `AtualizarVeiculo`, `ExcluirCorrida`, `GerarRelatorioLucro`), cada uma com um método `executar(...)`. Fazem as validações e coordenam a operação.
- **Models**: `Motorista`, `Veiculo`, `Corrida` e `Meta` herdam de `ModeloBase` (`db.Model`), que concentra as operações básicas de persistência: `salvar()`, `atualizar()`, `deletar()`, `listar_todos()`, `buscar_por_id()`.
- **Repository**: `RelatorioRepository` encapsula a única consulta especial do projeto — uma agregação (soma/agrupamento) de corridas por motorista para o relatório de lucro. CRUDs simples não usam Repository, conforme pedido no enunciado.
- Não há integração com IA/API externa nesta entrega, portanto não há chaves sensíveis a proteger; se isso mudar, usar variáveis de ambiente (`.env`).

## Funcionalidades Implementadas

1. Cadastrar motorista
2. Listar motoristas
3. Editar motorista
4. Excluir motorista
5. Cadastrar veículo
6. Listar veículos
7. Editar veículo
8. Excluir veículo
9. Registrar corrida
10. Editar corrida
11. Excluir corrida
12. Cadastrar meta financeira
13. Listar metas
14. Editar meta
15. Excluir meta
16. Relatório de lucro por motorista (consulta agregada via Repository)

Todas passam pelo fluxo completo Tela → API → Controller → Service → Model/Repository → Banco.

## Como rodar

### Backend

```bash
cd backend
pip install -r ../requirements.txt
python app.py
```

A API sobe em `http://127.0.0.1:5000`.

### Frontend

Abra os arquivos de `frontend/` com um servidor estático (ex.: extensão "Live Server" do VS Code) e acesse `index.html`. O frontend consome a API em `http://127.0.0.1:5000`.
