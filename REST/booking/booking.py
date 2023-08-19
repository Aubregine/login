from flask import Flask, jsonify, request, make_response
import json
import requests

app = Flask(__name__)

PORT = 3201
HOST = "0.0.0.0"

USER_PORT = 3203
SHOWTIMES_PORT = 3202
MOVIE_PORT = 3200

with open("./databases/bookings.json", "r") as json_file:
    bookings: list = json.load(json_file)["bookings"]


@app.route("/", methods=["GET"])
def home():
    return "<h1>Booking Service</h1>"


@app.route("/bookings", methods=["GET"])
def get_bookings():
    return make_response(jsonify(bookings), 200)


@app.route("/bookings/<string:user_id>", methods=["GET"])
def get_bookings_for_user(user_id: str):
    for booking in bookings:
        if booking["user_id"] == user_id:
            return make_response(jsonify(booking), 200)
    return make_response(jsonify({"message": "No bookings found for user"}), 404)


@app.route("/bookings/<string:user_id>", methods=["POST"])
def add_booking_for_user(user_id: str):
    """
    Adds a booking for a user

    First, we check if the data provided is valid by:
    - Checking if the user exists
    - Checking if the movie exists
    - Checking if the showtime exists

    If the data is valid, we add the booking to the database,
    either by creating a new entry or updating an existing one.
    """

    # first, check the data provided
    data: dict = request.get_json()
    if not data:
        return make_response(jsonify({"message": "No data provided"}), 400)

    user_id: str = data.get("user_id")
    movie_id: str = data.get("movie_id")
    date: str = data.get("date")

    if not user_id or not movie_id or not date:
        return make_response(jsonify({"message": "Missing data"}), 400)

    # check if the user exists
    # hopefully this will work with docker
    user_service_url = (
        f"{':'.join(request.base_url.split(':')[:2])}:{USER_PORT}/user/{user_id}"
    )
    user_response = requests.get(user_service_url)

    if user_response.status_code >= 400:
        return make_response(jsonify({"message": "User not found"}), 404)

    # check if the movie exists
    # hopefully this will work with docker
    movie_service_url = (
        f"{':'.join(request.base_url.split(':')[:2])}:{MOVIE_PORT}/movie/{movie_id}"
    )
    movie_response = requests.get(movie_service_url)

    if movie_response.status_code >= 400:
        return make_response(jsonify({"message": "Movie not found"}), 404)

    # check if the showtime exists
    # hopefully this will work with docker
    showtimes_service_url = f"{':'.join(request.base_url.split(':')[:2])}:{SHOWTIMES_PORT}/showtime/{movie_id}"
    showtimes_response = requests.get(showtimes_service_url)

    if showtimes_response.status_code >= 400:
        return make_response(jsonify({"message": "Showtime not found"}), 404)

    # the data is valid, add the booking
    user_found: bool = False
    date_found: bool = False

    for booking in bookings:
        if booking["user_id"] == user_id:
            user_found = True
            for date_booking in booking["dates"]:
                if date_booking["date"] == date:
                    date_found = True
                    if movie_id in date_booking["movies"]:
                        return make_response(
                            jsonify({"message": "Booking already exists"}), 400
                        )
                    date_booking["movies"].append(movie_id)
                    break
            if not date_found:
                booking["bookings"].append({"date": date, "movies": [movie_id]})
            break
    if not user_found:
        bookings.append(
            {"user_id": user_id, "bookings": [{"date": date, "movies": [movie_id]}]}
        )

    # update the database
    with open("./databases/bookings.json", "w") as json_file:
        json.dump({"bookings": bookings}, json_file, indent=2)

    return make_response(jsonify({"message": "Booking added"}), 201)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
