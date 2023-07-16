import shutil
import os
from time import sleep
from projeto_palavras.settings import APP
from projeto_palavras.db import (consultar_dados_user, 
                                 inserir_dados_user,
                                 consultar_dados_carteira_cripto)
from tabulate import tabulate


def _largura_altura_terminal():
    largura_terminal, altura_terminal = shutil.get_terminal_size()
    return {'largura': largura_terminal, 'altura': altura_terminal}

def _centralizar_texto(texto, largura_terminal):
    espacos = (largura_terminal - len(texto)) // 2
    texto_centralizado = " " * espacos + texto
    return texto_centralizado

def _limpar_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux, macOS, etc.
        os.system('clear')

def cabecalho():
    _limpar_terminal()

    texto_cabecalho = f' {APP["nome"]} - {APP["versao"]} '
    largura = _largura_altura_terminal()['largura'] - len(texto_cabecalho)
    
    form = '=' * int(largura // 2 - 1)
    texto = f'{form} {texto_cabecalho} {form}'
    print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
    print('')

def criar_usuario():
    usuario = consultar_dados_user()
    if not usuario:
        while True:
            cabecalho()

            texto = 'Você irá criar um usuário para gerenciar suas SEEDS WORDS:'
            print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
            sleep(1)
            nome: str = input('++ Digite seu Nome: ')
            senha_app: str = input('++ Digite uma senha para acesso [usada somente para acesso ao app]: ')
            chave_palavras: str = input('++ Digite uma chave de segurança [usada para acessar suas SEEDS WORDS]: ')
            print('')

            while True:
                opcao: str = input('++ Digite [s] para salvar ou [r] para reiniciar: ')
                print('')
                if opcao == 's' or opcao == 'r':
                    break
            if opcao == 's':
                try:
                    inserir_dados_user(nome=nome, 
                                       senha_app=senha_app, 
                                       chave_palavras=chave_palavras,
                                       chave_secreta=senha_app)
                    print(_centralizar_texto('USUÁRIO CRIADO COM SUCESSO!!!', _largura_altura_terminal()['largura']))
                    print('')
                except:
                    print(_centralizar_texto('ERRO AO SALVAR USUARIO [feche o programa e abra novamente]!!!', _largura_altura_terminal()['largura']))
                    print('')
                break

    else:
        inicio()

        
def inicio():
    _limpar_terminal()
    cabecalho()

    opcoes = f'''Opções >> Ver seeds [1] | Adicionar seeds [2]'''
    print(_centralizar_texto(opcoes, _largura_altura_terminal()['largura']))
    print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
    print('')

    lista_opcoes = ['1', '2']

    while True:
        dados_consulta = consultar_dados_carteira_cripto()
        
        opcao = input('Digite uma opção: ')
        if opcao in lista_opcoes:
            if opcao == '1':
                if dados_consulta:
                    lista_cabecalho = ['Id', 'Data de Criação', 'Nome Cripto', 'Nome Carteira', 'Seeds Words (criptografado)']
                    lista_valores = [[valor for valor in dicionario.values()] for dicionario in dados_consulta]
                    largura_coluna = int(_largura_altura_terminal()['largura'] / len(lista_cabecalho) * 1.5)
                    tabela = tabulate(lista_valores, 
                                    headers=lista_cabecalho, 
                                    tablefmt="fancy_grid", 
                                    maxcolwidths=largura_coluna)
                    print(tabela)
                else:
                    print(_centralizar_texto('NÃO EXISTE SEEDS SALVA', _largura_altura_terminal()['largura']))