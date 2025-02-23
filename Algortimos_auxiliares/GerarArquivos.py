import numpy as np
import os
import string

def save_file(file_name, conteudo):
    with open(file_name, 'w') as arquivo_saida:
        arquivo_saida.write(conteudo)

def mono_decrypt(ciphertext, key):
    with open(ciphertext, 'r') as f:
        texto_cifrado = f.read()
    
    with open(key, 'r') as f:
        key = f.read()
    
    az = string.ascii_lowercase
    key_dec = {key[i]: az[i] for i in range(26)}
    
    texto_decifrado = [key_dec[i] for i in texto_cifrado]
    return ''.join(texto_decifrado)

def mod_inverse(det, mod):
    for i in range(1, mod):
        if (det * i) % mod == 1:
            return i
    return None

def hill_decrypt(ciphertext, key_file):
    with open(ciphertext, 'r') as f:
        ciphertext = f.read()
    
    with open(key_file, 'r') as f:
        key_str = f.read().strip()
    
    key_str = key_str.replace('[', '').replace(']', '')
    key_rows = key_str.split('\n')
    key_matrix = np.array([list(map(int, row.split())) for row in key_rows])
    
    alphabet = string.ascii_lowercase
    mod = len(alphabet)
    
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = mod_inverse(det % mod, mod)
    if det_inv is None:
        raise ValueError("A chave fornecida não possui inverso modular.")
    
    adjugate = np.array([[key_matrix[1, 1], -key_matrix[0, 1]],
                          [-key_matrix[1, 0], key_matrix[0, 0]]])
    inverse_key_matrix = (det_inv * adjugate) % mod
    
    ciphertext = ciphertext.replace(" ", "")
    if len(ciphertext) % 2 != 0:
        ciphertext += "x"
    
    decrypted_text = ""
    for i in range(0, len(ciphertext), 2):
        pair = ciphertext[i:i+2]
        try:
            if pair[0] in alphabet and pair[1] in alphabet:
                vector = np.array([[alphabet.index(pair[0])], [alphabet.index(pair[1])]])
                decrypted_vector = np.dot(inverse_key_matrix, vector) % mod
                decrypted_text += alphabet[int(decrypted_vector[0, 0])]
                decrypted_text += alphabet[int(decrypted_vector[1, 0])]
        except ValueError:
            pass
    
    return decrypted_text

def vigenere_decrypt(ciphertext, key):
    with open(ciphertext, 'r') as f:
        ciphertext = f.read()
    
    with open(key, 'r') as f:
        key = f.read()
    
    alphabet = string.ascii_lowercase
    key = key.lower()
    ciphertext = ciphertext.lower()
    
    decrypted_text = ""
    key_index = 0
    
    for char in ciphertext:
        if char in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            decrypted_char = alphabet[(alphabet.index(char) - shift) % len(alphabet)]
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char
    
    return decrypted_text

def main():
    base_path = 'Texto_conhecido'
    grupo = 'Grupo05'

    cifrado_file = os.path.join(base_path, 'Cifrado', 'Mono', f'{grupo}_texto_cifrado.txt')
    key_file = os.path.join(base_path, 'Aberto', 'Mono', f'{grupo}_key.txt')
    texto_decifrado = mono_decrypt(cifrado_file, key_file)
    save_file(os.path.join(base_path, 'Aberto', 'Mono', f'{grupo}_texto_decifrado.txt'), texto_decifrado)

    cifrado_file = os.path.join(base_path, 'Cifrado', 'Hill', f'{grupo}_texto_cifrado.txt')
    key_file = os.path.join(base_path, 'Aberto', 'Hill', f'{grupo}_key.txt')
    texto_decifrado = hill_decrypt(cifrado_file, key_file)
    save_file(os.path.join(base_path, 'Aberto', 'Hill', f'{grupo}_texto_decifrado.txt'), texto_decifrado)

    cifrado_file = os.path.join(base_path, 'Cifrado', 'Vigenere', f'{grupo}_texto_cifrado1.txt')
    key_file = os.path.join(base_path, 'Aberto', 'Vigenere', f'{grupo}_key.txt')
    texto_decifrado = vigenere_decrypt(cifrado_file, key_file)
    save_file(os.path.join(base_path, 'Aberto', 'Vigenere', f'{grupo}_texto_decifrado1.txt'), texto_decifrado)

    cifrado_file = os.path.join(base_path, 'Cifrado', 'Vigenere', f'{grupo}_texto_cifrado2.txt')
    texto_decifrado = vigenere_decrypt(cifrado_file, key_file)
    save_file(os.path.join(base_path, 'Aberto', 'Vigenere', f'{grupo}_texto_decifrado2.txt'), texto_decifrado)

if __name__ == "__main__":
    main()