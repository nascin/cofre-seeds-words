import shutil
import os
import sys
from time import sleep
from cofre.settings import APP, DB
from cofre.db import (consultar_dados_user, 
                                 inserir_dados_user,
                                 consultar_dados_carteira_cripto,
                                 inserir_dados_carteira_cripto,
                                 _verificar_se_db_existe,
                                 excluir_item_carteira_cripto)
from cofre.utils import decrypt
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
    usuario = consultar_dados_user(DB['path_db'])
    if not usuario:
        while True:
            cabecalho()

            texto = 'Você irá criar um usuário para gerenciar suas SEEDS WORDS:'
            print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
            sleep(1)
            nome: str = input('++ Insira seu Nome: ')
            senha_app: str = input('++ Insira uma senha para acesso [usada somente para acesso ao app]: ')
            print('')

            while True:
                opcao: str = input('++ Digite [s] para salvar ou [r] para reiniciar: ')
                print('')
                if opcao == 's' or opcao == 'r':
                    break
            if opcao == 's':
                try:
                    inserir_dados_user(caminho_db=DB['path_db'],
                                       nome=nome, 
                                       senha_app=senha_app,
                                       chave_secreta=senha_app)
                    print(_centralizar_texto('USUÁRIO CRIADO COM SUCESSO!!!', _largura_altura_terminal()['largura']))
                    print('')
                    sleep(1.5)
                    inicio()
                except:
                    print(_centralizar_texto('ERRO AO SALVAR USUARIO [tente novamente]!!!', _largura_altura_terminal()['largura']))
                    print('')
                    sleep(1.5)
                    inicio()
                break

    else:
        inicio()

def login():
    _verificar_se_db_existe()
    cabecalho()

    texto = 'LOGIN'
    print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
    print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
    print('')

    usuario = consultar_dados_user(DB['path_db'])
    if usuario:
        senha_app = input('++ Insira a senha de acesso: ')
        senha_desencriptada = decrypt(consultar_dados_user(DB['path_db'])[0]['senha_app'], senha_app)
        if senha_desencriptada is not None:
            inicio()
        else:
            texto = 'SENHA DE ACESSO INCORRETA!'
            print('')
            print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
            print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
            print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
            print('')
            sleep(1.5)
            login()
    else:
        criar_usuario()

def inicio():
    cabecalho()

    opcoes = f'''Opções >> Ver seeds [1] | Adicionar seeds [2] | Buscar Seeds Words (por Id) [3] | Sair [4]'''
    print(_centralizar_texto(opcoes, _largura_altura_terminal()['largura']))
    print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
    print('')

    lista_opcoes = ['1', '2', '3', '4']

    while True:
        opcao = input('Digite uma opção do menu Opções: ')
        if opcao in lista_opcoes:
            if opcao == '1':
                buscar_todas_seeds_words()
            if opcao == '2':
                adicionar_seeds()
            if opcao == '3':
                buscar_seeds_words_por_id()
            if opcao == '4':
                sys.exit()

def buscar_todas_seeds_words():
    cabecalho()
    texto = 'Todas as SEEDS WORDS:'
    print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
    print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
    print('')

    dados_consulta = consultar_dados_carteira_cripto(DB['path_db'])

    if dados_consulta:
        lista_cabecalho = ['Id', 'Data de Criação', 'Nome Cripto', 'Nome Carteira', 'Seeds Words (criptografado)']
        lista_valores = [[valor for valor in dicionario.values()] for dicionario in dados_consulta]
        largura_coluna = int(_largura_altura_terminal()['largura'] / len(lista_cabecalho) * 1.5)
        tabela = tabulate(lista_valores, 
                        headers=lista_cabecalho, 
                        tablefmt="fancy_grid", 
                        maxcolwidths=largura_coluna)
        print(tabela)
        print('')
        while True:
            opcao = input('++ Digite [b] para buscar por Id ou [i] para voltar ao início: ')
            if opcao == 'b' or opcao == 'i':
                break
        if opcao == 'b':
            buscar_seeds_words_por_id()
        elif opcao == 'i':
            inicio()
    else:
        print(_centralizar_texto('NÃO EXISTE SEEDS WORDS PARA CONSULTA!!!', _largura_altura_terminal()['largura']))
        sleep(1.5)
        inicio()

