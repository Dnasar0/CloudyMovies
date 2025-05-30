import os
import threading
from flask import Flask
import grpc
from concurrent import futures
import tournament_pb2
import tournament_pb2_grpc
from pymongo import MongoClient
from bson import ObjectId

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
tournaments_collection = db["tournaments"]

class TournamentServiceServicer(tournament_pb2_grpc.TournamentServiceServicer):
    def CreateTournament(self, request, context):
        
        print("Creating tournament...")
        try:        
            tournament_data = {
                
                "date" : request.date,
                "name" : request.name,
                "creator" : request.creator,
                "prize" : request.prize,
                "players" : [{
                    "username" : player.username
                } for player in request.players]
            }
            print(tournament_data)
            
            result = tournaments_collection.insert_one(tournament_data)
            
            if result.inserted_id:
                print(f"Created tournament with ID: {result.inserted_id}")
                return tournament_pb2.Empty()
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error creating tournament: {str(e)}")
            return tournament_pb2.Empty()        

    def GetTournament(self, request, context):
        
        try:
            tournament_id = ObjectId(request.id)
            tournament = tournaments_collection.find_one({"_id": tournament_id})
            
            if tournament:
                return tournament_pb2.Tournament(
                    id=str(tournament["_id"]),
                    date=tournament["date"],
                    name=tournament["name"],
                    creator=tournament["creator"],
                    prize=tournament["prize"],
                    players=[tournament_pb2.Player(
                        username=player["username"],
                        highScore=player["highScore"]
                    ) for player in tournament["players"]]
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tournament not found")
                return None
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error retrieving tournament: {str(e)}")
            return None

    def UpdateTournament(self, request, context):
        
        try:
            tournament_id = ObjectId(request.id)
            tournament = tournaments_collection.find_one_and_update(
                {"_id": tournament_id},
                {
                    "$set": {
                        "date": request.date,
                        "name": request.name,
                        "creator": request.creator,
                        "prize": request.prize,
                        "players": [{
                            "username": player.username,
                            "highScore": player.highScore
                        } for player in request.players]
                    }
                },
                return_document=True
            )
            if tournament:
                print(f"Updated tournament with ID: {request.id}")
                return tournament_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tournament not found")
                return tournament_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error updating tournament: {str(e)}")
            return tournament_pb2.Empty()


    def DeleteTournament(self, request, context):
        
        try:
            tournament_id = ObjectId(request.id)
            result = tournaments_collection.delete_one({"_id": tournament_id})
            if result.deleted_count > 0:
                return tournament_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tournament not found")
                return tournament_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error deleting tournament: {str(e)}")
            return tournament_pb2.Empty()
        
    def ListTournaments(self, request, context):
        try:
            tournaments = tournaments_collection.find()
            tournament_list = tournament_pb2.TournamentList()

# Add all tournaments to the protobuf message
            for data in tournaments:
                tournament = tournament_list.tournaments.add()
                tournament.id = str(data.get("_id", ""))
                tournament.date = data.get("date", "")
                tournament.name = data.get("name", "Unknown Tournament")
                tournament.creator = data.get("creator", "Unknown")
                tournament.prize = data.get("prize", 0)

                for player_data in data.get("players", []):
                    player = tournament.players.add()
                    player.id = player_data.get("id", "")
                    player.username = player_data.get("username", "")
            return tournament_list
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error listing tournaments: {str(e)}")

    def JoinTournament(self, request, context):
        try:
            tournament_id = ObjectId(request.tournament_id)  # Fix field name
            new_player = {"username": request.player.username}  # Fix access to player username
            
            result = tournaments_collection.update_one(
                {"_id": tournament_id},
                {"$push": {"players": new_player}}  # Push new player to the players array
            )

            if result.modified_count > 0:
                print(f"Player {request.player.username} joined tournament {request.tournament_id}")
                return tournament_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tournament not found or player already in tournament")
                return tournament_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error joining tournament: {str(e)}")
            return tournament_pb2.Empty()
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tournament_pb2_grpc.add_TournamentServiceServicer_to_server(TournamentServiceServicer(), server)
    server.add_insecure_port('[::]:50053')
    print("Tournament server is running on port 50053...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    threading.Thread(target=run_health_server, daemon=True).start()
    serve()
