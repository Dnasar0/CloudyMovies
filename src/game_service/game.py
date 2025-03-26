import os

import grpc
from flask import Flask, render_template
from movie_service.movie_pb2_grpc import *
from movie_service.movie_pb2 import *

app = Flask(__name__)

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
movie_connection = grpc.insecure_channel(f"recommendations:50051")
#movie_connection = grpc.insecure_channel(f"{recommendations_host}:50051")
movie_client = MovieServiceStub(movie_connection)

@app.route("get/<int:given_id>")
def render_homepage(given_id):
    movie_request = MovieRequest(id=given_id)
    movie_response = movie_client.GetMovieById(movie_request)
    return render_template(
        "gameScreen.html",
        movie=movie_response
    )
@app.route("/scifi")
def render_scifipage():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    return render_template(
        "scifipage.html",
        recommendations=recommendations_response.recommendations,
    )
@app.route("/get/<int:given_id>")    
def render_getbook(given_id):
    getBook_request = BookRequest(id=given_id)
    getBook_response = getBook_client.GetBook(getBook_request)
    return render_template(
        "getbook.html",
        book = getBook_response
    )
