from flask import Flask, jsonify, Response
import pandas as pd

from models.model import db, City, User, Style, SocialEvent, load_from_pandas
from secret_keys import connection_string
app = Flask(__name__)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_ECHO"] = True
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/load_dummy_styles", methods=["GET"])
def load_dummy_styles():
    df_styles = pd.read_csv("data/outputs/styles.csv")
    load_from_pandas(Style, df_styles, db.session)
    return Response({"message": "success"}, status=200)

@app.route("/load_dummy_cities", methods=["GET"])
def load_dummy_cities():
    df_cities = pd.read_csv("data/outputs/cities.csv")
    load_from_pandas(City, df_cities, db.session)
    return Response({"message": "success"}, status=200)

@app.route("/load_dummy_users", methods=["GET"])
def load_dummy_users():
    df_users = pd.read_csv("data/outputs/users.csv")
    load_from_pandas(User, df_users, db.session)
    return Response({"message": "success"}, status=200)

@app.route("/load_dummy_social_events", methods=["GET"])
def load_dummy_social_events():
    df = pd.read_csv("data/outputs/social_events.csv")
    load_from_pandas(SocialEvent, df, db.session)
    return Response({"message": "success"}, status=200)

@app.route("/users", methods=["GET"])
def get_users():
    user_list = [user.to_dict() for user in User.query.all()]
    return Response(user_list, status=200)

@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.filter_by(id=id).one()
    return jsonify(user.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)
    
    