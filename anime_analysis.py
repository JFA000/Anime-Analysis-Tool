import pandas as pd, matplotlib.pyplot as plt, seaborn as sns ,csv
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
print("")

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

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FixedLocator

def plot(df,dfxlabel,dfylabel,dftitle):
    
    x = df[dfxlabel].values
    y = df[dfylabel].values
    
    plt.figure(figsize=(500, 70)) # 1300*700
    sns.set_style('darkgrid')
    plt.xlabel(dfxlabel)
    plt.ylabel(dfylabel)
    plt.title(dftitle)
    plt.ylim(min(y)-0.1, max(y)+0.01)
    plt.xticks(fontsize=8)

    # Create the barplot and get the plot object
    barplot = sns.barplot(x=x, y=y,color='tan')

    # Get the x-axis labels from the plot object
    x_labels = barplot.get_xticklabels()

    # Set the x-ticks using FixedLocator
    barplot.xaxis.set_major_locator(FixedLocator(range(len(x_labels))))

    # Show the values for each bar
    for index, value in enumerate(y):
        plt.text(index, value - 0.05, str(value), color='black', ha="center")

    # Set the x-axis labels on the plot object
    lenght = 22
    barplot.set_xticklabels([label.get_text()[:lenght]+'...' if len(label.get_text())>lenght else label.get_text() for label in x_labels])

genre_dict = get_genres(csv_path)
def select_genre():    
    for key, value in genre_dict.items():
       print(f"{key}: {value}")
    genre = genre_dict.get(int(input("Enter the genre number you want to select (1-43): ")))   
    return genre

selected_genre = select_genre() 
top10chosen = filter_by_genre(selected_genre)

print(f"\nYou selected {selected_genre}.\nShowing top 10 animes with the {selected_genre} genre: \n")
print(top10chosen[['Name', 'Score']].to_string(index=False))
plot(top10chosen,'Name','Score',f'Top 10 {selected_genre} Animes by Score')
plt.show()
result = {}
for genre in genre_dict.values():
    if genre != "Genres":
        mask = sorted_df['Genres'].str.contains(genre)
        genre_df = sorted_df[mask]
        result[genre] = genre_df['Score'].mean()

genres_average_df = pd.DataFrame(result.items(), columns=['Genre', 'Average Score'])
genres_average_df = genres_average_df.sort_values(by='Average Score', ascending=False)
top_genres_average_df = genres_average_df.head(10)
#plot(genres_average_df,'Genre','Average Score','Top Genres by Score')

'''
plt.figure(figsize=(13, 6))
sns.set_style('darkgrid')
sns.barplot(x=top_genres_average_df['Genre'], y=top_genres_average_df['Average Score'],color='tan')
plt.xlabel("Genres")
plt.ylabel("")
plt.ylim(6.5, 7.2)
plt.show()
'''