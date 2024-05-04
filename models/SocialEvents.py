from typing import List
from dataclasses import dataclass
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.types import Date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


@dataclass
class Style(db.Model):
    __tablename__ = "style"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

@dataclass
class StylesMatch(db.Model):
    __tablename__ = "styles_matchup"

    id_subject_style: Mapped[str] = mapped_column(ForeignKey("style.id"))
    id_object_style: Mapped[str] = mapped_column(ForeignKey("style.id"))
    match_value: Mapped[float] = mapped_column(nullable=True)

@dataclass
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    style_id: Mapped[str] = mapped_column(nullable=False)
    trip_id: Mapped["Trip"] = relationship(back_populates="user")

@dataclass
class City(db.Model):
    __tablename__ = "city"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    social_events: Mapped[List["SocialEvent"]] = relationship(back_populates="city")
    departure_trips: Mapped[List["Trip"]] = relationship(back_populates="departure_city")
    arrival_trips: Mapped[List["Trip"]] = relationship(back_populates="arrival_city")

@dataclass
class SocialEvent(db.Model):
    __tablename__ = "social_event"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[str] = mapped_column(ForeignKey("city.id"), nullable=False)
    city: Mapped["City"] = relationship(back_populates="social_events")
    day: Mapped[Date] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    style_id: Mapped[str] = mapped_column(ForeignKey("style.id"))

@dataclass
class Trip(db.Model):
    __tablename__ = "trip"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    departure_city_id: Mapped[str] = mapped_column(ForeignKey("city.id"), nullable=False)
    departure_city: Mapped["City"] = relationship(back_populates="arrival_trips")
    arrival_city_id: Mapped[str] = mapped_column(ForeignKey("city.id"), nullable=False)
    arrival_city: Mapped["City"] = relationship(back_populates="departure_trips")


