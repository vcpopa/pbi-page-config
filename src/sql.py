"""
This module provides a utility for connecting to a SQL Server database using SQLAlchemy.
It uses context managers
for managing the database connection and dotenv for loading environment variables.

Functions:
- connection: A context manager for creating and closing the database connection.
"""

from contextlib import contextmanager
import urllib
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from utils import get_credential  # pylint: disable=import-error


@contextmanager
def connection() -> Iterator[Engine]:
    """
    Context manager to create and close a database connection.

    Loads database connection parameters from environment variables, creates
    a SQLAlchemy engine, and yields the engine. The engine is closed when the
    context is exited.

    Returns:
        Iterator[Engine]: An iterator that yields a SQLAlchemy Engine.
    """

    connstr = get_credential("public-dataflow-connectionstring")
    params = urllib.parse.quote_plus(connstr)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    try:
        yield engine
    finally:
        engine.dispose()
