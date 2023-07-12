#region Imports
import pandas as pd, matplotlib.pyplot as plt
#endregion
#region Variables definition
csv_path = './anime_with_synopsis.csv' # Set the path of the CSV file
chunk_size = 4000  # Set the chunk size
df = pd.DataFrame() # Instantiate an empty DataFrame
selected_title = None
#endregion
#region Reading the file and transforming it into a dataframe
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    df = pd.concat([df, chunk], axis=0)
#endregion

print("\n╔══════════════════════════════════════════╗")
print("║  Welcome to the anime analysis program!  ║")
print("╚══════════════════════════════════════════╝")

print("\nTop 10 animes ranked by score:\n")
filtered_df = df[df['Score'] != 'Unknown'] #Remove Unknown Values
filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
filtered_df = filtered_df.dropna(subset=['Score'])
sorted_df = filtered_df.sort_values('Score', ascending=False) #Sort in descending order
top_10_animes = sorted_df.head(10)
print(top_10_animes[['Name', 'Score']].to_string(index=False))


print("\nThe 10 genres that appear the most among them are:")
genre_lists = top_10_animes['Genres'].str.split(',')
genres = [genre.strip() for genre_list in genre_lists for genre in genre_list]
genre_counts = pd.Series(genres).value_counts()
genre_count_str = genre_counts.to_string()
lines = genre_count_str.split('\n')

for line in lines[:10]:
    print(line + ' times')

def filter_by_genre(genre):
    filtered_df = df[df['Genres'].str.contains(genre)]
    filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
    filtered_df = filtered_df.dropna(subset=['Score'])
    sorted_df = filtered_df.sort_values('Score', ascending=False)
    top_10_animes = sorted_df.head(10)
    return top_10_animes[['Name', 'Score']]

print("\nGenre list")
genre_dict = {
    1: 'Action',
    2: 'Adventure',
    3: 'Cars',
    4: 'Comedy',
    5: 'Dementia',
    6: 'Demons',
    7: 'Drama',
    8: 'Ecchi',
    9: 'Fantasy',
    10: 'Game',
    11: 'Genres',
    12: 'Harem',
    13: 'Historical',
    14: 'Horror',
    15: 'Josei',
    16: 'Kids',
    17: 'Magic',
    18: 'Martial Arts',
    19: 'Mecha',
    20: 'Military',
    21: 'Music',
    22: 'Mystery',
    23: 'Parody',
    24: 'Police',
    25: 'Psychological',
    26: 'Romance',
    27: 'Samurai',
    28: 'School',
    29: 'Sci-Fi',
    30: 'Seinen',
    31: 'Shoujo',
    32: 'Shoujo Ai',
    33: 'Shounen',
    34: 'Shounen Ai',
    35: 'Slice of Life',
    36: 'Space', 
    37:'Sports', 
    38:'Super Power', 
    39:'Supernatural', 
    40:'Thriller', 
    41:'Unknown', 
    42:'Vampire', 
    43:'Yaoi'
}

for key, value in genre_dict.items():
   print(f"{key}: {value}")
genre = genre_dict.get(int(input("Enter the genre number you want to select (1-43): ")))
print(f"You selected {genre}.\nShowing top 10 animes with the {genre} genre: ")

top10chosen = filter_by_genre(genre)
print(top10chosen.to_string(index=False))
#Using Matplotlib

sorted_df['Score'] = sorted_df['Score'].astype(float)
x = sorted_df['Name'].values[:10]
y = sorted_df['Score'].values[:10]

plt.figure(figsize=(10, 6)) # ajustando o tamanho da figura

plt.bar(x, y)

# adicionando os nomes dos animes no eixo x
plt.xticks(x, x)

# rotacionando os rótulos do eixo x para melhor legibilidade
plt.xticks(rotation=90)

# nomeando o eixo x
plt.xlabel('Anime')

# nomeando o eixo y
plt.ylabel('Score')

# dando um título ao gráfico
plt.title('Top 10 Anime por Score')

plt.ylim(min(y) - 0.5, max(y) + 0.5) 

# mostrando o gráfico
plt.show()