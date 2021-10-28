# thirdparty
from sqlalchemy.ext.hybrid import hybrid_property

# project
from src.extensions import db


class Basket(db.Model):
    __tablename__ = "basket"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
    )
    user = db.relationship("src.tables.user.User", back_populates="baskets")

    pickup = db.Column(db.Boolean, comment="Самовывоз")

    items = db.relationship(
        "src.tables.basket_item.BasketItem",
        back_populates="basket",
        lazy="dynamic",
    )

    @hybrid_property
    def cost(self):
        return sum(item.price for item in self.items)
