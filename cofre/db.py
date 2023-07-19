import os
import sqlite3
from cofre.utils import data_atual, encrypt
from cofre.settings import DB


def _verificar_se_db_existe(camiho_db: str=DB['path_db']):
    if not os.path.exists(camiho_db):
        criar_db(camiho_db)

def criar_db(caminho_db: str):
    # Conexão com o banco de dados
    conn = sqlite3.connect(caminho_db)

    # Criar tabela carteira_cripto
    try:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS carteira_cripto (
            id INTEGER PRIMARY KEY,
            data_criacao DATE,
            nome_cripto VARCHAR(255),
            nome_carteira VARCHAR(255),
            palavras VARCHAR(255)
        );''')
        print('++ tabela CARTEIRA_CRIPTO criada')
    except Exception as err:
        print(f'++ Erro ao criar a tabela CARTEIRA_CRIPTO: {err}')

    # Criar tabela user
    try:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            data_criacao DATE,
            nome VARCHAR(255),
            senha_app VARCHAR(255)
        );''')
        print('++ tabela USER criada')
    except Exception as err:
        print(f'++ Erro ao criar a tabela USER: {err}')
    finally:
        # Confirmar as alterações
        conn.commit()
        # Fechando a conexão com o banco de dados
        conn.close()

def inserir_dados_carteira_cripto(caminho_db: str, nome_cripto: str, nome_carteira: str, palavras: str, chave_secreta: str):
    try:
        # Conectando ao banco de dados
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()

        # Dados a serem inseridos
        data_criacao = data_atual()
        nome_cripto = nome_cripto
        nome_carteira = nome_carteira
        palavras = encrypt(palavras, chave_secreta)

        # Executando a inserção de dados
        cursor.execute("INSERT INTO carteira_cripto (data_criacao, nome_cripto, nome_carteira, palavras) VALUES (?, ?, ?, ?)",
                    (data_criacao, nome_cripto, nome_carteira, palavras))

        # Salvando a transação
        conn.commit()
    except:
        assert f'Erro ao consultar dados'
    finally:
        # Fechando a conexão com o banco de dados
        conn.close()

def inserir_dados_user(caminho_db: str, nome: str, senha_app: str, chave_secreta: str):
    try:
        # Conectando ao banco de dados
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()

        # Dados a serem inseridos
        data_criacao = data_atual()
        nome = nome
        senha_app = encrypt(senha_app, chave_secreta)

        # Executando a inserção de dados
        cursor.execute("INSERT INTO user (data_criacao, nome, senha_app) VALUES (?, ?, ?)",
                    (data_criacao, nome, senha_app))

        # Salvando a transação
        conn.commit()
    except:
        assert f'Erro ao consultar dados'
    finally:
        # Fechando a conexão com o banco de dados
        conn.close()

def consultar_dados_carteira_cripto(caminho_db: str):
    try:
        # Conectando ao banco de dados
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()

        # Executando a consulta de dados
        cursor.execute('SELECT * FROM carteira_cripto')

        # Recuperando os resultados da consulta
        resultados = cursor.fetchall()
        dados: list = []

        for resultado in resultados:
            dados.append(
                {
                    "id": resultado[0],
                    "data_criacao": resultado[1],
                    "nome_cripto": resultado[2],
                    "nome_carteira": resultado[3],
                    "palavras": resultado[4]
                }
            )
        return dados
    except:
        assert f'Erro ao consultar dados'
    finally:
        # Fechando a conexão com o banco de dados
        conn.close()

def consultar_dados_user(caminho_db: str):
    try:
        # Conectando ao banco de dados
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()

        # Executando a consulta de dados
        cursor.execute('SELECT * FROM user')

        # Recuperando os resultados da consulta
        resultados = cursor.fetchall()
        dados: list = []

        for resultado in resultados:
            dados.append(
                {
                    "id": resultado[0],
                    "data_criacao": resultado[1],
                    "nome": resultado[2],
                    "senha_app": resultado[3]
                }
            )
        return dados
    except:
        assert f'Erro ao consultar dados'
    finally:
        # Fechando a conexão com o banco de dados
        conn.close()

def excluir_item_carteira_cripto(caminho_db: str, id: str):
    try:
        # Conectando ao banco de dados
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()

        # Excluindo o item da tabela
        cursor.execute('DELETE FROM carteira_cripto WHERE id = ?', (id,))

        # Commit das alterações no banco de dados
        conn.commit()
    except:
        assert f'Erro ao deletar {id}'
    finally:
        # Fechando a conexão com o banco de dados
        conn.close()
