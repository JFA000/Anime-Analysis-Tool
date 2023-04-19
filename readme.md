# Anime Synopsis Similarity

This is a Python project that aims to find the most similar animes in terms of synopsis using cosine similarity. To do this, we use a dataset with anime titles and their respective synopses.

## Libraries used

The following libraries are used in this project:

    'pandas'(version 1.3.2)
    'sklearn'(version 1.0.1)

## Variables defined

The variables defined in this project are:

    caminho_arquivo: a string that defines the path to the CSV file with the anime titles and synopses.
    chunk_size: an integer that defines the number of lines per chunk to be processed when reading the CSV file.
    df: an empty pandas DataFrame that will store the anime titles and synopses.

## Reading and transforming the file into a DataFrame

The file is read in chunks and each chunk is processed or concatenated with other chunks, as necessary. After all the chunks are processed, the resulting DataFrame contains all the anime titles and synopses.
Stopwords removed

The remove_stopwords function is used to remove stopwords from the synopses. This function has already been used in a previous file and is defined in the same file.
Vectorization

The synopses are vectorized using the CountVectorizer class from the sklearn library. The resulting matrix of token counts is used to calculate the cosine similarity between synopses.
How to use

The user is prompted to enter two indices of the anime titles to be compared. The cosine similarity between the synopses of these titles is then calculated and displayed. The user is then prompted to enter an index of an anime title to find the five most similar titles. The titles are displayed in descending order of similarity.

## Installation

To use this project, you must have Python 3.x and the required libraries installed. You can install them using pip:

pip install pandas scikit-learn

## Dataset Citation

This work uses the [Anime Recommendations Database](https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database) dataset, made available by Cooper Union for the Advancement of Science and Art on Kaggle. Special thanks to Cooper Union and the dataset creators for making this data available.

