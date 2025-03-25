import grpc
from concurrent import futures
import tournament_pb2
import tournament_pb2_grpc
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["cloudy_movies"]
accounts_collection = db["tournament"]

class TournamentServiceServicer(tournament_pb2_grpc.TournamentServiceServicer):
    def CreateTournament(self, request, context):
        
        try:        
            tournament_data = {
                
                "date" : request.date,
                "name" : request.name,
                "creator" : request.creator,
                "prize" : request.prize,
                "players" : [{
                    "username" : player.username,
                    "highScore" : player.highScore
                } for player in request.players]
            }
            
            result = accounts_collection.insert_one(tournament_data)
            
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
            tournament = accounts_collection.find_one({"_id": tournament_id})
            
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
            tournament = accounts_collection.find_one_and_update(
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
            result = accounts_collection.delete_one({"_id": tournament_id})
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tournament_pb2_grpc.add_TournamentServiceServicer_to_server(TournamentServiceServicer(), server)
    server.add_insecure_port('[::]:50053')
    print("Tournament server is running on port 50053...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
