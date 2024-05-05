import json
from flask import Flask, jsonify, Response
import pandas as pd

from flask_cors import CORS


from models.model import db, City, User, Style, SocialEvent, StylesMatch, CityDistance, load_from_pandas
from secret_keys import connection_string




# create the app
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config.from_object(__name__)

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

@app.route("/load_dummy_style_match", methods=["GET"])
def load_dummy_style_match():
    df = pd.read_csv("data/outputs/styles_match.csv")
    df["match_rate"] = df["match_rate"].values.astype(float)
    df["user_style_id"] = df["user_style_id"].values.astype(str)
    df["social_event_style_id"] = df["social_event_style_id"].values.astype(str)
    load_from_pandas(StylesMatch, df[["user_style_id", "social_event_style_id", "match_rate"]].copy(), db.session)
    return Response({"message": "success"}, status=200)

@app.route("/load_dummy_distances", methods=["GET"])
def load_dummt_distances():
    df = pd.read_csv("data/outputs/citydistance.csv", sep=",")
    df["distance"] = df["distance"].values.astype(int)
    df["origin_id"] = df["origin_id"].values.astype(str)
    df["destination_id"] = df["destination_id"].values.astype(str)

    df = df[["origin_id", "destination_id", "distance"]].copy()
    load_from_pandas(CityDistance, df, db.session)


    return Response({"message": "success"}, status=200)

@app.route("/users", methods=["GET"])
def get_users():
    user_list = [user.to_dict() for user in User.query.all()]
    return Response(json.dumps(user_list), status=200)


@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.filter_by(id=id).one()
    return jsonify(user.to_dict()), 200

@app.route("/social-events", methods=["GET"])
def get_social_events():
    social_event_list = [social_event.to_dict() for social_event in SocialEvent.query.all()]
    return Response(json.dumps(social_event_list), status=200)

@app.route("/social_events_for_user/<user_id>", methods=["GET"])
def get_social_events_for_user(user_id):
    stmt = SocialEvent().get_social_events_for_users(list(user_id))
    result = db.session.execute(stmt)
    result_list = [
        {
            "event_name": row.event_name,
            "price": row.price,
            "date": row.date.strftime("%Y/%m/%d"),
            "city": row.city,
            "distance": row.distance,
            "match_rate": row.match_rate,
            "style": row.style
        }
        for row in result]
    return Response(json.dumps(result_list), status=200)

if __name__ == '__main__':
    app.run(debug=True)
    
    