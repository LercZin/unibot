-- =========================================================================
-- UniBot — FAQ institucional
-- Cobre todas as categorias listadas na apresentação executiva (Fase 1):
-- notas, financeiro, histórico, declaração, calendário, renovação,
-- trancamento, login, estágio, TCC, diploma e secretaria.
--
-- Os links apontam para um portal fictício — troque pelos endereços
-- reais da instituição quando entrar em produção.
-- =========================================================================

USE unibot;

INSERT INTO faq_institucional (categoria, pergunta, resposta, palavras_chave, link) VALUES

-- ---------- NOTAS ----------
('notas',
 'Como vejo minhas notas?',
 'Você pode me perguntar diretamente aqui — por exemplo: *"como estou em POO?"*. Eu retorno suas notas, a média parcial e a situação na disciplina. Também é possível consultar no Portal do Aluno, em **Acadêmico → Notas**.',
 'notas ver consultar boletim como vejo',
 'https://portal.anhanguera.edu.br/academico/notas'),

('notas',
 'Onde fica meu boletim?',
 'O boletim oficial fica no Portal do Aluno, em **Acadêmico → Boletim**. Aqui no chat eu também posso te dar um resumo do desempenho por disciplina.',
 'boletim oficial impressao',
 'https://portal.anhanguera.edu.br/academico/boletim'),

('notas',
 'Quando saem as notas?',
 'As notas são lançadas pelos professores até **7 dias úteis após cada avaliação**. As notas finais do semestre saem até o último dia do calendário acadêmico. Posso te avisar quando uma nova nota for cadastrada — quer ativar?',
 'quando saem prazo lancamento notas',
 NULL),

('notas',
 'Fui aprovado ou reprovado?',
 'Para te dizer com precisão preciso que me informe a disciplina. Por exemplo: *"fui aprovado em estatística?"*. Eu calculo sua média ponderada e te dou a situação: **aprovado** (≥ 6,0), **em recuperação** (4,0–5,9) ou **em risco** (< 4,0).',
 'aprovado reprovado situacao final',
 NULL),

-- ---------- FINANCEIRO ----------
('financeiro',
 'Como emito um boleto?',
 'Para emitir seu boleto, acesse o Portal do Aluno em **Financeiro → 2ª via de boleto**. Selecione a mensalidade desejada e clique em *gerar boleto*. O PDF pode ser pago em qualquer banco até a data de vencimento.',
 'boleto emitir gerar segunda via 2a via',
 'https://portal.anhanguera.edu.br/financeiro/boletos'),

('financeiro',
 'Preciso da 2ª via da minha mensalidade',
 'A 2ª via fica em **Financeiro → 2ª via de boleto** no Portal do Aluno. Se o boleto estiver vencido há mais de 30 dias, entre em contato com o setor financeiro para receber um novo com juros recalculados.',
 'segunda via 2 via mensalidade boleto vencido',
 'https://portal.anhanguera.edu.br/financeiro/boletos'),

('financeiro',
 'Quando vence meu pagamento?',
 'O vencimento padrão é **todo dia 10** de cada mês. Você pode conferir a data exata do seu próximo boleto em **Financeiro → Próximos Vencimentos** no Portal do Aluno.',
 'vencimento data pagamento mensalidade quando',
 'https://portal.anhanguera.edu.br/financeiro/vencimentos'),

('financeiro',
 'Estou inadimplente, o que faço?',
 'Procure o **setor financeiro** assim que possível para negociar. Você pode: 1) Quitar os boletos em atraso pelo portal com juros recalculados; 2) Solicitar parcelamento; 3) Falar com a equipe pelo WhatsApp **(11) 1234-5678**. Pendências financeiras impedem a renovação de matrícula.',
 'inadimplente atraso pendencia negociar parcelar',
 'https://portal.anhanguera.edu.br/financeiro/negociacao'),

-- ---------- HISTÓRICO ----------
('historico',
 'Como pego meu histórico?',
 'Para solicitar o histórico escolar, acesse o Portal do Aluno em **Secretaria → Solicitar Documentos → Histórico Escolar**. O documento é emitido em até **5 dias úteis** e fica disponível para download no portal.',
 'historico escolar pegar solicitar',
 'https://portal.anhanguera.edu.br/secretaria/documentos'),

