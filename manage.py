import asyncio

import typer
from typer import Typer, echo, style
import re
from app.core.databases.postgres import get_session_without_depends
from app.api.models import User
from sqlalchemy.future import select
from app.core.utils.security import security

app = Typer()


async def check_superuser_exists(email: str) -> bool:
    async with get_session_without_depends() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalars().first()
        if existing_user:
            echo(
                style(
                    "User with this email already exists!",
                    fg=typer.colors.RED,
                    bold=True,
                )
            )
            return False
        return True


async def create_superuser(first_name: str, last_name: str, email: str, password: str):
    async with get_session_without_depends() as session:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            profile_picture="https://shaxzodbek.com/static/blog/img/shaxzodbek.png",
            password=security.hash_password(password),
            role_id=1,
            is_active=True,
        )
        session.add(user)
        await session.commit()
        echo(style("Superuser created successfully!", fg=typer.colors.GREEN, bold=True))


def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


@app.command(help="Create a superuser.")
def createsuperuser():
    first_name = typer.prompt(style("First name", fg=typer.colors.GREEN))
    last_name = typer.prompt(style("Last name", fg=typer.colors.GREEN))
    while True:
        email = typer.prompt(style("Email", fg=typer.colors.GREEN))
        if not validate_email(email):
            echo(
                style(
                    "Invalid email format. Try again.", fg=typer.colors.RED, bold=True
                )
            )
        if asyncio.run(check_superuser_exists(email)):
            break
    while True:
        password = typer.prompt(
            style("Password", fg=typer.colors.YELLOW), hide_input=True
        )
        confirm_password = typer.prompt(
            style("Repeat for confirmation", fg=typer.colors.YELLOW), hide_input=True
        )
        if password == confirm_password:
            break
        echo(
            style("Passwords do not match. Try again.", fg=typer.colors.RED, bold=True)
        )
    echo(style("\nSuperuser created successfully!", fg=typer.colors.GREEN, bold=True))
    echo(style(f"Name: {first_name} {last_name}", fg=typer.colors.BLUE))
    echo(style(f"Email: {email}", fg=typer.colors.BLUE))
    asyncio.run(create_superuser(first_name, last_name, email, password))


@app.command(help="See all superusers.")
def allsuperusers():
    async def fetch_superusers():
        async with get_session_without_depends() as session:
            result = await session.execute(
                select(User).where(User.role_id == 1).order_by(User.id)
            )
            return result.scalars().all()

    superusers = asyncio.run(fetch_superusers())
    if not superusers:
        echo(style("No superusers found.", fg=typer.colors.YELLOW, bold=True))
    else:
        echo(style("Superusers:", fg=typer.colors.CYAN, bold=True))
        for user in superusers:
            echo(
                style(
                    f"ID: {user.id}, Name: {user.full_name}, Email: {user.email}",
                    fg=typer.colors.BLUE,
                )
            )


if __name__ == "__main__":
    app()
