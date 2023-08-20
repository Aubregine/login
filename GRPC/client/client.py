from datetime import datetime
from flask import Flask, jsonify, make_response, request, render_template
import grpc
import user_pb2_grpc
import user_pb2


PORT = 3204
HOST = "0.0.0.0"  # localhost
USER_PORT = 3203

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Returns the home page
    We're not using any framework for the frontend, so we're just rendering a template
    Every page has its own template, so we're not using any template inheritance, nor any template engine
    """
    return make_response(render_template("home.html"), 200)


@app.route("/users", methods=["GET"])
def get_users():
    with grpc.insecure_channel(f"localhost:{USER_PORT}") as channel:
        stub = user_pb2_grpc.UsersStub(channel)
        res = stub.GetUsers(user_pb2.uEmpty())
        users = [{"id": user.id, "name": user.name} for user in res]
        return make_response(jsonify(users), 200)


@app.route("/user/<string:id>", methods=["GET"])
def get_user(id: str):
    """
    We use url parameters and request body parameters just to show of the different ways to pass data
    It's not a good idea to use both in the same app, but we're here to graduate, not to make a good app
    Either way, this is a GET request with url parameters
    """
    with grpc.insecure_channel(f"localhost:{USER_PORT}") as channel:
        stub = user_pb2_grpc.UsersStub(channel)
        try:
            user = stub.GetUserByID(user_pb2.uUserID(id=id))
            return jsonify(user)
        except grpc.RpcError as e:
            return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/user", methods=["POST"])
def add_user():
    req = request.get_json()
    if not req:
        return make_response(jsonify({"error": "No data provided"}), 400)

    name: str = req.get("name")
    id: str = req.get("id")

    if not name or not id:
        return make_response(jsonify({"error": "Missing data"}), 400)

    user: dict = {
        "id": id,
        "name": name,
        # we're using unix time
        "last_active": int((datetime.now() - datetime(1970, 1, 1)).total_seconds()),
    }

    with grpc.insecure_channel(f"localhost:{USER_PORT}") as channel:
        stub = user_pb2_grpc.UsersStub(channel)
        try:
            res = stub.AddUser(user_pb2.uUser(**user))
            return make_response(jsonify(res), 201)
        except grpc.RpcError as e:
            return make_response(jsonify({"error": e.details()}), e.code())


@app.route("/bookings", methods=["POST"])
def get_bookings():
    """
    This is a POST request with a request body, since GET requests shouldn't have a body
    Even if we are not posting anything, we're still need to use a POST request

    We retrieve all the bookings for the user from the booking service
    """
    req = request.get_json()

    if not req:
        return make_response(jsonify({"error": "No data provided"}), 400)

    id: str = req.get("id")

    with grpc.insecure_channel(f"localhost:{USER_PORT}") as channel:
        stub = user_pb2_grpc.UsersStub(channel)
        try:
            res = stub.GetBookingForUser(user_pb2.uUserID(id=id))
            return make_response(jsonify(res), 200)
        except grpc.RpcError as e:
            return make_response(jsonify({"error": e.details()}), e.code())


@app.route("/movies/<string:id>", methods=["GET"])
def get_movies_info(id: str):
    """
    First, we check if the user exists
    Then, we retrieve the bookings for that user
    And finally, we retrieve the movies info for each booking made by the user
    """

    with grpc.insecure_channel(f"localhost:{USER_PORT}") as channel:
        stub = user_pb2_grpc.UsersStub(channel)
        try:
            movies = stub.GetMoviesForUser(user_pb2.uUserID(id=id))
            return make_response(jsonify(movies), 200)
        except grpc.RpcError as e:
            return make_response(jsonify({"error": e.details()}), e.code())


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