('historico',
 'Preciso do histórico escolar',
 'O histórico escolar pode ser solicitado no Portal do Aluno em **Secretaria → Solicitar Documentos**. Existem duas versões: simples (gratuita) e com assinatura digital (R$ 25). Prazo: 5 dias úteis.',
 'historico escolar preciso documento oficial',
 'https://portal.anhanguera.edu.br/secretaria/documentos'),

('historico',
 'Preciso de um documento das disciplinas cursadas',
 'O documento se chama **Histórico Escolar** e lista todas as disciplinas cursadas, notas, carga horária e situação. Solicite em **Secretaria → Solicitar Documentos → Histórico Escolar** no portal.',
 'disciplinas cursadas relacao documento',
 'https://portal.anhanguera.edu.br/secretaria/documentos'),

-- ---------- DECLARAÇÃO DE MATRÍCULA ----------
('declaracao_matricula',
 'Como emito declaração de matrícula?',
 'A declaração de matrícula é emitida **na hora e gratuitamente** no Portal do Aluno, em **Secretaria → Declarações → Declaração de Matrícula**. Já vem com assinatura digital válida.',
 'declaracao matricula emitir',
 'https://portal.anhanguera.edu.br/secretaria/declaracoes'),

('declaracao_matricula',
 'Preciso de comprovante de que estou matriculado',
 'Esse documento se chama **Declaração de Matrícula** e você emite na hora em **Secretaria → Declarações** no portal. Tem validade de 60 dias.',
 'comprovante matriculado declaracao matricula',
 'https://portal.anhanguera.edu.br/secretaria/declaracoes'),

('declaracao_matricula',
 'Declaração para o banco / INSS',
 'Para banco, INSS, plano de saúde ou outros órgãos use a **Declaração de Matrícula com finalidade específica**, disponível em **Secretaria → Declarações → Declaração com Finalidade**. Informe no formulário qual é o destinatário.',
 'declaracao banco inss finalidade especifica',
 'https://portal.anhanguera.edu.br/secretaria/declaracoes'),

-- ---------- CALENDÁRIO ----------
('calendario',
 'Quando começam as aulas?',
 'O semestre **2026.1** começou em **3 de fevereiro de 2026** e o **2026.2** está previsto para **3 de agosto de 2026**. Confira o calendário completo no portal.',
 'aulas comecar inicio semestre',
 'https://portal.anhanguera.edu.br/academico/calendario'),

('calendario',
 'Quais são as datas do semestre?',
 'Semestre **2026.1**: aulas de **03/02 a 28/06**, provas N1 de **14 a 19/04**, provas N2 de **09 a 14/06**, recuperação de **23 a 28/06**. O calendário completo está no portal.',
 'datas semestre cronograma calendario',
 'https://portal.anhanguera.edu.br/academico/calendario'),

('calendario',
 'Quando é o período de provas?',
 'N1 (primeira avaliação) de **14 a 19 de abril** e N2 (segunda avaliação) de **9 a 14 de junho**. A semana de **recuperação** vai de **23 a 28 de junho**. Veja seus prazos específicos perguntando *"quais meus próximos prazos?"*.',
 'provas periodo avaliacoes n1 n2',
 'https://portal.anhanguera.edu.br/academico/calendario'),

('calendario',
 'Quando são as férias?',
 'O recesso entre semestres vai de **29 de junho a 2 de agosto de 2026**. Há ainda o recesso de inverno em **20 a 24 de julho**.',
 'ferias recesso pausa entre semestres',
 'https://portal.anhanguera.edu.br/academico/calendario'),

-- ---------- RENOVAR MATRÍCULA ----------
('renovacao',
 'Como renovo minha matrícula?',
 'A renovação acontece em **Acadêmico → Rematrícula** no Portal do Aluno. Você escolhe as disciplinas, aceita o contrato e confirma. Não esqueça de estar em dia com o financeiro — pendências bloqueiam a rematrícula.',
 'renovar matricula rematricula renovacao',
 'https://portal.anhanguera.edu.br/academico/rematricula'),

('renovacao',
 'Período de rematrícula',
 'A rematrícula para **2026.2** abre em **15 de julho** e fecha em **2 de agosto**. Depois disso, novas matrículas só com taxa de regularização.',
 'periodo rematricula data prazo',
 'https://portal.anhanguera.edu.br/academico/rematricula'),

