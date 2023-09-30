#region Program Startup
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns ,csv
from matplotlib.ticker import FixedLocator
csv_path = './anime_with_synopsis.csv' # Set the path of the CSV file
chunk_size = 4000  # Set the chunk size
df = pd.DataFrame() # Instantiate an empty DataFrame
selected_title = None
plt.rcParams['font.family'] = 'Arial'
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    df = pd.concat([df, chunk], axis=0)

#endregion
#region Functions
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

def select_genre():    
    for key, value in genre_dict.items():
       print(f"{key}: {value}")
    
    while True:
        selection = input("Enter the genre number you want to select (1-43): ")

        if not selection.isdigit() or int(selection) < 1 or int(selection) > 43:
            print("Incorrect genre. Please select a number between 1 and 43.")
        else:
            break

    genre = genre_dict.get(int(selection))
    return genre


def plot(df,dfxlabel,dfylabel,dftitle):
    
    x = df[dfxlabel].values
    y = df[dfylabel].values
    
    plt.figure(figsize=(50, 7))
    sns.set_style('darkgrid')
    plt.xlabel("")
    plt.ylabel("")
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
        plt.text(index, value - 0.05, str(round(value, 2)), color='black', ha="center")

    # Set the x-axis labels on the plot object
    lenght = 22
    barplot.set_xticklabels([label.get_text()[:lenght]+'...' if len(label.get_text())>lenght else label.get_text() for label in x_labels])
#endregion
#region Welcome Message
print("\n╔══════════════════════════════════════════╗")
print("║  Welcome to the anime analysis program!  ║")
print("╚══════════════════════════════════════════╝")
#endregion
#region Top 10 animes by score
print("\nTop 10 animes by average score:\n")
filtered_df = df[df['Score'] != 'Unknown'] #Remove Unknown Values
filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
filtered_df = filtered_df.dropna(subset=['Score'])
sorted_df = filtered_df.sort_values('Score', ascending=False) #Sort in descending order
sorted_df['Score'] = sorted_df['Score'].astype(float)
top_10_animes = sorted_df.head(10)
print(top_10_animes[['Name', 'Score']].to_string(index=False))
#endregion
#region Top 10 genres
print("\nThe 10 genres that appear the most among them are:")
genre_lists = top_10_animes['Genres'].str.split(',')
genres = [genre.strip() for genre_list in genre_lists for genre in genre_list]
genre_counts = pd.Series(genres).value_counts()
genre_count_str = genre_counts.to_string()
lines = genre_count_str.split('\n')
for line in lines[:10]:
    print(line + ' times')
print("")
#endregion
#region Plot all genre available scores
genre_dict = get_genres(csv_path)
result = {}
for genre in genre_dict.values():
    if genre != "Genres":
        mask = sorted_df['Genres'].str.contains(genre)
        genre_df = sorted_df[mask]
        result[genre] = genre_df['Score'].mean()

genres_average_df = pd.DataFrame(result.items(), columns=['Genre', 'Average Score'])
genres_average_df = genres_average_df.sort_values(by='Average Score', ascending=False)
top_genres_average_df = genres_average_df.head(10)
plot(genres_average_df,'Genre','Average Score','Top Genres by Score')
plt.xticks(rotation=45)
plt.savefig('Plots/Genre Score Distribution.png', dpi=300, bbox_inches='tight')
print("\nA file with the name `Genre Score Distribution.png` was created and contains the distribution of genres by score!\n")
#endregion
#region Plot by Genre Selection


selected_genre = ""
selected_genre = select_genre() 
top10chosen = filter_by_genre(selected_genre)

print(f"\nYou selected {selected_genre}.\nShowing top 10 animes with the {selected_genre} genre: \n")
print(top10chosen[['Name', 'Score']].to_string(index=False))
plot(top10chosen,'Name','Score',f'Top 10 {selected_genre} Animes by Score')
plt.savefig(f'Plots/Top {selected_genre} by Scores.png', dpi=300, bbox_inches='tight')
print(f"\nA file with the name `Top {selected_genre} by Scores.png` was created and contains the top {selected_genre} by score!\n")
#endregion
