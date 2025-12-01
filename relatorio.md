# Relatório de SCM e Processo de Desenvolvimento

## Estratégia de Branching Utilizada

Utilizamos a estratégia de **branching trunk-based**, estruturando o fluxo de desenvolvimento em pequenos blocos independentes. Para organização das tarefas:

* Branches de novas funcionalidades seguiam o padrão: **feat/nome-da-branch**
* Branches de correções seguiam o padrão: **fix/nome-da-branch**

Esse padrão facilitou a rastreabilidade das modificações, tornando simples identificar se uma branch estava relacionada a evolução ou correção do sistema.

## Procedimentos de Build e CI/CD

O processo de build foi baseado em Docker, permitindo que todo o time utilizasse o mesmo ambiente de execução. O Dockerfile incluía:

* Imagem base Python 3.11
* Instalação de dependências via `requirements.txt`
* Criação da pasta `instance`
* Exposição da porta 8080

Para desenvolvimento, utilizamos também Docker Compose, facilitando o uso de volumes e debug.

No CI/CD, utilizamos **GitHub Actions**, contendo etapas de:

* Checkout do repositório
* Configuração do Python
* Execução de linting com Flake8
* Execução de testes em ambiente Docker
* Automatização de versionamento e releases via *semantic-release*

Os arquivos completos (Dockerfile, docker-compose e pipeline YAML) permanecem no repositório.

## Forma de Versionamento Adotada (Tags e Releases)

O projeto utilizou uma estratégia de versionamento **totalmente automatizada** por meio do *python-semantic-release*, integrada à pipeline de CI/CD. A cada push na branch `main`, caso o código passasse pelos testes e validações, uma nova release era gerada automaticamente seguindo as regras de versionamento semântico (**Semantic Versioning**):

* **MAJOR** – quando ocorrem mudanças incompatíveis com versões anteriores.
* **MINOR** – quando novas funcionalidades são adicionadas.
* **PATCH** – quando correções de bugs são realizadas.

### Funcionamento das Releases

As releases eram criadas automaticamente com:

* Número de versão (ex.: `v1.5.0`)
* Lista de *features* incluídas
* Lista de *bug fixes*
* Link "Detailed Changes" mostrando comparação entre versões
* Assets disponibilizados para download (código fonte em `.zip` e `.tar.gz`)


Todas essas versões foram criadas de forma automatizada pela pipeline e identificadas pelo usuário `github-actions`, reforçando o uso consistente de versionamento automatizado.

Esse uso de *semantic-release* garantiu:

* Padronização automática de changelogs
* Controle claro de evolução do projeto
* Relação direta entre commits e releases
* Eliminação de processos manuais e propensos a erro

## Gestão de Issues

O fluxo de trabalho envolvendo issues foi o seguinte:

1. **Criação da issue** descrevendo claramente o problema ou a feature desejada.
2. **Associação da branch** criada especificamente para aquela issue.
3. **Desenvolvimento diretamente vinculado** à issue, utilizando mensagens como:

   * `ref #30` quando a alteração estava relacionada
   * `closes #30` quando o desenvolvimento finalizava completamente a issue
4. **Pull Request** associada à issue para permitir revisão e rastreabilidade.
5. **Fechamento automático** da issue após merge, quando utilizada a flag `closes`.

Esse fluxo manteve a rastreabilidade clara entre problemas, funcionalidades e commits.

## Reflexão


## Lições Aprendidas

Durante o projeto, algumas lições importantes foram observadas:

### Desafios

* Manter a disciplina no uso correto das branches (feat/fix)
* Controle de paralelismo: evitar branches muito grandes
* Alinhar commits com issues de forma consistente

### Melhorias Identificadas

* Padronizar ainda mais mensagens de commit
* Tornar o fluxo de CI/CD mais automatizado e menos dependente de tarefas manuais
* Criar templates de issues e PRs

### Como o Time Lidou com Problemas de SCM

* Resolvendo conflitos logo que surgiam, sem acumular merges
* Mantendo comunicação clara sobre quem estava trabalhando em quê
* Utilizando PRs com revisão obrigatória para reduzir problemas estruturais no código

### Contribuição Individual

**Jéssica Roberta de Souza Santos**: 
Durante o projeto, tivemos um incidente onde as regras de proteção de branch bloquearam o bot de release automático. Isso impediu a criação de tags intermediárias. A solução de SCM aplicada foi corrigir as permissões e gerar um Release Cumulativo, consolidando as mudanças pendentes em uma nova versão minor (v1.X.0), garantindo que nenhuma alteração ficasse sem rastreabilidade no Changelog.
dei o commit: git commit --allow-empty -m "feat: release cumulativo das funcionalidades anteriores"


