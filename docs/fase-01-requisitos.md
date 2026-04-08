# Fase 1 - Entendimento de Requisitos

## 1. Objetivo do documento

Este documento registra o entendimento inicial do projeto `RegistroEscolar`, uma plataforma SaaS de matricula online para multiplas escolas.

O objetivo desta fase e transformar uma ideia de produto em requisitos claros, rastreaveis e tecnicamente utilizaveis. Em engenharia de software, isso e fundamental porque:

- reduz ambiguidade antes da implementacao;
- melhora a comunicacao entre negocio e tecnologia;
- evita alto acoplamento causado por decisoes precipitadas;
- cria uma base para arquitetura, testes e documentacao futura.

## 2. Visao do produto

O sistema deve permitir que escolas configurem formularios de matricula online, publiquem links publicos por periodo letivo e recebam inscricoes de responsaveis sem exigir login do usuario final.

O produto tem dois contextos principais:

1. Painel administrativo autenticado:
   - gestao de escolas, periodos, turmas, formularios e links publicos;
   - acompanhamento das matriculas;
   - auditoria e operacao.

2. Fluxo publico de matricula:
   - acesso por link seguro;
   - preenchimento de formulario dinamico;
   - upload de documentos;
   - confirmacao sujeita a validacoes e disponibilidade de vagas.

## 3. Problema de negocio

Processos de matricula escolar costumam ser manuais, fragmentados e pouco auditaveis. Isso gera:

- retrabalho operacional;
- erros de preenchimento;
- dificuldade para controlar vagas em tempo real;
- baixa rastreabilidade de alteracoes;
- risco de perda de historico do formulario e dos documentos enviados.

## 4. Proposta de valor

Centralizar o processo de matricula em uma plataforma unica, com foco em:

- escalabilidade multi-escola;
- controle confiavel de vagas;
- formularios dinamicos versionados;
- seguranca de dados;
- operacao futura em Linux local e servidor Linux.

## 5. Premissas iniciais

As premissas abaixo foram inferidas a partir das tasks existentes no repositorio e devem ser confirmadas ao longo do discovery:

- o backend principal sera desenvolvido em Python;
- o sistema rodara localmente no WSL Ubuntu durante o desenvolvimento;
- o ambiente futuro de hospedagem tambem sera Linux;
- o produto sera multi-tenant, isto e, uma mesma aplicacao atendera multiplas escolas com isolamento logico;
- existira um painel administrativo e um fluxo publico sem login;
- a persistencia precisara suportar consistencia forte no controle de vagas.

## 6. Stakeholders e atores

### Stakeholders

- Dono do produto: define regras de negocio e prioridades.
- Escola cliente: utiliza o sistema para configurar e operar matriculas.
- Time tecnico: implementa, testa, monitora e mantem o produto.
- Responsavel pelo aluno: preenche a matricula publica.

### Atores do sistema

- `superadmin`: administra a plataforma de forma global.
- `admin_escola`: gerencia configuracoes da propria escola.
- `operador_matricula`: acompanha inscricoes e validacoes.
- `auditor`: consulta trilhas e eventos, sem permissao operacional ampla.
- `responsavel`: usuario externo que realiza a inscricao pelo link publico.

## 7. User stories iniciais

### Administracao

1. Como `admin_escola`, quero cadastrar ou configurar periodos letivos para organizar campanhas de matricula.
2. Como `admin_escola`, quero criar turmas com capacidade maxima para controlar vagas por turma.
3. Como `admin_escola`, quero montar formularios dinamicos para adaptar a matricula as necessidades da escola.
4. Como `admin_escola`, quero publicar uma versao imutavel do formulario para garantir consistencia historica.
5. Como `admin_escola`, quero gerar um link publico seguro para compartilhar a matricula com responsaveis.
6. Como `operador_matricula`, quero consultar inscricoes recebidas para analisar o andamento do processo.
7. Como `auditor`, quero ver quem alterou formulario, turmas e vagas para garantir rastreabilidade.

### Fluxo publico

8. Como `responsavel`, quero acessar um link publico e preencher a matricula sem precisar criar conta.
9. Como `responsavel`, quero enviar documentos exigidos para concluir a inscricao.
10. Como `responsavel`, quero receber um protocolo ao final para acompanhar minha solicitacao.

### Regras criticas

11. Como sistema, preciso impedir confirmacao de matricula quando nao houver mais vagas.
12. Como sistema, preciso validar campos obrigatorios no backend para nao depender apenas do frontend.
13. Como sistema, preciso vincular cada inscricao a versao exata do formulario publicado.

## 8. Requisitos funcionais iniciais

### RF01 - Gestao de escolas e contexto
- O sistema deve suportar multiplas escolas.
- Cada escola deve possuir dados e configuracoes isoladas logicamente.

### RF02 - Gestao de periodos letivos
- O sistema deve permitir criar, editar e ativar periodos letivos por escola.

### RF03 - Gestao de turmas
- O sistema deve permitir criar turmas com nome, turno e capacidade maxima.
- O sistema deve controlar a quantidade de matriculas confirmadas por turma.

### RF04 - Formularios dinamicos
- O sistema deve permitir criar formularios com campos configuraveis.
- Campos devem suportar tipos como texto, data, email, telefone, selecao e upload.
- O sistema deve versionar formularios publicados.

### RF05 - Publicacao de links
- O sistema deve gerar links publicos seguros associados a escola, periodo e versao do formulario.
- O sistema deve permitir definir status e validade do link.

### RF06 - Fluxo de matricula publica
- O sistema deve exibir o formulario publicado a partir do link publico.
- O sistema deve receber dados preenchidos pelo responsavel.
- O sistema deve permitir envio de documentos.
- O sistema deve retornar protocolo da solicitacao.

