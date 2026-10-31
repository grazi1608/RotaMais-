# Diagrama de classes do domínio

Diagrama das classes implementadas em `backend/models/` e dos relacionamentos entre elas.
As Models herdam de `ModeloBase`, que herda de `db.Model` (Flask-SQLAlchemy): o CRUD é feito com o ORM e os
relacionamentos são declarados com `db.relationship`. A estrutura das tabelas gerada a partir delas está em `backend/schema.sql`.
O GitHub renderiza o diagrama abaixo automaticamente (sintaxe Mermaid).

```mermaid
classDiagram
    direction TB

    class db_Model["db.Model"] {
        <<Flask-SQLAlchemy>>
    }

    class ModeloBase {
        <<abstract>>
        +int id
        +salvar() ModeloBase
        +atualizar(campos) ModeloBase
        +deletar() void
        +listar_todos()$
        +buscar_por_id(id)$
    }

    class Cadastro {
        <<mixin>>
        +datetime data_cadastro
        +registrar_data_cadastro() void
    }

    class Motorista {
        +str nome
        +str cpf
        +str cnh
        +str telefone
        +str email
        +date data_nascimento
        +str senha_hash
        +str token
        +definir_senha(senha) void
        +verificar_senha(senha) bool
        +gerar_token() str
        +revogar_token() void
        +to_dict() dict
    }

    class Veiculo {
        +str placa
        +str modelo
        +float consumo_por_km
        +int motorista_id
        +to_dict() dict
    }

    class Corrida {
        +datetime data_hora
        +float valor
        +float custo_estimado
        +float lucro
        +float distancia
        +int motorista_id
        +int veiculo_id
        +to_dict() dict
    }

    class Meta {
        +float valor_meta
        +date data_inicio
        +date data_fim
        +bool concluida
        +int motorista_id
        +to_dict() dict
    }

    class Gasto {
        +str tipo
        +str descricao
        +float valor
        +datetime data
        +int motorista_id
        +int veiculo_id
        +to_dict() dict
    }

    class ObjetivoCofrinho {
        +str nome
        +float valor_meta
        +float valor_guardado
        +int motorista_id
        +guardar(valor) void
        +progresso() int
        +calcular_progresso(valor_guardado, valor_meta)$ int
        +to_dict() dict
    }

    %% Herança
    db_Model <|-- ModeloBase
    ModeloBase <|-- Motorista
    ModeloBase <|-- Veiculo
    ModeloBase <|-- Corrida
    ModeloBase <|-- Meta
    ModeloBase <|-- Gasto
    ModeloBase <|-- ObjetivoCofrinho
    Cadastro <|-- Motorista

    %% Composição (db.relationship com cascade="all, delete-orphan" + ON DELETE CASCADE: apagar o pai apaga os filhos)
    Motorista "1" *-- "0..*" Veiculo : possui
    Motorista "1" *-- "0..*" Corrida : realiza
    Motorista "1" *-- "0..*" Meta : define
    Motorista "1" *-- "0..*" Gasto : registra
    Motorista "1" *-- "0..*" ObjetivoCofrinho : guarda para
    Veiculo "1" *-- "0..*" Corrida : usado em

    %% Agregação (referência opcional: ON DELETE SET NULL)
    Veiculo "0..1" o-- "0..*" Gasto : associado a
```

## Legenda dos relacionamentos

| Relacionamento | Tipo | Observação |
|---|---|---|
| `Motorista` → `Veiculo`, `Corrida`, `Meta`, `Gasto`, `ObjetivoCofrinho` | Composição (1 para N) | `db.relationship(..., cascade="all, delete-orphan")` em `Motorista` e chave estrangeira com `ON DELETE CASCADE`: ao excluir o motorista, seus registros são excluídos. |
| `Veiculo` → `Corrida` | Composição (1 para N) | `Veiculo.corridas` com `cascade="all, delete-orphan"` e `ON DELETE CASCADE`: ao excluir o veículo, suas corridas são excluídas. |
| `Veiculo` → `Gasto` | Agregação (0..1 para N) | `Gasto.veiculo_id` é opcional e o relacionamento `Veiculo.gastos` não tem cascade de exclusão (chave estrangeira `ON DELETE SET NULL`): ao excluir o veículo, o gasto continua existindo sem veículo. |
| `ModeloBase` → todos os Models | Herança | Classe base abstrata (`__abstract__ = True`, herda de `db.Model`, não vira tabela) com o `id` e o CRUD feito com o ORM (`salvar`, `atualizar`, `deletar`, `listar_todos`, `buscar_por_id`). |
| `Cadastro` → `Motorista` | Herança (mixin) | Acrescenta o campo `data_cadastro` (preenchido por `registrar_data_cadastro()`). Não é tabela própria; a coluna fica na tabela `motoristas`. |

## Onde cada classe está no código

| Classe | Arquivo |
|---|---|
| `ModeloBase` | `backend/models/base.py` |
| `Cadastro` | `backend/models/cadastro.py` |
| `Motorista` | `backend/models/motorista.py` |
| `Veiculo` | `backend/models/veiculo.py` |
| `Corrida` | `backend/models/corrida.py` |
| `Meta` | `backend/models/meta.py` |
| `Gasto` | `backend/models/gasto.py` |
| `ObjetivoCofrinho` | `backend/models/objetivo_cofrinho.py` |
