import asyncio
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases.postgres import get_general_session
from app.api.models import Unit, Ingredient, User


class Feed:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__faker = Faker()

    async def _feed_units(self, count: int) -> int:
        for i in range(count):
            new_unit = Unit(
                code=self.__faker.text(max_nb_chars=9),
                description=self.__faker.text(max_nb_chars=10),
            )
            self.__session.add(new_unit)
        await self.__session.commit()
        return count

    async def _feed_ingredients(self, count: int, max_units: int) -> int:
        for i in range(count):
            new_ingredient = Ingredient(
                name=self.__faker.word(),
                unit_id=self.__faker.random_int(min=1, max=max_units),
                quantity=self.__faker.random_int(min=1, max=100),
                min_threshold=self.__faker.random_int(min=1, max=30),
            )
            self.__session.add(new_ingredient)
        await self.__session.commit()
        return count

    async def _feed_users(self) -> int:
        email_list = set()
        while len(email_list) < 2000:
            email = self.__faker.email()
            if email not in email_list:
                email_list.add(email)
        for i in range(2000):
            email = random.choice(list(email_list))
            email_list.remove(email)
            new_user = User(
                email=email,
                password=self.__faker.password(),
                first_name=self.__faker.first_name(),
                last_name=self.__faker.last_name(),
                role_id=self.__faker.random_int(min=1, max=4),
                is_active=self.__faker.boolean(chance_of_getting_true=70),
                profile_picture=self.__faker.image_url(width=100, height=100),
            )
            self.__session.add(new_user)
        await self.__session.commit()
        return 2000

    async def run(self):
        units_id = await self._feed_units(5)
        ingredients_id = await self._feed_ingredients(5, units_id)
        users_max = await self._feed_users()


async def main():
    async for session in get_general_session():
        feed = Feed(session)
        await feed.run()
        break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception, {e}")