### RF07 - Validacao e estados
- O sistema deve validar obrigatoriedade, formato e regras de negocio no backend.
- O sistema deve manter estados de matricula como `draft`, `submitted`, `pending_validation`, `confirmed`, `rejected`, `waitlisted` e `cancelled`.

### RF08 - Controle de vagas
- O sistema deve confirmar matricula apenas se houver vaga disponivel no momento da transacao.
- O sistema deve bloquear concorrencia para evitar sobreposicao de confirmacoes.

### RF09 - Auditoria
- O sistema deve registrar acoes administrativas criticas.
- O sistema deve registrar mudancas em formularios, turmas, vagas e status de matricula.

## 9. Requisitos nao funcionais iniciais

### Seguranca
- Trafego protegido por TLS.
- Senhas com hash forte.
- Controle de acesso baseado em papeis e escopo por escola.
- Validacao rigorosa de uploads.
- Logs sem exposicao indevida de dados sensiveis.

### Performance
- APIs criticas devem responder com baixa latencia.
- Formularios publicos devem carregar rapidamente em rede movel.
- O sistema deve ser preparado para cache de schemas publicados.

### Confiabilidade
- O sistema deve garantir consistencia no controle de vagas.
- Backups e restauracao devem ser considerados desde a arquitetura.

### Observabilidade
- Logs estruturados, metricas e rastreamento devem ser previstos.
- Cada requisicao deve poder ser correlacionada por identificadores tecnicos.

### Portabilidade operacional
- O projeto deve funcionar bem em WSL Ubuntu durante o desenvolvimento.
- O projeto deve ser compativel com deploy futuro em servidor Linux, evitando dependencias de Windows.

## 10. Casos de erro relevantes

- link publico expirado;
- link publico inativo;
- turma sem vagas;
- envio de arquivo invalido;
- tentativa de acesso a dados de outra escola;
- formulario despublicado ou inconsistente;
- falha de concorrencia em alta disputa por vagas.

## 11. Riscos tecnicos identificados cedo

### Concorrencia por vagas
Se dois usuarios tentarem ocupar a ultima vaga ao mesmo tempo, o sistema precisa ter consistencia forte. Isso influencia banco, transacoes e design de servicos.

### Evolucao de formulario
Se um formulario mudar durante uma campanha ativa, nao podemos quebrar o historico das inscricoes anteriores. Isso exige versionamento imutavel.

### Isolamento multi-tenant
Uma falha de autorizacao pode expor dados entre escolas. Esse e um risco de seguranca e tambem de arquitetura.

### Uploads
Arquivos trazem risco de seguranca, custo de armazenamento e complexidade operacional.

## 12. Decisoes de engenharia que ja aparecem na Fase 1

Mesmo sem implementar nada, esta fase ja orienta boas praticas:

- **KISS (Keep It Simple, Stupid):** comecamos definindo o fluxo principal antes de pensar em todas as customizacoes futuras.
- **DRY (Don’t Repeat Yourself):** documentar regras centrais uma vez evita duplicacao de entendimento em codigo, teste e README.
- **Modularidade:** separar dominios como `schools`, `classes`, `forms` e `enrollments` melhora coesao.
- **Coesao:** cada modulo deve concentrar responsabilidades relacionadas ao mesmo dominio.
- **Baixo acoplamento:** formularios, matriculas, autenticacao e arquivos devem conversar por contratos claros, evitando dependencia excessiva.
- **SOLID:** ainda nao estamos criando classes, mas ja estamos protegendo o principio de responsabilidade unica ao separar problemas por contexto de negocio.

## 13. Glossario didatico

- **PEP 8:** guia oficial de estilo do Python. Ajuda a manter codigo legivel e consistente.
- **PEP 257:** convencoes de docstrings. Ajuda a documentar modulos, classes e funcoes de forma padronizada.
- **SOLID:** conjunto de principios de design orientado a objetos que reduz rigidez e facilita manutencao.
- **DRY:** evitar repeticao desnecessaria de logica e conhecimento.
- **KISS:** preferir solucoes simples e claras.
- **Coesao:** medir se um modulo faz coisas intimamente relacionadas.
- **Acoplamento:** medir o quanto um modulo depende de detalhes internos de outro.
- **Multi-tenant:** uma unica aplicacao atende varios clientes com isolamento de dados.

## 14. Fora do escopo por enquanto

Para manter foco na evolucao incremental, os itens abaixo nao serao detalhados nesta fase:

- layout visual final do painel;
- integracoes externas especificas;
- regras financeiras;
- relatorios analiticos avancados;
- deploy automatizado detalhado.

## 15. Perguntas que ainda precisam de confirmacao

- A matricula sera apenas solicitacao inicial ou ja podera efetivar aluno diretamente?
- Havera assinatura digital, aceite de termos ou anexos obrigatorios por tipo de escola?
- Havera integracao futura com ERP escolar ou sistemas do governo?
- O painel administrativo sera construido junto neste repositorio ou separado?
- Existe necessidade de multi-idioma?

## 16. Definicao de pronto da Fase 1

Consideraremos a Fase 1 concluida quando:

- a visao do produto estiver clara;
- atores e fluxos principais estiverem definidos;
- user stories iniciais estiverem descritas;
- requisitos funcionais e nao funcionais estiverem registrados;
- riscos principais estiverem identificados;
- houver base suficiente para desenhar a arquitetura na Fase 2.

## 17. Proximo passo quando autorizado

Na proxima fase, vamos transformar estes requisitos em arquitetura de software, definindo:

- estrutura de pastas;
- modulos Python;
- fronteiras de dominio;
- camadas como API, service, repository e models;
- escolhas que favorecem manutencao, testes e deploy em Linux.
