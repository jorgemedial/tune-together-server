import pandas as pd
import numpy.random as rnd
import datetime

df = pd.read_csv("data/input/hackupc-travelperk-dataset.csv")

cities = tuple(df["Arrival City"].unique())

people = tuple(df["Traveller Name"].unique())[:400]


styles = [
        "Rock",
        "Pop",
        "Indie",
        "Electro",
        "Techno",
        "Heavy",
        "Rap",
        "Reggae",
        "Classical",
        "Folk"
    ]


def get_random_departure_date():
    return datetime.date(2024, 6, 1) + datetime.timedelta(days=rnd.randint(0, 85))
   
def get_random_return_date(departure_date):
    return departure_date + datetime.timedelta(days=rnd.randint(5,15))

def get_random_departure_city():
    return rnd.randint(0, len(cities)-1)


def random_style():
    return rnd.randint(0, len(styles)-1)


df_users = pd.DataFrame({"name": people})
df_users["city_id"] = df_users["name"].apply(lambda row: get_random_departure_city())
df_users["style_id"] = df_users["name"].apply(lambda x: random_style())
df_users["departure_date"] = df_users["name"].apply(lambda x: get_random_departure_date())
df_users["arrival_date"] = df_users["departure_date"].apply(lambda date: get_random_return_date(date))

df_users.to_csv("data/outputs/users.csv", index_label="id")


def random_denom():
    return rnd.choice(["Fest", "Concert", "Music Event"])

df_social_events = pd.DataFrame({"city_id": tuple(range(len(cities)))*3})
df_social_events["date"] = df_social_events["city_id"].apply(
    lambda city: get_random_departure_date() + datetime.timedelta(days=2)
                                                          )
df_social_events["style_id"] = df_social_events["city_id"].apply(lambda city: random_style())
df_social_events["price"] = df_social_events.apply(lambda x: rnd.randint(10, 150), axis=1)
df_social_events["name"] = df_social_events.apply(
    lambda row: f"{cities[row["city_id"]]} {styles[row['style_id']]} {random_denom()}", axis=1)

df_social_events.to_csv("data/outputs/social_events.csv", index_label="id")

pd.DataFrame({"name": cities}).to_csv("data/outputs/cities.csv", index_label="id")
pd.DataFrame({"name": styles}).to_csv("data/outputs/styles.csv", index_label="id")
