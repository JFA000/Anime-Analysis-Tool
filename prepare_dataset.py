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
    df['sypnopsis'] = df['sypnopsis'].apply(remove_stopwords)# Aplica a função à coluna "synopsis"
    df = df.rename(columns={'sypnopsis': 'synopsis'}) #Sim, o arquivo original veio escrito 'sypnopsis' 
    df = df.drop(columns=['MAL_ID', 'Score','Genres']) # Remove a coluna de ID, Score e Generos.
    return ' '.join(filtered_words)

df.to_csv('anime_with_synopsis.csv', index=False) #Utilizado para salvar o arquivo editado com  todas as stop words removidas