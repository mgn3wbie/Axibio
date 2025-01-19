from sqlalchemy import Column, Integer, BigInteger, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import declarative_base
 
# all model classes must inherit from this
Base = declarative_base()

# the models act as table schema and allow to map python objects to tables and vice-versa

class Logs(Base):
    # postgres table name
    __tablename__ = "logs"
    
    # primary key
    id = Column(String(50), primary_key=True, index=True)
    stream_id = Column("streamId", String(50), nullable=False, index=True)
    creator_id = Column("creatorId", String(50), nullable=False, index=True)
    last_editor_id = Column("lastEditorId", String(50), nullable=False, index=True)

    metadata_ = Column("metadata", JSONB, nullable=False, default={})
    # ts in ms, postgres Integers are limited to 2147483647
    creation_date = Column("creationDate", BigInteger, nullable=False, index=True)
    last_edit_date = Column("lastEditDate", BigInteger, nullable=False, index=True)
    generated_date = Column("generatedDate", BigInteger, nullable=False, index=True)

    tags = Column(JSONB, nullable=False, default={})
    elems = Column(JSONB, nullable=False, default={}, index= True)

    # optional values
    location = Column(Text, nullable=True)
    hash = Column(Text, nullable=True)
    path = Column(Text, nullable=True)

class Event(Base):
    # postgres table name
    __tablename__ = "journal"

    id = Column("id", String(50), primary_key=True, index=True)
    name = Column("name", String(50), nullable=False, index=True)
    seq = Column("seq", Integer, nullable=False, index=True)
    ts = Column("ts", TIMESTAMP(timezone=True), nullable=False, index=True)
    # storing floating numbers as int to avoid losing precision
    temp = Column("temp", Integer, nullable=True, index=True)
    bat_ws = Column("batWs", Integer, nullable=True, index=True)
    reg_ws = Column("regWs", Integer, nullable=True, index=True)
    volts = Column("volts", Integer, nullable=True, index=True)
    period = Column("period", Integer, nullable=True, index=True)