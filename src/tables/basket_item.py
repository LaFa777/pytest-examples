# project
from src.extensions import db


class BasketItem(db.Model):
    __tablename__ = "basket_item"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    price = db.Column(db.Integer)

    basket_id = db.Column(
        db.Integer,
        db.ForeignKey("basket.id"),
    )
    basket = db.relationship("src.tables.basket.Basket", back_populates="items")
