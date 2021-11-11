# project
from src.extensions import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), index=True, unique=True, nullable=False)

    baskets = db.relationship(
        "src.tables.basket.Basket",
        back_populates="user",
        lazy="dynamic",
    )

    def __repr__(self):
        return "<User {}>".format(self.username)
