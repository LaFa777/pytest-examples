# thirdparty
import factory

# project
from src import tables


class BasketFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    pickup = factory.Faker("pybool")

    user = factory.SubFactory("src.fixtures.UserFactory")

    class Meta:
        model = tables.Basket
