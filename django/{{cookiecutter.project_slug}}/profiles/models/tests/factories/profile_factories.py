import factory
import random
from faker import Faker

from accounts.models.tests.factories.account_factories import AccountFactory
from profiles.models import Profile
from profiles.models.profile_models import Gender

fake = Faker()

gender_choices = ['Male', 'Female']


class GenderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Gender

    name = random.choice(gender_choices)


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    first_name = fake.first_name()
    middle_name = fake.last_name()
    last_name = fake.last_name()
    date_of_birth = fake.profile().get('birthdate')
    gender = factory.SubFactory(GenderFactory)
    account = factory.SubFactory(AccountFactory)
