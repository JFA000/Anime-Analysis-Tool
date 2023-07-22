import pandas as pd, matplotlib.pyplot as plt, csv
csv_path = './anime_with_synopsis.csv' # Set the path of the CSV file
chunk_size = 4000  # Set the chunk size
df = pd.DataFrame() # Instantiate an empty DataFrame
selected_title = None
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    df = pd.concat([df, chunk], axis=0)


print("\n╔══════════════════════════════════════════╗")
print("║  Welcome to the anime analysis program!  ║")
print("╚══════════════════════════════════════════╝")

print("\nTop 10 animes ranked by score:\n")
filtered_df = df[df['Score'] != 'Unknown'] #Remove Unknown Values
filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
filtered_df = filtered_df.dropna(subset=['Score'])
sorted_df = filtered_df.sort_values('Score', ascending=False) #Sort in descending order
sorted_df['Score'] = sorted_df['Score'].astype(float)
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

def get_genres(csv_path):
    genres = set()
    genre_dict = {}
    with open(csv_path,encoding='utf-8' ,newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            genres.update(row[3].split(','))

    genres = [genre.strip() for genre in genres]#Remove spaces
    genres = set(genres)#Remove duplicates
    genres = sorted(genres)#Sort in order

    for idx, genre in enumerate(genres, 1):
        genre_dict[idx] = genre
    
    return genre_dict

def plot(df,dfxlabel,dfylabel,dftitle):
    
    x = df[dfxlabel].values[:10]
    y = df[dfylabel].values[:10]
    

    plt.figure(figsize=(13, 7)) # 1300*700
    plt.xticks(rotation=90)
    plt.xlabel(dfxlabel)
    plt.ylabel(dfylabel)
    plt.title(dftitle)
    plt.ylim(min(y)-0.1, max(y)+0.01) 
    
    plt.bar(x, y)
    plt.show()

genre_dict = get_genres(csv_path)

def select_genre():    
    for key, value in genre_dict.items():
       print(f"{key}: {value}")
    genre = genre_dict.get(int(input("Enter the genre number you want to select (1-43): ")))
    print(f"You selected {genre}.\nShowing top 10 animes with the {genre} genre: ")
    return genre

top10chosen = filter_by_genre(select_genre())
print(top10chosen.to_string(index=False))

plot(sorted_df,'Name','Score','Top 10 Animes by Score')

result = {}
for genre in genre_dict.values():
    if genre != "Genres":
        mask = sorted_df['Genres'].str.contains(genre)
        genre_df = sorted_df[mask]
        result[genre] = genre_df['Score'].mean()

genres_average_df = pd.DataFrame(result.items(), columns=['Genre', 'Average Score'])

plt.figure(figsize=(10, 6))
plt.bar(genres_average_df['Genre'], genres_average_df['Average Score'])
plt.xlabel('Genre')
plt.ylabel('Average Score')
plt.title('Genre average score')
plt.ylim(min(genres_average_df['Average Score'])-0.1, max(genres_average_df['Average Score'])+0.01) 
plt.show()
