import nltk, pandas as pd
from nltk.corpus import stopwords

nltk.download('stopwords')
df = pd.read_csv('anime_with_synopsis.csv')

def remove_stopwords(df):
    stop_words = set(stopwords.words('english'))
    df['sypnopsis'] = df['sypnopsis'].fillna('')
    df['sypnopsis'] = df['sypnopsis'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    df = df.rename(columns={'sypnopsis': 'synopsis'})
    return df

df = remove_stopwords(df)
df.to_csv('anime_with_synopsis_cleaned.csv', index=False)
print("Execution successful. The database 'anime_with_synopsis.csv' is now available for use.")
