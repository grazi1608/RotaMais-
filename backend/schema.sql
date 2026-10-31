-- Estrutura do banco do RotaMais (SQLite), gerada a partir das Models (backend/models/).
-- Arquivo de referência/documentação: as tabelas são criadas automaticamente pelo
-- db.create_all() ao iniciar a API (backend/app.py). Rodar de novo não apaga dados.

CREATE TABLE IF NOT EXISTS motoristas (
	nome VARCHAR(120) NOT NULL,
	cpf VARCHAR(20) NOT NULL,
	cnh VARCHAR(20) NOT NULL,
	telefone VARCHAR(20),
	email VARCHAR(120),
	data_nascimento DATE,
	senha_hash VARCHAR(255),
	token VARCHAR(64),
	data_cadastro DATETIME NOT NULL,
	id INTEGER NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (cpf),
	UNIQUE (cnh),
	UNIQUE (email),
	UNIQUE (token)
);

CREATE TABLE IF NOT EXISTS metas (
	valor_meta FLOAT NOT NULL,
	data_inicio DATE NOT NULL,
	data_fim DATE NOT NULL,
	concluida BOOLEAN NOT NULL,
	motorista_id INTEGER NOT NULL,
	id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(motorista_id) REFERENCES motoristas (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS objetivos_cofrinho (
	nome VARCHAR(120) NOT NULL,
	valor_meta FLOAT NOT NULL,
	valor_guardado FLOAT NOT NULL,
	motorista_id INTEGER NOT NULL,
	id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(motorista_id) REFERENCES motoristas (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS veiculos (
	placa VARCHAR(10) NOT NULL,
	modelo VARCHAR(100) NOT NULL,
	consumo_por_km FLOAT NOT NULL,
	motorista_id INTEGER NOT NULL,
	id INTEGER NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (placa),
	FOREIGN KEY(motorista_id) REFERENCES motoristas (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS corridas (
	data_hora DATETIME NOT NULL,
	valor FLOAT NOT NULL,
	custo_estimado FLOAT NOT NULL,
	lucro FLOAT NOT NULL,
	distancia FLOAT NOT NULL,
	motorista_id INTEGER NOT NULL,
	veiculo_id INTEGER NOT NULL,
	id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(motorista_id) REFERENCES motoristas (id) ON DELETE CASCADE,
	FOREIGN KEY(veiculo_id) REFERENCES veiculos (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gastos (
	tipo VARCHAR(20) NOT NULL,
	descricao VARCHAR(255),
	valor FLOAT NOT NULL,
	data DATETIME NOT NULL,
	motorista_id INTEGER NOT NULL,
	veiculo_id INTEGER,
	id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(motorista_id) REFERENCES motoristas (id) ON DELETE CASCADE,
	FOREIGN KEY(veiculo_id) REFERENCES veiculos (id) ON DELETE SET NULL
);
