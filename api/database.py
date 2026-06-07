import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import DBAPIError

# loading .env file
load_dotenv()


def get_database_url() -> str:
    """
    The function `get_database_url` creates a database URL using environment variables for driver,
    username, password, host, port, and database name.
    :return: A database URL string is being returned by this function. The function creates a URL using
    the environment variables for the database driver, username, password, host, port, and database
    name, and then renders it as a string.
    """
    return URL.create(
        drivername=os.getenv("DATABASE_DRIVER"),
        username=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT", 5432),
        database=os.getenv("DATABASE_NAME"),
    ).render_as_string(hide_password=False)


engine = create_engine(get_database_url(), pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


# Verify database connection and credentials before starting the app
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
except DBAPIError as err:
    raise err
