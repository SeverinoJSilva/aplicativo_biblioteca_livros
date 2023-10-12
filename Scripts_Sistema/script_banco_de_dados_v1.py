#!/usr/bin/env python
# coding: utf-8

# # Criando um banco de dados

# In[1]:


# importando sqlite3
import sqlite3
# Abre uma conexão com um banco de dados e caso não exista o sistema cria
conn = sqlite3.connect('biblioteca_V1.db')
cursor = conn.cursor()

# Script do banco de dados
# 1. Criar a tabela Usuario
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_usuario (
        ID_USUARIO INTEGER PRIMARY KEY,
        NOME VARCHAR(60) NOT NULL,
        TELEFONE VARCHAR(20) NOT NULL,
        ENDERECO VARCHAR(60) NOT NULL,
        EMAIL VARCHAR(60) NOT NULL UNIQUE,
        SENHA_USUARIO TEXT NOT NULL, 
        TIPO_USUARIO TEXT NOT NULL DEFAULT 'usuario'
    )
''')

# 2. Criar a tabela Livro
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_livro (
        ID_ISBN INTEGER PRIMARY KEY,
        TITULO VARCHAR(60) NOT NULL,
        AUTOR VARCHAR(60) NOT NULL,
        EDITORA VARCHAR(30) NOT NULL,
        ANO INTEGER NOT NULL,
        PAGINAS INTEGER,
        VALOR DECIMAL(10, 2) NOT NULL,
        QUANTIDADE INTEGER(10),
        DESCRICAO VARCHAR(60),
        COMENTARIO VARCHAR(10000)
    )
''')

# 3. Criar a tabela Reserva
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_reserva (
        ID_RESERVA INTEGER PRIMARY KEY,
        DATA_RESERVA DATE,
        ID_USUARIO INTEGER,
        ID_ISBN INTEGER,
        FOREIGN KEY (ID_USUARIO) REFERENCES tb_usuario (ID_USUARIO)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ID_ISBN) REFERENCES tb_livro (ID_ISBN)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
''')

# 4. Criar a tabela Emprestimo
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_emprestimo (
        ID_EMPRESTIMO INTEGER PRIMARY KEY,
        DATA_RETIRADA DATE,
        DATA_DEVOLUCAO DATE,
        SITUACAO_EMPRESTIMO,
        ID_USUARIO INTEGER,
        ID_ISBN INTEGER,
        FOREIGN KEY (ID_USUARIO) REFERENCES tb_usuario (ID_USUARIO)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ID_ISBN) REFERENCES tb_livro (ID_ISBN)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
''')

# Verificar se já existe um administrador na tabela 'tb_usuario'
cursor.execute("SELECT ID_USUARIO FROM tb_usuario WHERE NOME = 'admin'")
admin_exists = cursor.fetchone()
# Se não existe um administrador, insira os dados do administrador do sistema
if not admin_exists:
    cursor.execute("INSERT INTO tb_usuario (ID_USUARIO, NOME, TELEFONE, ENDERECO, EMAIL, SENHA_USUARIO, TIPO_USUARIO) VALUES (?,?,?,?,?,?,?)",
                   (20230000, 'admin', 'admin','admin', 'admin','admin', 'admin'))

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados criados com sucesso!")


# In[ ]:




