import os

def excluir_arquivos(base_path, grupo):
    caminhos = [
        os.path.join(base_path, 'Aberto', 'Mono', f'{grupo}_texto_decifrado.txt'),
        os.path.join(base_path, 'Aberto', 'Mono', f'{grupo}_key.txt'),
        os.path.join(base_path, 'Aberto', 'Hill', f'{grupo}_texto_decifrado.txt'),
        os.path.join(base_path, 'Aberto', 'Hill', f'{grupo}_key.txt'),
        os.path.join(base_path, 'Aberto', 'Vigenere', f'{grupo}_texto_decifrado1.txt'),
        os.path.join(base_path, 'Aberto', 'Vigenere', f'{grupo}_texto_decifrado2.txt'),
        os.path.join(base_path, 'Aberto', 'Vigenere', f'{grupo}_key.txt'),
    ]

    for caminho in caminhos:
        if os.path.exists(caminho):
            os.remove(caminho)
            print(f'Arquivo excluído: {caminho}')
        else:
            print(f'Arquivo não encontrado: {caminho}')

def main():
    base_path = 'Texto_conhecido'
    grupo = 'Grupo05'

    excluir_arquivos(base_path, grupo)

if __name__ == "__main__":
    main()