# thirdparty
import factory

# project
from src import fixtures, tables


class BasketItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("pystr")
    price = factory.Faker("pyint")
    basket = factory.SubFactory(fixtures.BasketFactory)

    class Meta:
        model = tables.BasketItem
