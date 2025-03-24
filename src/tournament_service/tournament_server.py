import grpc
from concurrent import futures
import tournament_pb2
import tournament_pb2_grpc

class TournamentServiceServicer(tournament_pb2_grpc.TournamentServiceServicer):
    def CreateTournament(self, request, context):
        # Handle tournament creation logic
        print(f"Creating tournament: {request.name}")
        return tournament_pb2.Empty()  # Return an empty response on success

    def GetTournamentById(self, request, context):
        # Simulate getting tournament from a database
        print(f"Fetching tournament with ID: {request.id}")
        return tournament_pb2.Tournament(
            name="Best Movie Tournament",
            creator="Tournament Creator",
            prize=1000,
            players=[
                tournament_pb2.Account(username="user1", highScore=200),
                tournament_pb2.Account(username="user2", highScore=250)
            ]
        )

    def UpdateTournament(self, request, context):
        # Handle tournament update logic
        print(f"Updating tournament: {request.name}")
        return tournament_pb2.Empty()  # Return an empty response on success

    def DeleteTournament(self, request, context):
        # Handle tournament deletion logic
        print(f"Deleting tournament with ID: {request.id}")
        return tournament_pb2.Empty()  # Return an empty response on success

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tournament_pb2_grpc.add_TournamentServiceServicer_to_server(TournamentServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("Tournament server is running on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
