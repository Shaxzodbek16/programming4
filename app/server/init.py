import asyncio
from sqlalchemy.future import select


async def fill_roles():
    from app.core.databases.postgres import get_session_without_depends
    from app.api.models import Role

    async with get_session_without_depends() as session:
        roles = [
            Role(name="SuperAdmin"),
            Role(name="Admin"),
            Role(name="Chef"),
            Role(name="Manager"),
        ]
        q = await session.execute(select(Role))
        ex_roles = q.scalars().all()
        for role in roles:
            if role.name in [r.name for r in ex_roles]:
                continue
            session.add(role)
            await session.commit()
            await session.refresh(role)


def init():
    asyncio.create_task(fill_roles())
