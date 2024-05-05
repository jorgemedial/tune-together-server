import datetime
import json
from typing import List
from dataclasses import dataclass
from sqlalchemy import ForeignKey, exc, select

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

    def add(user_style, social_event_style, match_value, session):
        styles_match = StylesMatch(user_style_id=user_style.id, social_event_style_id=social_event_style.id, match_rate=match_value)
        session.add(styles_match)
        session.commit()


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
    
    def map_users_social_events(self):
        stmt = select(
                SocialEvent.id, User.id
            ).filter(
                SocialEvent.date <= User.departure_date
            ).filter(
                 SocialEvent.date >= User.arrival_date
            )
        return stmt
    
    def add_distance(self, stmt):
        pass
    
    
        




