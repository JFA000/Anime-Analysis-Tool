import csv

genres = set()

with open('anime_with_synopsis.csv',encoding='utf-8' ,newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        genres.update(row[3].split(','))
genres = [genre.strip() for genre in genres]#Remove spaces
genres = set(genres)#Remove duplicates
genres = sorted(genres)#Sort in order


print("Printing all genres present in 'anime_with_synopsis.csv': ")
for genre in genres:
    print(genre)
