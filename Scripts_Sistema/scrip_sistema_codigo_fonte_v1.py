#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Importando as Bibliotecas
import tkinter as tk
from tkinter import ttk
import os
import sqlite3
import datetime


# Script do Programa

# CONFIGURAÇÃO DE ACESSO DO PERFIL:  Admin e Gerente
# FUNÇÕES DE NÍVEL DE ACESSO: Admin e Gerente

# 1ª. PARTE - CADASTRO E ATUALIZAÇÃO DE USUARIOS:

# Função para abrir a janela para cadastrar o usuario
def cadastro():
    # Função para cadastrar usuario
    def cadastrar_usuario():
        #Abre uma conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Variaveis para verificar se não estão vazios
        var_nome =  caixa_texto_nome.get().strip().title()
        var_telefone = caixa_texto_telefone.get().strip()
        var_endereco =  caixa_texto_endereco.get().strip().title()
        var_email =  caixa_texto_email.get().strip().lower()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se não estão vazios
            if not var_nome or not var_telefone or not var_endereco or not var_email:
                raise ValueError("Por favor, preencha todas as informações.")
            # Verifique se o email já existe na tabela tb_usuario
            cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE EMAIL = ?", (var_email,))
            existing_user = cursor.fetchone()
            # Caso existe o e-mail, retorna erro
            if existing_user:
                raise ValueError("Este email já está registrado.")                   
            # Função para gerar ID unico da tabela usuario
            cursor.execute("SELECT MAX(ID_USUARIO) FROM tb_usuario")
            # Recupera o maior de tb_usuarios e adiciona 1 para obter o próximo ID disponível
            max_id_usuario = cursor.fetchone()[0]
            if max_id_usuario is None:
                max_id_usuario = 0
            id_usuario = max_id_usuario + 1
            # Gerando a senha (a primeira palavra do nome + "12345")
            senha_usuario = var_nome.split()[0].lower() + "12345"            
            # Insira o novo usuário com o ID_USUARIO obtido (não é necessário especificar o ID_USUARIO)
            cursor.execute("INSERT INTO tb_usuario (ID_USUARIO, NOME, TELEFONE, ENDERECO, EMAIL, SENHA_USUARIO) VALUES (?, ?, ?, ?, ?, ?)",
                           (id_usuario, var_nome, var_telefone, var_endereco, var_email, senha_usuario))
            # Consulta SQL para contar o número de registros na tabela tb_usuario
            cursor.execute("SELECT COUNT(*) FROM tb_usuario  WHERE ID_USUARIO > 20230000")
            # Recupera o resultado da consulta (número de registros) em uma variável
            numero_de_registros = cursor.fetchone()[0]            
            # Salvar as alterações e fechar a conexão
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            caixa_texto_nome.delete(0, 'end')            
            caixa_texto_telefone.delete(0, 'end')
            caixa_texto_endereco.delete(0, 'end')
            caixa_texto_email.delete(0, 'end')
            # Atualizar a mensagem na parte inferior da janela
            mensagem_label_cadastro.config(text="Cadastro Confirmado", fg="green")
            mensagem_label_total_usuarios.config(text=f'Você Possui {numero_de_registros} Usuários Cadastrados.', fg="blue")
        # Em caso de erro, exibir mensagem de erro na parte inferior da janela
        except ValueError as ve:
            mensagem_label_cadastro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_cadastro.config(text="Erro ao atualizar informações: " + str(e), fg="red")
        except Exception as e:
            mensagem_label_cadastro.config(text="Informação incompleta: " + str(e), fg="red")                   
            
    # Função para dados  atualizar usuario
    def atualizar_usuario():
        # Abre uma conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtem as variaveis para atualizar os dados
        id_usuario = combobox_atualizar_usuario.get()
        opcao_atualizacao = combobox_atualizar_opcao.get()
        nova_informacao = caixa_texto_label_para_atualizacao.get().strip().title()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_usuario, opcao_atualizacao e nova_informacao não estão vazios
            if not id_usuario or not opcao_atualizacao or not nova_informacao:
                raise ValueError("Por favor, preencha todas as informações.")
            # Converte o ID para inteiro                
            id_usuario = int(id_usuario) 
            # Atualiza as informações do usuário com base no ID_USUARIO
            cursor.execute(f"UPDATE tb_usuario SET {opcao_atualizacao} = ? WHERE ID_USUARIO = ?",
                           (nova_informacao, id_usuario))
            # Salva e Fecha conexão 
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_atualizar_usuario.delete(0, 'end')            
            combobox_atualizar_opcao.delete(0, 'end')
            caixa_texto_label_para_atualizacao.delete(0, 'end')
            # Retorna mensagem de sucesso do procedimento
            mensagem_label_cadastro.config(text="Informações atualizadas com sucesso", fg="green")
        except ValueError as ve:
            # Exibe uma mensagem de erro referente a alguma falha no processo
            mensagem_label_cadastro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            # Em caso de erro do SQLite exibe uma mensagem de erro
            mensagem_label_cadastro.config(text="Erro ao atualizar informações: " + str(e), fg="red")
        except Exception as e:
            mensagem_label_cadastro.config(text="Informação incompleta: " + str(e), fg="red")                

    # Obtendo listas dos ids das tabelas usuario
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para selecionar todos os valores da coluna ID_USUARIO
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE ID_USUARIO > 20230000")
    # Recupera todos os resultados da consulta em uma lista
    lista_usuario = [registro[0] for registro in cursor.fetchall()]    
    lista_opcao_usuario = ['NOME', 'TELEFONE', 'ENDERECO']            
    # Janela de Cadastro a ser aberta ao clicar no botão Cadastro
    janela_cadastro = tk.Toplevel()
    # Formatando o titulo da janela
    janela_cadastro.title('Cadastro de Usuários')
    # Cabeçalho da tela de cadastro
    label_cadastro_user = tk.Label(janela_cadastro, text='CADASTRO DE USUÁRIOS', borderwidth=2, relief='solid', 
                                   fg='black', bg='#2FD5D9', width=40, height=2)
    label_cadastro_user.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
    # label do nome
    label_nome= tk.Label(janela_cadastro, text='Nome:', anchor='w')
    label_nome.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_nome = tk.Entry(janela_cadastro, width=40)
    caixa_texto_nome.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    # label do telefone
    label_telefone= tk.Label(janela_cadastro, text='Telefone com DDD:', anchor='w')
    label_telefone.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_telefone = tk.Entry(janela_cadastro, width=40)
    caixa_texto_telefone.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    # label do endereço
    label_endereco= tk.Label(janela_cadastro, text='Endereço:', anchor='w')
    label_endereco.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_endereco = tk.Entry(janela_cadastro, width=40)
    caixa_texto_endereco.grid(row=3, column=1, columnspan=2,padx=10, pady=10, sticky='nsew')
    # label do e-mail
    label_email = tk.Label(janela_cadastro, text='E-mail:', anchor='w')
    label_email.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_email = tk.Entry(janela_cadastro, width=40)
    caixa_texto_email.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    # Criando botão de login e cadastro
    botao_cadastrar = tk.Button(janela_cadastro, text='Cadastrar', command=cadastrar_usuario)
    botao_cadastrar.grid(row=5, column=2, padx=10, pady=10, sticky='nsew')
    
    # Criando a Janela de Atualizacao
    # Texto da janela
    label_janela_atualizar = tk.Label(janela_cadastro, text='ATUALIZAR DADOS USUARIO', borderwidth=2, relief='solid', 
                                      fg='black', bg='#2FD5D9', width=40, height=2)
    label_janela_atualizar.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew' )
    # Label e caixa de texto para atualizar o usuario
    label_atualizar_usuario = tk.Label(janela_cadastro, text='Selecione o ID do Usuário: ', anchor='w')
    label_atualizar_usuario.grid(row=7, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    combobox_atualizar_usuario = ttk.Combobox(janela_cadastro, values=lista_usuario)
    combobox_atualizar_usuario.grid(row=7,column=2,  columnspan=3, padx=10, pady=10, sticky='nsew')
    # Label e caixa de seleçã para escolha dos campos para atualizacao
    label_atualizar_usuario1 = tk.Label(janela_cadastro, text='Selecione o Campo para Atualização: ', anchor='w')
    label_atualizar_usuario1.grid(row=8, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    combobox_atualizar_opcao = ttk.Combobox(janela_cadastro, values=lista_opcao_usuario)
    combobox_atualizar_opcao.grid(row=8,column=2,  columnspan=3, padx=10, pady=10, sticky='nsew')
    # label de caixa de texto para Receber a nota informação
    label_para_atualizacao= tk.Label(janela_cadastro, text='Preenha a Informação:', anchor='w')
    label_para_atualizacao.grid(row=9, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    caixa_texto_label_para_atualizacao = tk.Entry(janela_cadastro, width=40)
    caixa_texto_label_para_atualizacao.grid(row=9, column=2, columnspan=3, padx=10, pady=10, sticky='nsew')   
    # Botão de atualização
    botao_atualizar_usuario = tk.Button(janela_cadastro, text='Atualizar', command=atualizar_usuario)
    botao_atualizar_usuario.grid(row=10, column=2, padx=10, pady=10, sticky='nsew')                
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_cadastro = tk.Label(janela_cadastro, text="", fg="green")
    mensagem_label_cadastro.grid(row=11, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')     
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_total_usuarios = tk.Label(janela_cadastro, text="", fg="green")
    mensagem_label_total_usuarios.grid(row=12, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')  
    botao_sair = tk.Button(janela_cadastro, text='Voltar', command=janela_cadastro.destroy)
    botao_sair.grid(row=13, column=0, padx=10, pady=10, sticky='nsew')
    # Rodando a Janela
    janela_cadastro.mainloop()
    
# 2ª. PARTE - CADASTRO E ATUALIZAÇÃO DE LIVROS

# Função para abrir a janela para cadastrar o livro
def cadastrar_livro():
    # Função para Cadastrar livro
    def cadastro_de_livros():
        # Abre uma conexão com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtendo as variáveis para atualizar o banco de dados
        var_isbn = caixa_texto_isbn.get().strip()
        var_titulo = caixa_texto_titulo.get().strip().title()
        var_autor = caixa_texto_autor.get().strip().title()
        var_editora = caixa_texto_editora.get().strip().title()
        var_ano = caixa_texto_ano.get().strip()
        var_paginas = caixa_texto_pagina.get().strip()
        var_valor = caixa_texto_valor.get().strip()
        var_quantidade = caixa_texto_quantidade.get().strip()
        var_tema = caixa_texto_tema.get('1.0', 'end').title()
        var_comentario = caixa_texto_comentario.get('1.0', 'end')

        # Tenta executar a função e, caso haja erro, retorna o erro
        try:
            # Verifica se as variáveis foram preenchidas
            if not var_isbn or not var_titulo or not var_autor or not var_editora or not var_ano or not var_paginas or not var_valor or not var_quantidade:
                raise ValueError("Por favor, preencha todos os campos.")

            # Verifica se os campos de quantidade e ano são números inteiros antes de convertê-los
            if not caixa_texto_quantidade.get().isdigit() or not caixa_texto_ano.get().isdigit():
                raise ValueError("ISBN, Ano, Quantidade, Páginas devem conter apenas números.")
            var_quantidade = int(caixa_texto_quantidade.get())
            var_ano = int(caixa_texto_ano.get())
            var_valor = float(var_valor.replace(',', '.'))
            # Verifica se o ISBN já existe na tabela tb_livro, caso positivo retorna erro
            isbn = caixa_texto_isbn.get()
            cursor.execute("SELECT COUNT(*) FROM tb_livro WHERE ID_ISBN=?", (isbn,))
            livro_existente = cursor.fetchone()[0] > 0
            if livro_existente:
                mensagem_label_livro.config(text="Já existe um livro com o mesmo ISBN.", fg="red")
            else:
                cursor.execute("INSERT INTO tb_livro (ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, VALOR, QUANTIDADE, DESCRICAO, COMENTARIO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (var_isbn, var_titulo, var_autor, var_editora, var_ano, var_paginas, var_valor, var_quantidade, var_tema, var_comentario))
                # Consulta para contar o número de registros na tabela tb_livro
                cursor.execute("SELECT COUNT(*) FROM tb_livro")
                # Recupera o resultado da consulta (número de registros) em uma variável
                numero_de_livros = cursor.fetchone()[0]
                # Consulta a soma do valor dos livros
                cursor.execute("SELECT SUM(VALOR) FROM tb_livro")
                valor_total = cursor.fetchone()[0]
                # no caso do valor está zerado e não gerar erro
                if valor_total is None:
                    valor_total = 0
                # Salvar as alterações e fechar a conexão
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                caixa_texto_isbn.delete(0, 'end')
                caixa_texto_titulo.delete(0, 'end')
                caixa_texto_autor.delete(0, 'end')
                caixa_texto_editora.delete(0, 'end')
                caixa_texto_ano.delete(0, 'end')
                caixa_texto_pagina.delete(0, 'end')
                # para entry usamos (0, 'end')
                caixa_texto_valor.delete(0, 'end')
                caixa_texto_quantidade.delete(0, 'end')
                # para text usamos (1.0, tk.END)
                caixa_texto_tema.delete(1.0, tk.END)
                caixa_texto_comentario.delete(1.0, tk.END)
                # Atualizar mensagens de sucesso e total de livros cadastrados
                valor_real =  "{:.2f}".format(valor_total).replace('.', ',')
                mensagem_label_livro.config(text="Livro Cadastrado Com Sucesso!", fg="green")
                mensagem_label_total_livros.config(text=f"{numero_de_livros} livro(s) cadastrado(s). Avaliado(s) em R$ {valor_real}.", fg="blue")
        # Retorna mensagem de erro em caso de falha
        except ValueError as ve:
            mensagem_label_livro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_livro.config(text="Erro ao atualizar informações: " + str(e), fg="red")
        except Exception as e:
            mensagem_label_livro.config(text="Informação incompleta: " + str(e), fg="red")
     
              
    # Função para atualizar livro
    def atualizacao_livros():
        # Abre conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtem as variaveis para atualizacao dos dados
        id_isbn = combobox_atualizar_livro.get()
        opcao_atualizacao = combobox_atualizar_opcao.get()
        nova_informacao = caixa_texto_label_para_atualizacao.get().strip().title()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_isbn, opcao_atualizacao e nova_informacao não estão vazios
            if not id_isbn or not opcao_atualizacao or not nova_informacao:
                raise ValueError("Por favor, preencha todos os campos.")
            # Converte o ID_ISBN para inteiro
            id_isbn = int(id_isbn) 
            # Atualiza as informações do livro com base no ID_ISBN
            cursor.execute(f"UPDATE tb_livro SET {opcao_atualizacao} = ? WHERE ID_ISBN = ?", (nova_informacao, id_isbn))
            # Fecha a conexão com o banco de dados
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_atualizar_livro.delete(0, 'end')      
            combobox_atualizar_opcao.delete(0, 'end')      
            caixa_texto_label_para_atualizacao.delete(0, 'end')      
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_livro.config(text="Informações atualizadas com sucesso", fg="green")
        # Retorna erro em caso de falha na execução do código
        except ValueError as ve:
            mensagem_label_livro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_livro.config(text="Erro: " + str(e), fg="red")
        except Exception as e:
            mensagem_label_livro.config(text="Informação incompleta: " + str(e), fg="red")       
            
    # Obtendo listas dos ids das tabelas livro
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta para selecionar todos os valores da coluna ID_ISBN
    cursor.execute("SELECT ID_ISBN FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    lista_livro = [registro1[0] for registro1 in cursor.fetchall()] 
    # Lista de opções para atualizacao
    lista_opcao_livro = ['TITULO', 'AUTOR', 'EDITORA', 'ANO', 'VALOR', 'QUANTIDADE', 'DESCRICAO', 'COMENTARIO']
    # Criando a Janela de cadastro do livro
    janela_livro = tk.Toplevel()
    # Formatando o titulo
    janela_livro.title('Cadastro de Livros')
    # Cabeçalho da tela de cadastro
    label_cadastro_livro = tk.Label(janela_livro,text='CADASTRO DE LIVROS', borderwidth=2, relief='solid', 
                                    fg='black', bg='#2FD5D9', width=40, height=2)
    label_cadastro_livro.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=4)
    # label e caixa de entrada do ISBN
    label_isbn= tk.Label(janela_livro, text='ISBN:', anchor='e')
    label_isbn.grid(row=1, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_isbn = tk.Entry(janela_livro, width=40)
    caixa_texto_isbn.grid(row=1, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # label e caixa de entrada  do titulo
    label_titulo= tk.Label(janela_livro, text='Título:', anchor='e')
    label_titulo.grid(row=2, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_titulo = tk.Entry(janela_livro, width=40)
    caixa_texto_titulo.grid(row=2, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # label e caixa de entrada do autor
    label_autor= tk.Label(janela_livro, text='Autor:', anchor='e')
    label_autor.grid(row=3, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_autor = tk.Entry(janela_livro, width=40)
    caixa_texto_autor.grid(row=3, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # label e caixa de entrada da editora
    label_editora = tk.Label(janela_livro, text='Editora:', anchor='e')
    label_editora.grid(row=4, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_editora = tk.Entry(janela_livro, width=40)
    caixa_texto_editora.grid(row=4, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # label e caixa de entrada do Ano
    label_ano = tk.Label(janela_livro, text='Ano:', anchor='e')
    label_ano.grid(row=5, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_ano = tk.Entry(janela_livro, width=40)
    caixa_texto_ano.grid(row=5, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # label e caixa de entrada de quantidade de paginas
    label_paginas = tk.Label(janela_livro, text='Nr. Páginas:', anchor='e')
    label_paginas.grid(row=6, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_pagina = tk.Entry(janela_livro, width=40)
    caixa_texto_pagina.grid(row=6, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')    
    # Label e caixa de entrada do Valor
    label_valor =  tk.Label(janela_livro, text='Valor', anchor='e')
    label_valor.grid(row=7, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_valor = tk.Entry(janela_livro, width=40)
    caixa_texto_valor.grid(row=7, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # Label e caixa de entrada da quantidade
    label_quantidade =  tk.Label(janela_livro, text='Quantidade:', anchor='e')
    label_quantidade.grid(row=8, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_quantidade = tk.Entry(janela_livro, width=40)
    caixa_texto_quantidade.grid(row=8, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')    
    # label  e caixa de entrada do Tema
    label_tema= tk.Label(janela_livro, text='Descrição Temática:', anchor='e')
    label_tema.grid(row=9, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_tema = tk.Text(janela_livro, width=30, height=2)
    caixa_texto_tema.grid(row=9, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # label e caixa de texto para o cometario
    label_tema= tk.Label(janela_livro, text='Comentário/Resenha:', anchor='e')
    label_tema.grid(row=10, column=0, padx=10, pady=3, sticky='nsew')
    caixa_texto_comentario = tk.Text(janela_livro, width=30, height=2)
    caixa_texto_comentario.grid(row=10, column=1, columnspan=2,padx=10, pady=3, sticky='nsew')
    # Botão cadastar livro
    botao_cadastrarlivro = tk.Button(janela_livro, text='Cadastrar', command=cadastro_de_livros)
    botao_cadastrarlivro.grid(row=11, column=1, padx=10, pady=3, sticky='nsew')

    # Configurando caixa de entrada e botões de atualização de livros
    
    # Texto da funcionalidade
    label_janela_atualizar = tk.Label(janela_livro, text='ATUALIZAR DADOS LIVRO', borderwidth=2,relief='solid', 
                                      fg='black', bg='#2FD5D9', width=40, height=2)
    label_janela_atualizar.grid(row=12, column=0, columnspan=4, padx=10, pady=3, sticky='nsew' )
    # label para selecionar livro na lista_livro
    label_atualizar_usuario = tk.Label(janela_livro, text='Selecione o ISBN do Livro: ', anchor='w')
    label_atualizar_usuario.grid(row=13, column=0, padx=10, pady=3, sticky='nsew')
    combobox_atualizar_livro = ttk.Combobox(janela_livro, values=lista_livro)
    combobox_atualizar_livro.grid(row=13,column=1, padx=10, pady=3, sticky='nsew')
    # Label e caixa de selecao da opção a ser atualizada pela lista_opcao_livro
    label_atualizar_usuario1 = tk.Label(janela_livro, text='Selecione o Campo para Atualização: ', anchor='w')
    label_atualizar_usuario1.grid(row=14, column=0, padx=10, pady=3, sticky='nsew')
    combobox_atualizar_opcao = ttk.Combobox(janela_livro, values=lista_opcao_livro)
    combobox_atualizar_opcao.grid(row=14,column=1, padx=10, pady=3, sticky='nsew')
    # Label e caixa de entrada para receber a nova informação e bitão para atualizar o livro
    label_para_atualizacao= tk.Label(janela_livro, text='Preencha a Informação:', anchor='w')
    label_para_atualizacao.grid(row=15, column=0, padx=10, pady=5, sticky='nsew')
    caixa_texto_label_para_atualizacao = tk.Entry(janela_livro, width=40)
    caixa_texto_label_para_atualizacao.grid(row=15, column=1, padx=10, pady=3, sticky='nsew')    
    botao_atualizar_livro = tk.Button(janela_livro, text='Atualizar', command=atualizacao_livros)
    botao_atualizar_livro.grid(row=16, column=1, padx=10, pady=3, sticky='nsew')                
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_livro = tk.Label(janela_livro, text="", fg="green")
    mensagem_label_livro.grid(row=17, column=0, columnspan=3, padx=10, pady=3, sticky='nsew')   
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_total_livros = tk.Label(janela_livro, text="", fg="green")
    mensagem_label_total_livros.grid(row=18, column=0, columnspan=3, padx=10, pady=3, sticky='nsew')    
    botao_cadastrarlivro_sair = tk.Button(janela_livro, text='Voltar', command=janela_livro.destroy)
    botao_cadastrarlivro_sair.grid(row=19, column=0, padx=10, pady=3, sticky='nsew')
    # Rodando a Janela
    janela_livro.mainloop()

# 3ª. PARTE - RESERVA DE LIVROS:      

# Obtendo a data Atual e a data com 60 dias de prazo, para utilização nas variaveis em reservas e emprestimos
# Data Atual
data_atual = datetime.date.today()
data_atual_formatada = data_atual.strftime('%d/%m/%Y')
# Data para Devolução
data_futura = data_atual + datetime.timedelta(days=60)
data_futura_formatada = data_futura.strftime('%d/%m/%Y')    

# Função para abrir a janela para registrar a reserva    
def reservar_livro():
     # Função para registrar a reserva de um livro
    def cadastrar_reserva():
        # Conectando com o Banco de Dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtendo as O ID_USUARIO e o ID_ISBN para registro da reserva
        usuario_reserva =  combobox_seleciona_usuarios_reserva.get()
        livro_reserva  = combobox_selecionaLivros_reserva.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se usuario_reserva e livro_reserva não estão vazios
            if not usuario_reserva or not livro_reserva:
                raise ValueError("Por favor, preencha todas as informações.")    
            # Verificar se já existe uma reserva para o mesmo livro e usuário, caso afirmativo retorna erro
            cursor.execute("SELECT COUNT(*) FROM tb_reserva WHERE ID_USUARIO = ? AND ID_ISBN = ?", 
                           (usuario_reserva, livro_reserva))
            reserva_existente = cursor.fetchone()[0]
            if reserva_existente > 0:
                raise ValueError("O usuário já reservou este livro!")  
            # Obtem o maior id_reserva da tabela para poder gerar um novo
            cursor.execute("SELECT MAX(ID_RESERVA) FROM tb_reserva")
            # Recupera o maior id_reserva e adiciona 1 para obter o próximo ID disponível
            max_id_reserva = cursor.fetchone()[0]
            if max_id_reserva is None:
                max_id_reserva = 0
            id_reserva = max_id_reserva + 1
            # Insire uma nova reserva com o ID_RESERVA obtido
            cursor.execute("INSERT INTO tb_reserva (ID_RESERVA, ID_USUARIO, ID_ISBN, DATA_RESERVA) VALUES (?, ?, ?, ?)",
                           (id_reserva, usuario_reserva, livro_reserva, data_atual_formatada))
            # Consulta para contar o número de registros na tabela tb_reserva
            cursor.execute("SELECT COUNT(*) FROM tb_reserva")
            # Recupera o resultado da consulta (número de registros) em uma variável
            numero_de_reservas = cursor.fetchone()[0]            
            # Salvar as alterações e fechar a conexão
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_usuarios_reserva.delete(0, 'end')      
            combobox_selecionaLivros_reserva.delete(0, 'end')      
            # Atualizar a mensagem na parte inferior da janela
            mensagem_label_reserva.config(text="Reserva Registrada", fg="green")
            mensagem_label_total_reservas.config(text=f"Você Possui: {numero_de_reservas} livro(s) reservado(s).", fg="blue")        
            # Em caso de erro, exibir mensagem de erro na parte inferior da janela
        except ValueError as ve:
            # Exibe uma mensagem de erro se alguma informação estiver faltando ou inválida
            mensagem_label_reserva.config(text=str(ve), fg="red")  
        except sqlite3.Error as e:
            # Em caso de erro do SQLite, exibir mensagem de erro na parte inferior da janela
            mensagem_label_reserva.config(text="Erro: " + str(e), fg="red")            
        except Exception as e:
            # Exibe uma mensagem de erro se alguma informação estiver faltando ou inválida
            mensagem_label_reserva.config(text="Verifique o tipo os dados: " + str(e), fg="red")
    # Abre uma conexao com o banco de dados
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta para selecionar todos os valores da coluna Nome
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE ID_USUARIO > 20230000")
    # Recupera todos os resultados da consulta em uma lista
    usuarios = [registro[0] for registro in cursor.fetchall()]
    # Consulta para selecionar todos os LIVROS da coluna ID_ISBN
    cursor.execute("SELECT ID_ISBN FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    livros = [registro1[0] for registro1 in cursor.fetchall()]
    # Fechar a conexão
    conn.close()
    
    # Criando a Janela
    janela_reservar = tk.Toplevel()
    # Formatando o titulo
    janela_reservar.title('Reserva de Livros')
    # Cabeçalho da tela de cadastro
    label_cadastro_reserva = tk.Label(janela_reservar, text='REGISTRO DE RESERVA', borderwidth=2, relief='solid', 
                                      fg='black', bg='#2FD5D9', width=40, height=2)
    label_cadastro_reserva.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
    # label Caixa de seleção de usuarios
    label_selecionau_usuarios_reserva = tk.Label(janela_reservar, text='Selecionar Usuarios: ', anchor='w')
    label_selecionau_usuarios_reserva.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=1)
    combobox_seleciona_usuarios_reserva = ttk.Combobox(janela_reservar, values=usuarios)
    combobox_seleciona_usuarios_reserva.grid(row=1,column=1, padx=10, pady=10, sticky='nsew', columnspan=3)
    # label Caixa de seleção de livros
    label_selecionaLivros_reserva = tk.Label(janela_reservar, text='Selecionar Livros: ', anchor='w')
    label_selecionaLivros_reserva.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=1)
    combobox_selecionaLivros_reserva = ttk.Combobox(janela_reservar, values=livros)
    combobox_selecionaLivros_reserva.grid(row=2,column=1, padx=10, pady=10, sticky='nsew', columnspan=3)
    # Obtem de forma automatica a data referente ao registro do reserva
    label_datainicio_reserva  = tk.Label(janela_reservar, text="Data da Reserva: ", anchor='w')
    label_datainicio_reserva.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=1)
    calendario_datainicio_reserva = tk.Label(janela_reservar,text=f"{data_atual_formatada}", anchor='e')
    calendario_datainicio_reserva.grid(row=3, column=1, padx=10, pady=10, sticky='nsew', columnspan=3)
    # Criar o rótulo para exibir mensagens
    mensagem_label_reserva = tk.Label(janela_reservar, text="", fg="green")
    mensagem_label_reserva.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    mensagem_label_total_reservas = tk.Label(janela_reservar, text="", fg="green")
    mensagem_label_total_reservas.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    # botoes para reservar e voltar
    botao_reservar = tk.Button(janela_reservar, text='Reservar', command=cadastrar_reserva)
    botao_reservar.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')    
    botao_voltar = tk.Button(janela_reservar, text='Voltar', command=janela_reservar.destroy)
    botao_voltar.grid(row=7, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')    
    # Roda a janela
    janela_reservar.mainloop()    
    
# 4ª. PARTE - REGISTRAR E ATUALIZAR EMPRÉSTIMOS

# # Função para abrir a janela para registrar o empréstimo    
def registrar_emprestimo():
    # Função para registrar o empréstimo do livro
    def cadastrar_emprestimos():
        # Abre conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtendo a a varivavel a parti da caixa de selecao
        id_reserva = combobox_seleciona_id_reserva.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se o ID_RESERVA está vazio e retornará erro caso esteja
            if not id_reserva:
                raise ValueError("Por favor, selecione uma reserva válida.")
            # Consulta para obter o ID_ISBN do livro na reserva selecionada
            cursor.execute("SELECT ID_ISBN FROM tb_reserva WHERE ID_RESERVA = ?", (id_reserva,))
            id_isbn = cursor.fetchone()
            # Verifica se a reserva existe e obtem o ID_ISBN, pois ao executar o emprestimo, o mesmo é removido da tabela reserva
            if id_isbn:
                id_isbn = id_isbn[0]
            else:
                raise ValueError("Reserva não encontrada ou livro não definido.")
            # Obtem o ID_ISBN a partir da ID_RESERVA, para verificar se há estoque:
            cursor.execute("SELECT ID_ISBN FROM tb_reserva WHERE ID_RESERVA = ?", (id_reserva,))
            resultado_isbn = cursor.fetchone()
            id_isbn = resultado_isbn[0]
            # Verifica na tabela livro a quantidade de livros a partir do id_isbn da consulta anterior é maior que 0:
            cursor.execute("SELECT QUANTIDADE FROM tb_livro WHERE ID_ISBN = ?", (id_isbn,))
            resultado_qtde = cursor.fetchone()
            quantidade_livro = resultado_qtde[0]
            # Verifica se a quantidade de livro é maior que zero, caso negativo, retorna erro.
            if quantidade_livro <= 0:
                raise ValueError("O livro não está disponível, verificar o estoque!")
            # Consulta para obter o maior ID_EMPRESTIMO existente para gerar um novo ID_EMPRESTIMO
            cursor.execute("SELECT MAX(ID_EMPRESTIMO) FROM tb_emprestimo")
            max_id_emprestimo = cursor.fetchone()[0]
            # Função para gerar o novo ID_EMPRESTIMO
            if max_id_emprestimo is None:
                max_id_emprestimo = 0
            id_emprestimo = max_id_emprestimo + 1
            # otendo o id do usuario da tabela reserva
            cursor.execute("SELECT ID_USUARIO FROM tb_reserva WHERE ID_RESERVA = ?", (id_reserva,))
            id_usuario_reserva = cursor.fetchone()[0]
            # Registra um novo empréstimo com o próximo ID_EMPRESTIMO gerado
            cursor.execute("INSERT INTO tb_emprestimo (ID_EMPRESTIMO, DATA_RETIRADA, DATA_DEVOLUCAO, SITUACAO_EMPRESTIMO, ID_USUARIO, ID_ISBN ) VALUES (?, ?, ?, ?, ?, ?)",
                           (id_emprestimo, data_atual_formatada, data_futura_formatada, "Emprestado", id_usuario_reserva, id_isbn))
            # Faz a contagem dos registros para exibir na tela após a atualização
            cursor.execute("SELECT COUNT(*) FROM tb_emprestimo")
            numero_de_emprestimos = cursor.fetchone()[0]       
            # Atualizando a quantidade de livros na tb_livro a partir do emprestimo de um livro:
            cursor.execute("UPDATE tb_livro SET QUANTIDADE = QUANTIDADE - 1 WHERE ID_ISBN = ?", (id_isbn,))
            # Removendo a registro da reserva a partir do emprestimo do livro
            cursor.execute("DELETE FROM tb_reserva WHERE ID_RESERVA = ?", (id_reserva,))
            # Salvando os dados na tabela
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_id_reserva.delete(0, 'end')      
            # Atualizar a mensagem na parte inferior da janela
            mensagem_label_emprestimo.config(text="Empréstimo Registrado", fg="green")
            mensagem_label_total_emprestimo.config(text=f"{numero_de_emprestimos} empréstimo(s) registrado(s).", fg="blue")
        except ValueError as ve:
            # Exibe uma mensagem de erro se alguma informação estiver faltando ou inválida
            mensagem_label_emprestimo.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            # Em caso de erro do SQLite, exibir mensagem de erro na parte inferior da janela
            mensagem_label_emprestimo.config(text="Erro: " + str(e), fg="red")                        
        except Exception as e:
            mensagem_label_emprestimo.config(text="Informação incompleta: " + str(e), fg="red")
    # Função para atualizar o status do livro
    def atualizar_status():
        # Abre uma conexão com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Verifica se usuario e livro não estão vazios
        id_emprestimo = combobox_atualizar_empretimo.get()
        novo_status = combobox_selecionar_status.get()
        # Tenta executa a função e caso haja erro, retorna o erro        
        try:
            # Verifica se id_emprestimo e nova_situacao não estão vazios
            if not id_emprestimo or not novo_status:
                raise ValueError("Por favor, selecione todas as informações.")
            id_emprestimo = int(id_emprestimo)  # Converte o ID_EMPRESTIMO para inteiro
            # Obtém o status atual do empréstimo
            cursor.execute("SELECT SITUACAO_EMPRESTIMO FROM tb_emprestimo WHERE ID_EMPRESTIMO = ?", (id_emprestimo,))
            status_atual = cursor.fetchone()[0]
            # Verifica se o novo status é diferente do status atual
            if novo_status == status_atual:
                raise ValueError("O status já é o mesmo selecionado.")            
            # Atualiza a situação do empréstimo e a data da alteracao da situação com base no ID_EMPRESTIMO
            cursor.execute("UPDATE tb_emprestimo SET SITUACAO_EMPRESTIMO = ?, DATA_DEVOLUCAO = ? WHERE ID_EMPRESTIMO = ?",
                           (novo_status, data_atual_formatada, id_emprestimo))
            # Obtendo o ID_ISBN a partir da consuta para atualizar a quantidade em tb_livro, quando o livro é devolvido
            cursor.execute("SELECT ID_ISBN FROM tb_emprestimo WHERE ID_EMPRESTIMO = ?", (id_emprestimo,))
            resultado = cursor.fetchone()
            id_isbn = resultado[0]
            # Atualizando a quantidade da tb_livros a partir da situação do livro para o Status Devolvido
            cursor.execute("UPDATE tb_livro SET QUANTIDADE = QUANTIDADE + 1 WHERE ID_ISBN = ? AND ? = 'Devolvido'", 
                           (id_isbn, novo_status))
            # Fechando conexao e salvando alteraccoes
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_atualizar_empretimo.delete(0, 'end')      
            combobox_selecionar_status.delete(0, 'end')      
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_emprestimo.config(text="Situação do empréstimo atualizada com sucesso", fg="green")
        # Retorna uma mensage de erro em caso de falha na execução da função ou erro nos dados.           
        except ValueError as ve:
            mensagem_label_emprestimo.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_emprestimo.config(text="Erro ao atualizar situação do empréstimo: " + str(e), fg="red")
        except Exception as e:
            mensagem_label_emprestimo.config(text="Informação incompleta: " + str(e), fg="red")            
    # Lista de Opções
    lista_status = ['Devolvido','Extraviado','Reembolsado']
    # Obtendo a lista de Usuarios da Tabela Reserva
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para selecionar todos os valores da coluna Nome
    cursor.execute("SELECT ID_RESERVA FROM tb_reserva")
    # Recupera todos os resultados da consulta em uma lista
    id_reservas = [registro_1[0] for registro_1 in cursor.fetchall()]
    # Obtendo a lista de livros emprestados pelo ID_EMPRESTIMO.
    cursor.execute("SELECT ID_EMPRESTIMO FROM tb_emprestimo WHERE SITUACAO_EMPRESTIMO = 'Emprestado'")
    # Recupera todos os resultados da consulta em uma lista
    emprestimo_status = [registro[0] for registro in cursor.fetchall()]
    # Fechar a conexão
    conn.commit()
    conn.close()    
    # Criando a Janela
    janela_emprestimo = tk.Toplevel()
    # Formatando o titulo
    janela_emprestimo.title('Registro de Empréstimos')
    # Cabeçalho da tela de cadastro
    label_cadastro_emprestimos = tk.Label(janela_emprestimo, text='REGISTRO DE EMPRESTIMOS', 
                                          borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=35, height=2)
    label_cadastro_emprestimos.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=4)
    # Label e Caixa de seleção de usuarios
    label_seleciona_id_reserva = tk.Label(janela_emprestimo, text='Selecionar ID da Reserva: ', anchor='w')
    label_seleciona_id_reserva.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
    combobox_seleciona_id_reserva = ttk.Combobox(janela_emprestimo, values=id_reservas)
    combobox_seleciona_id_reserva.grid(row=1,column=1, padx=10, pady=10, sticky='nsew')
    # Label e Periodo de Inicio do Empréstimo
    label_datainicio_emprestimo  = tk.Label(janela_emprestimo, text="Data Inicial do Empréstimo:", anchor='w')
    label_datainicio_emprestimo.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
    calendario_datainicio_emprestimo = tk.Label(janela_emprestimo, text=f"{data_atual_formatada}", anchor='e')
    calendario_datainicio_emprestimo.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')
    # Label e Periodo de Final do Empréstimo
    label_datafinal_emprestimos = tk.Label(janela_emprestimo, text="Data Final do Empréstimo:", anchor='w')
    label_datafinal_emprestimos.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
    calendario_datafinal_emprestimo = tk.Label(janela_emprestimo, text=f"{data_futura_formatada}", anchor='e')
    calendario_datafinal_emprestimo.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
    # botão para emprestar livro
    botao_emprestar = tk.Button(janela_emprestimo, text='Emprestar', command=cadastrar_emprestimos)
    botao_emprestar.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')
    # Cabecalho da atualização dos dados de emprestimo
    label_status_emprestimos = tk.Label(janela_emprestimo, text='ATUALIZAR STATUS DE EMPRESTIMOS', 
                                        borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=35, height=2)
    label_status_emprestimos.grid(row=6, column=0, padx=10, pady=10, sticky='nsew', columnspan=4)
    # label e caixa de seleção para selecionar o ID_EMPRESTIMO a partir da emprestimo_status
    label_selecionar_id_emprestimo = tk.Label(janela_emprestimo, text='Selecione o ID do Emprestimo: ', anchor='w')
    label_selecionar_id_emprestimo.grid(row=7, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    combobox_atualizar_empretimo = ttk.Combobox(janela_emprestimo, values=emprestimo_status)
    combobox_atualizar_empretimo.grid(row=7,column=1,  padx=10, pady=10, sticky='nsew')
    # Label de uma lista de opções para atualizar o status a partir da lista_status
    label_atualizar_status = tk.Label(janela_emprestimo, text='Selecione o Status: ', anchor='w')
    label_atualizar_status.grid(row=8, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')    
    combobox_selecionar_status = ttk.Combobox(janela_emprestimo, values=lista_status)
    combobox_selecionar_status.grid(row=8,column=1, padx=10, pady=10, sticky='nsew')
    # Botão de atualizar o status
    botao_atualizar_status_emprestimo = tk.Button(janela_emprestimo, text='Atualizar Status', command=atualizar_status)
    botao_atualizar_status_emprestimo.grid(row=9, column=1, padx=10, pady=10, sticky='nsew')
    # Criar o rótulo para exibir mensagens
    mensagem_label_emprestimo = tk.Label(janela_emprestimo, text="", fg="green")
    mensagem_label_emprestimo.grid(row=10, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    mensagem_label_total_emprestimo = tk.Label(janela_emprestimo, text="", fg="green")
    mensagem_label_total_emprestimo.grid(row=11, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    # Botão para voltar ao menu anterior
    botao_emprestar_voltar = tk.Button(janela_emprestimo, text='Voltar', command=janela_emprestimo.destroy)
    botao_emprestar_voltar.grid(row=12, column=0, padx=10, pady=10, sticky='nsew')    
    # Rodando a Janela
    janela_emprestimo.mainloop()        

# 5ª. PARTE - CONSULTA DE USUARIOS, LIVROS, RESERVAS E EMPRESTIMOS

# Função para abrir a janela de consulta dos dados
def consultar_dados():
    # Consultando os totois de registros
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta o total de registros na tabela tb_usuario
    cursor.execute("SELECT COUNT(*) FROM tb_usuario  WHERE ID_USUARIO > 20230000")
    total_usuarios = cursor.fetchone()[0]
    # Consulta o total de registros na tabela tb_livro
    cursor.execute("SELECT COUNT(*) FROM tb_livro")
    total_livros = cursor.fetchone()[0]
    # Consulta o total de registros na tabela tb_reserva
    cursor.execute("SELECT COUNT(*) FROM tb_reserva")
    total_reservas = cursor.fetchone()[0]
    # Consulta o total de registros na tabela tb_emprestimo
    cursor.execute("SELECT COUNT(*) FROM tb_emprestimo")
    total_emprestimos = cursor.fetchone()[0]
    #Fechando a conexao com o Banco de dados
    conn.close()

    # Função para consultar os usuarios
    def consultar_usuarios():
        # obtem o nome da coluna
        coluna_tb_usuario = combobox_label_ordena_consulta_usuario.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se coluna_tb_usuario não está vazio
            if not coluna_tb_usuario:
                raise ValueError("Por favor, preencha todas as informações.")   
            # Conectar ao banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Consulta SQL para selecionar todos os dados da tabela de usuários
            consulta_sql = f"SELECT ID_USUARIO, NOME, TELEFONE, EMAIL FROM tb_usuario  WHERE ID_USUARIO > 20230000 ORDER BY {coluna_tb_usuario} ASC "
            # Executar a consulta SQL
            cursor.execute(consulta_sql)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_label_ordena_consulta_usuario.delete(0, 'end')      
            # Limpar a caixa de texto
            caixa_retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            caixa_retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                caixa_retorno_consulta.insert(tk.END, str(resultado) + "\n\n")
            # Atualiza a mensagem na parte inferior da janela                
            mensagem_label_total_consulta.config(text=f"Total: {total_usuarios} usuário(s) cadastrado(s).", fg="blue")   
            mensagem_label_connsulta_alerta.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Retorna uma mensagem de erro em caso de falha na execução da função ou erro nos dados.              
        except ValueError as ve:
            mensagem_label_connsulta_alerta.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_connsulta_alerta.config(text="Erro ao consultar dados" + str(e), fg="red")                    
        except Exception as e:
            mensagem_label_connsulta_alerta.config(text="Informação incompleta: " + str(e), fg="red")                 

    # Função para consutlar os livros
    def consultar_livros():
        # Obtem o nome da coluna
        coluna_tb_livro = combobox_label_ordena_consulta_livro.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se coluna_tb_livro  não está vazia
            if not coluna_tb_livro:
                raise ValueError("Por favor, preencha todas as informações.")   
            # Conectar ao banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Consulta SQL para selecionar todos os dados da tabela de usuários
            consulta_sql = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, VALOR, QUANTIDADE, DESCRICAO FROM tb_livro ORDER BY {coluna_tb_livro} ASC"
            # Executar a consulta SQL
            cursor.execute(consulta_sql)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            #consultando o valor total em livros
            cursor.execute("SELECT SUM(VALOR) FROM tb_livro")            
            valor_total = cursor.fetchone()[0]
            # no caso do valor está zerado e não gerar erro
            if valor_total is None:
                valor_total = 0            
            valor_real =  "{:.2f}".format(valor_total).replace('.', ',')            
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_label_ordena_consulta_livro.delete(0, 'end')      
            # Limpar a caixa de texto
            caixa_retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            caixa_retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                caixa_retorno_consulta.insert(tk.END, str(resultado) + "\n\n")
            mensagem_label_total_consulta.config(text=f"{total_livros} livro(s) cadastrado(s), avaliado(s) em R$ {valor_real}.", fg="blue")         
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_connsulta_alerta.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Retorna uma mensagem de erro em caso de falha na execução da função ou erro nos dados.               
        except ValueError as ve:
            mensagem_label_connsulta_alerta.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_connsulta_alerta.config(text="Erro ao consultar dados" + str(e), fg="red")   
        except Exception as e:
            mensagem_label_connsulta_alerta.config(text="Informação incompleta: " + str(e), fg="red")               
    
    # Função para consultar as reservas
    def consultar_reservas():
        # Obtem o nome da coluna
        coluna_tb_reserva = combobox_label_ordena_consulta_reserva.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se coluna_tb_reserva não está vazia
            if not coluna_tb_reserva:
                raise ValueError("Por favor, preencha todas as informações.")           
            # Conectar ao banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Consulta SQL para selecionar todos os dados da tb_reserva
            consulta_sql = f"SELECT * FROM tb_reserva ORDER BY {coluna_tb_reserva} ASC"
            # Executar a consulta SQL
            cursor.execute(consulta_sql)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_label_ordena_consulta_reserva.delete(0, 'end')      
            # # Limpar a caixa de texto
            # Limpar o texto da caixa de texto
            caixa_retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            caixa_retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                caixa_retorno_consulta.insert(tk.END, str(resultado) + "\n\n")                
            mensagem_label_total_consulta.config(text=f"Total: {total_reservas} livro(s) reservado(s).", fg="blue")   
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_connsulta_alerta.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Retorna uma mensagem de erro em caso de falha na execução da função ou erro nos dados.   
        except ValueError as ve:
            mensagem_label_connsulta_alerta.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_connsulta_alerta.config(text="Erro ao consultar dados" + str(e), fg="red")        
        except Exception as e:
            mensagem_label_connsulta_alerta.config(text="Informação incompleta: " + str(e), fg="red")               
         
    # Função para consultar empréstimos
    def consultar_emprestimo():
        # Obtem o nome da coluna
        coluna_tb_emprestimo = combobox_label_ordena_consulta_emprestimo.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se coluna_tb_emprestimo não está vazia
            if not coluna_tb_emprestimo:
                raise ValueError("Por favor, preencha todas as informações.")           
            # Conectar ao banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Consulta SQL para selecionar todos os dados da tb_emprestimo
            consulta_sql = f"SELECT * FROM tb_emprestimo ORDER BY {coluna_tb_emprestimo} ASC"
            # Executar a consulta SQL
            cursor.execute(consulta_sql)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_label_ordena_consulta_emprestimo.delete(0, 'end')      
            # Limpar a caixa de texto
            caixa_retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            caixa_retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                caixa_retorno_consulta.insert(tk.END, str(resultado) + "\n\n")
            mensagem_label_total_consulta.config(text=f"Total: {total_emprestimos} empréstimo(s) registrado(s).", fg="blue") 
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_connsulta_alerta.config(text="Consulta Realizada Com Sucesso!", fg="green")        
        # Retorna uma mensagem de erro em caso de falha na execução da função ou erro nos dados.   
        except ValueError as ve:
            mensagem_label_connsulta_alerta.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_connsulta_alerta.config(text="Erro ao consultar dados" + str(e), fg="red") 
        except Exception as e:
            mensagem_label_connsulta_alerta.config(text="Informação incompleta: " + str(e), fg="red")               

    # Funções de filtro de usuarios
    
    # Função abre um nova janela de filtro de usuarios
    def filtro_de_usuario():
        # Função para filtrar a consulta de usuarios
        def filtrar_usuarios():
            # Abre uma conexão com o banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Obtendo a variavel pelo nome dos usuarios
            consulta_usuarios_cadastrado = combobox_seleciona_nome.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_usuarios_cadastrado não está vazia
                if not consulta_usuarios_cadastrado:
                    raise ValueError("Por favor, selecione um usuário.")   
                # Consulta SQL para selecionar todos os dados da tabela de usuários
                consulta_de_usuario = f"SELECT ID_USUARIO, NOME, TELEFONE, EMAIL FROM tb_usuario  WHERE ID_USUARIO > 20230000 AND NOME = '{consulta_usuarios_cadastrado}'"
                # Executar a consulta SQL 
                cursor.execute(consulta_de_usuario)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Salva e Fechar a conexão com o banco de dados
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_nome.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informações 
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe uma mensagem de erro se alguma informação estiver faltando ou inválida
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")  
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                   
    
        # Obtendo a lista pelo nome dos usuarios
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Consulta nomes
        cursor.execute("SELECT NOME FROM tb_usuario WHERE ID_USUARIO > 20230000")
        # Recupera todos os resultados da consulta em uma lista
        usuarios = [registro1[0] for registro1 in cursor.fetchall()]
        # Salvando e fechando a conexao com o banco de dados
        conn.commit()
        conn.close()
        # Criando a Janela
        janela_consulta_cadastro = tk.Toplevel()
        # Formatando o titulo
        janela_consulta_cadastro.title('Consulta Cadastros')
        # Cabeçalho da tela de cadastro
        label_consulta_livros = tk.Label(janela_consulta_cadastro, text='CONSULTA CADASTRO', 
                                         borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
        label_consulta_livros.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=5)
        # Label, caixa de seleção e botão para a Lista de titulos
        label_seleciona_nome = tk.Label(janela_consulta_cadastro, text='Selecione por Nome: ', anchor='w')
        label_seleciona_nome.grid(row=1, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_nome = ttk.Combobox(janela_consulta_cadastro, values=usuarios)
        combobox_seleciona_nome.grid(row=1,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_nomes = tk.Button(janela_consulta_cadastro, text='Filtrar Usuarios', command=filtrar_usuarios)
        botao_consulta_nomes.grid(row=1, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de usuarios
        retorno_consulta = tk.Text(janela_consulta_cadastro, width=60, height=10)
        retorno_consulta.grid(row=2, column=0, columnspan=4,  padx=5, pady=5, sticky='nsew')
        # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
        mensagem_label_retorno_consultas = tk.Label(janela_consulta_cadastro, text="", fg="green")
        mensagem_label_retorno_consultas.grid(row=3, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
        # Botão Sair
        botao_voltar = tk.Button(janela_consulta_cadastro, text='Voltar', command=janela_consulta_cadastro.destroy)
        botao_voltar.grid(row=4, column=3, padx=5, pady=5, sticky='nsew')
        # Rodando a Janela
        janela_consulta_cadastro.mainloop()            
        
    # Função para filtro de livros 

    # Função abre um nova janela de consultar filtro avancado de livros
    def filtro_de_livros():
        # Função para consulta por titulo
        def consulta_titulo():
            # Abre uma conexão com o banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Obtendo a variavel consulta_titulo
            consulta_titulo = combobox_seleciona_titulos.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_titulo não está vazia
                if not consulta_titulo:
                    raise ValueError("Por favor, selecione um livro pelo título.")   
                # Consulta SQL para selecionar todos os dados da tb_livro pelo titulo
                consulta_sql_titulos = f"SELECT * FROM tb_livro WHERE TITULO = '{consulta_titulo}'"
                # Executar a consulta SQL por titulo
                cursor.execute(consulta_sql_titulos)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Salva e Fechar a conexão com o banco de dados
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_titulos.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informações 
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe uma mensagem em caso de erro               
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")           
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                   

        # Função para consulta por autor
        def consulta_autores():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel consulta_autores
            consulta_autores = combobox_seleciona_autores.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_autores não está vazia
                if not consulta_autores:
                    raise ValueError("Por favor, selecione o autor.")   
                # Consulta SQL para selecionar todos os dados da tabela de usuários
                consulta_sql_autores = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, VALOR, QUANTIDADE, DESCRICAO FROM tb_livro WHERE AUTOR = '{consulta_autores}'"
                # Executar a consulta SQL
                cursor.execute(consulta_sql_autores)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_autores.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe uma mensagem de erro                 
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")   
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                     
                
        # Função para consulta por editora
        def consulta_editora():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel 
            consulta_editora = combobox_seleciona_editora.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_editora não esta vazia
                if not consulta_editora:
                    raise ValueError("Por favor, selecione o editora.")   
                # Consulta SQL para selecionar todos os dados da tabela de usuários
                consulta_sql_editora = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, VALOR, QUANTIDADE, DESCRICAO FROM tb_livro WHERE EDITORA = '{consulta_editora}'"
                # Executar a consulta SQL
                cursor.execute(consulta_sql_editora)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_editora.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe uma mensagem de erro                 
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                # Em caso de erro do SQLite, exibir mensagem de erro na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")    
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                  
                
        # Consulta por ano
        def consulta_ano():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel 
            consulta_ano = combobox_seleciona_ano.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_ano não esta vazia
                if not consulta_ano:
                    raise ValueError("Por favor, selecione o editora.")   
                # Consulta SQL para selecionar todos os dados da tabela de usuários
                consulta_sql_ano = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, VALOR, QUANTIDADE, DESCRICAO FROM tb_livro WHERE ANO = {consulta_ano}"
                # Executar a consulta SQL
                cursor.execute(consulta_sql_ano)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_ano.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe mensagem de erro em caso de problemas com o codigo
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")   
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")           

        # função para consultar o ISBN
        def consulta_isbn():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel
            consulta_isbn = caixa_texto_consulta_isbn.get()      
            try:
                # Obtendo o ID_ISBN digitado pelo usuário
                consulta_isbn = caixa_texto_consulta_isbn.get()
                # Verifica se a entrada não está vazia e se informar preenchia é um número
                if not consulta_isbn:
                    raise ValueError("Por favor, insira um ID_ISBN.")  
                 # Verifica se a entrada é um valor numérico
                if not consulta_isbn.isnumeric():
                    raise ValueError("Por favor, insira apenas números para o ID_ISBN.")
                # Consulta SQL para selecionar os dados com base no ID_ISBN
                consulta_sql_isbn = f"SELECT * FROM tb_livro WHERE ID_ISBN = {consulta_isbn}"    
                # Executa a consulta SQL
                cursor.execute(consulta_sql_isbn)
                # Obtém os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obtém o resultado da consulta
                resultado = cursor.fetchone()
                # Fecha a conexão com o banco de dados
                conn.close()
                # Se resultado for None, o ID_ISBN não foi encontrado
                if resultado is None:
                    mensagem_label_retorno_consultas.config(text="ID_ISBN não encontrado no banco de dados.", fg="red")
                    retorno_consulta.delete(1.0, tk.END)  # Limpar a caixa de resultado
                else:
                    # Limpa o conteúdo das caixas de texto
                    caixa_texto_consulta_isbn.delete(0, 'end')      
                    # Limpar a caixa de texto caso haja informacao
                    retorno_consulta.delete(1.0, tk.END)
                    # Inserir os nomes das colunas na caixa de texto
                    retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                    # Preencher a caixa de texto com os resultados
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")
                    # Atualiza a mensagem na parte inferior da janela
                    mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")

            # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas            
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")        
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")         

        # Codigo da janela filtro de livros
    
        # Abrindo uma conexao com o Banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Consulta titulos
        cursor.execute("SELECT TITULO FROM tb_livro")
        # Recupera todos os resultados da consulta em uma lista
        lista_titulos =[registro1[0] for registro1 in cursor.fetchall()]
        titulos = sorted(list(set(lista_titulos)))
        # Consulta autores
        cursor.execute("SELECT AUTOR FROM tb_livro")
        # Recupera todos os resultados da consulta em uma lista
        lista_autores = [registro2[0] for registro2 in cursor.fetchall()]
        autores = sorted(list(set(lista_autores)))
        # Recupera todos os resultados da consulta em uma lista
        cursor.execute("SELECT EDITORA FROM tb_livro")
        # Recupera todos os resultados da consulta em uma lista
        lista_editora = [registro3[0] for registro3 in cursor.fetchall()]
        editora = sorted(list(set(lista_editora)))
        # Recupera todos os resultados da consulta em uma lista
        cursor.execute("SELECT ANO FROM tb_livro")
        # Recupera todos os resultados da consulta em uma lista
        lista_ano = [registro4[0] for registro4 in cursor.fetchall()]
        ano = sorted(list(set(lista_ano)))
        # Salva e Fechar a conexão
        conn.commit()
        conn.close()
        # Criando a Janela
        janela_consultas = tk.Toplevel()
        # Formatando o titulo
        janela_consultas.title('Consulta livros')
        # Cabeçalho da tela de cadastro
        label_consulta_livros = tk.Label(janela_consultas, text='CONSULTA LIVROS', 
                                         borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
        label_consulta_livros.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=5)
        # Label, caixa de seleção e botão para a Lista de titulos
        label_seleciona_titulos = tk.Label(janela_consultas, text='Selecione por Título: ', anchor='w')
        label_seleciona_titulos.grid(row=1, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_titulos = ttk.Combobox(janela_consultas, values=titulos)
        combobox_seleciona_titulos.grid(row=1,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_livros = tk.Button(janela_consultas, text='Consulta Títulos', command=consulta_titulo)
        botao_consulta_livros.grid(row=1, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de Autores
        label_seleciona_autores = tk.Label(janela_consultas, text='Selecione o Autor: ', anchor='w')
        label_seleciona_autores.grid(row=2, column=0, padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_autores = ttk.Combobox(janela_consultas, values=autores)
        combobox_seleciona_autores.grid(row=2,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_autores = tk.Button(janela_consultas, text='Consulta Autor', command=consulta_autores)
        botao_consulta_autores.grid(row=2, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de editoras
        label_seleciona_editora = tk.Label(janela_consultas, text='Selecione a Editora: ', anchor='w')
        label_seleciona_editora.grid(row=3, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_editora = ttk.Combobox(janela_consultas, values=editora)
        combobox_seleciona_editora.grid(row=3,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_editora = tk.Button(janela_consultas, text='Consulta Editora', command=consulta_editora)
        botao_consulta_editora.grid(row=3, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de anos de publicacao                
        label_seleciona_ano = tk.Label(janela_consultas, text='Selecione o Ano: ', anchor='w')
        label_seleciona_ano.grid(row=4, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_ano = ttk.Combobox(janela_consultas, values=ano)
        combobox_seleciona_ano.grid(row=4,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_ano = tk.Button(janela_consultas, text='Consulta Ano', command=consulta_ano)
        botao_consulta_ano.grid(row=4, column=4,  padx=5, pady=5, sticky='nsew')
        #label e caixa de texto consulta isbn
        label_consulta_isbn = tk.Label(janela_consultas, text='Informe o número do ISBN: ', anchor='w')
        label_consulta_isbn.grid(row=5, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        caixa_texto_consulta_isbn = tk.Entry(janela_consultas, width=40)
        caixa_texto_consulta_isbn.grid(row=5,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_isbn = tk.Button(janela_consultas, text='Consulta ISBN', command=consulta_isbn)
        botao_consulta_isbn.grid(row=5, column=4,  padx=5, pady=5, sticky='nsew')           
        # Retorno em uma caixa de texto com o resultado da consulta realizada
        retorno_consulta = tk.Text(janela_consultas, width=80, height=10)
        retorno_consulta.grid(row=6, column=0, columnspan=4,  padx=5, pady=5, sticky='nsew')
        # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
        mensagem_label_retorno_consultas = tk.Label(janela_consultas, text="", fg="green")
        mensagem_label_retorno_consultas.grid(row=7, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
        # Botão Sair
        botao_sair = tk.Button(janela_consultas, text='Voltar', command=janela_consultas.destroy)
        botao_sair.grid(row=8, column=3,  padx=5, pady=5, sticky='nsew')
        # Rodando a Janela
        janela_consultas.mainloop()                            
            
    # Função para filtro de reserva de livros

    # Função abre um nova janela de consultar reservas
    def filtro_de_reserva():
        # Função para consulta por id_reserva
        def consulta_id_reserva():
            # Abre uma conexão com o banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Obtendo a variavel
            consulta_id_reserva = combobox_seleciona_id_reserva.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_id_reserva não está vazia
                if not consulta_id_reserva:
                    raise ValueError("Por favor, selecione um ID de Reserva.")   
                # Consulta SQL para selecionar todos os dados da tb_reserva
                consulta_sql_reservas_id = f"SELECT * FROM tb_reserva WHERE ID_RESERVA = {consulta_id_reserva}"
                # Executar a consulta SQL 
                cursor.execute(consulta_sql_reservas_id)
                # Obter os nomes das colunas da tb_reserva
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Salva e Fechar a conexão com o banco de dados
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_id_reserva.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informações 
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Retorna uma mensagem de erro em caso de falha
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")     
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                    

        # Função para consulta por autor
        def consulta_id_usuario():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel 
            consulta_id_usuario = combobox_seleciona_id_usuario.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_id_usuario não está vazia
                if not consulta_id_usuario:
                    raise ValueError("Por favor, selecione um ID de Usuário.")   
                # Consulta SQL para selecionar todos os dados da tb_reserva
                consulta_sql_usuarios = f"SELECT * FROM tb_reserva WHERE ID_USUARIO = {consulta_id_usuario}"
                # Executar a consulta SQL
                cursor.execute(consulta_sql_usuarios)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_id_usuario.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            #Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")      
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                  
                
        # Função para consulta por editora
        def consulta_id_isbn():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel 
            consulta_id_isbn = combobox_seleciona_id_isbn.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_id_isbn não está vazia
                if not consulta_id_isbn:
                    raise ValueError("Por favor, selecione um ID ISBN.")   
                # Consulta SQL para selecionar todos os dados da tb_reserva
                consulta_sql_isbn = f"SELECT * FROM tb_reserva WHERE ID_ISBN = {consulta_id_isbn}"
                # Executar a consulta SQL
                cursor.execute(consulta_sql_isbn)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_id_isbn.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            #Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")      
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")              
                
        # Abrindo conexão com Banco de Dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Consulta ID_RESERVA
        cursor.execute("SELECT ID_RESERVA FROM tb_reserva")
        # Recupera todos os resultados da consulta em uma lista
        lista_id_reservas =[registro1[0] for registro1 in cursor.fetchall()]
        id_reserva_tb_reservas = sorted(list(set(lista_id_reservas)))
        # Consulta ID_USUARIO
        cursor.execute("SELECT ID_USUARIO FROM tb_reserva")
        # Recupera todos os resultados da consulta em uma lista
        lista_id_usuario_tb_reserva = [registro2[0] for registro2 in cursor.fetchall()]
        id_usuario_reserva = sorted(list(set(lista_id_usuario_tb_reserva)))
        # Consulta ID_ISBN
        cursor.execute("SELECT ID_ISBN FROM tb_reserva")
        # Recupera todos os resultados da consulta em uma lista
        lista_id_isbn_reservas = [registro3[0] for registro3 in cursor.fetchall()]
        id_isbn_reservas = sorted(list(set(lista_id_isbn_reservas)))
        # Salva e Fechar a conexão
        conn.commit()
        conn.close()
        
        # Criando a Janela
        janela_filtro_reserva = tk.Toplevel()
        # Formatando o titulo
        janela_filtro_reserva.title('Consulta Reservas')
        # Cabeçalho da tela de cadastro
        label_consulta_livros = tk.Label(janela_filtro_reserva, text='CONSULTA RESERVAS', 
                                         borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
        label_consulta_livros.grid(row=0, column=0,  padx=5, pady=5, sticky='nsew', columnspan=5)
        # Label, caixa de seleção e botão para a Lista de titulos
        label_seleciona_id_reserva = tk.Label(janela_filtro_reserva, text='Selecione por ID da Reserva: ', anchor='w')
        label_seleciona_id_reserva.grid(row=1, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_id_reserva = ttk.Combobox(janela_filtro_reserva, values=id_reserva_tb_reservas)
        combobox_seleciona_id_reserva.grid(row=1,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_id_reserva = tk.Button(janela_filtro_reserva, text='Consulta ID Reserva', command= consulta_id_reserva)
        botao_consulta_id_reserva.grid(row=1, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de Autores
        label_seleciona_id_usuario = tk.Label(janela_filtro_reserva, text='Selecione o ID do Usuário: ', anchor='w')
        label_seleciona_id_usuario.grid(row=2, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_id_usuario = ttk.Combobox(janela_filtro_reserva, values=id_usuario_reserva)
        combobox_seleciona_id_usuario.grid(row=2,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_id_usuario = tk.Button(janela_filtro_reserva, text='Consulta ID Usuario', command=consulta_id_usuario)
        botao_consulta_id_usuario.grid(row=2, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de editoras
        label_seleciona_id_isbn = tk.Label(janela_filtro_reserva, text='Selecione o ID do ISBN: ', anchor='w')
        label_seleciona_id_isbn.grid(row=3, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_id_isbn = ttk.Combobox(janela_filtro_reserva, values=id_isbn_reservas)
        combobox_seleciona_id_isbn.grid(row=3,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_id_isbn = tk.Button(janela_filtro_reserva, text='Consulta ID ISBN', command=consulta_id_isbn)
        botao_consulta_id_isbn.grid(row=3, column=4,  padx=5, pady=5, sticky='nsew')
        # Retorno em uma caixa de texto com o resultado da consulta realizada
        retorno_consulta = tk.Text(janela_filtro_reserva, width=80, height=10)
        retorno_consulta.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
        mensagem_label_retorno_consultas = tk.Label(janela_filtro_reserva, text="", fg="green")
        mensagem_label_retorno_consultas.grid(row=6, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
        # Botão Sair
        botao_sair = tk.Button(janela_filtro_reserva, text='Voltar', command=janela_filtro_reserva.destroy)
        botao_sair.grid(row=7, column=3, padx=5, pady=5, sticky='nsew')
        # Rodando a Janela
        janela_filtro_reserva.mainloop()                  

    # Função de Filtro de Emprestimo de livros
    
    # Função abre uma janela de filtro de emprestimos
    def filtro_de_emprestimo():
        # Função para consulta por id_emprestimo
        def consulta_id_emprestimo():
            # Abre uma conexão com o banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # Obtendo a variavel
            consulta_id_emprestimo = combobox_seleciona_id_emprestimo.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_id_emprestimo não está vazia
                if not consulta_id_emprestimo:
                    raise ValueError("Por favor, selecione um ID de Reserva.")   
                # Consulta SQL para selecionar todos os dados da tb_emprestimo
                consulta_sql_emprestimo = f"SELECT * FROM tb_emprestimo WHERE ID_EMPRESTIMO = {consulta_id_emprestimo}"
                # Executar a consulta SQL 
                cursor.execute(consulta_sql_emprestimo)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Salva e Fechar a conexão com o banco de dados
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_id_emprestimo.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informações 
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            #Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")      
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                

        # Função para consulta por id de usuario do emprestimo
        def consulta_id_usuario_emprestimo():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel
            consulta_id_usuario_emprestimo = combobox_seleciona_id_usuario_emprestimo.get()

            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_id_usuario_emprestimo não está vazia
                if not consulta_id_usuario_emprestimo:
                    raise ValueError("Por favor, selecione um ID de Usuário.")   
                # Consulta SQL para selecionar todos os dados da tabela de usuários
                consulta_sql_usuarios_emprestimo = f"SELECT * FROM tb_emprestimo WHERE ID_USUARIO = {consulta_id_usuario_emprestimo}"

                # Executar a consulta SQL
                cursor.execute(consulta_sql_usuarios_emprestimo)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_id_usuario_emprestimo.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")      
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")                
                
        # Função para consulta por isbn
        def consulta_id_isbn_emprestimo():
            # abre uma conexão com o Banco de dados
            conn = sqlite3.connect('biblioteca_V1.db')
            cursor = conn.cursor()
            # obtendo a variavel 
            consulta_id_isbn_emprestimo = combobox_seleciona_id_isbn_emprestimo.get()
            # Tenta executa a função e caso haja erro, retorna o erro
            try:
                # Verifica se consulta_id_isbn_emprestimo não está vazia
                if not consulta_id_isbn_emprestimo:
                    raise ValueError("Por favor, selecione um ID ISBN.")   
                # Consulta SQL para selecionar todos os dados da tb_emprestimo
                consulta_sql_id_isbn_emprestimo = f"SELECT * FROM tb_emprestimo WHERE ID_ISBN = {consulta_id_isbn_emprestimo}"
                # Executar a consulta SQL
                cursor.execute(consulta_sql_id_isbn_emprestimo)
                # Obter os nomes das colunas da tabela
                nomes_colunas = [description[0] for description in cursor.description]
                # Obter todos os resultados
                resultados = cursor.fetchall()
                # Fechar a conexão com o banco de dados
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_seleciona_id_isbn_emprestimo.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                for resultado in resultados:
                    retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
            except ValueError as ve:
                mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
            except sqlite3.Error as e:
                mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")      
            except Exception as e:
                mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")              
                
        # Obtendo a lista de titulos e autores e retornando uma lista
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Consulta ID_EMPRESTIMO
        cursor.execute("SELECT ID_EMPRESTIMO FROM tb_emprestimo")
        # Recupera todos os resultados da consulta em uma lista
        lista_id_emprestimos =[registro1[0] for registro1 in cursor.fetchall()]
        lista_emprestimo = sorted(list(set(lista_id_emprestimos)))
        # Consulta ID_USUARIO
        cursor.execute("SELECT ID_USUARIO FROM tb_emprestimo")
        # Recupera todos os resultados da consulta em uma lista
        lista_id_usuarios = [registro2[0] for registro2 in cursor.fetchall()]
        lisa_usuarios = sorted(list(set(lista_id_usuarios)))
        # Consulta ID_ISBN        
        cursor.execute("SELECT ID_ISBN FROM tb_emprestimo")
        # Recupera todos os resultados da consulta em uma lista
        lista_id_isbn = [registro3[0] for registro3 in cursor.fetchall()]
        lista_isbn = sorted(list(set(lista_id_isbn)))
        # Salva e Fechar a conexão
        conn.commit()
        conn.close()

        # Criando a Janela
        janela_filtro_emprestimo = tk.Toplevel()
        # Formatando o titulo
        janela_filtro_emprestimo.title('Consulta Emprestimos')
        # Cabeçalho da tela de cadastro
        label_consulta_livros = tk.Label(janela_filtro_emprestimo, text='CONSULTA EMPRESTIMO', 
                                         borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
        label_consulta_livros.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=5)
        # Label, caixa de seleção e botão para a Lista de titulos
        label_seleciona_id_emprestimo = tk.Label(janela_filtro_emprestimo, text='Selecione por ID da Empréstimo: ', anchor='w')
        label_seleciona_id_emprestimo.grid(row=1, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_id_emprestimo = ttk.Combobox(janela_filtro_emprestimo, values=lista_emprestimo)
        combobox_seleciona_id_emprestimo.grid(row=1,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_id_emprestimo = tk.Button(janela_filtro_emprestimo, text='Consulta ID Reserva', command=consulta_id_emprestimo)
        botao_consulta_id_emprestimo.grid(row=1, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de Autores
        label_seleciona_id_usuario_emprestimo = tk.Label(janela_filtro_emprestimo, text='Selecione o ID do Usuário: ', anchor='w')
        label_seleciona_id_usuario_emprestimo.grid(row=2, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_id_usuario_emprestimo = ttk.Combobox(janela_filtro_emprestimo, values=lisa_usuarios)
        combobox_seleciona_id_usuario_emprestimo.grid(row=2,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_id_usuario_emprestimo = tk.Button(janela_filtro_emprestimo, text='Consulta ID Usuario', command=consulta_id_usuario_emprestimo)
        botao_consulta_id_usuario_emprestimo.grid(row=2, column=4,  padx=5, pady=5, sticky='nsew')
        # Label, caixa de seleção e botão para a lista de editoras
        label_seleciona_id_isbn_emprestimo = tk.Label(janela_filtro_emprestimo, text='Selecione o ID do ISBN: ', anchor='w')
        label_seleciona_id_isbn_emprestimo.grid(row=3, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
        combobox_seleciona_id_isbn_emprestimo = ttk.Combobox(janela_filtro_emprestimo, values=lista_isbn)
        combobox_seleciona_id_isbn_emprestimo.grid(row=3,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
        botao_consulta_id_isbn_emprestimo = tk.Button(janela_filtro_emprestimo, text='Consulta ID ISBN', command=consulta_id_isbn_emprestimo)
        botao_consulta_id_isbn_emprestimo.grid(row=3, column=4, padx=5, pady=5, sticky='nsew')
        # Retorno em uma caixa de texto com o resultado da consulta realizada
        retorno_consulta = tk.Text(janela_filtro_emprestimo, width=100, height=10)
        retorno_consulta.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
        mensagem_label_retorno_consultas = tk.Label(janela_filtro_emprestimo, text="", fg="green")
        mensagem_label_retorno_consultas.grid(row=6, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
        # Botão Sair
        botao_sair = tk.Button(janela_filtro_emprestimo, text='Voltar', command=janela_filtro_emprestimo.destroy)
        botao_sair.grid(row=7, column=3,  padx=5, pady=5, sticky='nsew')
        # Rodando a Janela
        janela_filtro_emprestimo.mainloop()                  
        
    # Lista de opções das  colunas para executar as consultas
    opcoes_ordenacao_usuario = ['ID_USUARIO', 'NOME', 'TELEFONE', 'ENDERECO', 'EMAIL']
    opcoes_ordenacao_livro = ['ID_ISBN', 'TITULO', 'AUTOR', 'EDITORA', 'ANO', 'VALOR', 'DESCRICAO']
    opcoes_ordenacao_reserva = ['ID_RESERVA', 'ID_USUARIO', 'ID_ISBN', 'DATA_RESERVA'] 
    opcoes_ordenacao_emprestimo =  ['ID_EMPRESTIMO', 'DATA_RETIRADA', 'DATA_DEVOLUCAO', 'SITUACAO_EMPRESTIMO', 'ID_USUARIO', 'ID_ISBN'] 
    # Criando a Janela de Consulta
    janela_consulta = tk.Toplevel()
    # Formatando a janela de Consulta
    janela_consulta.title('Consulta Dados')
    label_janela_consulta = tk.Label(janela_consulta, text='CONSULTA DE INFORMAÇÕES', 
                                     borderwidth=2,relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_janela_consulta.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew', )
    # Label da Consulta
    label_ordena_subtitulo = tk.Label(janela_consulta, text='CONSULTE USUÁRIOS, LIVROS, RESERVAS E EMPRÉSTIMOS', anchor='center')
    label_ordena_subtitulo.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')    
    # Ordena Usuario
    label_consulta_usuario = tk.Label(janela_consulta, text='Selecione como deseja filtrar os Usuário:', anchor='w')
    label_consulta_usuario.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky='nsew')        
    combobox_label_ordena_consulta_usuario = ttk.Combobox(janela_consulta, values=opcoes_ordenacao_usuario)
    combobox_label_ordena_consulta_usuario.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')   
    botao_consulta_usuario = tk.Button(janela_consulta, text='Consultar', command=consultar_usuarios)
    botao_consulta_usuario.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')  
    # Ordena Livro
    label_consulta_livro = tk.Label(janela_consulta, text='Selecione como deseja filtrar os Livros:', anchor='w')
    label_consulta_livro.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky='nsew')       
    combobox_label_ordena_consulta_livro = ttk.Combobox(janela_consulta, values=opcoes_ordenacao_livro)
    combobox_label_ordena_consulta_livro.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')    
    botao_consulta_livros = tk.Button(janela_consulta, text='Consultar', command=consultar_livros)
    botao_consulta_livros.grid(row=3, column=2, padx=5, pady=5, sticky='nsew')      
    # Ordena Reserva
    label_consulta_reservas = tk.Label(janela_consulta, text='Selecione como deseja filtrar as Reservas:', anchor='w')
    label_consulta_reservas.grid(row=4, column=0, columnspan=1, padx=5, pady=5, sticky='nsew')           
    combobox_label_ordena_consulta_reserva = ttk.Combobox(janela_consulta, values=opcoes_ordenacao_reserva)
    combobox_label_ordena_consulta_reserva.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')    
    botao_consulta_reservas = tk.Button(janela_consulta, text='Consultar', command=consultar_reservas)
    botao_consulta_reservas.grid(row=4, column=2, padx=5, pady=5, sticky='nsew')     
    # Ordena Emprestimo
    label_consulta_emprestimos = tk.Label(janela_consulta, text='Selecione como deseja filtrar os Empréstimos:', anchor='w')
    label_consulta_emprestimos.grid(row=5, column=0, columnspan=1, padx=5, pady=5, sticky='nsew')       
    combobox_label_ordena_consulta_emprestimo = ttk.Combobox(janela_consulta, values=opcoes_ordenacao_emprestimo)
    combobox_label_ordena_consulta_emprestimo.grid(row=5, column=1, padx=5, pady=5, sticky='nsew')  
    botao_consulta_emprestimos = tk.Button(janela_consulta, text='Consultar', command=consultar_emprestimo)
    botao_consulta_emprestimos.grid(row=5, column=2, padx=5, pady=5, sticky='nsew')        
    # Caixa retorno da Consulta
    caixa_retorno_consulta = tk.Text(janela_consulta, width=100, height=10)
    caixa_retorno_consulta.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
    # Mensagens de Retorno das Consultas
    mensagem_label_total_consulta = tk.Label(janela_consulta, text="", fg="green")
    mensagem_label_total_consulta.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
    mensagem_label_connsulta_alerta = tk.Label(janela_consulta, text="", fg="green")
    mensagem_label_connsulta_alerta.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')    
    # Filtros Avançados
    label_ordena_subtitulo1 = tk.Label(janela_consulta, text='FILTROS AVANÇADOS', anchor='center')
    label_ordena_subtitulo1.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')      
    botao_filtro_usuario = tk.Button(janela_consulta, text='Filtrar Usuários', command=filtro_de_usuario)
    botao_filtro_usuario.grid(row=10, column=0, padx=5, pady=5, sticky='nsew')  
    botao_filtrar_livros = tk.Button(janela_consulta, text='Filtrar Livros', command=filtro_de_livros)
    botao_filtrar_livros.grid(row=10, column=1, padx=5, pady=5, sticky='nsew')  
    botao_filtrar_reservas = tk.Button(janela_consulta, text='Filtrar Reservas', command=filtro_de_reserva)
    botao_filtrar_reservas.grid(row=11, column=0, padx=5, pady=5, sticky='nsew')     
    botao_filtrar_emprestimos = tk.Button(janela_consulta, text='Filtrar Emprestimos', command=filtro_de_emprestimo)
    botao_filtrar_emprestimos.grid(row=11, column=1, padx=5, pady=5, sticky='nsew')           
    # Botão para encerra a janela
    botao_consulta_voltar = tk.Button(janela_consulta, text='Voltar', command=janela_consulta.destroy)
    botao_consulta_voltar.grid(row=12, column=2, padx=5, pady=5, sticky='nsew')   

# 5ª. PARTE - REMOÇÃO DE USUARIOS, LIVROS, RESERVAS E EMPRÉSTIMOS DE LIVROS    

# Função para abrir a janela de remoção de registros de usuarios, livros, reservas e empréstimos de livros
def remover():
    # Função para Remover Usuário
    def remove_user():
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtém o ID_USUARIO
        id_usuario = combobox_remover_usuario.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_usuario não está vazio
            if not id_usuario:
                raise ValueError("Por favor, selecione um usuário.") 
            # Verifica se o ID_USUARIO existe na tabela tb_usuario
            cursor.execute("SELECT COUNT(*) FROM tb_usuario WHERE ID_USUARIO = ?", (id_usuario,))
            usuario_existente = cursor.fetchone()[0] > 0
            # Deleta o usuario da tabela tb_usuario
            if usuario_existente:
                # Se o usuário existe, remove-o
                cursor.execute("DELETE FROM tb_usuario WHERE ID_USUARIO = ?", (id_usuario,))
                # Consulta SQL para contar o número de registros na tabela tb_usuario após a exclusão, desconsiderando o usuario admin
                cursor.execute("SELECT COUNT(*) FROM tb_usuario WHERE ID_USUARIO > 20230000")
                numero_de_usuarios = cursor.fetchone()[0]
                # Salvar as alterações e fechar a conexão
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_remover_usuario.delete(0, 'end')      
                # Atualizar a mensagem na parte inferior da janela
                mensagem_label_removido.config(text="Usuário removido com sucesso!", fg="green")
                mensagem_label_total_remocao.config(text=f" {numero_de_usuarios} Usuário(s) Cadastrado(s).", fg="blue")
            # Se o usuário não existe, exibe uma mensagem de erro
            else:
                mensagem_label_removido.config(text="ID de Usuário não encontrado.", fg="red")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
        except ValueError as ve:
            mensagem_label_removido.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_removido.config(text="Erro ao Remover Usuário. " + str(e), fg="red")
        except Exception as e:
            mensagem_label_removido.config(text="Informação incompleta: " + str(e), fg="red")               

    # Função para Remover Livro
    def remove_livro():
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtém o ID_ISBN 
        id_isbn = combobox_remover_livro.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_isbn não está vazia
            if not id_isbn:
                raise ValueError("Por favor, selecione um livro.") 
            # Verifica se o ID_ISBN existe na tabela tb_livro
            cursor.execute("SELECT COUNT(*) FROM tb_livro WHERE ID_ISBN = ?", (id_isbn,))
            livro_existente = cursor.fetchone()[0] > 0
            # Se o livro existe, remove-o
            if livro_existente:
                cursor.execute("DELETE FROM tb_livro WHERE ID_ISBN = ?", (id_isbn,))
                # Consulta SQL para contar o número de registros na tabela tb_livro após a exclusão
                cursor.execute("SELECT COUNT(*) FROM tb_livro")
                numero_de_livros = cursor.fetchone()[0]
                # Salvar as alterações e fechar a conexão
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_remover_livro.delete(0, 'end')      
                # Atualizar a mensagem na parte inferior da janela
                mensagem_label_removido.config(text="Livro Removido Com Sucesso!", fg="green")
                mensagem_label_total_remocao.config(text=f"Total: {numero_de_livros} livro(s) cadastrado(s).", fg="blue")
            # Se o livro não existe, retorna erro            
            else:
                mensagem_label_removido.config(text="ID de Livro não encontrado.", fg="red")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
        except ValueError as ve:
            mensagem_label_removido.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_removido.config(text="Erro ao Remover Usuário. " + str(e), fg="red")
        except Exception as e:
            mensagem_label_removido.config(text="Informação incompleta: " + str(e), fg="red")    

    # Função para remover reserva        
    def remove_reserva():
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtém o ID de reserva
        id_reserva = combobox_remover_reserva.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_reserva não está vazio
            if not id_reserva:
                raise ValueError("Por favor, selecione uma reserva.") 
            # Verifica se o ID de reserva existe na tabela tb_reserva
            cursor.execute("SELECT COUNT(*) FROM tb_reserva WHERE ID_RESERVA = ?", (id_reserva,))
            reserva_existente = cursor.fetchone()[0] > 0
            # Se a reserva existe, remove-a
            if reserva_existente:
                cursor.execute("DELETE FROM tb_reserva WHERE ID_RESERVA = ?", (id_reserva,))
                # Consulta SQL para contar o número de registros na tabela tb_reserva após a exclusão
                cursor.execute("SELECT COUNT(*) FROM tb_reserva")
                numero_de_reservas = cursor.fetchone()[0]
                # Salvar as alterações e fechar a conexão
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_remover_reserva.delete(0, 'end')      
                # Atualizar a mensagem na parte inferior da janela
                mensagem_label_removido.config(text="Reserva Removida Com Sucesso!", fg="green")
                mensagem_label_total_remocao.config(text=f"Você Possui {numero_de_reservas} Livro(s) Reservado(s).", fg="blue")
            # Se a reserva não existe, retorna erro
            else:
                mensagem_label_removido.config(text="ID de Reserva não encontrado.", fg="red")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
        except ValueError as ve:
            mensagem_label_removido.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_removido.config(text="Erro ao Remover Usuário. " + str(e), fg="red")
        except Exception as e:
            mensagem_label_removido.config(text="Informação incompleta: " + str(e), fg="red")    
        
    # Função para Remover Empréstimo
    def remove_emprestimo():
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtém o ID_EMPRESTIMO 
        id_emprestimo = combobox_remover_emprestimo.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_emprestimo não está vazia
            if not id_emprestimo:
                raise ValueError("Por favor, selecione um empréstimo.") 
            # Verifica se o ID_EMPRESTIMO existe na tabela tb_emprestimo
            cursor.execute("SELECT COUNT(*) FROM tb_emprestimo WHERE ID_EMPRESTIMO = ?", (id_emprestimo,))
            emprestimo_existente = cursor.fetchone()[0] > 0
            # Se o empréstimo existe, remove-o
            if emprestimo_existente:
                cursor.execute("DELETE FROM tb_emprestimo WHERE ID_EMPRESTIMO = ?", (id_emprestimo,))
                # Consulta SQL para contar o número de registros na tabela tb_emprestimo após a exclusão
                cursor.execute("SELECT COUNT(*) FROM tb_emprestimo")
                numero_de_emprestimos = cursor.fetchone()[0]
                # Salvar as alterações e fechar a conexão
                conn.commit()
                conn.close()
                # Limpa o conteúdo das caixas de texto
                combobox_remover_emprestimo.delete(0, 'end')      
                # Atualizar a mensagem na parte inferior da janela
                mensagem_label_removido.config(text="Empréstimo Removido Com Sucesso!", fg="green")
                mensagem_label_total_remocao.config(text=f"Você Possui {numero_de_emprestimos} Livro(s) Emprestado(s).", fg="blue")
            # Se o empréstimo não existe, retorna erro      
            else:
                mensagem_label_removido.config(text="ID de Empréstimo não encontrado.", fg="red")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas
        except ValueError as ve:
            mensagem_label_removido.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_removido.config(text="Erro ao Remover Usuário. " + str(e), fg="red")
        except Exception as e:
            mensagem_label_removido.config(text="Informação incompleta: " + str(e), fg="red")    
            
    # Obtendo listas dos ids das tabelas usuario, livro, reserva e emprestimo
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para selecionar todos os valores da coluna ID_USUARIO
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE ID_USUARIO > 20230000 ORDER BY ID_USUARIO ASC")
    # Recupera todos os resultados da consulta em uma lista
    lista_usuario = [registro1[0] for registro1 in cursor.fetchall()]
    # Consulta SQL para selecionar todos os valores da coluna ID_ISBN
    cursor.execute("SELECT ID_ISBN FROM tb_livro  ORDER BY ID_ISBN ASC")
    # Recupera todos os resultados da consulta em uma lista
    lista_livros = [registro2[0] for registro2 in cursor.fetchall()]
    # Consulta SQL para selecionar todos os valores da coluna ID_RESERVA
    cursor.execute("SELECT ID_RESERVA FROM tb_reserva  ORDER BY ID_RESERVA ASC")
    # Recupera todos os resultados da consulta em uma lista
    lista_reserva = [registro3[0] for registro3 in cursor.fetchall()]
    # Consulta SQL para selecionar todos os valores da coluna ID_EMPRESTIMO
    cursor.execute("SELECT ID_EMPRESTIMO FROM tb_emprestimo  ORDER BY ID_EMPRESTIMO ASC")
    # Recupera todos os resultados da consulta em uma lista
    lista_emprestimo = [registro4[0] for registro4 in cursor.fetchall()]
    # Fechar a conexão
    conn.close()    
    
    # janela de remoção de livros
    janela_remover = tk.Toplevel()
    # Formatando a janela de Consulta
    janela_remover.title('Remover Registros')
    label_janela_remover = tk.Label(janela_remover, text='REMOVER REGISTROS', 
                                    borderwidth=2,relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_janela_remover.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='nsew' )
    # Removendo Usuario
    label_remove_usuario = tk.Label(janela_remover, text='Selecione o ID do Usuário: ', anchor='w')
    label_remove_usuario.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    combobox_remover_usuario = ttk.Combobox(janela_remover, values=lista_usuario)
    combobox_remover_usuario.grid(row=1,column=3, padx=10, pady=10, sticky='nsew')
    botao_remover_usuario = tk.Button(janela_remover, text='Remover Usuário', command=remove_user)
    botao_remover_usuario.grid(row=1, column=4, padx=10, pady=10, sticky='nsew')          
    # Removendo Livro
    label_remove_livros = tk.Label(janela_remover, text='Selecione o ISBN do Livro: ', anchor='w')
    label_remove_livros.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    combobox_remover_livro = ttk.Combobox(janela_remover, values=lista_livros)
    combobox_remover_livro.grid(row=2,column=3, padx=10, pady=10, sticky='nsew')
    botao_remover_livros = tk.Button(janela_remover, text='Remover Livro', command=remove_livro)
    botao_remover_livros.grid(row=2, column=4, padx=10, pady=10, sticky='nsew')   
    # Remover Reserva
    label_remove_reserva = tk.Label(janela_remover, text='Selecione o ID da Reserva: ', anchor='w')
    label_remove_reserva.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    combobox_remover_reserva = ttk.Combobox(janela_remover, values=lista_reserva)
    combobox_remover_reserva.grid(row=3,column=3, padx=10, pady=10, sticky='nsew')
    botao_remover_reserva = tk.Button(janela_remover, text='Remover Reserva', command=remove_reserva)
    botao_remover_reserva.grid(row=3, column=4, padx=10, pady=10, sticky='nsew')   
    # Remover Empréstimo
    label_remove_emprestimo = tk.Label(janela_remover, text='Selecione o ID do Empréstimo: ', anchor='w')
    label_remove_emprestimo.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    combobox_remover_emprestimo = ttk.Combobox(janela_remover, values=lista_emprestimo)
    combobox_remover_emprestimo.grid(row=4,column=3, padx=10, pady=10, sticky='nsew')
    botao_remover_emprestimo = tk.Button(janela_remover, text='Remover Empréstimo', command=remove_emprestimo)
    botao_remover_emprestimo.grid(row=4, column=4, padx=10, pady=10, sticky='nsew')       
    # Mensagem de Confirmação ou erro
    mensagem_label_removido = tk.Label(janela_remover, text="", fg="green")
    mensagem_label_removido.grid(row=5, column=2, columnspan=4, padx=10, pady=10, sticky='nsew')
    mensagem_label_total_remocao = tk.Label(janela_remover, text="", fg="green")
    mensagem_label_total_remocao.grid(row=6, column=2, columnspan=4, padx=10, pady=10, sticky='nsew')
    # Botão Voltar
    botao_remover_sair = tk.Button(janela_remover, text='Voltar', command=janela_remover.destroy)
    botao_remover_sair.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')   

 
 # CONFIGURAÇÃO DE ACESSO DO PERFIL USUARIO
 
 # 1ª. PARTE - JANELA CONSULTA LIVROS PARA USUARIOS   

# Função abre um nova janela de consultar para o perfil usuario
def filtro_de_livros():
    # Função para consulta por titulo
    def consulta_titulo():
        # Abre uma conexão com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtendo a variavel
        consulta_titulo = combobox_seleciona_titulos.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se consulta_titulo não está vazia
            if not consulta_titulo:
                raise ValueError("Por favor, selecione um livro pelo título.")   
            # Consulta SQL para selecionar todos os dados da tb_livro
            consulta_sql_titulos = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, DESCRICAO, COMENTARIO FROM tb_livro WHERE TITULO = '{consulta_titulo}'"
            # Executar a consulta SQL por titulo
            cursor.execute(consulta_sql_titulos)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Salva e Fechar a conexão com o banco de dados
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_titulos.delete(0, 'end')      
            # Limpar a caixa de texto caso haja informações 
            retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
            for resultado in resultados:
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas            
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")        
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")               
                        
    # Função para consulta por autor
    def consulta_autores():
        # abre uma conexão com o Banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtendo a variavel consulta_autoresnão  para depois verificar se não está vazio
        consulta_autores = combobox_seleciona_autores.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se consulta_autores não está vazia
            if not consulta_autores:
                raise ValueError("Por favor, selecione o autor.")   
            # Consulta SQL para selecionar todos os dados da tb_livro
            consulta_sql_autores = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, DESCRICAO FROM tb_livro WHERE AUTOR = '{consulta_autores}'"
            # Executar a consulta SQL
            cursor.execute(consulta_sql_autores)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_autores.delete(0, 'end')      
            # Limpar a caixa de texto caso haja informacao
            retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas            
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")        
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")        

    # Função para consulta por editora
    def consulta_editora():
        # abre uma conexão com o Banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtendo a variavel consulta_autoresnão  para depois verificar se não está vazio
        consulta_editora = combobox_seleciona_editora.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se consulta_editora não está vazia
            if not consulta_editora:
                raise ValueError("Por favor, selecione o editora.")   
            # Consulta SQL para selecionar todos os dados da tb_livro
            consulta_sql_editora = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, DESCRICAO FROM tb_livro WHERE EDITORA = '{consulta_editora}'"
            # Executar a consulta SQL
            cursor.execute(consulta_sql_editora)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_editora.delete(0, 'end')      
            # Limpar a caixa de texto caso haja informacao
            retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas            
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")        
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")     
            
    # função para consulta por ano
    def consulta_ano():
        # abre uma conexão com o Banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtendo a variavel
        consulta_ano = combobox_seleciona_ano.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se consulta_ano não está vazia
            if not consulta_ano:
                raise ValueError("Por favor, selecione o editora.")   
            # Consulta SQL para selecionar todos os dados da tb_livro
            consulta_sql_ano = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, DESCRICAO FROM tb_livro WHERE ANO = {consulta_ano}"
            # Executar a consulta SQL
            cursor.execute(consulta_sql_ano)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_ano.delete(0, 'end')      
            # Limpar a caixa de texto caso haja informacao
            retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados
            for resultado in resultados:
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas            
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")        
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red") 

    # função para consultar o ISBN
    def consulta_isbn():
        # abre uma conexão com o Banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtendo a variavel
        consulta_isbn = caixa_texto_consulta_isbn.get()      
        try:
            # Obtendo o ID_ISBN digitado pelo usuário
            consulta_isbn = caixa_texto_consulta_isbn.get()
            # Verifica se a entrada não está vazia e se informar preenchia é um número
            if not consulta_isbn:
                raise ValueError("Por favor, insira um ID_ISBN.")  
             # Verifica se a entrada é um valor numérico
            if not consulta_isbn.isnumeric():
                raise ValueError("Por favor, insira apenas números para o ID_ISBN.")
            # Consulta SQL para selecionar os dados com base no ID_ISBN
            consulta_sql_isbn = f"SELECT ID_ISBN, TITULO, AUTOR, EDITORA, ANO, PAGINAS, DESCRICAO, COMENTARIO FROM tb_livro WHERE ID_ISBN = {consulta_isbn}"    
            # Executa a consulta SQL
            cursor.execute(consulta_sql_isbn)
            # Obtém os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obtém o resultado da consulta
            resultado = cursor.fetchone()
            # Fecha a conexão com o banco de dados
            conn.close()
            # Se resultado for None, o ID_ISBN não foi encontrado
            if resultado is None:
                mensagem_label_retorno_consultas.config(text="ID_ISBN não encontrado no banco de dados.", fg="red")
                 # Limpar a caixa de resultado
                retorno_consulta.delete(1.0, tk.END) 
            else:
                # Limpa o conteúdo das caixas de texto
                caixa_texto_consulta_isbn.delete(0, 'end')      
                # Limpar a caixa de texto caso haja informacao
                retorno_consulta.delete(1.0, tk.END)
                # Inserir os nomes das colunas na caixa de texto
                retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
                # Preencher a caixa de texto com os resultados
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")
                # Atualiza a mensagem na parte inferior da janela
                mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Exibe mensagem de erro na parte inferior da janela, cajo ocorra problemas            
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")        
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")         
        
    # Obtendo a lista de titulos e autores e retornando uma lista
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta titulos
    cursor.execute("SELECT TITULO FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    lista_titulos =[registro1[0] for registro1 in cursor.fetchall()]
    titulos = sorted(list(set(lista_titulos)))
    # Consulta autores
    cursor.execute("SELECT AUTOR FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    lista_autores = [registro2[0] for registro2 in cursor.fetchall()]
    autores = sorted(list(set(lista_autores)))
    # Recupera todos os resultados da consulta em uma lista
    cursor.execute("SELECT EDITORA FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    lista_editora = [registro3[0] for registro3 in cursor.fetchall()]
    editora = sorted(list(set(lista_editora)))
    # Recupera todos os resultados da consulta em uma lista
    cursor.execute("SELECT ANO FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    lista_ano = [registro4[0] for registro4 in cursor.fetchall()]
    ano = sorted(list(set(lista_ano)))
    # Salva e Fechar a conexão
    conn.commit()
    conn.close()
    
    # Criando a Janela de consulta livros
    janela_consultas = tk.Toplevel()
    # Formatando o titulo
    janela_consultas.title('Consulta livros')
    # Cabeçalho da tela de cadastro
    label_consulta_livros = tk.Label(janela_consultas, text='CONSULTA LIVROS', 
                                     borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_consulta_livros.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=5)
    # Label, caixa de seleção e botão para a Lista de titulos
    label_seleciona_titulos = tk.Label(janela_consultas, text='Selecione por Título: ', anchor='w')
    label_seleciona_titulos.grid(row=1, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
    combobox_seleciona_titulos = ttk.Combobox(janela_consultas, values=titulos)
    combobox_seleciona_titulos.grid(row=1,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_livros = tk.Button(janela_consultas, text='Consulta Títulos', command=consulta_titulo)
    botao_consulta_livros.grid(row=1, column=4,  padx=5, pady=5, sticky='nsew')
    # Label, caixa de seleção e botão para a lista de Autores
    label_seleciona_autores = tk.Label(janela_consultas, text='Selecione o Autor: ', anchor='w')
    label_seleciona_autores.grid(row=2, column=0, padx=5, pady=5, sticky='nsew', columnspan=1)
    combobox_seleciona_autores = ttk.Combobox(janela_consultas, values=autores)
    combobox_seleciona_autores.grid(row=2,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_autores = tk.Button(janela_consultas, text='Consulta Autor', command=consulta_autores)
    botao_consulta_autores.grid(row=2, column=4,  padx=5, pady=5, sticky='nsew')
    # Label, caixa de seleção e botão para a lista de editoras
    label_seleciona_editora = tk.Label(janela_consultas, text='Selecione a Editora: ', anchor='w')
    label_seleciona_editora.grid(row=3, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
    combobox_seleciona_editora = ttk.Combobox(janela_consultas, values=editora)
    combobox_seleciona_editora.grid(row=3,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_editora = tk.Button(janela_consultas, text='Consulta Editora', command=consulta_editora)
    botao_consulta_editora.grid(row=3, column=4,  padx=5, pady=5, sticky='nsew')
    # Label, caixa de seleção e botão para a lista de anos de publicacao                
    label_seleciona_ano = tk.Label(janela_consultas, text='Selecione o Ano: ', anchor='w')
    label_seleciona_ano.grid(row=4, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
    combobox_seleciona_ano = ttk.Combobox(janela_consultas, values=ano)
    combobox_seleciona_ano.grid(row=4,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_ano = tk.Button(janela_consultas, text='Consulta Ano', command=consulta_ano)
    botao_consulta_ano.grid(row=4, column=4,  padx=5, pady=5, sticky='nsew')
    #label e caixa de texto consulta isbn
    label_consulta_isbn = tk.Label(janela_consultas, text='Pesquise pelo ISBN: ', anchor='w')
    label_consulta_isbn.grid(row=5, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
    caixa_texto_consulta_isbn = tk.Entry(janela_consultas, width=40)
    caixa_texto_consulta_isbn.grid(row=5,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_isbn = tk.Button(janela_consultas, text='Consulta ISBN', command=consulta_isbn)
    botao_consulta_isbn.grid(row=5, column=4,  padx=5, pady=5, sticky='nsew')    
    # Retorno em uma caixa de texto com o resultado da consulta realizada
    retorno_consulta = tk.Text(janela_consultas, width=120, height=10)
    retorno_consulta.grid(row=6, column=0, columnspan=4,  padx=5, pady=5, sticky='nsew')
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_retorno_consultas = tk.Label(janela_consultas, text="", fg="green")
    mensagem_label_retorno_consultas.grid(row=7, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
    # Botão Sair
    botao_sair = tk.Button(janela_consultas, text='Voltar', command=janela_consultas.destroy)
    botao_sair.grid(row=8, column=3,  padx=5, pady=5, sticky='nsew')
    # Rodando a Janela
    janela_consultas.mainloop()    


# 2ª. PARTE - USUARIO ALTERA SENHA DE ACESSO

# Função para abair a janela de atualização de senha do usuario
def alterar_senha():
    # Função para atualizar os dados de acesso dos usuários
    def atualizar_senha():
        # Abre uma conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtem a ID_USUARIO a partir do login do usuario ao sistema e abre um caixa para informar a nova senha
        id_usuario = lista_usuario[0]
        nova_senha = caixa_texto_label_para_atualizacao.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_usuario, nova_senha não estão vazios
            if not id_usuario or not nova_senha:
                raise ValueError("Por favor, preencha todas as informações.")
                
            id_usuario = int(id_usuario)  # Converte o ID para inteiro
            # Atualiza as informações do usuário com base no ID_USUARIO
            cursor.execute(f"UPDATE tb_usuario SET SENHA_USUARIO = ? WHERE ID_USUARIO = ?",
                           (nova_senha, id_usuario))
            # Salva e Fecha a conexão com o Banco  de Dados
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            caixa_texto_label_para_atualizacao.delete(0, 'end')      
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_cadastro.config(text="Senha Alterada com sucesso!", fg="green")
        except ValueError as ve:
            # Exibe uma mensagem de erro se alguma informação estiver faltando
            mensagem_label_cadastro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            # Em caso de erro do SQLite, exibir mensagem de erro na parte inferior da janela
            mensagem_label_cadastro.config(text="Erro ao atualizar informações: " + str(e), fg="red")
   
    # obtendo o nome de usuario do login
    name_user = entry_usuario.get()    
    # Abre uma conexao com o banco de dados
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para consulta o ID_USUARIO a partir do login
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE EMAIL = ?",(name_user,))
    # Recupera todos os resultados da consulta em uma lista
    lista_usuario = [registro1[0] for registro1 in cursor.fetchall()]    
    # Salva e Fechar a conexão com o banco de dados
    conn.commit()
    conn.close()    
    
    # Janela de alteração de senha
    janela_altera_senha = tk.Toplevel()
    # Formatando o titulo da janela
    janela_altera_senha.title('Controle de Acesso')
    # Texto da janela
    label_janela_atualizar = tk.Label(janela_altera_senha, text='ALTERAR SENHA DE ACESSO DO USUARIO',
                                      borderwidth=2,relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_janela_atualizar.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='nsew' )
    # label de caixa de texto para Receber a nota informação
    label_para_atualizacao= tk.Label(janela_altera_senha, text='Informe Nova Senha:', anchor='w')
    label_para_atualizacao.grid(row=9, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    caixa_texto_label_para_atualizacao = tk.Entry(janela_altera_senha, width=40, show='*')
    caixa_texto_label_para_atualizacao.grid(row=9, column=2, columnspan=3, padx=10, pady=10, sticky='nsew')   
    # Botão de atualização
    botao_atualizar_usuario = tk.Button(janela_altera_senha, text='Atualizar', command=atualizar_senha)
    botao_atualizar_usuario.grid(row=10, column=2, padx=10, pady=10, sticky='nsew')                
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_cadastro = tk.Label(janela_altera_senha, text="", fg="green")
    mensagem_label_cadastro.grid(row=11, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')     
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_total_usuarios = tk.Label(janela_altera_senha, text="", fg="green")
    mensagem_label_total_usuarios.grid(row=12, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')  
    botao_sair = tk.Button(janela_altera_senha, text='Voltar', command=janela_altera_senha.destroy)
    botao_sair.grid(row=13, column=0, padx=10, pady=10, sticky='nsew')
    # Rodando a Janela
    janela_altera_senha.mainloop()   
    

# 3ª PARTE - USUARIO REGISTRA RESERVA        

# Função para abria da janela de reserva de usuario
def registro_reserva_usuario():
    # Função para registrar a reserva do perfil usuario
    def cadastrar_reserva_usuario():
        # Conectando com o Banco de Dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtendo id do livro
        livro_reserva  = combobox_selecionaLivros_reserva.get()
        # obtendo id do usuario de forma automatica para o usuario pelo nome de usuario
        id_usuario = id_usuarios_reserva[0]
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_usuario e livro_reserva não estão vazios
            if not id_usuario or not livro_reserva:
                raise ValueError("Por favor, preencha todas as informações.")    
            # Consulta para verificar se já existe uma reserva para o mesmo livro e usuário
            cursor.execute("SELECT COUNT(*) FROM tb_reserva WHERE ID_USUARIO = ? AND ID_ISBN = ?", (id_usuario, livro_reserva))
            reserva_existente = cursor.fetchone()[0]
            # Caso ja existe reserva retorna um erro
            if reserva_existente > 0:
                raise ValueError("O usuário já reservou este livro!")            
            # Obtem o maior id da tabela para poder gerar um novo
            cursor.execute("SELECT MAX(ID_RESERVA) FROM tb_reserva")
            # Recupera o maior id_reserva e adiciona 1 para obter o próximo ID disponível
            max_id_reserva = cursor.fetchone()[0]
            if max_id_reserva is None:
                max_id_reserva = 0
            id_reserva = max_id_reserva + 1
            # Insere uma nova reserva com o ID_RESERVA gerado
            cursor.execute("INSERT INTO tb_reserva (ID_RESERVA, ID_USUARIO, ID_ISBN, DATA_RESERVA) VALUES (?, ?, ?, ?)",
                           (id_reserva, id_usuario, livro_reserva, data_atual_formatada))
            # Salvar as alterações e fechar a conexão
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_selecionaLivros_reserva.delete(0, 'end')      
            # Atualizar a mensagem na parte inferior da janela
            mensagem_label_total_reservas.config(text="Reserva registrada", fg="green")
            # Em caso de erro, exibir mensagem de erro na parte inferior da janela
        except ValueError as ve:
            mensagem_label_total_reservas.config(text=str(ve), fg="red")  
        except sqlite3.Error as e:
            mensagem_label_total_reservas.config(text="Erro: " + str(e), fg="red")            
        except Exception as e:
            mensagem_label_total_reservas.config(text="Verifique o tipo os dados: " + str(e), fg="red")
            
    # Obtendo o nome de usuairo do login
    name_user = entry_usuario.get()                
    # Abre uma conexao com o banco de dados
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para selecionar o id_usuairo a partir do nome de usuario do login
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE EMAIL = ?",(name_user,))
    id_usuarios_reserva = cursor.fetchone()
    # Recupera todos os resultados da consulta em uma lista
    id_usuarios = [registro_1[0] for registro_1 in cursor.fetchall()]
    # Consulta SQL para selecionar todos os LIVROS da coluna titulo
    cursor.execute("SELECT ID_ISBN FROM tb_livro")
    # Recupera todos os resultados da consulta em uma lista
    livros = [registro[0] for registro in cursor.fetchall()]
    # Fechar a conexão
    conn.close()

    # Criando a Janela
    janela_reservar_usuario = tk.Toplevel()
    # Formatando o titulo
    janela_reservar_usuario.title('Reserva de Livros')
    # Cabeçalho da tela de cadastro
    label_cadastro_reserva = tk.Label(janela_reservar_usuario, text='REGISTRO DE RESERVA', 
                                      borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_cadastro_reserva.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
    # label Caixa de seleção de livros
    label_selecionaLivros_reserva = tk.Label(janela_reservar_usuario, text='Selecionar Livros: ', anchor='w')
    label_selecionaLivros_reserva.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=1)
    combobox_selecionaLivros_reserva = ttk.Combobox(janela_reservar_usuario, values=livros)
    combobox_selecionaLivros_reserva.grid(row=2,column=1, padx=10, pady=10, sticky='nsew', columnspan=3)
    # Obtem de forma automatica a data referente ao registro do reserva
    label_datainicio_reserva  = tk.Label(janela_reservar_usuario, text="Data da Reserva: ", anchor='w')
    label_datainicio_reserva.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=1)
    calendario_datainicio_reserva = tk.Label(janela_reservar_usuario,text=f"{data_atual_formatada}", anchor='e')
    calendario_datainicio_reserva.grid(row=3, column=1, padx=10, pady=10, sticky='nsew', columnspan=3)
    # Criar o rótulo para exibir mensagens
    mensagem_label_reserva = tk.Label(janela_reservar_usuario, text="", fg="green")
    mensagem_label_reserva.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    mensagem_label_total_reservas = tk.Label(janela_reservar_usuario, text="", fg="green")
    mensagem_label_total_reservas.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
    # botoes para reservar e voltar
    botao_reservar = tk.Button(janela_reservar_usuario, text='Reservar', command=cadastrar_reserva_usuario)
    botao_reservar.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')    
    botao_voltar = tk.Button(janela_reservar_usuario, text='Voltar', command=janela_reservar_usuario.destroy)
    botao_voltar.grid(row=7, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')    
    # janela executando
    janela_reservar_usuario.mainloop()    

#  4ª. PARTE -  CONSULTA SOLICITACOES DO USUARIO (RESERVAS/EMPRESTIMOS)

# função para abrir a janela consulta das solicitações do usuario
def meus_pedidos():
    # função para executar a consulta as soliticações de reservas ou emprestimos
    def minhas_solicitacoes():
        # Abre uma conexão com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtendo a variaveis 
        id_usuario_consulta = id_usuario_login
        consulta_solicitacoes = combobox_seleciona_tabela.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_usuario_consulta e consulta_solicitacoes não estão vazios
            if not consulta_solicitacoes:
                raise ValueError("Por favor, selecione um tipo de consulta.")   
            # Ajustando o texto do nome da tabela para Reservas e Empréstimos na caixa de selecao
            if consulta_solicitacoes == 'Reservas':
                consulta_sql = f"SELECT * FROM tb_reserva WHERE ID_USUARIO = {id_usuario_consulta}"
            else:
                consulta_sql = f"SELECT * FROM tb_emprestimo WHERE ID_USUARIO = {id_usuario_consulta}"
            # Executando a consulta as solicitações
            cursor.execute(consulta_sql)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Salva e Fechar a conexão com o banco de dados
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_tabela.delete(0, 'end')      
            # Limpar a caixa de texto caso haja informações 
            retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
            for resultado in resultados:
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
            # Em caso de erro, exibir mensagem de erro na parte inferior da janela
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")  
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro: " + str(e), fg="red")            
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Verifique o tipo os dados: " + str(e), fg="red")    
            
    # Obtendo o nome de usuario do login
    name_user = entry_usuario.get()    
    # Abre uma conexao com o banco de dados
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para selecionar o ID_USUARIO a partir do nome de usuario do login
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario  WHERE EMAIL = ?",(name_user,))
    # Recupera todos os resultados da consulta em uma lista
    lista_usuario = [registro1[0] for registro1 in cursor.fetchall()]    
    id_usuario_login = lista_usuario[0]
    # Fechando a conexao com o banco de dados
    conn.close()
    # Abrindo a janelra de reservas e emprestimo
    janela_minhas_reservas = tk.Toplevel()
    tabelas = ['Reservas', 'Emprestimos']
    # Formatando o titulo
    janela_minhas_reservas.title('Minhas Solicitações de Livros')
    # Cabeçalho da tela de cadastro
    label_cabecalho = tk.Label(janela_minhas_reservas, text='MINHAS SOLICITAÇÕES',
                               borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_cabecalho.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=5)
    # Label, caixa de seleção e botão para a lista de editoras
    label_seleciona_tabela = tk.Label(janela_minhas_reservas, text='Selecione o que deseja consultar: ', anchor='w')
    label_seleciona_tabela.grid(row=3, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
    combobox_seleciona_tabela = ttk.Combobox(janela_minhas_reservas, values=tabelas)
    combobox_seleciona_tabela.grid(row=3,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_tabelas = tk.Button(janela_minhas_reservas, text='Consultar', command=minhas_solicitacoes)
    botao_consulta_tabelas.grid(row=3, column=4, padx=5, pady=5, sticky='nsew')
    # Retorno em uma caixa de texto com o resultado da consulta realizada
    retorno_consulta = tk.Text(janela_minhas_reservas, width=100, height=10)
    retorno_consulta.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_retorno_consultas = tk.Label(janela_minhas_reservas, text="", fg="green")
    mensagem_label_retorno_consultas.grid(row=6, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
    # Botão Sair
    botao_sair = tk.Button(janela_minhas_reservas, text='Voltar', command=janela_minhas_reservas.destroy)
    botao_sair.grid(row=7, column=3,  padx=5, pady=5, sticky='nsew')
    # Executa a janela
    janela_minhas_reservas.mainloop()
    
# CONFIGURAÇÃO DOS PERFIS DE USUÁRIO AO SISTEMA  

# 1ª. PARTE - JANELA PARA CONFIGURAR O ACESSO DE TODOS OS USUARIOS A BIBLIOTECA   

# Função para abrir a janela de atualização de nivel de acesso
def controle_acesso():
    # Função para atualizar O nivel de acesso dos usuários na tb_login alterando o tipo de usuario
    def atualizar_nivel_acesso():
        # Abre uma conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # obtem as variaveis para atualizar os dados
        id_usuario = combobox_atualizar_usuario.get()
        opcao_atualizacao = combobox_atualizar_opcao.get()
        nova_informacao = caixa_texto_label_para_atualizacao.get().lower()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se id_usuario, opcao_atualizacao e nova_informacao não estão vazios
            if not id_usuario or not opcao_atualizacao or not nova_informacao:
                raise ValueError("Por favor, preencha todas as informações.")
            id_usuario = int(id_usuario)  # Converte o ID para inteiro
            # Atualiza as informações do usuário com base no ID_USUARIO
            cursor.execute(f"UPDATE tb_usuario SET {opcao_atualizacao} = ? WHERE ID_USUARIO = ?",
                           (nova_informacao, id_usuario))
            # Salva e fecha a conexão com  o banco de dados
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_atualizar_usuario.delete(0, 'end') 
            combobox_atualizar_opcao.delete(0, 'end')   
            caixa_texto_label_para_atualizacao.delete(0, 'end')   
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_cadastro.config(text="Informações atualizadas com sucesso", fg="green")
        except ValueError as ve:
            # Exibe uma mensagem de erro se alguma informação estiver faltando
            mensagem_label_cadastro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            # Em caso de erro do SQLite, exibir mensagem de erro na parte inferior da janela
            mensagem_label_cadastro.config(text="Erro ao atualizar informações: " + str(e), fg="red")
    # Obtendo listas dos ids das tabelas usuario
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()
    # Consulta SQL para selecionar todos os valores da coluna ID_USUARIO
    cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE ID_USUARIO > 20230000")
    # Recupera todos os resultados da consulta em uma lista
    lista_usuario = [registro1[0] for registro1 in cursor.fetchall()]    
    opcao_controle = ['SENHA_USUARIO', 'TIPO_USUARIO']            
    # Janela de Cadastro a ser aberta ao clicar no botão Cadastro
    janela_controle = tk.Toplevel()
    # Formatando o titulo da janela
    janela_controle.title('Controle de Acesso')
    # Criando a Janela de Atualizacao
    # Texto da janela
    label_janela_atualizar = tk.Label(janela_controle, text='ATUALIZAR DADOS DE ACESSO DO USUARIO', 
                                      borderwidth=2,relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_janela_atualizar.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='nsew' )
    # Nivel de acesso
    label_janela_nivel = tk.Label(janela_controle,
                                  text="TIPOS DE USUÁRIOS:\n'admin', 'gerente' e 'usuario'.", 
                                  width=40, height=5)
    label_janela_nivel.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky='nsew' )
    # Label e caixa de texto para atualizar o usuario
    label_atualizar_usuario = tk.Label(janela_controle, text='Selecione o ID do Usuário: ', anchor='w')
    label_atualizar_usuario.grid(row=7, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    combobox_atualizar_usuario = ttk.Combobox(janela_controle, values=lista_usuario)
    combobox_atualizar_usuario.grid(row=7,column=2,  columnspan=3, padx=10, pady=10, sticky='nsew')
    # Label e caixa de seleçã para escolha dos campos para atualizacao
    label_atualizar_usuario1 = tk.Label(janela_controle, text='Selecione o Campo para Atualização: ', anchor='w')
    label_atualizar_usuario1.grid(row=8, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    combobox_atualizar_opcao = ttk.Combobox(janela_controle, values=opcao_controle)
    combobox_atualizar_opcao.grid(row=8,column=2,  columnspan=3, padx=10, pady=10, sticky='nsew')
    # label de caixa de texto para Receber a nota informação
    label_para_atualizacao= tk.Label(janela_controle, text='Preenha a Informação:', anchor='w')
    label_para_atualizacao.grid(row=9, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
    caixa_texto_label_para_atualizacao = tk.Entry(janela_controle, width=40)
    caixa_texto_label_para_atualizacao.grid(row=9, column=2, columnspan=3, padx=10, pady=10, sticky='nsew')   
    # Botão de atualização
    botao_atualizar_usuario = tk.Button(janela_controle, text='Atualizar', command=atualizar_nivel_acesso)
    botao_atualizar_usuario.grid(row=10, column=2, padx=10, pady=10, sticky='nsew')                
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_cadastro = tk.Label(janela_controle, text="", fg="green")
    mensagem_label_cadastro.grid(row=11, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')     
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_total_usuarios = tk.Label(janela_controle, text="", fg="green")
    mensagem_label_total_usuarios.grid(row=12, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')  
    botao_sair = tk.Button(janela_controle, text='Voltar', command=janela_controle.destroy)
    botao_sair.grid(row=13, column=0, padx=10, pady=10, sticky='nsew')
    # Rodando a Janela
    janela_controle.mainloop()
    
# 2ª. PARTE - JANELA DE CONSULTA AOS PERFIS DE ACESSO DE TODOS OS USUARIOS DA BIBLIOTECA   

# Abre uma janela para consulta de dados da tb_login    
def perfil_acesso():
    # Função para filtrar a consulta de usuarios
    def filtrar_usuarios_login():
        # Abre uma conexão com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Obtendo a variavel pelo nome dos usuarios
        consulta_tipo_usuario = combobox_seleciona_situacao.get()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se consulta_usuarios_cadastrado não está vazia
            if not consulta_tipo_usuario:
                raise ValueError("Por favor, selecione tipo de usuário.")   
            # Consulta dos os usuarios cadastro e os perfis de acesso, podendo filtrar por tipo_usuario
            if consulta_tipo_usuario == "Todos":
                consulta_de_usuario_perfil = ("SELECT ID_USUARIO, EMAIL, SENHA_USUARIO, TIPO_USUARIO FROM tb_usuario")
            else:
                consulta_de_usuario_perfil = f"SELECT ID_USUARIO, EMAIL, SENHA_USUARIO, TIPO_USUARIO FROM tb_usuario WHERE TIPO_USUARIO = '{consulta_tipo_usuario}'"
            # Executar a consulta SQL 
            cursor.execute(consulta_de_usuario_perfil)
            # Obter os nomes das colunas da tabela
            nomes_colunas = [description[0] for description in cursor.description]
            # Obter todos os resultados
            resultados = cursor.fetchall()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Limpa o conteúdo das caixas de texto
            combobox_seleciona_situacao.delete(0, 'end')      
            # Limpar a caixa de texto caso haja informações 
            retorno_consulta.delete(1.0, tk.END)
            # Inserir os nomes das colunas na caixa de texto
            retorno_consulta.insert(tk.END, ", ".join(nomes_colunas) + "\n\n")
            # Preencher a caixa de texto com os resultados e pula uma linha para adicinar nova informação
            for resultado in resultados:
                retorno_consulta.insert(tk.END, str(resultado) + "\n\n")    
            # Atualiza a mensagem na parte inferior da janela
            mensagem_label_retorno_consultas.config(text="Consulta Realizada Com Sucesso!", fg="green")
        # Exibe uma mensagem de erro se alguma informação estiver faltando ou inválida
        except ValueError as ve:
            mensagem_label_retorno_consultas.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            mensagem_label_retorno_consultas.config(text="Erro ao consultar dados" + str(e), fg="red")  
        except Exception as e:
            mensagem_label_retorno_consultas.config(text="Informação incompleta: " + str(e), fg="red")             
   
    # Lista de filtros para consulta dos dados na tb_login port tipo de perfil
    tipos = ['Todos', 'admin', 'gerente', 'usuario']
    # Criando a Janela
    janela_tb_perfil = tk.Toplevel()
    # Formatando o titulo
    janela_tb_perfil.title('Consulta Perfil de Usuários')
    # Cabeçalho da tela de cadastro
    label_consulta_livros = tk.Label(janela_tb_perfil, text='CONSULTA PERFIL DE USUÁRIOS', 
                                     borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_consulta_livros.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=5)
    # Label, caixa de seleção e botão para a Lista de titulos
    label_seleciona_nome = tk.Label(janela_tb_perfil, text='Selecione por Tipo: ', anchor='w')
    label_seleciona_nome.grid(row=1, column=0,  padx=5, pady=5, sticky='nsew', columnspan=1)
    combobox_seleciona_situacao = ttk.Combobox(janela_tb_perfil, values=tipos)
    combobox_seleciona_situacao.grid(row=1,column=1,  padx=5, pady=5, sticky='nsew', columnspan=3)
    botao_consulta_nomes = tk.Button(janela_tb_perfil, text='Filtrar Perfis', command=filtrar_usuarios_login)
    botao_consulta_nomes.grid(row=1, column=4,  padx=5, pady=5, sticky='nsew')
    # Label, caixa de seleção e botão para a lista de usuarios
    retorno_consulta = tk.Text(janela_tb_perfil, width=60, height=10)
    retorno_consulta.grid(row=2, column=0, columnspan=4,  padx=5, pady=5, sticky='nsew')
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_retorno_consultas = tk.Label(janela_tb_perfil, text="", fg="green")
    mensagem_label_retorno_consultas.grid(row=3, column=0, columnspan=3,  padx=5, pady=5, sticky='nsew') 
    # Botão Sair
    botao_voltar = tk.Button(janela_tb_perfil, text='Voltar', command=janela_tb_perfil.destroy)
    botao_voltar.grid(row=4, column=3, padx=5, pady=5, sticky='nsew')
    # Rodando a Janela
    janela_tb_perfil.mainloop()            
        
# FUNCIONALIDADE DA JANELA PRINCIPAL DO SISTEMA  

# Função para limpar os dados preenchidos de usuário e senha
def limpar():
    entry_usuario.delete(0, 'end') 
    entry_senha.delete(0, 'end') 

# Função para fazer Login no Sistema
def clique():
    # Abri uma conexão com o banco de dados
    conn = sqlite3.connect('biblioteca_V1.db')
    cursor = conn.cursor()    
    # Obter os dados digitados pelo usuário
    name_user = entry_usuario.get()
    senha_user = entry_senha.get()
    # Consultar o banco de dados para verificar o usuário
    cursor = conn.cursor()
    cursor.execute('SELECT EMAIL, SENHA_USUARIO, TIPO_USUARIO FROM tb_usuario WHERE EMAIL = ?', (name_user,))
    resultado = cursor.fetchone()
    # Verifica o nome, senha e o tipo de usuario para liberar o acesso pelo tipo de perfil
    if resultado:
        email, senha, tipo = resultado
        if senha_user == senha:
            abrir_janela_menu(usuario_tipo=tipo)
        else:
            mensagem_label_login.config(text="Senha Incorreta", fg="red")
    else:
        mensagem_label_login.config(text="Usuário não encontrado", fg="red")
    # Fechar a conexão com o banco de dados quando a aplicação for encerrada
    conn.close()
        
# Função que abre uma janela para fazer o cadastro de novos usuarios no sistema     
def faca_cadastro():
    # Função que efetuar o registro dos dados no sistema     
    def cadastrar_usuario():
        #Abre uma conexao com o banco de dados
        conn = sqlite3.connect('biblioteca_V1.db')
        cursor = conn.cursor()
        # Variaveis para verificar se não estão vazios
        var_nome =  caixa_texto_nome.get().strip().title()
        var_telefone = caixa_texto_telefone.get().strip()
        var_endereco =  caixa_texto_endereco.get().strip().title()
        var_email =  caixa_texto_email.get().strip().lower()
        # Tenta executa a função e caso haja erro, retorna o erro
        try:
            # Verifica se não estão vazios
            if not var_nome or not var_telefone or not var_endereco or not var_email:
                raise ValueError("Por favor, preencha todas as informações.")
            # Verifique se o email já existe na tabela tb_usuario
            cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE EMAIL = ?", (var_email,))
            existing_user = cursor.fetchone()
            # Caso o e-mail já esteja cadastrado, retorna erro
            if existing_user:
                raise ValueError("Este email já está registrado.")               
            # Função para gerar ID unico da tabela usuario
            cursor.execute("SELECT MAX(ID_USUARIO) FROM tb_usuario")
            # Recupera o maior de tb_usuarios e adiciona 1 para obter o próximo ID disponível
            max_id_usuario = cursor.fetchone()[0]
            if max_id_usuario is None:
                max_id_usuario = 0
            id_usuario = max_id_usuario + 1
            # Gerando a senha (a primeira palavra do nome + "12345")
            senha_usuario = var_nome.split()[0].lower() + "12345"            
            # Insira o novo usuário com o ID_USUARIO obtido (não é necessário especificar o ID_USUARIO)
            cursor.execute("INSERT INTO tb_usuario (ID_USUARIO, NOME, TELEFONE, ENDERECO, EMAIL, SENHA_USUARIO) VALUES (?, ?, ?, ?, ?, ?)",
                           (id_usuario, var_nome, var_telefone, var_endereco, var_email, senha_usuario))
            # Salvando e Fechando a conexão com o Banco de dados
            conn.commit()
            conn.close()
            # Limpa o conteúdo das caixas de texto
            caixa_texto_nome.delete(0, 'end') 
            caixa_texto_telefone.delete(0, 'end')   
            caixa_texto_endereco.delete(0, 'end')   
            caixa_texto_email.delete(0, 'end')               
            # Atualizar a mensagem na parte inferior da janela
            mensagem_label_cadastro.config(text=f"Cadastro Realizado, Aguarde!\n {var_nome.split()[0].title()}, você receberá um e-mail com login e senha!", fg="green")
        # Em caso de erro, exibir mensagem de erro na parte inferior da janela
        except ValueError as ve:
            # Exibe uma mensagem de erro se alguma informação estiver faltando
            mensagem_label_cadastro.config(text=str(ve), fg="red")
        except sqlite3.Error as e:
            # Em caso de erro do SQLite, exibir mensagem de erro na parte inferior da janela
            mensagem_label_cadastro.config(text="Erro ao atualizar informações: " + str(e), fg="red")

    # Janela de Cadastro a ser aberta ao clicar no botão Cadastro
    janela_cadastro = tk.Toplevel()
    # Formatando o titulo da janela
    janela_cadastro.title('Cadastro de Usuários')
    # Cabeçalho da tela de cadastro
    label_cadastro_user = tk.Label(janela_cadastro, text='CADASTRO DE USUÁRIOS', 
                                   borderwidth=2, relief='solid', fg='black', bg='#2FD5D9', width=40, height=2)
    label_cadastro_user.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)
    # label do nome
    label_nome= tk.Label(janela_cadastro, text='Nome:', anchor='w')
    label_nome.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_nome = tk.Entry(janela_cadastro, width=40)
    caixa_texto_nome.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    # label do telefone
    label_telefone= tk.Label(janela_cadastro, text='Telefone com DDD:', anchor='w')
    label_telefone.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_telefone = tk.Entry(janela_cadastro, width=40)
    caixa_texto_telefone.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    # label do endereço
    label_endereco= tk.Label(janela_cadastro, text='Endereço:', anchor='w')
    label_endereco.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_endereco = tk.Entry(janela_cadastro, width=40)
    caixa_texto_endereco.grid(row=3, column=1, columnspan=2,padx=10, pady=10, sticky='nsew')
    # label do e-mail
    label_email = tk.Label(janela_cadastro, text='E-mail:', anchor='w')
    label_email.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
    caixa_texto_email = tk.Entry(janela_cadastro, width=40)
    caixa_texto_email.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
    # Criando o rótulo para exibir mensagens em caso de erro ou de execução correta do código
    mensagem_label_cadastro = tk.Label(janela_cadastro, text="", fg="green")
    mensagem_label_cadastro.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')    
    # Criando botão de login e cadastro
    botao_cadastrar = tk.Button(janela_cadastro, text='Cadastrar', command=cadastrar_usuario)
    botao_cadastrar.grid(row=6, column=2, padx=10, pady=10, sticky='nsew')    
    # Botão sair
    botao_sair = tk.Button(janela_cadastro, text='Voltar', command=janela_cadastro.destroy)
    botao_sair.grid(row=7, column=0, padx=10, pady=10, sticky='nsew')    
    # Rodando a Janela
    janela_cadastro.mainloop()
  
 #  JANELA PRINCIPAL DO SISTEMA - PERSONALIZADO POR PERFIL DE USUSARIO/ACESSO 

# Função para idenficar o perfil do usuário e abrir a janela de menus conforme perfil.
def abrir_janela_menu(usuario_tipo):
    # Obtem o nome e-mail do usuario para a mensagem de boas vindas
    name_user = entry_usuario.get()
    email = f"{name_user.upper()}"
    nome = email.split('@')[0]
    janela_menu = tk.Toplevel()
    janela_menu.title('Gerenciamento de Biblioteca')
    label_aplicativo = tk.Label(janela_menu, text=F'Olá {nome.title()}, hoje é {data_atual_formatada}.\n\nSeja Bem Vindo ao Sistema de Gestão de Livros!', 
                                borderwidth=2, relief='solid', fg='black', bg='#2FD5D9',font=('Dreaming Outloud Pro', 12), width=40, height=10)
    label_aplicativo.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
    # Botão para sair do sistema
    botao_voltar = tk.Button(janela_menu, text='Sair', command=janela_menu.destroy)
    botao_voltar.grid(row=8, column=1, padx=10, pady=10, sticky='nsew')       
    
    # Perfil de login de usuário administrador do sistema, default de criacao junto com o banco de dados
    # usuario: admin, senha: admin, esse tipo de perfil tem acesso total ao sistema
    if usuario_tipo == 'admin':
        # Botão cadastrar usuario
        botao_cadastro = tk.Button(janela_menu, text='Cadastrar Usuários', command=cadastro)
        botao_cadastro.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')      
        # Botão cadastrar livro
        botao_livros = tk.Button(janela_menu, text='Cadastrar Livros', command=cadastrar_livro)
        botao_livros.grid(row=1, column=1,padx=10, pady=10, sticky='nsew')        
        # Adicione aqui os botões e ações específicos para administradores
        botao_remover = tk.Button(janela_menu, text='Remover Registros', command=remover)
        botao_remover.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')  
        # Botão de Consultas
        botao_consultas = tk.Button(janela_menu, text='Consultar Registros', command=consultar_dados)
        botao_consultas.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')    
        # Botão registrar reserva
        botao_reserva = tk.Button(janela_menu, text='Registrar Reservas', command=reservar_livro)
        botao_reserva.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')   
        # Botão registrar emprestimo
        botao_emprestimo = tk.Button(janela_menu, text='Registrar Empréstimos', command=registrar_emprestimo)
        botao_emprestimo.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')                   
        # Botão de controle de acesso
        botao_acesso = tk.Button(janela_menu, text='Config. Acesso', command=controle_acesso)
        botao_acesso.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')
        # Botão de controle de acesso
        botao_consulta_login = tk.Button(janela_menu, text='Perfil de Acesso', command=perfil_acesso)
        botao_consulta_login.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')
        # Botão para mudar a senha 
        botao_mudar_senha = tk.Button(janela_menu, text='Alterar Senha', command=alterar_senha)
        botao_mudar_senha.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')  
    # Perfil de login de gerente do sistema, tem acesso ao registro de reserva e empréstimo de livros para qualquer usuario,
    # Pode consultar toda a base de dados, pode atualizar a situação dos empréstimo, registrando devolução e extravio de livros e mudar sua senha.
    elif usuario_tipo == 'gerente':
        # Botão registrar reserva
        botao_reserva = tk.Button(janela_menu, text='Registrar Reservas', command=reservar_livro)
        botao_reserva.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        # Botão registrar emprestimo
        botao_emprestimo = tk.Button(janela_menu, text='Registrar Empréstimos', command=registrar_emprestimo)
        botao_emprestimo.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')           
        # Botão de Consultas
        botao_consultas = tk.Button(janela_menu, text='Consultar Registros', command=consultar_dados)
        botao_consultas.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
                # Botão para mudar a senha 
        botao_mudar_senha = tk.Button(janela_menu, text='Alterar Senha', command=alterar_senha)
        botao_mudar_senha.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')  
    # Perfil de login usuário é o perfil também chamado de cliente, ele pode pesquisar todos os livros, reservar qualquer livro
    # consultar reservas e empréstimos e alterar sua senha
    elif usuario_tipo == 'usuario':
        # Botão registrar reserva
        botao_reserva = tk.Button(janela_menu, text='Registrar Reservas', command=registro_reserva_usuario)
        botao_reserva.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
        #Botão pesquisar livro:
        botao_consulta_livros = tk.Button(janela_menu, text='Consultar Livros', command=filtro_de_livros)
        botao_consulta_livros.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')  
        # Botão consulta reservas
        botao_consulta_reservas = tk.Button(janela_menu, text='Minhas Solicitações', command=meus_pedidos)
        botao_consulta_reservas.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')  
        # Botão para mudar a senha 
        botao_mudar_senha = tk.Button(janela_menu, text='Alterar Senha', command=alterar_senha)
        botao_mudar_senha.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')         
    # Rodando a Janela
    janela_menu.mainloop()
    
# Criando a janela principal de login
janela = tk.Tk()
#Formatando o titulo
janela.title('Gestão de Biblioteca')
# label da janela principal
label_aplicativo = tk.Label(janela, text=f'SISTEMA DE GESTÃO DE LIVROS', borderwidth=1, relief='solid',
                            fg='black', bg='#2FD5D9', width=35, height=2, font=('Bauhaus 93', 18) )
label_aplicativo.grid(row=0, column=0,  columnspan=4, padx=5, pady=5, sticky='nsew')
# Cabeçalho
label_cadastro_livros = tk.Label(janela, text='Faça o Login', font=('Helvetica', 10))
label_cadastro_livros.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='nsew')
# Caixa de texto do e-mail
label_usuario = tk.Label(janela, text='E-mail:')
label_usuario.grid(row=2, column=0, padx=2, pady=5, sticky='e')
entry_usuario = tk.Entry(width=20)
entry_usuario.grid(row=2, column=1, columnspan=2, padx=2, pady=5, sticky='nsew')
# Caixa de texto do senha
label_senha = tk.Label(janela, text='Senha:')
label_senha.grid(row=3, column=0, padx=2, pady=5, sticky='e')
entry_senha = tk.Entry(width=20, show='*')
entry_senha.grid(row=3, column=1,columnspan=2, padx=2, pady=5, sticky='nsew')
# Criando botão de login e cadastro
botao_login = tk.Button(janela, text='Entrar', command=clique)
botao_login.grid(row=4, column=1, padx=2, pady=5, sticky='nsew')
botao_limpa_login = tk.Button(janela, text='Limpar', command=limpar)
botao_limpa_login.grid(row=4, column=2, padx=2, pady=5, sticky='nsew')
# Criando o rótulo para exibir mensagens de erro de login
mensagem_label_login = tk.Label(janela, text="", fg="green")
mensagem_label_login.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
# Caso não tenha dados de login o usuario poder fazer o cadastro e aguarda a liberação de acesso
label_cadastro_de_usuarios = tk.Label(janela, text='Faça o Seu Cadastro', font=('Helvetica', 10))
label_cadastro_de_usuarios.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
# Botão de cadastro  e cadastro
botao_solicita_login = tk.Button(janela, text='Cadastrar', command=faca_cadastro)
botao_solicita_login.grid(row=7, column=1, padx=2, pady=20, sticky='nsew')
# Botão sair
botao_sair = tk.Button(janela, text='Sair', command=janela.destroy)
botao_sair.grid(row=7, column=2, padx=2, pady=20, sticky='nsew')   
# Rodando a Janela
janela.mainloop()


# In[ ]:




