# thirdparty
import factory

# project
from src import tables


class BasketItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("pystr")
    price = factory.Faker("pyint")

    basket = factory.SubFactory("src.fixtures.BasketFactory")

    class Meta:
        model = tables.BasketItem