('renovacao',
 'Quero continuar no próximo semestre',
 'Que bom! Para continuar, basta fazer a rematrícula no período de **15/07 a 02/08** em **Acadêmico → Rematrícula** no portal. Se tiver dúvidas sobre as disciplinas a cursar, fale com a Coordenação do seu curso.',
 'continuar proximo semestre rematricula',
 'https://portal.anhanguera.edu.br/academico/rematricula'),

-- ---------- TRANCAMENTO ----------
('trancamento',
 'Quero trancar minha matrícula',
 'O trancamento é solicitado em **Acadêmico → Trancamento de Matrícula** no Portal do Aluno. Você fica afastado por um semestre (renovável até **4 vezes**). A solicitação só é aprovada se você estiver sem pendências financeiras.',
 'trancar trancamento matricula afastar',
 'https://portal.anhanguera.edu.br/academico/trancamento'),

('trancamento',
 'Como pausar meus estudos?',
 'A pausa formal é o **trancamento de matrícula**. Solicite em **Acadêmico → Trancamento** no portal. Durante o período trancado você não paga mensalidade nem acumula faltas.',
 'pausar estudos trancar afastamento',
 'https://portal.anhanguera.edu.br/academico/trancamento'),

('trancamento',
 'Posso me afastar por um semestre?',
 'Pode sim — é o **trancamento**, válido por **um semestre** e renovável até 4 vezes. Solicite em **Acadêmico → Trancamento** no portal. Se a ausência for por motivo de saúde, há trancamento extraordinário; envie o atestado pela secretaria.',
 'afastar um semestre licenca trancamento',
 'https://portal.anhanguera.edu.br/academico/trancamento'),

-- ---------- LOGIN / ACESSO ----------
('login',
 'Esqueci minha senha',
 'Na tela de login, clique em **"Esqueci minha senha"**. Você receberá um link de redefinição no e-mail cadastrado em até 5 minutos. Se não chegar, confira o spam ou fale com o suporte.',
 'esqueci senha redefinir recuperar',
 'https://portal.anhanguera.edu.br/conta/recuperar-senha'),

('login',
 'Não consigo acessar o portal',
 'Tente: 1) Clicar em **"Esqueci minha senha"** para resetar; 2) Limpar cookies do navegador; 3) Tentar em outro navegador. Se nada funcionar, acione o **suporte técnico** pelo e-mail **suporte@anhanguera.edu.br**.',
 'nao consigo acessar portal login problema',
 'https://portal.anhanguera.edu.br/conta/recuperar-senha'),

('login',
 'Minha conta está bloqueada',
 'Contas são bloqueadas após **5 tentativas erradas** de senha. O desbloqueio automático acontece em **30 minutos**. Para destravar antes, fale com o suporte em **suporte@anhanguera.edu.br** informando seu nome e matrícula.',
 'conta bloqueada bloqueio desbloquear',
 NULL),

('login',
 'Primeiro acesso ao sistema',
 'No primeiro acesso, use sua **matrícula** como usuário e **CPF (apenas números)** como senha. O sistema vai pedir para você cadastrar uma nova senha e um e-mail de recuperação.',
 'primeiro acesso inicial senha padrao',
 'https://portal.anhanguera.edu.br/conta/primeiro-acesso'),

-- ---------- ESTÁGIO ----------
('estagio',
 'Como faço para estagiar?',
 'Para iniciar um estágio, você precisa: 1) Ter cumprido pelo menos **40% da carga horária do curso**; 2) Encontrar uma vaga compatível; 3) Solicitar o **Termo de Compromisso de Estágio (TCE)** no setor de estágios. Acesse o portal de vagas para começar.',
 'estagio estagiar iniciar primeiro',
 'https://portal.anhanguera.edu.br/estagio'),

('estagio',
 'Onde assino o contrato de estágio?',
 'O **Termo de Compromisso de Estágio (TCE)** é assinado digitalmente pela DocuSign. O setor de estágios envia o link para o seu e-mail cadastrado depois que a empresa preenche a parte dela. Prazo de tramitação: 3 a 5 dias úteis.',
 'contrato termo compromisso estagio tce assinar',
 'https://portal.anhanguera.edu.br/estagio/contrato'),

('estagio',
 'Quais vagas de estágio existem?',
 'O **Portal de Vagas** lista oportunidades atualizadas por curso, área e cidade. Há também parcerias com a CIEE e o IEL. Acesse com seu login do portal.',
 'vagas estagio oportunidades portal',
 'https://portal.anhanguera.edu.br/estagio/vagas'),

