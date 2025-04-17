from pymongo import MongoClient
import pandas as pd

if __name__ == '__main__':

    # Connect to MongoDB (make sure MongoDB is running)
    client = MongoClient("mongodb://localhost:40291/")

    # Create a database and collections for each dataset
    db = client["cloudy_movies"]
    movies_collection = db["movies"]
    crew_collection = db["crew"]
    actors_collection = db["actors"]
    themes_collection = db["themes"]
    genres_collection = db["genres"]
    posters_collection = db["posters"]
    accounts_collection = db["accounts"]

    # Load CSV files using pandas
    movies_df = pd.read_csv("data/movies.csv")
    crew_df = pd.read_csv("data/crew.csv")
    actors_df = pd.read_csv("data/actors.csv")
    themes_df = pd.read_csv("data/themes.csv")
    genres_df = pd.read_csv("data/genres.csv")
    posters_df = pd.read_csv("data/posters.csv")

    # Insert data into MongoDB
    movies_collection.insert_many(movies_df.to_dict(orient='records'))
    print("Movies data loaded into MongoDB!")
    crew_collection.insert_many(crew_df.to_dict(orient='records'))
    print("Crew data loaded into MongoDB!")
    actors_collection.insert_many(actors_df.to_dict(orient='records'))
    print("Actors data loaded into MongoDB!")
    themes_collection.insert_many(themes_df.to_dict(orient='records'))
    print("Themes data loaded into MongoDB!")
    genres_collection.insert_many(genres_df.to_dict(orient='records'))
    print("Genres data loaded into MongoDB!")
    posters_collection.insert_many(posters_df.to_dict(orient='records'))

    print("Data loaded into MongoDB!")