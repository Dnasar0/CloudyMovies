import os

import grpc
from flask import Flask, render_template
from movie_pb2_grpc  import MovieServiceStub 
from movie_pb2 import MovieRequest



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
movie_connection = grpc.insecure_channel("host.docker.internal:50052")
#movie_connection = grpc.insecure_channel(f"{recommendations_host}:50051")
movie_client = MovieServiceStub(movie_connection)

@app.route("/get/<int:given_id>")
def render_homepage(given_id):
    movie_request = MovieRequest(movieId=given_id)
    movie_response = movie_client.GetMovieById(movie_request)
    print(movie_request)
    return render_template(
        "gameScreen.html",
        movie=movie_response
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