-- ---------- TCC ----------
('tcc',
 'Preciso de informações sobre o TCC',
 'O TCC é obrigatório no penúltimo e último semestre. Etapas: 1) Escolha o tema e o orientador; 2) Cadastre o projeto na plataforma de TCC; 3) Submeta a monografia até a data limite; 4) Faça a defesa em banca. As normas estão no portal.',
 'tcc trabalho conclusao curso informacoes',
 'https://portal.anhanguera.edu.br/tcc'),

('tcc',
 'Como escolho meu orientador?',
 'Cada coordenação publica a lista de professores disponíveis no início do semestre. Você manda um e-mail apresentando seu tema e, se o professor aceitar, o vínculo é registrado em **Acadêmico → TCC → Vincular Orientador**.',
 'orientador tcc escolher professor',
 'https://portal.anhanguera.edu.br/tcc/orientadores'),

('tcc',
 'Normas da monografia',
 'A monografia segue as **normas ABNT**. O documento completo com modelo Word, capa oficial e regras de formatação está no portal de TCC. Resumo: fonte Times 12, espaço 1,5, margens 3/2/3/2, no mínimo 40 páginas.',
 'normas monografia abnt formatacao tcc',
 'https://portal.anhanguera.edu.br/tcc/normas'),

-- ---------- DIPLOMA ----------
('diploma',
 'Como solicito meu diploma?',
 'Após colar grau, o diploma é solicitado em **Secretaria → Diploma**. Você precisa de: histórico finalizado, ENADE realizado, quitação financeira e cópia autenticada do RG. Prazo de emissão: **90 a 180 dias** (registro no MEC).',
 'diploma solicitar pedir emitir',
 'https://portal.anhanguera.edu.br/secretaria/diploma'),

('diploma',
 'Quando é a colação de grau?',
 'A colação oficial acontece **em julho** (semestre 1) e **em janeiro** (semestre 2). A data exata da sua turma é divulgada pela coordenação cerca de **60 dias antes**. Há também colação em gabinete sob solicitação.',
 'colacao grau formatura data',
 'https://portal.anhanguera.edu.br/secretaria/colacao'),

('diploma',
 'Certificado de conclusão',
 'O **certificado de conclusão** é emitido após a colação de grau, enquanto o diploma definitivo (com registro MEC) não fica pronto. Ele tem validade legal e pode ser solicitado em **Secretaria → Certificados** no portal.',
 'certificado conclusao curso provisorio',
 'https://portal.anhanguera.edu.br/secretaria/certificados'),

-- ---------- SECRETARIA / ATENDIMENTO HUMANO ----------
('secretaria',
 'Quero falar com uma pessoa',
 'Claro! Você pode falar com a secretaria por: **WhatsApp (11) 1234-5678** (seg-sex 8h-21h, sáb 8h-12h), **e-mail secretaria@anhanguera.edu.br**, ou presencialmente no campus de **9h às 21h**. Quer que eu abra um chamado pra você?',
 'falar pessoa atendente humano secretaria atendimento',
 'https://portal.anhanguera.edu.br/atendimento'),

('secretaria',
 'Telefone da secretaria',
 'Os contatos da secretaria são: **WhatsApp (11) 1234-5678**, **telefone fixo (11) 4321-8765** e **e-mail secretaria@anhanguera.edu.br**. Horário: seg-sex 8h-21h, sáb 8h-12h.',
 'telefone secretaria contato whatsapp',
 NULL),

('secretaria',
 'Atendimento presencial',
 'A secretaria atende presencialmente no campus de **segunda a sexta das 9h às 21h** e **sábados das 9h às 12h**. Recomendo agendar antes pelo portal em **Secretaria → Agendar Atendimento**.',
 'presencial atendimento campus horario',
 'https://portal.anhanguera.edu.br/secretaria/agendar'),

('secretaria',
 'E-mail de contato',
 'Os e-mails oficiais são: **secretaria@anhanguera.edu.br** (geral), **financeiro@anhanguera.edu.br** (financeiro), **suporte@anhanguera.edu.br** (problemas no portal) e **coordenacao@anhanguera.edu.br** (coordenação do curso).',
 'email contato secretaria',
 NULL);
