from datetime import datetime
from flask import Flask, jsonify, make_response, request, render_template
import json

import requests


PORT = 3203
HOST = "0.0.0.0"  # localhost

BOOKING_PORT = 3201
MOVIE_PORT = 3200

app = Flask(__name__)

with open("./databases/users.json", "r") as json_file:
    users: list = json.load(json_file)["users"]


@app.route("/", methods=["GET"])
def home():
    """
    This is a GET request with no parameters

    Returns the home page
    We're not using any framework for the frontend, so we're just rendering a template
    Every page has its own template, so we're not using any template inheritance, nor any template engine
    """
    return make_response(render_template("home/home.html"), 200)


@app.route("/users", methods=["GET"])
def get_users():
    """
    This is a GET request with no parameters

    We simply dump the users database
    """
    # TODO: create an html page for this
    return jsonify(users)


@app.route("/user/<string:id>", methods=["GET"])
def get_user(id: str):
    """
    We use url query parameters and request body parameters just to show of the different ways to pass data
    It's not a good idea to use both in the same app, but we're here to graduate, not to make a good app
    Either way, this is a GET request with query parameters
    """
    for user in users:
        if user["id"] == id:
            # TODO: create an html page for this
            return jsonify(user)
    return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/user", methods=["POST"])
def add_user():
    """
    This is a POST request with a request body
    """
    req = request.get_json()
    if not req:
        return make_response(jsonify({"error": "No data provided"}), 400)

    name: str = req.get("name")
    id: str = req.get("id")

    if not name or not id:
        return make_response(jsonify({"error": "Missing data"}), 400)

    if id in [user["id"] for user in users]:
        return make_response(jsonify({"error": "User already exists"}), 400)

    user: dict = {
        "id": id,
        "name": name,
        # we're using unix time
        "last_active": int((datetime.now() - datetime(1970, 1, 1)).total_seconds()),
    }
    users.append(user)

    # save to database
    with open("./databases/users.json", "w") as json_file:
        json.dump({"users": users}, json_file, indent=2)

    # TODO: create an html page for this
    return make_response(jsonify(user), 201)


@app.route("/bookings", methods=["GET"])
def get_bookings():
    """
    This is a GET request with a request body

    We retrieve all the bookings for the user from the booking service
    """
    req = request.get_json()

    if not req:
        return make_response(jsonify({"error": "No data provided"}), 400)

    id: str = req.get("id")
    name: str = req.get("name")

    if not id:
        if not name:
            return make_response(jsonify({"error": "Missing data"}), 400)
        # retrieve id from name
        for user in users:
            if user["name"] == name:
                id = user["id"]
                break

    if not id or id not in [user["id"] for user in users]:
        return make_response(jsonify({"error": "User not found"}), 404)

    # hopefully this will work with docker
    url: str = (
        f"{':'.join(request.base_url.split(':')[:2])}:{BOOKING_PORT}/bookings/{id}"
    )
    res = requests.get(url)

    if res.status_code >= 400:
        return make_response(jsonify({"error": "Error retrieving bookings"}), 400)

    # TODO: create an html page for this
    return make_response(jsonify(res.json()), 200)


@app.route("/movies/<string:id>", methods=["GET"])
def get_movies_info(id: str):
    """
    This is a GET request with query parameters

    First, we check if the user exists
    Then, we retrieve the bookings for that user
    And finally, we retrieve the movies info for each booking made by the user
    """
    user = None
    for u in users:
        if u["id"] == id:
            user = u
            break

    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    # hopefully this will work with docker
    url: str = (
        f"{':'.join(request.base_url.split(':')[:2])}:{BOOKING_PORT}/bookings/{id}"
    )

    res = requests.get(url)
    if res.status_code >= 400:
        return make_response(jsonify({"error": "Error retrieving bookings"}), 400)

    bookings = res.json()

    seen_movies: set[int] = set()
    movies: list = []

    for date in bookings["dates"]:
        # to avoid duplicates
        for movie_id in date["movies"]:
            if movie_id not in seen_movies:
                seen_movies.add(movie_id)

                # hopefully this will work with docker
                movie_url: str = f"{':'.join(request.base_url.split(':')[:2])}:{MOVIE_PORT}/movie/{movie_id}"
                movie_response = requests.get(movie_url)

                if movie_response.ok:
                    movies.append(movie_response.json())

    # TODO: create an html page for this
    return make_response(jsonify(movies), 200)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