Uma das principais lições aprendidas foi que a automação não elimina a necessidade de supervisão. Durante o projeto, confiamos que o pipeline de Release Automático estava gerando as tags corretamente após cada merge. No entanto, devido a um conflito de regras de proteção de branch (Branch Protection Rules), o job de release falhou silenciosamente por um período.
Isso nos ensinou que:
Monitoramento é crucial: Não basta configurar o GitHub Actions; é preciso verificar a aba "Actions" regularmente ou configurar notificações (email/Slack) para falhas.*
Falhas silenciosas geram acúmulo: A falta de monitoramento causou um acúmulo de funcionalidades sem versão (version gap), exigindo uma intervenção manual para gerar um 'Release Cumulativo'.*
Melhoria futura: Como melhoria para os próximos passos, implementaríamos webhooks para avisar a equipe imediatamente quando um pipeline crítico falhar na branch main.


Uma lição prática sobre ambiente de desenvolvimento foi a distinção entre a identidade do autor (git config user.name) e a autenticação de acesso (Credenciais do Sistema Operacional). O erro de permissão nos ensinou a importância de verificar o Gerenciador de Credenciais do Windows ao trocar de usuários e reforçou a recomendação de usar chaves SSH ou ambientes isolados (como containers ou máquinas virtuais) para evitar conflitos de identidade em máquinas compartilhadas.

**Lourenço Jamba Mphili**: 
No âmbito da arquitetura da aplicação Flask, a consistência entre o Frontend e o Backend provou ser crítica para a estabilidade do sistema. Enfrentamos erros de construção de URL (BuildError) causados por divergências na nomenclatura das rotas, onde os templates HTML referenciavam endpoints que não correspondiam exatamente aos nomes das funções definidas nas rotas Python. Esse cenário evidenciou a importância de manter um padrão rigoroso de nomenclatura para funções e rotas, além de validar constantemente as referências cruzadas entre as camadas de visualização e controle para evitar falhas em tempo de execução que comprometam a navegação do usuário.

A segurança e a validação de dados também foram temas centrais de aprendizado. Ao atualizar as regras de negócio referentes à Carga Horária das disciplinas, observou-se que a alteração isolada nas restrições do formulário HTML foi insuficiente, pois o servidor continuava rejeitando os novos valores. Isso consolidou o entendimento de que a validação no Frontend serve primordialmente para a experiência do usuário, enquanto a segurança real e a integridade das regras de negócio residem exclusivamente no Backend. Concluiu-se que qualquer alteração de regra de negócio exige uma atualização sincronizada e obrigatória na lógica do servidor antes de ser refletida na interface.

Por fim, a modernização da infraestrutura através da containerização trouxe lições valiosas sobre o ciclo de vida da aplicação. A implementação do Docker e do Docker Compose permitiu a criação de um ambiente de desenvolvimento determinístico e isolado, eliminando problemas de compatibilidade entre diferentes máquinas. Uma otimização crucial foi aplicada na inicialização do banco de dados, onde implementamos uma verificação lógica para impedir a recriação desnecessária das tabelas a cada reinício do container. Juntamente com a automação dos testes via scripts de pipeline, essas melhorias garantiram que o ambiente seja não apenas robusto, mas também eficiente, preservando a persistência dos dados e agilizando o fluxo de trabalho da equipe.

**Lucas de Carvalho Silvestre**: De minha perspectiva as lições aprendidas foram centradas no desenvolvimento interpessoal, na gestão de falhas e na expansão de competências técnicas e emocionais.
No começo, identificamos um desafio primordial: a sintonia/sinergia inicial do grupo. Superar essa barreira exigiu um esforço consciente para estabelecer a sincronização das tarefas e a cooperação mútua; para o grupo obter o trabalho mais fluido e eficaz, e ainda de como lidar com as falhas no processo.

Do ponto de vista acadêmico a necessidade de aprender novas ferramentas foi uma constante, proporcionando a oportunidade de ampliar o conhecimento de todos os membros e incorporando métodos mais eficientes ao fluxo de trabalho. O projeto exigiu gerenciamento de tempo, prazos e expectativas, consolidando a lição de que a inteligência emocional é tão vital quanto a competência técnica para o sucesso de qualquer projeto.

**Tobias Oliveira**: Além das lições técnicas aprendidas, por meio do levantamento dúvidas, enganos corrigidos, conversas e pesquisas feitas ao longo do projeto, faço algumas reflexões sobre o grupo e o conhecimento necessário para gerenciar um projeto com certa complexidade: 
* A dificuldade de trabalhar em grupo, principalmente à distância, com os membros com suas diferenças de conhecimento, disponibilidade de horários, diferentes visões e aspirações com relação ao projeto, sem dúvidas é uma experiência que me traz mais maturidade e amplia minha visão de mundo. 
* Outro ponto de lição aprendida, é a necessidade de partir de um nível de conhecimento e ideia do projeto compartilhada por todos os membros. Para assim trabalhar de forma mais eficiente e atingir os objetivos com maior clareza.  


***Nota ao professor**: na seção de contribuidores, no github, existem dois perfis extras, além do action-user. `mphili10` é outro usuário do Lourenço, membro do time. `nielsonjr` é um usuário de um computador usado pela Jéssica. Ambos foram incluídos por erros da equipe, que não verificou o usuário que estava fazendo os PR/modificações.*
