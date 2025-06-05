import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from app.api.models import *
from app.core.models.base import BaseModel
from app.core.settings import Settings, get_settings
from app.server.main import get_app

settings: Settings = get_settings()

engine = create_engine("postgresql+psycopg2://" + settings.get_test_database_url)
TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def db_session():
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session", autouse=True)
def set_up_db():
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="function", autouse=True)
def db_session_rollback(db_session):
    try:
        yield
    finally:
        db_session.rollback()


@pytest.fixture(scope="function", autouse=True)
def create_roles(db_session):
    db_session.query(Role).delete()
    db_session.commit()
    roles = [
        Role(name="SuperAdmin"),
        Role(name="Admin"),
        Role(name="Chef"),
        Role(name="Manager"),
    ]
    db_session.add_all(roles)
    db_session.commit()


@pytest.fixture(scope="session")
def http_client():
    app = get_app()
    with TestClient(app) as test_client:
        yield test_client
