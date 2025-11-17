![Build Status](https://github.com/jessica-leoa/gerenciador-de-frequencia/actions/workflows/main.yml/badge.svg)
![License](https://img.shields.io/github/license/jessica-leoa/gerenciador-de-frequencia)
![Last Commit](https://img.shields.io/github/last-commit/jessica-leoa/gerenciador-de-frequencia)
![Top Languages](https://img.shields.io/github/languages/top/jessica-leoa/gerenciador-de-frequencia)
![Repo Size](https://img.shields.io/github/repo-size/jessica-leoa/gerenciador-de-frequencia)
![Contributors](https://img.shields.io/github/contributors/jessica-leoa/gerenciador-de-frequencia)
![Open Issues](https://img.shields.io/github/issues/jessica-leoa/gerenciador-de-frequencia)
![Forks](https://img.shields.io/github/forks/jessica-leoa/gerenciador-de-frequencia)
![Stars](https://img.shields.io/github/stars/jessica-leoa/gerenciador-de-frequencia)
![Version](https://img.shields.io/github/v/tag/jessica-leoa/gerenciador-de-frequencia)
# Sistema de Gerenciamento de Frequência

Um projeto acadêmico desenvolvido para a disciplina de Gerência de Configuração de Software ministrado pelo professor Leopoldo Motta Teixeira, focado na aplicação prática de versionamento, containerização e pipelines de CI/CD.


## 1. Visão Geral

Este projeto consiste em um sistema simples para gerenciamento de frequência de alunos. O objetivo principal, no entanto, **não é** o desenvolvimento do software em si, mas sim utilizá-lo como um objeto de estudo para aplicar e demonstrar os conceitos fundamentais da Gerência de Configuração de Software (GCS).

O foco está em:
- **Versionamento de Código (Git):** Utilização de um fluxo de trabalho com branches, commits atômicos e tags para gerenciar a evolução do código-fonte.
- **Containerização (Docker):** Criação de um ambiente padronizado e isolado para a aplicação, garantindo que ela funcione de forma consistente em qualquer máquina.
- **Integração e Entrega Contínua (CI/CD):** Automação do processo de build, teste e publicação da aplicação utilizando GitHub Actions.

## 2. Escopo do Projeto: Módulo do Professor (MVP)

Para manter o projeto focado nos objetivos da disciplina, o desenvolvimento inicial contempla apenas o **Módulo do Professor**, com as seguintes funcionalidades essenciais:

-   ✅ **Fucionalidade do Professor:**
    -   [ ] Criar disciplina
    -   [ ] adicionar carga horária da disciplina
    -   [ ] Cadastrar alunos nas disciplinas
    -   [ ] Editar disciplina e carga horária 

-   ✅ **Dashboard de Turmas:**
    -   [ ] O professor visualiza uma lista das turmas
    -   [ ] Editar lista de chamada, o professor pode corrigir a presença ou falta do aluno

-   ✅ **Realização de Chamada:**
    -   [ ] Ao selecionar uma turma, o sistema exibe a lista de alunos.
    -   [ ] Marcar o status de cada aluno como **"Presente"** ou **"Faltou"**
    -   [ ] Funcionalidade para salvar a chamada, registrando a data e os status de presença

-   ✅ **Histórico de Frequência:**
    -   [ ] Consulta do registro de frequência de uma turma para uma data específica
    -   [ ] Ver alunos reprovado por falta

## 3 Método de gerenciamento
- Metodologia ágil Scrum
- Usaremos o Trunk-based development como prática de versionamento pois entendo que atender  melhor as práticas DevOps
- Usaremos o GitHub Project como ferramente de gerenciamento de requisitos e as Milistones como Sprints, associando Issues as essas Milistones.
- As atualizações no código só será feita via Pull Request
- Versionamento semantico com SemVer

## 4. Tecnologias Utilizadas

| Categoria      | Tecnologia                                                              | Propósito                                             |
| -------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| **Backend**        |                             | Servidor web para a lógica da aplicação               |
| **Frontend**       |                                              |  |
| **GCS & DevOps**   | Git & GitHub                                                            | Versionamento e hospedagem do código                  |
| **Containerização**| Docker                                                                  | Criação e gerenciamento do ambiente da aplicação      |
| **CI/CD**          | GitHub Actions                                                          | Automação de build e integração contínua              |

*Observação: Nesta fase inicial, não será utilizado um banco de dados. Os dados das turmas e alunos serão simulados ("mockados") diretamente no código-fonte para simplificar o ambiente.*

## 5. Como Executar o Projeto Localmente

Para executar esta aplicação, você precisará ter o **Git** e o **Docker** instalados em sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/jessica-leoa/gerenciador-de-frequencia.git
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd gerenciador-de-frequencia
    ```

3.  **Construa a imagem Docker:**
    Este comando lê o `Dockerfile` e cria uma imagem contendo todas as dependências e o código da aplicação.
    ```bash
    docker build -t gerenciador-de-frequencia .
    ```

4.  **Execute o contêiner a partir da imagem:**
    Este comando inicia um contêiner, mapeando a porta 8080 do seu computador para a porta 8080 do contêiner.
    ```bash
    docker run -p 8080:8080 gerenciador-de-frequencia
    ```

5.  **Acesse a aplicação:**
    Abra seu navegador e acesse [http://localhost:8080](http://localhost:8080)

## 6. Estrutura do Repositório (Planejada)

```

```

## 7. Autores

**Jéssica Roberta de Souza Santos**

**Lourenço Jamba Mphili**

**Lucas de Carvalho Silvestre**

**Tobias Oliveira**


---
