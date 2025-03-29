import os

import grpc
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from movie_pb2_grpc  import MovieServiceStub 
from movie_pb2 import MovieRequest, Empty
from account_pb2 import Account
from account_pb2_grpc import AccountServiceStub
import random


app = Flask(__name__)
CORS(app)
app.debug = True

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
movie_connection = grpc.insecure_channel("movie_service:50052")
account_connection = grpc.insecure_channel("account_service:50051")
account_client = AccountServiceStub(account_connection)
movie_client = MovieServiceStub(movie_connection)

@app.route("/")
def render_index():
    return render_template("firstScreen.html")

@app.route("/submit", methods=["POST"])
def create_account():
    username = request.form["username"]
    print(username)
    password = request.form["password"]
    print(password)
    account_type = request.form["accountType"]
    print(account_type)

    try:
        print("Creating account...")
        # Call gRPC CreateAccount function
        account_client.CreateAccount(Account(
            username=username,
            password=password,
            highScore=0,  # Default high score
            account_type=account_type
        ))
        print("Account created successfully!")
        return render_tworandom()
    except grpc.RpcError as e:
        return f"Error: {e.details()}"


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
    
    movie_response = movie_client.GetRandomMovie(request = Empty())
    #Ver isto ideia era mandar json com infos, web recebe e subsitui valores antigos de movie1 com estes ver como fazer isso
    movie_data = {
        'id': movie_response.movieId,
        'title': movie_response.title,
        'poster': movie_response.poster,
        'rating': movie_response.rating,
        'year': movie_response.year,
    }
    print(movie_data)
    return jsonify(movie_data)

@app.route("/getTwoRandom")
def render_tworandom():
    movie_response1 = movie_client.GetRandomMovie(request = Empty())
    movie_response2 = movie_client.GetRandomMovie(request = Empty())
    return render_template(
        "gameScreen.html",
        movie1=movie_response1,
        movie2=movie_response2
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
