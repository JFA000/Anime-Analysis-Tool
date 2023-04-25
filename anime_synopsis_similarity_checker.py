#region Imports
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
#endregion
#region Variables definition
file_path = './anime_with_synopsis.csv' # Set the path of the CSV file
chunk_size = 4000  # Set the chunk size
df = pd.DataFrame() # Instantiate an empty DataFrame
selected_title = 0
#endregion
#region Reading the file and transforming it into a dataframe

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    df = pd.concat([df, chunk], axis=0)


#endregion
#region Vectorization

df['synopsis'] = df['synopsis'].fillna('') #Fill empty columns with an empty string
vectorizer = CountVectorizer() # Instantiate the CountVectorizer object
synopsis_matrix = vectorizer.fit_transform(df['synopsis']) # Create the token count matrix for the 'synopsis' column
vocab = vectorizer.get_feature_names_out() # Get the vocabulary (list of words) of the vectorizer

#print(vocab) # Display the vectorized words
#endregion
#region Database search
print("\n╔══════════════════════════════════════════╗")
print("║   Welcome to anime comparison program!   ║")
print("╚══════════════════════════════════════════╝")


# Check if the selected title is in the anime list
selected_title = ""
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
                    response = input("\nThe search did not yield any results or suggestions. Do you want to perform a new search? (y/n) ")
                    if response.lower() == 'n':
                        exit()
                    else:
                        selected_title = input("\nEnter the anime you want to compare").strip().upper()
                else:
                    selected_title = suggested_title
                    print(f"\nThe search did not yield any results. We suggest searching for: '{selected_title}'.")
            else:
                response = input("\nThe search did not yield any results or suggestions. Do you want to perform a new search? (y/n) ")
                if response.lower() == 'n':
                    exit()
                else:
                    selected_title = input("\nEnter the anime you want to compare").strip().upper()


    # Get the synopsis of the selected title
selected_synopsis = synopsis_matrix[df['Name'] == title3]

    # Calculate the cosine similarity between the selected synopsis and the synopses of all other titles
similarities = cosine_similarity(selected_synopsis, synopsis_matrix).flatten()

    # Get the indices of the titles in descending order of similarity
decreasing_similarity_indices = similarities.argsort()[::-1][1:6]

print(f"\nThe five most similar titles to '{title3}' are:\n")
for indice in decreasing_similarity_indices:
    title = df.iloc[indice, 0]
    similarity = similarities[indice]
    print(f"'{title}' (cosine similarity: {similarity:.2f})")


#endregion
#region Visual display of the dataframe
'''
print(df.columns)# column only
print(df)#Everything
print(df['sypnopsis'])# synopsis only
'''
#endregion