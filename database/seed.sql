-- =========================================================================
-- UniBot — Dados de exemplo para desenvolvimento e demo.
-- Senha padrão de todos os usuários: "senha123" (hash bcrypt abaixo).
-- =========================================================================

USE unibot;

-- senha = "senha123"
SET @senha := '$2b$12$1u6HQAHAW0MUF4vPX.qbt.CD/kns7NHhf6KsA.7FHLdqOE/MX75Eu';

-- ----- Usuários -----
INSERT INTO usuario (id, nome, email, senha_hash, tipo) VALUES
  (1, 'Lucas Carvalho',  'lucas@unibot.edu.br',  @senha, 'estudante'),
  (2, 'Pedro Oliveira',  'pedro@unibot.edu.br',  @senha, 'estudante'),
  (3, 'Danilo Portela',  'danilo@unibot.edu.br', @senha, 'professor'),
  (4, 'Admin UniBot',    'admin@unibot.edu.br',  @senha, 'administrador');

INSERT INTO estudante (usuario_id, matricula, curso, semestre) VALUES
  (1, '2025001', 'Análise e Desenvolvimento de Sistemas', 4),
  (2, '2025002', 'Análise e Desenvolvimento de Sistemas', 4);

INSERT INTO professor (usuario_id, registro_docente, titulacao) VALUES
  (3, 'DOC-1234', 'Mestre');

INSERT INTO administrador (usuario_id, departamento) VALUES
  (4, 'TI');

-- ----- Disciplinas -----
INSERT INTO disciplina (id, codigo, nome, carga_horaria, ementa, professor_id) VALUES
  (1, 'POO2',  'Programação Orientada a Objetos II', 80,
   'Pilares da POO: encapsulamento, herança, polimorfismo, abstração. Padrões de projeto introdutórios.', 3),
  (2, 'CHAT',  'Chatbot',                            40,
   'Fundamentos de chatbots e PLN. Integração com LLMs.', 3),
  (3, 'BD2',   'Banco de Dados II',                  80,
   'Modelagem relacional avançada, índices, transações, normalização.', 3);

-- ----- Matrículas -----
INSERT INTO matricula (id, estudante_id, disciplina_id, periodo) VALUES
  (1, 1, 1, '2026.1'),
  (2, 1, 2, '2026.1'),
  (3, 1, 3, '2026.1'),
  (4, 2, 1, '2026.1'),
  (5, 2, 2, '2026.1');

-- ----- Prazos -----
INSERT INTO prazo (disciplina_id, titulo, descricao, tipo, data_entrega) VALUES
  (1, 'Entrega do projeto UniBot', 'Documentação + código no GitHub', 'projeto', '2026-06-15 23:59:00'),
  (1, 'Prova bimestral',           'Conteúdo: heranças e polimorfismo', 'prova',   '2026-05-28 19:00:00'),
  (2, 'Quiz de PLN',                'Tokenização, intenções e LLMs',     'atividade','2026-05-20 23:59:00'),
  (3, 'Trabalho de modelagem',      'DER + script SQL',                  'trabalho','2026-06-05 23:59:00');

-- ----- Materiais -----
INSERT INTO material (disciplina_id, titulo, tipo, url, descricao) VALUES
  (1, 'Herança em Python (vídeo)', 'video', 'https://example.com/heranca', 'Aula introdutória'),
  (1, 'Slides — Polimorfismo',     'slide', 'https://example.com/poli.pdf', ''),
  (2, 'Documentação do Claude',    'link',  'https://docs.anthropic.com',   'Referência oficial');

-- ----- Notas -----
INSERT INTO nota (matricula_id, tipo, valor, peso, data) VALUES
  (1, 'AV1', 8.0, 1.0, '2026-04-10'),
  (1, 'AV2', 7.5, 1.0, '2026-04-25'),
  (2, 'Quiz1', 9.0, 0.5, '2026-04-15');

-- ----- Base de conhecimento -----
INSERT INTO base_conhecimento (disciplina_id, topico, conteudo, metadados) VALUES
  (1, 'Herança',
   'Herança é o mecanismo pelo qual uma classe filha reaproveita atributos e métodos de uma classe pai, evitando duplicação de código.',
   JSON_OBJECT('palavras_chave', JSON_ARRAY('heranca','classe','subclasse'))),
  (1, 'Polimorfismo',
   'Polimorfismo permite que objetos de classes diferentes respondam ao mesmo método de formas distintas. Em Python, isso ocorre naturalmente via duck typing e via sobrescrita de métodos.',
   JSON_OBJECT('palavras_chave', JSON_ARRAY('polimorfismo','sobrescrita'))),
  (2, 'Intenção (NLU)',
   'A classificação de intenção identifica o objetivo do usuário em uma mensagem (ex: consultar nota, tirar dúvida). Pode ser feita por regras, modelos clássicos de ML ou LLMs.',
   JSON_OBJECT('palavras_chave', JSON_ARRAY('intencao','nlu','classificacao')));

-- ----- Conversa inicial de exemplo -----
INSERT INTO conversa (id, usuario_id, titulo) VALUES (1, 1, 'Boas-vindas');
INSERT INTO mensagem (conversa_id, remetente, texto, intencao) VALUES
  (1, 'bot', 'Olá, Lucas! Eu sou o UniBot. Posso te ajudar com dúvidas de conteúdo, prazos, notas e materiais. Como posso ajudar?', 'saudacao');
