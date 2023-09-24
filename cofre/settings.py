import os


# Aplicação
class App:
    nome = 'COFRE PALAVRAS CHAVE'
    versao = 'v1.1.1'

app = App()

# Banco de dados
class Db:
    path_db = os.path.join(os.getcwd(), 'db_palavras_chave.sqlite3') 

db = Db()