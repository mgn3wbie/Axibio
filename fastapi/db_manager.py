from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

# all model classes must inherit from this
class Base(DeclarativeBase):
    pass

# creates db engine
# todo : find a way to pass this from docker env or secret var
engine = create_engine("postgresql://julien:a_complex_password@postgres/octave")

# generates all tables in the db (doesnt recreate existing)
def create_missing_db_elements():
    Base.metadata.create_all(engine)