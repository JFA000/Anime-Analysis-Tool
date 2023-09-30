# Project Description

The Anime Synopsis Similarity Checker is a Python program that allows users to find the most similar anime titles based on their synopses using cosine similarity. It uses a dataset with anime titles and their respective synopses to perform the similarity check.
The Anime Analysis is Python program that creates an analysis about the animes on the csv files, showing averages and creating plots for visualization

## Usage
The program has two three parts: dataset preparation, similarity checking and analysis. To use the program, first, download the scripts and the database and put them in the same folder. Then, execute the python script `prepare_dataset.py` to create the database so the program can work with it. This is a one-time process.
    
    python prepare_dataset.py
   
After the dataset is created, execute the `anime_synopsis_similarity_checker.py` to find the most similar anime titles based on their synopses using cosine similarity.
    
    python anime_synopsis_similarity_checker.py
    
Once the program is running, the user is prompted to enter the title of the anime they want to search for. If the title is found in the dataset, the program returns the synopsis of the anime and a list of the most similar anime titles based on their synopses.

To use the Anime Analysis program, execute the `anime_analysis.py` and follow the program instructions.
    
    python anime_analysis.py

Once the program is running, the program will request user inputs and automatically create plots based on the user input.
## Credits and Citations 
This work uses the [Anime Recommendations Database](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020) dataset, made available by Hernan Valdivieso. Special thanks to Hernan Valdivieso and the dataset creators for making this data available.

This program was created by [Jonatas Fernandes Andrade](https://github.com/JFA000) and [Gabriel Medina da Assunção](https://github.com/gabs4841).
### Contributions
- Jonatas Fernandes Andrade: Worked on the anime synopsis similarity checker and the anime analysis program.
- Gabriel Medina da Assunção: Worked on the anime synopsis similarity checker.