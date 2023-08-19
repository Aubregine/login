from flask import Flask, jsonify, request, make_response
import json

app = Flask(__name__)

PORT = 3200
HOST = "0.0.0.0"

with open("./databases/movies.json", "r") as json_file:
    movies: list = json.load(json_file)["movies"]


@app.route("/", methods=["GET"])
def home():
    return "<h1>Movie Service</h1>"


@app.route("/movies", methods=["GET"])
def get_movies():
    return make_response(jsonify(movies), 200)


@app.route("/movie/<string:movie_id>", methods=["GET"])
def get_movie(movie_id: str):
    for movie in movies:
        if movie["id"] == movie_id:
            return make_response(jsonify(movie), 200)
    return make_response(jsonify({"message": "Movie not found"}), 404)


@app.route("/movie-by-title/<string:title>", methods=["GET"])
def get_movie_by_name(title: str):
    for movie in movies:
        if movie["title"] == title:
            return make_response(jsonify(movie), 200)
    return make_response(jsonify({"message": "Movie not found"}), 404)


@app.route("/movie", methods=["POST"])
def add_movie():
    data: dict = request.get_json()
    if not data:
        return make_response(jsonify({"message": "No data provided"}), 400)

    title: str = data.get("title")
    rating: float = data.get("rating")
    director: str = data.get("director")
    id: str = data.get("id")

    if not title or not rating or not director or not id:
        return make_response(jsonify({"message": "Missing data"}), 400)

    for movie in movies:
        if movie["id"] == id:
            return make_response(jsonify({"message": "Movie already exists"}), 400)

    new_movie: dict = {"title": title, "rating": rating, "director": director, "id": id}
    movies.append(new_movie)

    # update the database
    with open("./databases/movies.json", "w") as json_file:
        json.dump({"movies": movies}, json_file, indent=2)

    return make_response(jsonify({"message": "Movie added"}), 201)


@app.route("/movie/<string:movie_id>", methods=["DELETE"])
def delete_movie(movie_id: str):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            with open("./databases/movies.json", "w") as json_file:
                json.dump({"movies": movies}, json_file, indent=2)
            return make_response(jsonify({"message": "Movie deleted"}), 200)
    return make_response(jsonify({"message": "Movie not found"}), 404)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
