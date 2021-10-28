# thirdparty
import factory

# project
from src import tables


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    username = factory.Faker("pystr")

    class Meta:
        model = tables.User
