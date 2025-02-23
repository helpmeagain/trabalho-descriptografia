import re
from unidecode import unidecode
import numpy as np
import string

def parse(file_name):

	# abre o arquivo para leitura
	with open(file_name, 'r') as arquivo_entrada:
	    # lê o conteúdo do arquivo
	    conteudo = arquivo_entrada.read()

	# transforma as letras em minúsculas
	conteudo = conteudo.lower()

	# remove os acentos das vogais
	conteudo = unidecode(conteudo)

	# remove todos os caracteres que não são letras
	conteudo = re.sub(r'[^a-z]', '', conteudo)
	return conteudo

def save_file(file_name,conteudo):
	# abre um novo arquivo para escrita
	with open(file_name, 'w') as arquivo_saida:
	    # escreve o conteúdo no arquivo
	    arquivo_saida.write(conteudo)

def enc_monosyllabic(conteudo,tamanho,grupo):
	n = len(conteudo)-tamanho+1
	r = np.random.randint(0, n)
	texto_aberto = conteudo[r:r+tamanho]

	az = string.ascii_lowercase

	key = np.random.permutation(26)
	key = ''.join([az[key[i]] for i in range(26)])

	key_enc = {az[i] : key[i] for i in range(26)}
	key_dec = {key[i] : az[i] for i in range(26)}

	texto_cifrado = [key_enc[i] for i in texto_aberto]

	# texto_aberto = [key_dec[i] for i in texto_cifrado]

	save_file('Cifrado/Mono/' + grupo + '_' + 'texto_cifrado.txt',''.join(texto_cifrado))
	save_file('Aberto/Mono/' + grupo + '_' + 'key.txt',key)
	save_file('Aberto/Mono/' + grupo + '_' + 'texto_aberto.txt',''.join(texto_aberto))

def inv_multiplicativo(b,m):
  A = np.array([1, 0, m])
  B = np.array([0, 1, b])
  
  while True:
    if B[2] == 0:
      return 0
  
    if B[2] == 1:
      return B[1] % m 
  
    Q = np.floor( A[2]/B[2] )
    T = A - Q*B
    A = B
    B = T


def enc_hill(conteudo,tamanho,grupo):
	n = len(conteudo)-tamanho+1
	r = np.random.randint(0, n)
	texto_aberto = conteudo[r:r+tamanho]

	az = string.ascii_lowercase
	alf2dec = {az[i] : i for i in range(26)}
	dec2alf = {i : az[i] for i in range(26)}

	while True:
		key = np.random.randint(0,26,(2,2))
		if np.linalg.det(key) in [1,3,5,7,9,11,15,17,19,21,23,25]:
			inv_det = inv_multiplicativo(np.linalg.det(key),26)
			inv_key = np.array([ [key[1,1], -key[0,1]], [-key[1,0], key[0,0]]])
			inv_key = (inv_det*inv_key) % 26
			break


	texto_numerico = [alf2dec[i] for i in texto_aberto]
	texto_cifrado = np.array(texto_numerico).reshape((50,2)).T
	texto_cifrado = key@texto_cifrado % 26
	texto_cifrado = texto_cifrado.T.reshape(tamanho)
	texto_cifrado = [dec2alf[i] for i in texto_cifrado]


	# texto_numerico = [alf2dec[i] for i in texto_cifrado]
	# texto_aberto = np.array(texto_numerico).reshape((50,2)).T
	# texto_aberto = inv_key@texto_aberto % 26
	# texto_aberto = texto_aberto.T.reshape(tamanho)
	# texto_aberto = [dec2alf[i] for i in texto_aberto]


	save_file('Cifrado/Hill/' + grupo + '_' + 'texto_cifrado.txt',''.join(texto_cifrado))
	save_file('Aberto/Hill/' + grupo + '_' + 'key.txt',np.array2string(key))
	save_file('Aberto/Hill/' + grupo + '_' + 'texto_aberto.txt',''.join(texto_aberto))

def enc_vigenere(conteudo,tamanho,grupo):
	n = len(conteudo)-tamanho+1

	r = np.random.randint(0, n)
	texto_aberto1 = conteudo[r:r+tamanho]
	r = np.random.randint(0, n)
	texto_aberto2 = conteudo[r:r+tamanho]

	key = np.random.randint(0, 26, (tamanho))

	az = string.ascii_lowercase
	alf2dec = {az[i] : i for i in range(26)}
	dec2alf = {i : az[i] for i in range(26)}

	texto_numerico = [alf2dec[i] for i in texto_aberto1]
	texto_cifrado1 = ( np.array(texto_numerico) + key ) % 26
	texto_cifrado1 = [dec2alf[i] for i in texto_cifrado1]

	texto_numerico = [alf2dec[i] for i in texto_aberto2]
	texto_cifrado2 = ( np.array(texto_numerico) + key ) % 26
	texto_cifrado2 = [dec2alf[i] for i in texto_cifrado2]

	key_texto = [dec2alf[i] for i in key]


	save_file('Cifrado/Vigenere/' + grupo + '_' + 'texto_cifrado1.txt',''.join(texto_cifrado1))
	save_file('Cifrado/Vigenere/' + grupo + '_' + 'texto_cifrado2.txt',''.join(texto_cifrado2))
	save_file('Aberto/Vigenere/' + grupo + '_' + 'key.txt',''.join(key_texto))
	save_file('Aberto/Vigenere/' + grupo + '_' + 'texto_aberto1.txt',''.join(texto_aberto1))
	save_file('Aberto/Vigenere/' + grupo + '_' + 'texto_aberto2.txt',''.join(texto_aberto2))


def main():

	conteudo = parse('policarpo_quaresma.txt')
	group = 'Grupo00'

	enc_monosyllabic(conteudo,100,group)
	enc_hill(conteudo,100,group)
	enc_vigenere(conteudo,100,group)



if __name__ == "__main__":
    main()	
