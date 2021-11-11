# thirdparty
import factory

# project
from src import tables


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    username = factory.Faker("pystr")

    class Meta:
        model = tables.User

    class Params:
        marina = factory.Trait(username="Марина")
