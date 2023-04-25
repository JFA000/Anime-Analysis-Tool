import nltk
import pandas as pd
from nltk.corpus import stopwords

df = pd.DataFrame()
print(df)
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    
    df['synopsis'] = df['synopsis'].fillna('')
    df['sypnopsis'] = df['sypnopsis'].apply(remove_stopwords)# Apply the function to the "synopsis" column
    df = df.rename(columns={'sypnopsis': 'synopsis'}) #Rename the mistype
    df = df.drop(columns=['MAL_ID', 'Score','Genres']) # Remove the ID, Score, and Genres columns.
    return ' '.join(filtered_words)

df.to_csv('anime_with_synopsis.csv', index=False) #Used to save the edited file with all stop words removed.