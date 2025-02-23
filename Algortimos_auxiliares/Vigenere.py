import string
from collections import defaultdict
import unicodedata

def preprocess_book(book_path):
    with open(book_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    processed = []
    for c in text:
        if c in string.ascii_lowercase:
            processed.append(c)
        else:
            normalized = unicodedata.normalize('NFD', c)
            stripped = ''.join([char for char in normalized if not unicodedata.combining(char)])
            if stripped in string.ascii_lowercase:
                processed.append(stripped)
    return ''.join(processed)

def char_to_num(c):
    return ord(c) - ord('a')

def num_to_char(n):
    return chr(n % 26 + ord('a'))

def find_plaintexts(cipher1, cipher2, book_text):
    len_msg = len(cipher1)
    diff = [(char_to_num(cipher1[i]) - char_to_num(cipher2[i])) % 26 for i in range(len_msg)]
    
    book_clean = preprocess_book(book_text)
    if len(book_clean) < len_msg:
        return None, None
    
    substring_dict = defaultdict(list)
    for i in range(len(book_clean) - len_msg + 1):
        substr = book_clean[i:i+len_msg]
        substring_dict[substr].append(i)
    
    for i in range(len(book_clean) - len_msg + 1):
        p1_candidate = book_clean[i:i+len_msg]
        p2_candidate = []
        for j in range(len_msg):
            p1_num = char_to_num(p1_candidate[j])
            p2_num = (p1_num - diff[j]) % 26
            p2_candidate.append(num_to_char(p2_num))
        p2_candidate_str = ''.join(p2_candidate)
        if p2_candidate_str in substring_dict:
            return p1_candidate, p2_candidate_str
    return None, None

def recover_key(cipher, plaintext):
    key = []
    for c, p in zip(cipher, plaintext):
        k_num = (char_to_num(c) - char_to_num(p)) % 26
        key.append(num_to_char(k_num))
    return ''.join(key)

ciphertext1 = input("Insira o primeiro texto cifrado: ")
ciphertext2 = input("Insira o segundo texto cifrado: ")
print("Escolha o livro:")
print("1) Policarmo Quaresma")
print("2) Recordações do Escrivão Isaías Caminha")

while True:
    escolha = input("Digite o número da opção desejada (1 ou 2): ")
    if escolha in ['1', '2']:
        if escolha == '1':
            texto = 'Texto_desconhecido/policarpo_quaresma.txt'
        else:
            texto = 'Texto_desconhecido/recordacoes_do_escrivao.txt'
        break
    else:
        print("Erro: Escolha inválida. Digite 1 ou 2.")
p1, p2 = find_plaintexts(ciphertext1, ciphertext2, texto)

if p1 and p2:
    key = recover_key(ciphertext1, p1)
    print(f"Chave encontrada: {key}")
    print(f"Texto 1 decifrado: {p1}")
    print(f"Texto 2 decifrado: {p2}")
else:
    print("Nenhum par válido encontrado")