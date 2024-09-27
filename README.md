# Gestor de Cliente

<br>

## Índice de Conteúdo

- [Descrição](#descrição) <br>
- [Funcionalidades](#funcionalidades) <br>
- [Tecnologias Utilizadas](#tecnologias-utilizadas) <br>
- [Instalação](#instalação) <br>
- [Estrutura de Arquivos](#estrutura-de-arquivos) <br>
- [Licença](#licença) <br>

## Descrição

O Gestor de Cliente é um sistema simples e prático desenvolvido para auxiliar clínicas a cadastrar e agendar clientes de maneira rápida e eficiente. Com uma interface amigável e intuitiva, o sistema permite que os usuários gerenciem clientes, funcionários e consultas de forma integrada.

O projeto utiliza Bootstrap para o frontend, oferecendo uma interface responsiva, e o FullCalendar para um calendário nativo. O backend é construído com Flask, fornecendo rotas para todas as operações necessárias, e o banco de dados utilizado é o SQLite, com planos de migração futura para MongoDB.

## Funcionalidades

  - Login: Sistema de autenticação de usuários.
  - Cadastro de Clientes: Registre novos clientes com facilidade.
  - Cadastro de Funcionários: Gerencie os funcionários da clínica, com permissões específicas.
  - Calendário e Agendamento: Visualize um calendário integrado para agendar e visualizar consultas.
  - Tarefas: Acompanhe as tarefas e agendamentos ao clicar no dia correspondente no calendário.

## Tecnologias Utilizadas
### Frontend

  - Bootstrap: Framework CSS para estilização e design responsivo.
  - FullCalendar: Plugin JavaScript para exibição e gestão de eventos em formato de calendário.

### Backend

  - Flask: Framework web em Python para criação de rotas e lógica do servidor.
  - Flask-WTF: Extensão para integração de formulários no Flask.
  - SQLite: Banco de dados utilizado no projeto com possibilidade de migração para MongoDB no futuro.

## Instalação

   1. Clone este repositório:



    git clone https://github.com/seu_usuario/gestor-cliente.git

2. Navegue até o diretório do projeto:

bash

    cd gestor-cliente

3. Crie e ative um ambiente virtual:

bash

    python -m venv venv
    source venv/bin/activate   # No Windows use `venv\Scripts\activate`

4. Instale as dependências:

bash

    pip install -r requirements.txt

5. Execute o servidor:

bash

    flask run

6. Acesse o sistema em `http://localhost:5000.`

## Estrutura de Arquivos

  - `/templates:` Contém os arquivos HTML.
  - `/static:` Arquivos estáticos, como CSS e JS.
  - `app.py:` Arquivo principal que contém as rotas e a lógica da aplicação.
  - `forms.py:` Contém os formulários do sistema.
  - `models.py:` Define as tabelas do banco de dados.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais informações.
