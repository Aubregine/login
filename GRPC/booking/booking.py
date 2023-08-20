import grpc
import json
from concurrent import futures
import booking_pb2_grpc
import booking_pb2

PORT = 3201

USER_PORT = 3203
SHOWTIMES_PORT = 3202
MOVIE_PORT = 3200


class BookingServicer(booking_pb2_grpc.BookingsServicer):
    def __init__(self):
        with open("./databases/bookings.json", "r") as f:
            self.bookings: list = json.load(f)["bookings"]

    def GetBookings(self, request, context):
        for booking in self.bookings:
            dates = [
                booking_pb2.bDate(date=date["date"], movies=date["movies"])
                for date in booking["dates"]
            ]
            yield booking_pb2.bBooking(user_id=booking["user_id"], dates=dates)

    def GetBookingForUser(self, request, context):
        for booking in self.bookings:
            if booking["user_id"] == request.user_id:
                dates = [
                    booking_pb2.bDate(date=date["date"], movies=date["movies"])
                    for date in booking["dates"]
                ]
                return booking_pb2.bBooking(user_id=booking["user_id"], dates=dates)
        # If no booking is found, raise an error
        context.abort(grpc.StatusCode.NOT_FOUND, "Booking not found")

    def AddBookingForUser(self, request, context):
        """
        We're using the same algorithm as the REST API here.
        But we don't have the exact same data structure, therefore we need to
        make some adjustments (ie. the data provided only contains one date and
        one movie)
        """
        # check if the user exists
        with grpc.insecure_channel(f"localhost:{USER_PORT}") as channel:
            stub = booking_pb2_grpc.UsersStub(channel)
            try:
                stub.GetUserByID(booking_pb2.uUserID(id=request.user_id))
            except grpc.RpcError as e:
                context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        # check if the movie exists
        with grpc.insecure_channel(f"localhost:{MOVIE_PORT}") as channel:
            stub = booking_pb2_grpc.MoviesStub(channel)
            try:
                stub.GetMovieByID(booking_pb2.mMovieID(id=request.movie_id))
            except grpc.RpcError as e:
                context.abort(grpc.StatusCode.NOT_FOUND, "Movie not found")

        # check if the showtime exists
        with grpc.insecure_channel(f"localhost:{SHOWTIMES_PORT}") as channel:
            stub = booking_pb2_grpc.ShowtimesStub(channel)
            try:
                stub.GetShowtimeByID(booking_pb2.sShowtimeID(id=request.showtime_id))
            except grpc.RpcError as e:
                context.abort(grpc.StatusCode.NOT_FOUND, "Showtime not found")

        # add the booking
        user_found: bool = False
        date_found: bool = False

        for booking in self.bookings:
            if booking["user_id"] == request.userId:
                user_found = True
                for date_booking in booking["dates"]:
                    if date_booking["date"] == request.dates[0].date:
                        date_found = True
                        if request.dates[0].movies in date_booking["movies"]:
                            context.abort(
                                grpc.StatusCode.ALREADY_EXISTS, "Booking already exists"
                            )
                        date_booking["movies"].append(request.dates[0].movies)
                        break
                if not date_found:
                    booking["bookings"].append(
                        {
                            "date": request.dates[0].date,
                            "movies": request.dates[0].movies,
                        }
                    )
                break
        if not user_found:
            self.bookings.append(
                {
                    "user_id": request.userId,
                    "bookings": [
                        {
                            "date": request.dates[0].date,
                            "movies": request.dates[0].movies,
                        }
                    ],
                }
            )

        # Write to file
        with open("./databases/bookings.json", "w") as f:
            json.dump({"bookings": self.bookings}, f, indent=2)
        return booking_pb2.bResponse(
            message="Booking added successfully",
            success=True,
        )
