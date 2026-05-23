-- =========================================================================
-- UniBot — Schema MySQL 8.0
-- Modelo lógico do DER (12 tabelas) baseado na documentação do projeto.
-- =========================================================================

DROP DATABASE IF EXISTS unibot;
CREATE DATABASE unibot
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE unibot;

-- -------------------------------------------------------------------------
-- 1) usuario  — atributos comuns a todos os perfis
-- -------------------------------------------------------------------------
CREATE TABLE usuario (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  nome           VARCHAR(120)  NOT NULL,
  email          VARCHAR(160)  NOT NULL UNIQUE,
  senha_hash     VARCHAR(255)  NOT NULL,
  tipo           ENUM('estudante','professor','administrador') NOT NULL,
  data_cadastro  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ativo          TINYINT(1)    NOT NULL DEFAULT 1,
  INDEX idx_usuario_tipo (tipo)
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 2) estudante  — especialização (1:1 com usuario)
-- -------------------------------------------------------------------------
CREATE TABLE estudante (
  usuario_id  INT          PRIMARY KEY,
  matricula   VARCHAR(20)  NOT NULL UNIQUE,
  curso       VARCHAR(80)  NOT NULL,
  semestre    TINYINT      NOT NULL DEFAULT 1,
  CONSTRAINT fk_estudante_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 3) professor  — especialização (1:1 com usuario)
-- -------------------------------------------------------------------------
CREATE TABLE professor (
  usuario_id        INT          PRIMARY KEY,
  registro_docente  VARCHAR(40)  NOT NULL UNIQUE,
  titulacao         VARCHAR(60)  NOT NULL,
  CONSTRAINT fk_professor_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 4) administrador  — especialização (1:1 com usuario)
-- -------------------------------------------------------------------------
CREATE TABLE administrador (
  usuario_id    INT          PRIMARY KEY,
  departamento  VARCHAR(60)  NOT NULL DEFAULT 'TI',
  CONSTRAINT fk_admin_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 5) disciplina
-- -------------------------------------------------------------------------
CREATE TABLE disciplina (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  codigo         VARCHAR(20)  NOT NULL UNIQUE,
  nome           VARCHAR(120) NOT NULL,
  carga_horaria  SMALLINT     NOT NULL,
  ementa         TEXT,
  professor_id   INT,
  CONSTRAINT fk_disciplina_professor
    FOREIGN KEY (professor_id) REFERENCES professor(usuario_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 6) matricula  — N:N entre estudante e disciplina
-- -------------------------------------------------------------------------
CREATE TABLE matricula (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  estudante_id    INT          NOT NULL,
  disciplina_id   INT          NOT NULL,
  periodo         VARCHAR(10)  NOT NULL,
  status          ENUM('ativa','trancada','concluida','cancelada') NOT NULL DEFAULT 'ativa',
  data_matricula  DATE         NOT NULL DEFAULT (CURRENT_DATE),
  UNIQUE KEY uq_matricula (estudante_id, disciplina_id, periodo),
  CONSTRAINT fk_matricula_estudante
    FOREIGN KEY (estudante_id) REFERENCES estudante(usuario_id) ON DELETE CASCADE,
  CONSTRAINT fk_matricula_disciplina
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 7) prazo
-- -------------------------------------------------------------------------
CREATE TABLE prazo (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  disciplina_id  INT          NOT NULL,
  titulo         VARCHAR(160) NOT NULL,
  descricao      TEXT,
  tipo           ENUM('prova','trabalho','atividade','projeto') NOT NULL,
  data_entrega   DATETIME     NOT NULL,
  INDEX idx_prazo_data (data_entrega),
  CONSTRAINT fk_prazo_disciplina
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 8) material
-- -------------------------------------------------------------------------
CREATE TABLE material (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  disciplina_id  INT          NOT NULL,
  titulo         VARCHAR(160) NOT NULL,
  tipo           ENUM('video','pdf','artigo','link','slide') NOT NULL,
  url            VARCHAR(500) NOT NULL,
  descricao      TEXT,
  CONSTRAINT fk_material_disciplina
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 9) nota
-- -------------------------------------------------------------------------
CREATE TABLE nota (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  matricula_id  INT           NOT NULL,
  tipo          VARCHAR(40)   NOT NULL,
  valor         DECIMAL(5,2)  NOT NULL,
  peso          DECIMAL(4,2)  NOT NULL DEFAULT 1.00,
  data          DATE          NOT NULL,
  CONSTRAINT fk_nota_matricula
    FOREIGN KEY (matricula_id) REFERENCES matricula(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 10) conversa
-- -------------------------------------------------------------------------
CREATE TABLE conversa (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id    INT          NOT NULL,
  titulo        VARCHAR(160) NOT NULL DEFAULT 'Conversa',
  data_inicio   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_conversa_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 11) mensagem
-- -------------------------------------------------------------------------
CREATE TABLE mensagem (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  conversa_id    INT        NOT NULL,
  remetente      ENUM('usuario','bot') NOT NULL,
  texto          TEXT       NOT NULL,
  intencao       VARCHAR(40),
  tokens_usados  INT        NOT NULL DEFAULT 0,
  data_envio     TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mensagem_conversa_data (conversa_id, data_envio),
  CONSTRAINT fk_mensagem_conversa
    FOREIGN KEY (conversa_id) REFERENCES conversa(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 12) base_conhecimento  — conteúdo didático ligado à disciplina (RF05)
-- -------------------------------------------------------------------------
CREATE TABLE base_conhecimento (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  disciplina_id  INT          NOT NULL,
  topico         VARCHAR(160) NOT NULL,
  conteudo       TEXT         NOT NULL,
  metadados      JSON,
  FULLTEXT KEY ft_bc (topico, conteudo),
  CONSTRAINT fk_bc_disciplina
    FOREIGN KEY (disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 13) faq_institucional  — perguntas administrativas/processuais
-- Resposta determinística sem chamar a LLM — atende RNF01 (latência) e
-- RNF10 (confiabilidade) para fluxos previsíveis (financeiro, documentos,
-- calendário, etc.).
-- -------------------------------------------------------------------------
CREATE TABLE faq_institucional (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  categoria       ENUM(
    'notas','financeiro','historico','declaracao_matricula',
    'calendario','renovacao','trancamento','login','estagio',
    'tcc','diploma','secretaria'
  ) NOT NULL,
  pergunta        VARCHAR(300) NOT NULL,
  resposta        TEXT         NOT NULL,
  palavras_chave  VARCHAR(400),
  link            VARCHAR(500),
  ativo           TINYINT(1)   NOT NULL DEFAULT 1,
  FULLTEXT KEY ft_faq (pergunta, resposta, palavras_chave),
  INDEX idx_faq_categoria (categoria)
) ENGINE=InnoDB;
