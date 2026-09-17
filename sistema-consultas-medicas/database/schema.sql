-- =====================================================================
-- SISTEMA DE GERENCIAMENTO DE CONSULTAS MEDICAS
-- Script de criacao do banco de dados (MySQL)
-- Baseado na ERS: RF01-RF16 e RN01-RN12
-- =====================================================================

CREATE DATABASE IF NOT EXISTS clinica_consultas
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE clinica_consultas;

DROP TABLE IF EXISTS movimentacao;
DROP TABLE IF EXISTS exame;
DROP TABLE IF EXISTS consulta;
DROP TABLE IF EXISTS medico;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS usuario;

-- ---------------------------------------------------------------------
-- Tabela: usuario  (RF01, RF02, RF03 / RN01, RN02)
-- ---------------------------------------------------------------------
CREATE TABLE usuario (
    idUsuario     INT AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(150)    NOT NULL,
    email         VARCHAR(150)    NOT NULL UNIQUE,
    senha         VARCHAR(255)    NOT NULL,
    perfil        ENUM('ADMINISTRADOR','ATENDENTE','MEDICO','PACIENTE') NOT NULL,
    ativo         TINYINT(1)      NOT NULL DEFAULT 1,
    dataCadastro  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: paciente  (RF04, RF05, RF06 / RN03)
-- ---------------------------------------------------------------------
CREATE TABLE paciente (
    idPaciente      INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(150)  NOT NULL,
    cpf             VARCHAR(14)   NOT NULL UNIQUE,
    dataNascimento  DATE          NOT NULL,
    telefone        VARCHAR(20),
    email           VARCHAR(150),
    endereco        VARCHAR(255)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: medico  (RF07, RF08, RF09 / RN04)
-- ---------------------------------------------------------------------
CREATE TABLE medico (
    idMedico        INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(150)  NOT NULL,
    crm             VARCHAR(20)   NOT NULL UNIQUE,
    especialidade   VARCHAR(100)  NOT NULL,
    telefone        VARCHAR(20),
    email           VARCHAR(150),
    idUsuario       INT NULL,
    CONSTRAINT fk_medico_usuario FOREIGN KEY (idUsuario)
        REFERENCES usuario(idUsuario) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: consulta  (RF10, RF11, RF12, RF13 / RN05, RN06, RN07, RN08, RN09, RN10)
-- ---------------------------------------------------------------------
CREATE TABLE consulta (
    idConsulta    INT AUTO_INCREMENT PRIMARY KEY,
    dataConsulta  DATE  NOT NULL,
    horaConsulta  TIME  NOT NULL,
    status        ENUM('AGENDADA','REALIZADA','CANCELADA') NOT NULL DEFAULT 'AGENDADA',
    motivo        VARCHAR(255),
    observacoes   TEXT,
    idPaciente    INT NOT NULL,
    idMedico      INT NOT NULL,
    idUsuario     INT NULL,
    CONSTRAINT fk_consulta_paciente FOREIGN KEY (idPaciente)
        REFERENCES paciente(idPaciente) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_medico FOREIGN KEY (idMedico)
        REFERENCES medico(idMedico) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_usuario FOREIGN KEY (idUsuario)
        REFERENCES usuario(idUsuario) ON DELETE SET NULL ON UPDATE CASCADE,
    -- RN06: um medico nao pode ter duas consultas no mesmo dia/horario
    CONSTRAINT uq_medico_data_hora UNIQUE (idMedico, dataConsulta, horaConsulta)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: movimentacao  (Log de Movimentacoes / auditoria do sistema)
-- ---------------------------------------------------------------------
CREATE TABLE movimentacao (
    idMovimentacao  INT AUTO_INCREMENT PRIMARY KEY,
    tipo            ENUM('LOGIN','CADASTRO','ATUALIZACAO','AGENDAMENTO','CANCELAMENTO','EXCLUSAO')
                    NOT NULL,
    entidade        ENUM('SISTEMA','USUARIO','PACIENTE','MEDICO','CONSULTA','EXAME') NOT NULL,
    descricao       VARCHAR(255) NOT NULL,
    autor           VARCHAR(150) NOT NULL,
    idUsuario       INT NULL,
    dataHora        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mov_usuario FOREIGN KEY (idUsuario)
        REFERENCES usuario(idUsuario) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_mov_data ON movimentacao(dataHora DESC);
CREATE INDEX idx_mov_entidade ON movimentacao(entidade);

-- ---------------------------------------------------------------------
-- Tabela: exame  (RF14, RF15, RF16 / RN11, RN12)
-- ---------------------------------------------------------------------
CREATE TABLE exame (
    idExame          INT AUTO_INCREMENT PRIMARY KEY,
    nome             VARCHAR(150) NOT NULL,
    tipo             VARCHAR(100),
    dataSolicitacao  DATE NOT NULL DEFAULT (CURRENT_DATE),
    dataRealizacao   DATE NULL,
    resultado        TEXT NULL,
    observacoes      TEXT,
    status           ENUM('SOLICITADO','AGENDADO','REALIZADO','CANCELADO') NOT NULL DEFAULT 'SOLICITADO',
    idPaciente       INT NOT NULL,
    idMedico         INT NOT NULL,
    idConsulta       INT NULL,
    idUsuario        INT NULL,
    CONSTRAINT fk_exame_paciente FOREIGN KEY (idPaciente)
        REFERENCES paciente(idPaciente) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_exame_medico FOREIGN KEY (idMedico)
        REFERENCES medico(idMedico) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_exame_consulta FOREIGN KEY (idConsulta)
        REFERENCES consulta(idConsulta) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_exame_usuario FOREIGN KEY (idUsuario)
        REFERENCES usuario(idUsuario) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;
