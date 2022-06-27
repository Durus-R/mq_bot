import os.path
import sys

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guild"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    prefix = sqlalchemy.Column(sqlalchemy.String)
    losung_channel = sqlalchemy.Column(sqlalchemy.Integer)
    losung_hour = sqlalchemy.Column(sqlalchemy.Integer)
    autodel_channel = sqlalchemy.Column(sqlalchemy.Integer)
    autodel_timeout = sqlalchemy.Column(sqlalchemy.Integer)


def create_sqlite_engine():
    """
    Creates a sqlalchemy engine for sqlite.
    """
    if "inux" in sys.platform and os.path.exists("/DB/database.sqlite"):
        engine = create_engine("sqlite:////DB/database.sqlite", echo=False, future=True)
    else:
        engine = create_engine("sqlite:///database.sqlite", echo=False, future=True)
    if not sqlalchemy.inspect(engine).has_table('guild'):
        Base.metadata.create_all(engine)
    return engine
