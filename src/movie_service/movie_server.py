import grpc
from concurrent import futures
import random
import movie_pb2
import movie_pb2_grpc

MOVIES = [
    movie_pb2.Movie(movieId=1, title="Inception", rating=8.8, year=2010, poster="inception.jpg"),
    movie_pb2.Movie(movieId=2, title="The Matrix", rating=8.7, year=1999, poster="matrix.jpg")
]

class MovieService(movie_pb2_grpc.MovieServiceServicer):
    def GetAllMovies(self, request, context):
        return movie_pb2.MovieList(movies=MOVIES)

    def GetRandomMovie(self, request, context):
        return random.choice(MOVIES)

    def CreateMovie(self, request, context):
        MOVIES.append(request)
        return movie_pb2.Empty()

    def GetMovieById(self, request, context):
        for movie in MOVIES:
            if movie.movieId == request.movieId:
                return movie
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Movie not found")
        return movie_pb2.Movie()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServiceServicer_to_server(MovieService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
