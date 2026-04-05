import csv
import unicodedata

# Função para normalizar texto
def normalizar(texto):
    texto = texto.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

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


def criar_tabela_hash(filmes):
    tabela = {}
    
    for filme in filmes:
        titulo = normalizar(filme["titulo"])
        tabela[titulo] = filme
    
    return tabela


def buscar_filme(tabela, titulo):
    return tabela.get(normalizar(titulo))


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
            print(f"Título : {resultado.get('titulo', 'N/A')}")
            print(f"Ano    : {resultado.get('ano', 'N/A')}")
            print(f"Gênero : {resultado.get('genero', 'N/A')}")
            print("-" * 30)
        else:
            print("\n❌ Filme não encontrado.")


if __name__ == "__main__":
    main()