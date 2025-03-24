from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB (make sure MongoDB is running)
client = MongoClient("mongodb://localhost:27017/")

# Create a database and collections for each dataset
db = client["my_database"]
movies_collection = db["movies"]
crew_collection = db["crew"]
actors_collection = db["actors"]
themes_collection = db["themes"]
genres_collection = db["genres"]


# Load CSV files using pandas
movies_df = pd.read_csv("data/movies.csv")
crew_df = pd.read_csv("data/crew.csv")
actors_df = pd.read_csv("data/actors.csv")
themes_df = pd.read_csv("data/themes.csv")
genres_df = pd.read_csv("data/genres.csv")

# Insert data into MongoDB
movies_collection.insert_many(movies_df.to_dict(orient='records'))
crew_collection.insert_many(crew_df.to_dict(orient='records'))
actors_collection.insert_many(actors_df.to_dict(orient='records'))
themes_collection.insert_many(themes_df.to_dict(orient='records'))
genres_collection.insert_many(genres_df.to_dict(orient='records'))

print("Data loaded into MongoDB!")
