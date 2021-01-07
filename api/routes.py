from api.models.user import User
from flask.helpers import make_response
from flask import json, request

from api import app
from api.models.repo import Repo


@app.route("/healthcheck")
def healthcheck():
    return make_response("OK", 200)


@app.route("/users")
def get_users():
    return make_response("OK", 200)


repo = Repo(None)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.form
    name = data.get("name")
    user = User(name)
    repo.insert(user)
    return make_response(json.loads({"name": user.name}), 200)
