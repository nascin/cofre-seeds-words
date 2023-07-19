import os
import sqlite3
import pytest
from cofre.db import (criar_db, 
                      inserir_dados_carteira_cripto,
                      inserir_dados_user,
                      excluir_item_carteira_cripto)
from cofre.utils import excluir_arquivo, decrypt


class TestBancoDeDados:
    @pytest.fixture
    def caminho_testes(self):
        return 'tests/dados'

    def criar_db_teste(self, caminho_db: str):
        criar_db(caminho_db)

    def limpeza_db_teste(self, caminho_db: str):
        excluir_arquivo(caminho_db)

    def test_criar_db(self, caminho_testes):
        '''Teste para criar banco de dados'''

        caminho_arquivo_db = os.path.join(caminho_testes, 'criar_db.sqlite3')
        self.criar_db_teste(caminho_arquivo_db)
        
        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect(caminho_arquivo_db)
            cursor = conn.cursor()

            # Verificar se a tabela foi criada corretamente
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='carteira_cripto'")
            result = cursor.fetchone()
            assert result is not None

            # Verificar se as colunas foram criadas corretamente
            cursor.execute("PRAGMA table_info(carteira_cripto)")
            columns = cursor.fetchall()
            expected_columns = [
                (0, 'id', 'INTEGER', 0, None, 1),
                (1, 'data_criacao', 'DATE', 0, None, 0),
                (2, 'nome_cripto', 'VARCHAR(255)', 0, None, 0),
                (3, 'nome_carteira', 'VARCHAR(255)', 0, None, 0),
                (4, 'palavras', 'VARCHAR(255)', 0, None, 0)
            ]
            assert columns == expected_columns

        finally:
            conn.close()
            self.limpeza_db_teste(caminho_arquivo_db)

    def test_inserir_dados_carteira_cripto(self, caminho_testes):
        '''Teste inserir dados da carteira'''

        caminho_arquivo_db = os.path.join(caminho_testes, 'inserir_dados_carteira_cripto.sqlite3')
        self.criar_db_teste(caminho_arquivo_db)

        nome_cripto = "Bitcoin"
        nome_carteira = "Carteira1"
        palavras = "palavras_secretas"
        chave_secreta = "chave_secreta_teste"

        # Função que será testada
        inserir_dados_carteira_cripto(caminho_arquivo_db, nome_cripto, nome_carteira, palavras, chave_secreta)

        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect(caminho_arquivo_db)
            cursor = conn.cursor()

            # Verificar se os dados foram inseridos corretamente
            cursor.execute("SELECT * FROM carteira_cripto WHERE nome_cripto = ? AND nome_carteira = ?",
                        (nome_cripto, nome_carteira))
            result = cursor.fetchone()
            assert result is not None
            assert result[2] == nome_cripto
            assert result[3] == nome_carteira
            assert decrypt(result[4], chave_secreta) == palavras

        finally:
            conn.close()
            self.limpeza_db_teste(caminho_arquivo_db)

    def test_inserir_dados_user(self, caminho_testes):
        '''Teste inserir dados do usuário'''

        caminho_arquivo_db = os.path.join(caminho_testes, 'inserir_dados_user.sqlite3')
        self.criar_db_teste(caminho_arquivo_db)

        nome = "Mailson"
        senha_app = "Senha_app"
        chave_secreta = "chave_secreta_teste"

        # Função que será testada
        inserir_dados_user(caminho_arquivo_db, nome, senha_app, chave_secreta)

        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect(caminho_arquivo_db)
            cursor = conn.cursor()

            # Verificar se os dados foram inseridos corretamente
            cursor.execute("SELECT * FROM user WHERE id = ?",('1'))
            result = cursor.fetchone()
            assert result is not None
            assert result[2] == nome
            assert decrypt(result[3], chave_secreta) == senha_app

        finally:
            conn.close()
            self.limpeza_db_teste(caminho_arquivo_db)

    def test_excluir_item_carteira_cripto(self, caminho_testes):
        '''Teste para deletar seeds words'''

        # Criar banco e inserir dados para teste
        caminho_arquivo_db = os.path.join(caminho_testes, 'deletar_item_carteira_cripto.sqlite3')
        self.criar_db_teste(caminho_arquivo_db)
        inserir_dados_carteira_cripto(caminho_db=caminho_arquivo_db,
                                      nome_cripto='Bitcoin',
                                      nome_carteira='Carteira Principal',
                                      palavras='palavras_de_recuperação',
                                      chave_secreta='chave_secreta')

        try:
            # Executa a função de exclusão do item
            excluir_item_carteira_cripto(caminho_arquivo_db, id='1')

            # Verifica se o item foi excluído corretamente
            conn = sqlite3.connect(caminho_arquivo_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM carteira_cripto WHERE id=?", ('1',))
            result = cursor.fetchone()

            # Verifica se o item foi excluído corretamente
            assert result is None
        finally:
            # Fecha a conexão com o banco de dados
            conn.close()
            self.limpeza_db_teste(caminho_arquivo_db)