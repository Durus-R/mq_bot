import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


# TODO : Everything but finished.
class Guild(Base):
    __tablename__ = "guild"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    prefix = sqlalchemy.Column(sqlalchemy.String)
    losung_channel = sqlalchemy.Column(sqlalchemy.Integer)
    losung_hour = sqlalchemy.Column(sqlalchemy.Integer)


def create_sqlite_engine():
    """
    Creates a sqlalchemy engine for sqlite.
    """
    engine = create_engine("sqlite:///database.sqlite", echo=True, future=True)
    if not sqlalchemy.inspect(engine).has_table('guild'):
        Base.metadata.create_all(engine)
    return engine
