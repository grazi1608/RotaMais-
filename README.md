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

- **Controllers**: implementados como classes (`flask.views.MethodView`, e uma classe simples para autenticação), uma por recurso (`MotoristaController`, `VeiculoController`, `CorridaController`, `MetaController`, `RelatorioLucroController`, `AuthController`). Só traduzem request → chamada ao Service → response; não têm regra de negócio.
- **Services**: uma classe por caso de uso (ex.: `CriarMotorista`, `AtualizarVeiculo`, `ExcluirCorrida`, `GerarRelatorioLucro`, `RegistrarUsuario`, `AutenticarUsuario`), cada uma com um método `executar(...)`. Fazem as validações e coordenam a operação.
- **Models**: `Motorista`, `Veiculo`, `Corrida` e `Meta` herdam de `ModeloBase` (`db.Model`), que concentra as operações básicas de persistência: `salvar()`, `atualizar()`, `deletar()`, `listar_todos()`, `buscar_por_id()`.
- **Repository**: `RelatorioRepository` encapsula a única consulta especial do projeto — uma agregação (soma/agrupamento) de corridas por motorista para o relatório de lucro. CRUDs simples não usam Repository, conforme pedido no enunciado.
- **Autenticação**: login por token (`Authorization: Bearer <token>`), gerado em `/auth/login` ou `/auth/registrar` e armazenado no `localStorage` do frontend. Optamos por token em vez de sessão/cookie porque o frontend roda em outra origem (porta) que o backend — evita as regras frágeis de cookie cross-origin entre navegadores. As rotas de Veículo, Corrida, Meta, Gasto, Cofrinho e Relatório exigem token válido; o CRUD de Motoristas (`/motoristas`) permanece aberto por simplicidade nesta entrega. Gastos e Cofrinho sempre usam o motorista do token (`request.motorista_atual`), nunca um `motorista_id` enviado pelo cliente — evita que alguém manipule dados de outro motorista.
- Não há integração com IA/API externa nesta entrega, portanto não há chaves sensíveis a proteger; se isso mudar, usar variáveis de ambiente (`.env`).

## Princípios SOLID aplicados

- **S — Single Responsibility**: cada Service resolve um único caso de uso (`CriarGasto`, `GuardarDinheiroNoObjetivo`, `ExcluirCorrida`...); Controllers só traduzem HTTP ↔ Service; Models só sabem persistir a si mesmos.
- **O — Open/Closed**: novos casos de uso (ex.: "guardar dinheiro no cofrinho") viram uma nova classe de Service, sem alterar as classes existentes de CRUD.
- **L — Liskov Substitution**: todo Model herda de `ModeloBase` e pode ser usado por qualquer código que espere um `ModeloBase` (`salvar()`, `atualizar()`, `deletar()`, `listar_todos()`, `buscar_por_id()` funcionam igual para todos).
- **I — Interface Segregation**: cada Controller expõe só os métodos HTTP que faz sentido para aquele recurso (ex.: `Auth` não tem `delete`, `Relatório` só tem `get`), em vez de uma interface genérica única.
- **D — Dependency Inversion**: os Controllers dependem da "forma" dos Services (todos expõem `.executar(...)`), não dos detalhes internos de acesso a dados — quem fala com o banco é o Model (ou o Repository, nas consultas agregadas).

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
