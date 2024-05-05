import datetime
import json
from typing import List
from dataclasses import dataclass
from sqlalchemy import ForeignKey, exc, select, text

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy



class Base(DeclarativeBase):
    pass
            
db = SQLAlchemy(model_class=Base)

def load_from_pandas(cls, df, session):
        try:
            for index, row in df.iterrows():
                base = cls(**{column_name: row[column_name] for column_name in df.columns})
                session.add(base)
            session.commit()
        except exc.IntegrityError:
            pass

@dataclass
class Style(db.Model):
    __tablename__ = "style"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="style")
    social_events: Mapped[List["SocialEvent"]] = relationship(back_populates="style")

    def add(id, name, session):
        style = Style(id=id, name=name)
        session.add(style)
        session.commit()

@dataclass
class CityDistance(db.Model):
    __tablename__ = "citydistance"

    origin_id: Mapped[str] = mapped_column(ForeignKey("city.id"), primary_key=True)
    destination_id: Mapped[str] = mapped_column(ForeignKey("city.id"), primary_key=True)
    distance: Mapped[int] = mapped_column(nullable=False)

@dataclass
class StylesMatch(db.Model):
    __tablename__ = "styles_match"

    user_style_id: Mapped[str] = mapped_column(ForeignKey("style.id"), primary_key=True)
    social_event_style_id: Mapped[str] = mapped_column(ForeignKey("style.id"), primary_key=True)
    match_rate: Mapped[float] = mapped_column(nullable=True)

    # def add(user_style, social_event_style, match_value, session):
    #     styles_match = StylesMatch(user_style_id=user_style.id, social_event_style_id=social_event_style.id, match_rate=match_value)
    #     session.add(styles_match)
    #     session.commit()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    style_id: Mapped[str] = mapped_column(ForeignKey("style.id"), nullable=False)
    style: Mapped["Style"] = relationship(back_populates="users")
    city: Mapped["City"] = relationship(back_populates="users")
    city_id: Mapped[str] = mapped_column(ForeignKey("city.id"))
    departure_date: Mapped[datetime.date] = mapped_column(nullable=False)
    arrival_date: Mapped[datetime.date] = mapped_column(nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "style": self.style.name,
            "city": self.city.name,
            "departure_time": self.departure_date.strftime("%Y/%m/%d"),
            "arrival_date": self.arrival_date.strftime("%Y/%m/%d")
        }


@dataclass
class City(db.Model):
    __tablename__ = "city"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    social_events: Mapped[List["SocialEvent"]] = relationship(back_populates="city")
    users: Mapped[List["User"]] = relationship(back_populates="city")
    


class SocialEvent(db.Model):
    __tablename__ = "social_event"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[str] = mapped_column(ForeignKey("city.id"), nullable=False)
    city: Mapped["City"] = relationship(back_populates="social_events")
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    style_id: Mapped[str] = mapped_column(ForeignKey("style.id"), nullable=False)
    style: Mapped["Style"] = relationship(back_populates="social_events")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city.name,
            "date": self.date.strftime("%Y/%m/%d"),
            "price": self.price,
            "style": self.style.name
        }
    @staticmethod
    def format_list_sql(values):
        return ','.join([f"'{value}'" for value in values])

    def get_social_events_for_users(self, user_ids):
        stmt = text(
f"""
WITH
social_cte AS (
    SELECT 
        social_event.name AS event_name,
        social_event.price AS price,
        social_event.date AS date,
        social_event.city_id AS city_id,
        social_event.style_id AS style_id,
        city.name AS city,
        style.name AS style
    FROM
        social_event
    JOIN city
        on city.id = social_event.city_id
    JOIN style
        on style.id = social_event.style_id 
),


FILTER_USER AS(
    SELECT
        s.*,
        u.name as user_name,
        u.id as user_id,
        u.city_id as user_city_id,
        u.style_id as user_style_id
    FROM social_cte as s
    CROSS JOIN "user" as u
    WHERE 
        u.id in ({self.format_list_sql(user_ids)}) and
        u.departure_date <= s.date and
        u.arrival_date >= s.date
),

ADD_DISTANCE AS(
    SELECT
        f.*,
        cd.distance as distance
    FROM FILTER_USER AS f
    JOIN citydistance AS cd
        on cd.origin_id = f.user_city_id 
        and cd.destination_id = f.city_id       
),

ADD_MATCH AS(
    SELECT
        ad.*,
        sm.match_rate
    FROM ADD_DISTANCE AS ad
    JOIN styles_match as sm
        ON ad.style_id = sm.social_event_style_id
        and ad.user_style_id = sm.user_style_id
)


SELECT 
    event_name,
    price,
    date,
    city,
    style,
    distance,
    match_rate

FROM ADD_MATCH;


            """
)
        
        return stmt
    

    
        




