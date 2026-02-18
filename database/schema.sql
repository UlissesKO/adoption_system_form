-- script de criação e migração do banco de dados

CREATE DATABASE tocadospeludos;

USE DATABASE tocadospeludos;



CREATE TABLE adotantes (
    id INTEGER PRIMARY KEY auto_increment,
    nome VARCHAR(50) NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    telefone VARCHAR(50),
    endereco TEXT,
    ambiente TEXT -- casa, apartamento, quintal etc.
);


CREATE TABLE pets (
    id INTEGER PRIMARY KEY auto_increment,
    nome VARCHAR(50) NOT NULL,
    idade INTEGER,
    especie TEXT,
    foto TEXT -- caminho da imagem
);
-- definição das tabelas CRUD