'''
Created on 8 de mar de 2017

@author: wendell
'''

from pyrsa.rsa import KeyGenerator
from pyrsa.rsa import RSA

import pickle
import time

def encpypt(msg_filename, encrypt_filename, encoder, pool=True):
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


if __name__ == '__main__':
    pass

    pubk_filename = './data/keys/pubk.txt'
    privk_filename = './data/keys/privk.txt'

    msg_filename = './data/sample/message.txt'
    encrypt_filename = './data/sample/encrypt_msg.dat'
    msgdec_filename = './data/sample/decod_message.txt'

    # Gerando chaves
    k = KeyGenerator(32, 512)
    k.generate(True)

    print("\nPublic (n, e): ", k.get_public_key())
    print("Private (n, d): ", k.get_private_key())

    # Salvando chaves em arquivos separados
    with open(pubk_filename, 'w+') as pubk_file:
        pubk_file.write(str(k.get_public_key()))
        pubk_file.close()

    with open(privk_filename, 'w+') as privk_file:
        privk_file.write(str(k.get_private_key()))
        privk_file.close()

    encoder = RSA(k)

    begin = time.time()
    encpypt(msg_filename, encrypt_filename, encoder, False)
    decode(encrypt_filename, msgdec_filename, encoder, False)
    end = time.time()
    print('Tempo decorrido (for): ', end - begin, 's')

    begin = time.time()
    encpypt(msg_filename, encrypt_filename, encoder, True)
    decode(encrypt_filename, msgdec_filename, encoder, True)
    end = time.time()
    print('Tempo decorrido (map): ', end - begin, 's')


