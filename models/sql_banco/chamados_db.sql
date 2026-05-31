CREATE TABLE perfil (
   id INT PRIMARY KEY AUTO_INCREMENT,
   nome VARCHAR(30) NOT NULL UNIQUE

);

INSERT INTO perfil (id , nome) VALUES
(1,'Usuário'),
(2,'Administrador'),
(3,'Técnico');


CREATE TABLE usuario ( 
   id INT PRIMARY KEY AUTO_INCREMENT,  
   nome VARCHAR(100) NOT NULL, 
   matricula VARCHAR(20) NOT NULL UNIQUE,
   email VARCHAR(100) NOT NULL UNIQUE,
   senha VARCHAR(255) NOT NULL, 
   ativo BOOLEAN NOT NULL DEFAULT TRUE,  
   perfil_id INT NOT NULL,
   data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (perfil_id) REFERENCES perfil(id) 
);

INSERT INTO usuario (nome, matricula, email, senha, perfil_id)
VALUES ('Joao', '123456', 'admin@email.com', 'admin123', 2);

INSERT INTO usuario (nome, matricula, email, senha, perfil_id)
VALUES ('Maria Clara', '151515', 'maria@gmail.com', '123456', 1);

INSERT INTO usuario (nome, matricula, email, senha, perfil_id)
VALUES ('Lilian', '808080', 'lilian@gmail.com', '123', 3);


CREATE TABLE prioridade ( 
   id INT PRIMARY KEY AUTO_INCREMENT,  
   nome VARCHAR(20) NOT NULL UNIQUE,
   sla_horas INT NOT NULL
); 

INSERT INTO prioridade (id,nome,sla_horas) VALUES
(1, 'Baixa', 24),
(2, 'Média', 6),
(3, 'Alta' ,1);



CREATE TABLE status_chamado ( 
   id INT PRIMARY KEY AUTO_INCREMENT,
   nome VARCHAR(30) NOT NULL UNIQUE
); 

INSERT INTO `status_chamado` (id,nome) VALUES 
(1, 'Aberto'), 
(2, 'Em andamento'), 
(3, 'Encerrados');



CREATE TABLE motivo_solicitacao ( 
   id INT PRIMARY KEY AUTO_INCREMENT,
   nome VARCHAR(50) NOT NULL UNIQUE
); 

INSERT INTO motivo_solicitacao (id, nome) VALUES
(1, 'Erro'),
(2, 'Acesso'),
(3, 'Solicitação'),
(4, 'Atualização'),
(5, 'Dúvida'),
(6, 'Outros');



CREATE TABLE chamado (
   id INT PRIMARY KEY AUTO_INCREMENT,
   titulo VARCHAR(150) NOT NULL,
   descricao TEXT NOT NULL,
   prioridade_id INT NOT NULL,
   motivo_id INT NOT NULL,
   status_id INT NOT NULL,
   solicitante_id INT NOT NULL,
   tecnico_id INT NULL,
   data_abertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   data_encerramento DATETIME NULL,
   ativo BOOLEAN NOT NULL DEFAULT TRUE,
   FOREIGN KEY (prioridade_id) REFERENCES prioridade(id),
   FOREIGN KEY (motivo_id) REFERENCES motivo_solicitacao(id),
   FOREIGN KEY (status_id) REFERENCES status_chamado(id),
   FOREIGN KEY (solicitante_id) REFERENCES usuario(id),
   FOREIGN KEY (tecnico_id) REFERENCES usuario(id)
);



CREATE TABLE historico_chamado (
   id INT PRIMARY KEY AUTO_INCREMENT,
   chamado_id INT NOT NULL,
   usuario_id INT NOT NULL,
   acao VARCHAR(255) NOT NULL,
   data_acao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (chamado_id) REFERENCES chamado(id),
   FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);
