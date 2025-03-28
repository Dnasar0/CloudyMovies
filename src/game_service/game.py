import os

import grpc
from flask import Flask, render_template
from movie_pb2_grpc  import MovieServiceStub 
from movie_pb2 import MovieRequest
import random


app = Flask(__name__)
app.debug = True

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
""""
with open("client.key", "rb") as fp:
    client_key = fp.read()
with open("client.pem", "rb") as fp:
    client_cert = fp.read()
with open("ca.pem", "rb") as fp:
    ca_cert = fp.read()
creds = grpc.ssl_channel_credentials(ca_cert, client_key, client_cert)
"""
movie_connection = grpc.insecure_channel("movie_service:50052")
#movie_connection = grpc.insecure_channel(f"{recommendations_host}:50051")
movie_client = MovieServiceStub(movie_connection)

@app.route("/")
def render_index():
    return render_template("firstScreen.html")

@app.route("/get/<int:given_id>")
def render_homepage(given_id):
    movie_request = MovieRequest(movieId=given_id)
    movie_response = movie_client.GetMovieById(movie_request)
    print(movie_request)
    return render_template(
        "game1Screen.html",
        movie=movie_response
    )

@app.route("/getRandom")
def render_random():
    randomMovieId = 1000000+random.randint(1,82447)
    movie_request = MovieRequest(movieId=randomMovieId)
    movie_response = movie_client.GetMovieById(movie_request)
    print(movie_request)
    return render_template(
        "game1Screen.html",
        movie=movie_response
    )

@app.route("/getTwoRandom")
def render_tworandom():
    randomMovieId1 = 1000000+random.randint(1,82447)
    randomMovieId2 = 1000000+random.randint(1,82447)
    movie_request1 = MovieRequest(movieId=randomMovieId1)
    movie_request2 = MovieRequest(movieId=randomMovieId2)
    movie_response1 = movie_client.GetMovieById(movie_request1)
    movie_response2 = movie_client.GetMovieById(movie_request2)
    return render_template(
        "gameScreen.html",
        movie1=movie_response1,
        movie2=movie_response2
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