def buscar_seeds_words_por_id():
    cabecalho()
    texto = 'Buscar SEEDS WORDS por Id'
    print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
    print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
    print('')

    dados_consulta = consultar_dados_carteira_cripto(DB['path_db'])
    lista_valores = [[valor for valor in dicionario.values()] for dicionario in dados_consulta]

    while True:
        try:
            id_carteira = int(input('++ Digite o ID seeds words para buscar: '))
            if isinstance(id_carteira, int):
                break
            else:
                print('-- Digite um número inteiro!')
        except ValueError:
            print('-- Digite um número inteiro!')

    if len(lista_valores) == 0:
        print(_centralizar_texto('SEEDS WORDS NÃO ENCONTRADA!!!', _largura_altura_terminal()['largura']))
        sleep(1.5)
        print('')
        while True:
            opcao = input('++ Digite [b] para nova busca, ou [i] para voltar ao início: ')
            if opcao == 'b' or opcao == 'i':
                break
        if opcao == 'b':
            buscar_seeds_words_por_id()
        elif opcao == 'i':
            inicio()
    else:
        for valor in lista_valores:
            if valor[0] == id_carteira:
                lista_cabecalho = ['Id', 'Data de Criação', 'Nome Cripto', 'Nome Carteira', 'Seeds Words (criptografado)']
                largura_coluna = int(_largura_altura_terminal()['largura'] / len(lista_cabecalho) * 1.5)
                tabela = tabulate([valor], 
                                headers=lista_cabecalho, 
                                tablefmt="fancy_grid", 
                                maxcolwidths=largura_coluna)
                print(tabela)
                print('')

                while True:
                    opcao = input('++ Digite [d] para desencriptar, [b] nova busca, [e] excluir ou [i] para voltar ao início: ')
                    if opcao == 'd' or opcao == 'b' or opcao == 'e' or opcao == 'i':
                        break
                if opcao == 'd':
                    chave_secreta = input('++ Insira a chave secreta: ')
                    seeds_desencriptada = decrypt(valor[4], chave_secreta)

                    if seeds_desencriptada is not None:
                        texto = 'SEEDS WORDS DESENCRIPTADA:'
                        print('')
                        print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print('')
                        print(seeds_desencriptada)
                        print('')
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print('')
                    else:
                        texto = 'CHAVE SECRETA INVÁLIDA!'
                        print('')
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print('')

                    while True:
                        nova_opcao = input('++ Digite [b] para nova busca ou [i] para voltar ao início: ')
                        if nova_opcao == 'b' or nova_opcao == 'i':
                            break
                    if nova_opcao == 'b':
                        buscar_seeds_words_por_id()
                    elif nova_opcao == 'i':
                        inicio()
                elif opcao == 'b':
                    buscar_seeds_words_por_id()
                elif opcao == 'e':
                    chave_secreta = input('++ Insira a chave secreta para DELETAR seeds words: ')
                    seeds_desencriptada = decrypt(valor[4], chave_secreta)

                    if seeds_desencriptada is not None:
                        excluir_item_carteira_cripto(caminho_db=DB['path_db'],id=valor[0])

                        texto = f'SEEDS WORDS [Cripto: {valor[2]} - Nome da Carteira {valor[3]}] DELETADA!'
                        print('')
                        print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print('')
                        print(f'PALAVRAS SECRETAS: ({seeds_desencriptada})')
                        print('')
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print('')
                        sleep(5)
                        inicio()
                    else:
                        texto = 'CHAVE SECRETA INVÁLIDA!'
                        print('')
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
                        print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                        print('')
                        sleep(1.5)
                        buscar_seeds_words_por_id()

                elif opcao == 'i':
                    inicio()

def adicionar_seeds():
    cabecalho()

    opcoes = f'''Opções >> Ver seeds [1] | Adicionar seeds [2]'''
    print(_centralizar_texto(opcoes, _largura_altura_terminal()['largura']))
    print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
    print('')

    lista_opcoes = ['1', '2']

    while True:
        cabecalho()

        texto = 'Adicionar novas SEEDS WORDS:'
        print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
        print('')
        sleep(1)
        nome_cripto: str = input('++ Insira o nome da Blockchain: ')
        nome_carteira: str = input('++ Insira o nome da carteira [Ex: carteira principal]: ')
        palavras: str = input('++ Insira as SEEDS WORDS [separadas por espaço]: ')
        chave_secreta = input('++ Insira uma CHAVE SECRETA [usada para desencriptar suas SEEDS WORDS]: ')
        print('')

        while True:
            opcao: str = input('++ Digite [s] para salvar, [r] para reiniciar ou [i] para voltar ao início: ')
            print('')
            if opcao == 's' or opcao == 'r' or opcao == 'i':
                break
        if opcao == 's':
            try:
                inserir_dados_carteira_cripto(caminho_db=DB['path_db'],
                                              nome_cripto=nome_cripto, 
                                              nome_carteira=nome_carteira, 
                                              palavras=palavras,
                                              chave_secreta=chave_secreta)
                
                texto = 'SEEDS WORDS ADICIONADAS COM SUCESSO!!!'
                print('')
                print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                print('')
                print(_centralizar_texto(texto, _largura_altura_terminal()['largura']))
                print('')
                print(_centralizar_texto('-'*_largura_altura_terminal()['largura'], _largura_altura_terminal()['largura']))
                print('')
                sleep(1.5)
                inicio()
            except:
                print(_centralizar_texto('ERRO AO ADICIONAR NOVAS SEEDS WORDS [tente novamente]!!!', _largura_altura_terminal()['largura']))
                print('')
                sleep(1.5)
                adicionar_seeds()
            break
        elif opcao == 'i':
            inicio()
            break
