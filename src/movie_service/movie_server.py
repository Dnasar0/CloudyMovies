import os
import threading
import math
from flask import Flask
import grpc
from concurrent import futures
import random
import movie_pb2
import movie_pb2_grpc
from types import SimpleNamespace
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return "OK", 200

def run_health_server():
    app.run(host='0.0.0.0', port=8080)

username = os.environ["DB_USER"]
password = os.environ["DB_PASS"]

client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.o6uzq0y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client["cloudy_movies"]
movies_collection = db["movies"]
genres_collection = db["genres"]
themes_collection = db["themes"]
crew_collection = db["crew"]
actors_collection = db["actors"]
poster_collection = db["posters"]

class MovieService(movie_pb2_grpc.MovieServiceServicer):
    #So retorna o nome e id dos filmes
    def GetAllMovies(self, request, context):
        return movies_collection.find({}, {"_id": 1, "name": 1})

    def GetRandomMovie(self, request, context):
        
        while True:
            movie = movies_collection.aggregate([{"$sample": {"size": 1}}]).next()
            id = movie["id"]
            poster = poster_collection.find_one({"id": id})
            actors = actors_collection.find({"id": id})
            genres = genres_collection.find({"id": id})
            crew = crew_collection.find({"id": id})
            theme = themes_collection.find({"id": id})

            if (movie and "rating" in movie and movie["rating"] is not None and not math.isnan(movie["rating"]) and poster and "link" in poster):
                return movie_pb2.Movie(
                    movieId=int(movie["id"]),
                    title=str(movie["name"]),
                    year=int(movie["date"]),
                    tagline=str(movie["tagline"]),
                    description=str(movie["description"]),
                    duration=int(movie["minute"]),
                    rating=float(movie["rating"]),
                    poster=str(poster["link"])	
                )

    def CreateMovie(self, request, context):
        id = movies_collection.count_documents({}) + 1000000 + 1
        movie_data = {
            "id": id,
            "name": request.title,
            "date": request.year,
            "tagline": request.tagline,
            "description": request.description,
            "minute": request.minutes,
            "rating": request.rating
        }
        genre_data = {
            "id": id,
            "genre": request.genre
        }
        theme_data = {
            "id": id,
            "theme": request.theme
        }
        crew_data = {
            "id": id,
            "role": request.role,
            "name": request.crewName,
        }
        actor_data = {
            "id": id,
            "role": request.role,
            "name": request.actorName,
        }
        movies_collection.insert_one(movie_data)
        genres_collection.insert_one(genre_data)
        themes_collection.insert_one(theme_data)
        crew_collection.insert_one(crew_data)
        actors_collection.insert_one(actor_data)
        return movie_pb2.Empty()

    def GetMovieById(self, request, context):
        print("Pedido de filme recebido: ", request.movieId)
        while True:
            movie = movies_collection.find_one({"id": request.movieId})
            poster = poster_collection.find_one({"id": request.movieId})
            actors = actors_collection.find({"id": request.movieId})
            genres = genres_collection.find({"id": request.movieId})
            crew = crew_collection.find({"id": request.movieId})
            theme = themes_collection.find({"id": request.movieId})

            if (movie and "rating" in movie and movie["rating"] is not None and not math.isnan(movie["rating"]) and poster and "link" in poster):
                break

            request.movieId = 1000000 + random.randint(1, 82447)
        return movie_pb2.Movie(
            movieId=int(movie["id"]),
            title=str(movie["name"]),
            year=int(movie["date"]),
            tagline=str(movie["tagline"]),
            description=str(movie["description"]),
            duration=int(movie["minute"]),
            rating=float(movie["rating"]),
            poster=str(poster["link"])	
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServiceServicer_to_server(MovieService(), server)
    server.add_insecure_port('[::]:50052')
    print("Movie server is running on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    serve()
