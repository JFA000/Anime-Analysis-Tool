#region Imports
import pandas as pd, difflib, math 
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

print("\nThe 10 lowest ranked animes are:\n")
filtered_df = df[df['Score'] != 'Unknown'] #Remove Unknown Values
sorted_df = filtered_df.sort_values('Score', ascending=True) #Sort in descending order
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

