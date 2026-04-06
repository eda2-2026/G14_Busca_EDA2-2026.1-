import csv
import unicodedata

# -----------------------------
# Normalização de texto
# -----------------------------
def normalizar(texto):
    texto = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# -----------------------------
# Carregar filmes
# -----------------------------
def carregar_filmes(caminho):
    filmes = []
    
    try:
        with open(caminho, encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=',')
            for linha in leitor:
                filmes.append(linha)
    except FileNotFoundError:
        print("Erro: arquivo filmes.csv não encontrado.")
        return []
    
    return filmes

# -----------------------------
# Função de hash
# -----------------------------
def funcao_hash(chave, tamanho):
    chave = normalizar(chave)
    hash_val = 0
    
    for caractere in chave:
        hash_val += ord(caractere)
    
    return hash_val % tamanho

# -----------------------------
# Criar tabela hash manual
# -----------------------------
def criar_tabela_hash(filmes, tamanho=100):
    tabela = [[] for _ in range(tamanho)]  # lista de listas
    
    for filme in filmes:
        titulo = filme["titulo"]
        indice = funcao_hash(titulo, tamanho)
        
        # Encadeamento (chaining)
        tabela[indice].append(filme)
    
    return tabela

# -----------------------------
# Buscar filme
# -----------------------------
def buscar_filme(tabela, titulo):
    indice = funcao_hash(titulo, len(tabela))
    lista = tabela[indice]
    
    titulo_normalizado = normalizar(titulo)
    
    for filme in lista:
        if normalizar(filme["titulo"]) == titulo_normalizado:
            return filme
    
    return None

# -----------------------------
# Main
# -----------------------------
def main():
    filmes = carregar_filmes("filmes.csv")

    if not filmes:
        return

    tabela = criar_tabela_hash(filmes)

    print("=== 🎬 BUSCADOR DE FILMES ===")

    while True:
        titulo = input("\nDigite o nome do filme (ou 'sair'): ").strip()

        if normalizar(titulo) == "sair":
            print("Encerrando...")
            break

        resultado = buscar_filme(tabela, titulo)

        if resultado:
            print("\n🎬 Filme encontrado!")
            print("-" * 30)
            print(f"Título      : {resultado.get('titulo', 'N/A')}")
            print(f"Ano         : {resultado.get('ano', 'N/A')}")
            print(f"Gênero      : {resultado.get('genero', 'N/A')}")
            print(f"Diretor(es) : {resultado.get('diretor', 'N/A')}")
            print(f"Críticos    : {resultado.get('pontoCrit', 'N/A')}")
            print(f"Audiência   : {resultado.get('pontoAud', 'N/A')}")
            print("-" * 30)
        else:
            print("\n❌ Filme não encontrado.")

if __name__ == "__main__":
    main()