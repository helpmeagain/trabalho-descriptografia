import re
from collections import Counter
import math

# Frequência de letras em português (valores percentuais aproximados)
PORTUGUESE_FREQ = {
    'A': 14.63, 'E': 12.57, 'O': 10.73, 'S': 7.81, 'R': 6.53,
    'I': 6.18, 'N': 5.70, 'D': 4.99, 'M': 4.74, 'C': 4.02,
    'L': 3.82, 'U': 3.60, 'T': 3.45, 'P': 2.74, 'V': 2.40,
    'G': 2.15, 'B': 1.92, 'F': 1.81, 'H': 1.28, 'Q': 0.99,
    'J': 0.40, 'Z': 0.36, 'X': 0.24, 'K': 0.13, 'Y': 0.12, 'W': 0.09
}

# Palavras e bigramas comuns
COMMON_WORDS = set([
    "de", "que", "com", "nao", "para", "uma", "os", "se", "ao", "mais",
    "esta", "por", "as", "em", "da", "do", "e", "a", "o", "um", "nos",
    "pelo", "isto", "tu", "das", "dos", "ele", "bem", "sem", "sao"
])

COMMON_BIGRAMS = set([
    "de", "en", "es", "qu", "nt", "co", "ra", "br", "ar", "pa",
    "er", "te", "do", "da", "os", "as", "em", "ad", "ed", "ao"
])


def preprocess_text(text):
    """Remove caracteres não alfabéticos e converte para maiúsculas."""
    text = re.sub(r'[^A-Z\s]', '', text.upper())
    return text


def count_frequencies(text):
    """Conta a frequência de cada letra no texto, ignorando espaços."""
    clean_text = text.replace(" ", "")
    return Counter(clean_text)


def frequency_order(frequency_dict):
    """Retorna as letras ordenadas por frequência (da mais alta para a mais baixa)."""
    return [item[0] for item in frequency_dict.most_common()]


def apply_mapping(text, mapping):
    """Substitui as letras do texto cifrado conforme o mapeamento."""
    return ''.join([mapping.get(c, c) for c in text])


def calculate_chi_squared(text):
    """Calcula a estatística chi-quadrado para a frequência de letras."""
    observed = Counter(text.replace(" ", ""))
    total = sum(observed.values())
    score = 0

    for char, exp_freq in PORTUGUESE_FREQ.items():
        observed_count = observed.get(char, 0)
        expected_count = total * (exp_freq / 100)
        if expected_count > 0:
            score += ((observed_count - expected_count) ** 2) / expected_count

    return score


def enhanced_score(text):
    """Combina múltiplas métricas de qualidade para avaliar o texto decifrado."""
    text = text.upper()
    words = text.split()
    word_score = sum(1 for word in words if word.lower() in COMMON_WORDS)

    # Score de bigramas
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_score = sum(1 for bg in bigrams if bg in COMMON_BIGRAMS)

    # Chi-squared (quanto menor, melhor)
    chi_score = 1 / (1 + calculate_chi_squared(text))  # Converter para valor positivo

    return word_score + bigram_score + chi_score * 10


def optimize_mapping(cipher_text, initial_mapping):
    """Otimiza o mapeamento usando hill-climbing com múltiplos critérios."""
    best_mapping = initial_mapping.copy()
    best_score = enhanced_score(apply_mapping(cipher_text, best_mapping))

    improvement = True
    while improvement:
        improvement = False
        # Priorizar letras mais frequentes primeiro
        ordered_chars = frequency_order(count_frequencies(cipher_text))

        for char1 in ordered_chars:
            for char2 in ordered_chars:
                if char1 == char2 or char1 not in best_mapping or char2 not in best_mapping:
                    continue

                # Criar novo mapeamento candidato
                new_mapping = best_mapping.copy()
                new_mapping[char1], new_mapping[char2] = new_mapping[char2], new_mapping[char1]

                # Calcular score
                decrypted = apply_mapping(cipher_text, new_mapping)
                current_score = enhanced_score(decrypted)

                # Manter a melhoria
                if current_score > best_score:
                    best_mapping = new_mapping
                    best_score = current_score
                    improvement = True
                    break  # Reiniciar a busca após uma melhoria
            if improvement:
                break

    return best_mapping


def decrypt_monoalphabetic(cipher):
    """Função principal para descriptografar uma cifra monoalfabética."""
    # Pré-processar e analisar a cifra
    processed = preprocess_text(cipher)
    freq = count_frequencies(processed)
    ordered_freq = frequency_order(freq)

    # Criar mapeamento inicial considerando a frequência relativa
    initial_map = {}
    for cipher_char, pt_char in zip(ordered_freq, PORTUGUESE_FREQ.keys()):
        initial_map[cipher_char] = pt_char

    # Otimizar o mapeamento
    final_map = optimize_mapping(processed, initial_map)

    # Aplicar o mapeamento final e formatar o resultado
    decrypted = apply_mapping(processed, final_map)
    return decrypted.lower()


# Exemplo de uso
if __name__ == "__main__":
    cipher_input = input("Insira a cifra: ")
    decrypted_text = decrypt_monoalphabetic(cipher_input)
    print("\nTexto decifrado:", decrypted_text)