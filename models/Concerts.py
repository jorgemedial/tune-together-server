from dataclasses import dataclass
from sqlalchemy.types import Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

@dataclass
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    style_id: Mapped[str] = mapped_column(nullable=False)

@dataclass
class Concert(db.Model):
    __tablename__ = "concert"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    day: Mapped[Date] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    style: Mapped[]

@dataclass
class Style(db.Model):
    __tablename__ = "style"

    id: Mapped[str] = mapped_column(primary_key=True)
    


