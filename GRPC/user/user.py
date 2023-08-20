import grpc
import user_pb2_grpc
import user_pb2
import booking_pb2_grpc
import booking_pb2
import movie_pb2_grpc
import movie_pb2
import json
from concurrent import futures

PORT = 3203

BOOKING_PORT = 3201
MOVIE_PORT = 3200


class UserServicer(user_pb2_grpc.UsersServicer):
    def __init__(self):
        with open("./databases/users.json", "r") as f:
            self.users: list = json.load(f)["users"]

    def GetUsers(self, request, context):
        for user in self.users:
            yield user_pb2.uUser(
                id=user["id"],
                name=user["name"],
                last_active=user["last_active"],
            )

    def GetUserByID(self, request, context):
        for user in self.users:
            if user["id"] == request.id:
                return user_pb2.uUser(
                    id=user["id"],
                    name=user["name"],
                    last_active=user["last_active"],
                )
        # If no user is found, raise an error
        context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

    def AddUser(self, request, context):
        # Check if user already exists
        for user in self.users:
            if user["id"] == request.id:
                # If user already exists, raise an error
                context.abort(grpc.StatusCode.ALREADY_EXISTS, "User already exists")
        # If user does not exist, add user to database
        self.users.append(
            {
                "id": request.id,
                "name": request.name,
                "last_active": request.last_active,
            }
        )
        # Write to file
        with open("./databases/users.json", "w") as f:
            json.dump(self.users, f, indent=2)
        return user_pb2.uResponse(
            message="User added successfully",
            success=True,
        )

    def GetBookingForUser(self, request, context):
        # Check if user exists
        if not request["id"] in [user["id"] for user in self.users]:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        # ask booking service for bookings
        try:
            with grpc.insecure_channel(f"localhost:{BOOKING_PORT}") as channel:
                stub = booking_pb2_grpc.BookingsStub(channel)
                booking = stub.GetBookingForUser(booking_pb2.UserID(id=request["id"]))
                return booking
        except grpc.RpcError as e:
            context.abort(e.code(), e.details())

    def GetMoviesForUser(self, request, context):
        # Check if user exists
        if not request["id"] in [user["id"] for user in self.users]:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        # ask booking service for bookings
        try:
            with grpc.insecure_channel(f"localhost:{BOOKING_PORT}") as channel:
                stub = booking_pb2_grpc.BookingsStub(channel)
                booking = stub.GetBookingForUser(booking_pb2.UserID(id=request["id"]))
        except grpc.RpcError as e:
            context.abort(e.code(), e.details())

        # then, ask movie service the movie data

        movies: list = []
        seen_movies: set = set()

        for date in booking["dates"]:
            # to avoid duplicates
            for movie_id in date["movies"]:
                if movie_id not in seen_movies:
                    seen_movies.add(movie_id)

                    # ask the movie service for the movie data
                    try:
                        with grpc.insecure_channel(
                            f"localhost:{MOVIE_PORT}"
                        ) as channel:
                            stub = movie_pb2_grpc.MoviesStub(channel)
                            movie = stub.GetMovie(movie_pb2.MovieID(id=movie_id))
                            movies.append(movie)
                    except grpc.RpcError as e:
                        context.abort(e.code(), e.details())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UsersServicer_to_server(UserServicer(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
