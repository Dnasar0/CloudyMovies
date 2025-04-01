from datetime import datetime
import os

import grpc
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from movie_pb2_grpc  import MovieServiceStub 
from movie_pb2 import MovieRequest, Empty
from account_pb2 import Account, AccountRequest
from account_pb2_grpc import AccountServiceStub
from tournament_pb2 import Tournament
from tournament_pb2_grpc import TournamentServiceStub


app = Flask(__name__)
CORS(app)
app.debug = True

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
movie_connection = grpc.insecure_channel("movie_service:50052")
account_connection = grpc.insecure_channel("account_service:50051")
tournament_connection = grpc.insecure_channel("tournament_service:50053")
account_client = AccountServiceStub(account_connection)
movie_client = MovieServiceStub(movie_connection)
tournament_client = TournamentServiceStub(tournament_connection)

@app.route("/")
def render_index():
    return render_template("firstScreen.html")

@app.route("/tournament")
def render_tournament():
    return render_template("tournament.html")

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
    
@app.route("/updateHighScore", methods=["POST"])
def update_high_score():
    username = request.json["username"]
    new_score = request.json["highScore"]

    try:
        print(f"Updating high score for {username}...")

        # Call gRPC UpdateHighScore function
        account_client.UpdateHighScore(Account(
            username=username,
            highScore=new_score
        ))

        print("High score update request sent!")
        return jsonify({"message": "High score update request sent!"}), 200

    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), 500

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
    
@app.route("/getTournaments", methods=["GET"])
def get_tournaments():
    tournaments_response = tournament_client.ListTournaments(Empty())  # Use the correct response object
    return jsonify([{
        "id": t.id,
        "name": t.name,
        "creator": t.creator,
        "prize": t.prize,
        "players": [{"username": p.username} for p in t.players]
    } for t in tournaments_response.tournaments])  # Access tournaments from TournamentList


@app.route("/createTournament", methods=["POST"])
def create_tournament():
    data = request.json
    print(data)
    tournament_client.CreateTournament(Tournament(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Auto-generate date
        name=data["name"],
        creator=data["creator"],
        prize=int(data["prize"]),  # Ensure prize is an integer
        players=[Account(username=p["username"]) for p in data["players"]]
    ))
    return "Tournament Created", 200

@app.route("/joinTournament", methods=["POST"])
def join_tournament():
    data = request.json
    
    tournament_id = data["tournamentId"]
    username = data["username"]
    
    join_request = Tournament.JoinTournamentRequest(
        tournament_id=tournament_id,
        player=Account(username=username)
    )
    
    tournament_client.JoinTournament(join_request)
    return "Joined Tournament", 200

@app.route("/account/<username>", methods=["GET"])
def get_acount(username):
    accountRequest = AccountRequest(username=username)
    account_response = account_client.GetAccount(accountRequest)
    return render_template(
        "accountScreen.html",
        account=account_response
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
