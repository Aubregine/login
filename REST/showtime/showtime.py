from flask import Flask, jsonify, request, make_response
import json

app = Flask(__name__)

PORT = 3202
HOST = "0.0.0.0"

with open("./databases/showtimes.json", "r") as json_file:
    showtimes: list = json.load(json_file)["showtimes"]


@app.route("/", methods=["GET"])
def home():
    return "<h1>Showtime Service</h1>"


@app.route("/showtimes", methods=["GET"])
def get_showtimes():
    return make_response(jsonify(showtimes), 200)


@app.route("/showtime/<string:date>", methods=["GET"])
def get_showtime(date: str):
    for showtime in showtimes:
        if showtime["date"] == date:
            return make_response(jsonify(showtime), 200)
    return make_response(jsonify({"message": "Showtime not found"}), 404)


@app.route("/showtime", methods=["POST"])
def create_showtime():
    showtime = request.get_json()

    if not showtime:
        return make_response(jsonify({"message": "No data provided"}), 400)

    date: str = showtime.get("date")
    movies: list = showtime.get("movies")

    if not date or not movies:
        return make_response(jsonify({"message": "Invalid data provided"}), 400)

    for showtime in showtimes:
        if showtime["date"] == date:
            return make_response(jsonify({"message": "Showtime already exists"}), 400)

    new_showtime: dict = {"date": date, "movies": movies}
    showtimes.append(new_showtime)

    # update the database
    with open("./databases/showtimes.json", "w") as json_file:
        json.dump({"showtimes": showtimes}, json_file, indent=2)

    return make_response(jsonify({"message": "Showtime created"}), 201)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
