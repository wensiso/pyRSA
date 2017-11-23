"""
Created on 8 de mar de 2017

@author: wendell
"""
from binhex import openrsrc

from UnityTweakTool.elements import option

from pyrsa.rsa import RSAKey, RSA
from optparse import OptionParser

import pickle
import time
import sys


prog = 'pyRSA'
cmd = 'python3 pyrsa.py'
version = '0.1'
div = '\n------------------------------'

usage = cmd + ' -e <arquivo_em_texto_aberto> -o <saída_encriptada> [options]'
usage += '\n' + cmd + '-d <arquivo_encriptado> -o <saída_em_texto_aberto> [options].'

parser = OptionParser(prog=prog, usage=usage, version='%prog ' + version)

parser.add_option("-e", "--encrypt", dest="msg_filename", type='str',
                  help='arquivo aberto para ser encriptado')
parser.add_option("-d", "--decrypt", dest="encrypt_filename", type='str',
                  help='arquivo encriptado para ser decifrado')
parser.add_option('-o', '--output', dest='dest_filename', type='str',
                  help='arquivo de destino/saída.')
parser.add_option("-l", "--list", dest="list", action='store_true', default='False',
                  help='não utiliza map-reduce para encriptar/desencriptar (mais lento - desligado por padrão)')
parser.add_option("-k", "--keys", dest="genkeys", action='store_true', default='False',
                  help='gera um novo par de chaves')
parser.add_option("-v", "--verbose", dest="verbose", action='store_true',
                  default='False', help='imprime o arquivo aberto')


# noinspection PyShadowingNames,PyShadowingNames,PyShadowingNames
def encrypt(msg_filename, encrypt_filename, encoder, pool=True):
    print("\nArquivo da mensagem original: ", msg_filename)
    with open(msg_filename, 'r') as msgfile:
        msg = msgfile.read()
        # print("Mensagem original: ", m)
        msgfile.close()

        print("\nEncriptando arquivo...")
        c = encoder.encode_str(msg, pool)

        # Salvando arquivo encriptado
        print("Salvando arquivo encriptado em: ", encrypt_filename)
        with open(encrypt_filename, 'wb+') as encfile:
            pickle.dump(c, encfile)
            # print("Arquivo encriptado ", c)
            encfile.close()


# noinspection PyShadowingNames,PyShadowingNames
def decode(encrypt_filename, msgdec_filename, decoder, pool=True):
    print("\nAbrindo arquivo encriptado: ", encrypt_filename)
    with open(encrypt_filename, 'rb') as encfile:
        c = pickle.Unpickler(encfile).load()
        print("Desencriptando arquivo...")
        msgdec = decoder.decode_str(c, pool)
        # print ("\nArquivo desencriptado: ", msgdec)
        encfile.close()

        # Salvando arquivo desencriptado
        with open(msgdec_filename, 'w+') as decfile:
            print("Salvando arquivo desencriptado em: ", msgdec_filename)
            decfile.write(msgdec)
            decfile.close()


def main():

    print(prog, version, div)
    (options, args) = parser.parse_args()

    out_filename = ''
    reuse = False
    mapreduce = True
    pubk_filename = './data/keys/pubk.txt'
    privk_filename = './data/keys/privk.txt'

    if options.list is True:
        mapreduce = False

    if options.dest_filename:
        out_filename = options.dest_filename
    else:
        print("É obrigatório informar um arquivo de saída", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    k = RSAKey(verbose=True)

    if options.genkeys is True:

        k.auto_build(True)

        print('Gerando as chaves...')
        print("\nPublic (n, e): ", k.get_public())
        print("Private (n, d): ", k.get_private())

        # Salvando chaves em arquivos separados
        with open(pubk_filename, 'w+') as pubk_file:
            pubk_file.write(str(k.get_public()))
            pubk_file.close()

        with open(privk_filename, 'w+') as privk_file:
            privk_file.write(str(k.get_private()))
            privk_file.close()

            reusestr = input('Reutilizar a chave recém-gerada (S/N)? ')

        reuse = True
        if reusestr.startswith('n') or reusestr.startswith('N'):
            reuse = False

    if reuse is False:
        if options.msg_filename:
            print('Informe a chave pública (n, e): ')
            n = input('n: ')
            e = input('e: ')
            k.set_public(int(n), int(e))
            print('Sua chave pública:', k.get_public())
        elif options.encrypt_filename:
            print('Informe a chave privada (n, d): ')
            n = input('n: ')
            e = input('d: ')
            k.set_private(int(n), int(e))
            print('Sua chave privada:', k.get_private())

    encoder = RSA(k)

    begin = time.time()
    if options.msg_filename:
        print('Encriptando arquivo', options.msg_filename, '...')
        begin = time.time()
        encrypt(options.msg_filename, out_filename, encoder, mapreduce)
    elif options.encrypt_filename:
        print('Decriptando arquivo', options.encrypt_filename, '...')
        begin = time.time()
        decode(options.encrypt_filename, out_filename, encoder, mapreduce)
    else:
        print("É obrigatório informar um arquivo de entrada", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    end = time.time()
    print('Tempo decorrido: ', end - begin, 's')
    print('Arquivo salvo: ', out_filename)


if __name__ == '__main__':
    pass
    main()
