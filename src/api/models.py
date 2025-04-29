from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

likes_people = db.Table(
    "likes_people",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id_user"), primary_key=True),
    db.Column("people_id", db.Integer, db.ForeignKey("people.id_people"), primary_key=True)
)

likes_planets = db.Table(
    "likes_planets",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id_user"), primary_key=True),
    db.Column("`planets_id`", db.Integer, db.ForeignKey("planets.id_planets"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    liked_people = relationship("People", secondary=likes_people, back_populates="likes_user")
    liked_planets = relationship("Planets", secondary=likes_planets, back_populates="likes_user")


    def serialize(self):
        return {
            "id_user": self.id_user,
            "email": self.email,
            "username": self.username,
            "liked_people": [ppl.serialize() for ppl in self.liked_people],
            "liked_planets": [pla.serialize() for pla in self.liked_planets]
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = "people"
    id_people: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(50))
    mass: Mapped[int] = mapped_column()

    def serialize(self):
        return {
            "id_people": self.id_people,
            "name": self.name,
            "gender": self.gender,
            "mass": self.mass
        }
    
class Planets(db.Model):
    __tablename__ = "planets"
    id_planet: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    diameter: Mapped[int] = mapped_column()

    def serialize(self):
        return {
            "id_planet": self.id_planet,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter
        }