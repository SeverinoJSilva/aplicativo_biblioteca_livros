## Documentação do Projeto de um Sistema para Gestão de Empréstimo de Livros de uma Biblioteca


## Sobre o Projeto:
## Sistema de Apoio a Gestão de uma Biblioteca Escolar ou Pessoal

## Descrição do Tema:
- O sistema deve dar apoio a gestão de uma biblioteca escolar, o sistema só gerencia livros. Cada livro tem um número de exemplares, um período máximo de empréstimo e uma descrição.  Um título só pode ser emprestado a leitores cadastrados, que possuem um período de empréstimo e um título pode ou não estar disponível para empréstimo.  O sistema também, deve permitir o tratamento de perda e dar apoio ao controle de reservas e empréstimos.
## Justificativa:
- O projeto atual é um pequeno ajuste no modelo de projeto sugerido de biblioteca, a diferença desse projeto está na possibilidade de utilização para fins pessoais de um usuário comum que deseja gerenciar sua biblioteca.
- O formato escolhido permite atender tanto a demanda de uma biblioteca escolar como qualquer outro usuário que queira gerenciar uma biblioteca pessoal, fazendo o controle de seus livros.

## Especificações dos Requisitos:

- RF01 – O sistema deve exigir que o usuário faça a login para realizar consultas e reservas.
- RF02 – O sistema deve permitir que o usuário faça o cadastro para acesso ao sistema.
- RF03 – O sistema deve permitir a reserva de um ou mais livros mesmo sem estoque.
- RF04 –  sistema deve impedir o registro de empréstimo de um livro sem estoque.
- RF05 – O sistema deve permitir a consulta de todos os livros por autor, ano, editora ou título.
- RF06 – O Sistema dever permitir a reservar de um livro pelo próprio usuário ou gerente
- RF07 – Os pedidos de reservas são obrigatórios para efetivar o empréstimo.
- RF08 – O empréstimo é incluído/confirmado pelo responsável pela biblioteca/gerente ou admin.
- RF08 – O sistema deve registrar o início do empréstimo, quando da inclusão do empréstimo pelo - bibliotecário/gerente ou admin.
- RF09 – O sistema deve permitir o registro da devolução, o extravio ou o reembolso do livro.
- RF10 – O sistema também deve permitir o gerenciamento de usuários, livros, reservas e empréstimos pelo administrador do sistema.

## Diagrama de Caso de Uso:
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/e0b3eac5-cace-4f56-bab3-c13902a4c172)

## Descrição dos Cenários de Caso de Uso:

- 1.  Login:  Usuário faz login no sistema.
- 2. Cadastro: Caso o usuário não tenha cadastro, ele realizar o cadastro no sistema.
- 3. Pesquisar Livro: Permite ao usuário pesquisar livros no sistema por título, autor, editora e ano e obter informações sobre os livros.
- 4. Reservar: Permite ao usuário reservar o livro detalhado.
- 5. Confirmar Reserva: Rotina interna do sistema que registra o pedido de reserva do usuário.
- 6. Minhas Solicitações: O usuário também pode consultar suas reservas e seus empréstimos.
- 7. O Usuário também pode alterar a sua senha de acesso ao sistema.


## Modelo Conceitual
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/ab8060b8-f6de-42d4-8002-bd0acd4c5158)

## Diagrama de Entidade e Relacionamento DER
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/edd74cc0-cfc3-4aad-a723-932d3847b4e3)

## Diagrama de Classes
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/89db49dc-0e0e-442b-a173-b875de3fd157)



## Diagrama de Sequências
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/842bd164-c5bd-4644-9bc0-de25693d3834)

## Apresentação do Protótipo do Sistema

- Abaixo é apresentado um protótipo do sistema no formato aplicativo para Desktop. A lógica de funcionamento dos menus e das janelas em futura versão para celular ou web, deve seguir um layout muito parecido com o do desktop.

## Página de Login
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/71846e76-caf4-46d8-a364-bddee2f8e550)

## Página de Cadastro
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/a0e0a04f-d026-404f-9fc3-09e1076d96a3)

## Página Principal

- A Janela do menu principal foi personalizada para atender a necessidade de gerenciamento de acesso ao sistema.
Foram criados 3 tipos de usuários:
- 1.	“admin” 	- Usuário com acesso total ao sistema. Esse usuário foi incluído na criação do banco de dados, é responsável também por gerenciar os tipos de acessos dos demais usuários do sistema.
- 2.	“gerente” - Usuário com acesso de supervisor e operador do sistema.
- 3.	“usuário” - Usuário com acesso de cliente, para consultar os livros, registrar reservas de livros, e consultar suas transações de reservas e empréstimos.
- Nas janelas abaixo, são apresentado o layout dos usuários: ADMIN perfil ‘admin’, SEVERINO perfil “gerente” e JANAINA perfil “usuário”.

![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/0007dc4e-5e35-473c-a225-3739d4b197b1)
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/c8b036ed-3ae2-4535-8261-87c014b3ecf1)
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/a0aa4196-55de-44eb-af95-46a8fdc18239)


## Página de Pesquisa
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/c83c7441-0ac0-4114-85f8-5a129074e745)

## Resultado da Pesquisa
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/8c7c4d45-65f7-493a-a2f4-a0e73e62c136)

## Janela de Reserva
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/f5606bd7-548d-4cd7-a439-1f310d5532ba)


## Janela de Confirmação da Reserva
![image](https://github.com/SeverinoJSilva/aplicativo_biblioteca_livros/assets/102735338/d1e4d014-73ca-41e8-997b-6c280a8a2691)





