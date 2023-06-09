#region Imports
import pandas as pd, difflib, math 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
#region Vectorization
df['synopsis'] = df['synopsis'].fillna('') #Fill empty columns with an empty string
vectorizer = CountVectorizer() # Instantiate the CountVectorizer object
synopsis_matrix = vectorizer.fit_transform(df['synopsis']) # Create the token count matrix for the 'synopsis' column
vocab = vectorizer.get_feature_names_out() # Get the vocabulary (list of words) of the vectorizer
#endregion
#region Database search
print("\n╔══════════════════════════════════════════╗")
print("║   Welcome to anime comparison program!   ║")
print("╚══════════════════════════════════════════╝")
#Check if the selected title is in the anime list
while not selected_title:
    selected_title = input("\nEnter the title of the anime you want to search for: ").strip().upper()

if selected_title in df['Name'].str.upper().values:
    title3 = df.loc[df['Name'].str.upper() == selected_title, 'Name'].iloc[0]
else:
    while True:
        title3 = df.loc[df['Name'].str.upper().str.contains(selected_title, case=False), 'Name']
        if len(title3) > 0:
            title3 = title3.iloc[0]
            break
        else:
            words_selected_title = selected_title.split()
            existing_words = []
            for word in words_selected_title:
                found_word = difflib.get_close_matches(word, vocab, n=1, cutoff=0.5)
                if len(found_word) > 0:
                    existing_words.append(found_word[0])
            if len(existing_words) > 0:
                suggested_title = ' '.join(existing_words)
                if suggested_title == selected_title:
                    response = input("\nThe search did not yield any results or suggestions. Do you want to perform a new search? (y/n): ")
                    if response.lower() == 'n' or response.lower() == 'y':
                        if response.lower() == 'n':
                            exit()
                        else:
                            selected_title = input("\nEnter the anime you want to compare: ").strip().upper()
                    else:
                        print("\nInvalid input. Please enter 'y' or 'n'.")
                else:
                    title3 = suggested_title
                    print(f"\nThe search did not yield any results. We suggest searching for: '{suggested_title}'.")
                    selected_title = title3  # Change selected_title to title3
            else:
                response = input("\nThe search did not yield any results or suggestions. Do you want to perform a new search? (y/n): ")
                if response.lower() == 'n' or response.lower() == 'y':
                    if response.lower() == 'n':
                            exit()
                    else:
                            selected_title = input("\nEnter the anime you want to compare: ").strip().upper()
                else:
                    print("\nInvalid input. Please enter 'y' or 'n'.")

if selected_title != title3:
    print(f"Match found for: '{title3}'.")
    selected_title = title3
#endregion 
#region Show vocabulary and similar titles
selected_anime = df[df['Name'].str.upper() == selected_title.upper()]
selected_synopsis_matrix = vectorizer.transform(selected_anime['synopsis']).toarray()
selected_vocab = vectorizer.get_feature_names_out()
print(f"\nThe {selected_title.title()} vocabulary is: ")
print([word for word in selected_vocab if selected_synopsis_matrix[0, vectorizer.vocabulary_[word]] != 0])

def show_selected_title_genres():
    # select the first row from selected_anime
    row = selected_anime.iloc[0]

    # get the value of the column containing the genres
    value = row['Genres'] # change 'genres' to the name of the column containing the genres

    
    genres = value.split(',')

    # print each genre separately
    print("\nThe selected title genres are:")
    for genre in genres:
        print(genre)

show_selected_title_genres()
    # Get the synopsis of the selected title
selected_synopsis = synopsis_matrix[df['Name'] == title3]
    # Calculate the cosine similarity between the selected synopsis and the synopses of all other titles
similarities = cosine_similarity(selected_synopsis, synopsis_matrix).flatten()
    # Get the indices of the titles in descending order of similarity
decreasing_similarity_indices = similarities.argsort()[::-1][1:11]
print(f"\nThe ten most similar titles to '{title3}' are:\n")
counter= 1
for i in decreasing_similarity_indices:
    title = df.iloc[i, 1]
    genre = df.iloc[i, 3]
    similarity = similarities[i]
    similarity_deg = math.degrees(math.acos(similarity))
    print(f"{counter:2}: '{title}'  \nGenres: {genre}\nCosine similarity: {similarity:.2f}/{similarity_deg:.2f}°.\n")
    counter+=1
#endregion
