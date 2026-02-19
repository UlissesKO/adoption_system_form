-- script de criação e migração do banco de dados

CREATE DATABASE tocadospeludos;

USE DATABASE tocadospeludos;


-- DADOS DOS ADOTANTES NO PAINEL 
CREATE TABLE adotantes (
    id_adotante INTEGER PRIMARY KEY auto_increment,
    nome VARCHAR(50) NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    telefone VARCHAR(50),
    endereco TEXT,
    ambiente TEXT -- casa, apartamento, quintal etc.
);

-- METADADOS TELA PREFERENCIAS (DADOS DOS ANIMAIS NAS OPCOES DE SELECAO)
CREATE TABLE pets(
    id_pet INT auto_increment PRIMARY KEY,
    animal VARCHAR(20) NOT NULL,
    sexo CHAR(1),
    idade INT,
    raca VARCHAR(50) NOT NULL
);

-- TELA PREFERENCIAS
CREATE TABLE adocoes (
    id_adotante INT,
    id_pet INT,
    FOREIGN KEY (id_adotante) REFERENCES adotantes(id_adotante),
    FOREIGN KEY (id_pet) REFERENCES pets(id_pet)
);



INSERT INTO pets (animal, sexo, idade, raca) VALUES
('Cachorro', 'M', 3, 'Labrador'),
('Cachorro', 'F', 2, 'Poodle'),
('Cachorro', 'M', 5, 'Bulldog'),
('Cachorro', 'F', 1, 'Beagle'),
('Cachorro', 'M', 4, 'Pastor Alemão'),
('Cachorro', 'F', 6, 'Golden Retriever'),
('Cachorro', 'M', 2, 'Shih Tzu'),
('Cachorro', 'F', 3, 'Yorkshire'),
('Cachorro', 'M', 7, 'Boxer'),
('Cachorro', 'F', 4, 'Dálmata'),

('Gato', 'M', 2, 'Siamês'),
('Gato', 'F', 1, 'Persa'),
('Gato', 'M', 3, 'Maine Coon'),
('Gato', 'F', 4, 'Angorá'),
('Gato', 'M', 5, 'Bengal'),
('Gato', 'F', 2, 'Sphynx'),
('Gato', 'M', 6, 'British Shorthair'),
('Gato', 'F', 3, 'Ragdoll'),
('Gato', 'M', 1, 'Scottish Fold'),
('Gato', 'F', 7, 'Norueguês da Floresta');



-- definição das tabelas CRUD