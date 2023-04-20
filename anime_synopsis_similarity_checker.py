#region importações
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#endregion
#region Definição de variaveis
caminho_arquivo = './anime_with_synopsis.csv' # Define o caminho do arquivo CSV
chunk_size = 10000  # 10 mil linhas por chunk # Define o tamanho do chunk
df = pd.DataFrame() # Define um DataFrame vazio
#endregion
#region Leitura do arquivo e transformação em dataframe
# Itera sobre cada chunk do arquivo CSV
for chunk in pd.read_csv(caminho_arquivo, chunksize=chunk_size):
    # Processa ou concatena o chunk com outros chunks
    # Exemplo: 
    # do something with chunk
    # df = pd.concat([df, chunk], axis=0)
    
    # Exemplo: Concatena o chunk com o DataFrame vazio
    df = pd.concat([df, chunk], axis=0)


#endregion

#region Vetorização
#df['synopsis'] = df['synopsis'].fillna('')#Preencher colunas vazias com uma string vazia. (Já realizado e salvo no dataset)


# Define o objeto CountVectorizer
vectorizer = CountVectorizer()

# Cria a matriz de contagem de tokens para a coluna 'synopsis'
synopsis_matrix = vectorizer.fit_transform(df['synopsis'])

# Obtém o vocabulário (lista de palavras) do vetorizador
vocab = vectorizer.get_feature_names_out()

# Define o objeto CountVectorizer
vectorizer = CountVectorizer()

# Cria a matriz de contagem de tokens para a coluna 'synopsis'
synopsis_matrix = vectorizer.fit_transform(df['synopsis'])

# Obtém o vocabulário (lista de palavras) do vetorizador
vocab = vectorizer.get_feature_names_out()


#print(vocab) # Exibe as palavras vetorizadas

choice = input("What would you like to do?\n1. Compare two anime titles\n2. Find the most similar anime titles based on your title\nEnter your choice (1 or 2): ")

if choice == '1':
    # Obtém as matrizes de vetorização das sinopses na linha 100 e na linha 200
    valor1 = int(input("Digite um índice de titulo do dataset (0 - 16213) para ser comparado: "))
    valor2 = int(input("Digite um índice de titulo do dataset (0 - 16213) para comparar com o primeiro: "))

    titulo_1 = df.iloc[valor1, 0]  # obtém o nome do título correspondente à linha selecionada pelo usuário
    titulo_2 = df.iloc[valor2, 0]  # obtém o nome do título correspondente à linha selecionada pelo usuário


    synopsis_1 = synopsis_matrix[valor1]
    synopsis_2 = synopsis_matrix[valor2]


    # Calcula a similaridade do cosseno entre as duas matrizes
    similarity = cosine_similarity(synopsis_1, synopsis_2)

    print(f"\nOs titulos escolhidos foram:\n 1 - '{titulo_1}'\n 2 - '{titulo_2}'\nA similaridade cosseno desses titulos é de: {similarity[0][0]:.2f}")

elif choice == '2':
    # Obtém o índice do título selecionado
    titulo_selecionado = int(input("\nDigite o índice do título (0 - 16213) que deseja comparar: "))
    titulo_3 = df.iloc[titulo_selecionado, 0]
    # Obtém a sinopse do título selecionado
    synopsis_selecionada = synopsis_matrix[titulo_selecionado]

    # Calcula a similaridade do cosseno entre a sinopse selecionada e as sinopses de todos os outros títulos
    similaridades = cosine_similarity(synopsis_selecionada, synopsis_matrix).flatten()

    # Obtém os índices dos títulos em ordem decrescente de similaridade

    indices_similaridade_decrescente = similaridades.argsort()[::-1][1:6]
    # Obtém o índice do título com a maior similaridade (excluindo o título selecionado)
    indice_maior_similaridade = indices_similaridade_decrescente[1]

    # Obtém o título com a maior similaridade e seu valor de similaridade
    titulo_maior_similaridade = df.iloc[indice_maior_similaridade, 0]
    similaridade_maior = similaridades[indice_maior_similaridade]

    #print(f"O título selecionado foi: {titulo_3}.\n O titulo com a maior similaridade cosseno em relação a ele é '{titulo_maior_similaridade}', com uma similaridade de :{similaridade_maior:.2f}")
    print(f"Os cinco títulos mais semelhantes a '{titulo_3}' são:\n")
    for indice in indices_similaridade_decrescente:
        titulo = df.iloc[indice, 0]
        similaridade = similaridades[indice]
        print(f"'{titulo}' (similaridade cosseno: {similaridade:.2f})")

else:
    # If user input is invalid, display error message
    print("Invalid choice. Please try again.")

#endregion
#region Exibição visual do dataframe
'''
print(df.columns)# Mostra apenas as colunas do DataFrame

print(df)
print(df['sypnopsis'])# Mostra apenas a coluna "synopsis
'''
#endregion