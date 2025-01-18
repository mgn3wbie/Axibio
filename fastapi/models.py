from sqlalchemy import Column, Integer, BigInteger, JSON, String, Text
from sqlalchemy.orm import declarative_base
 
# all model classes must inherit from this
print('creating Base')
Base = declarative_base()

class Logs(Base):
    # postgres table name
    __tablename__ = "logs"
    
    # primary key
    id = Column(Integer, primary_key=True, index=True)    
    
    # id in octave api
    octave_id = Column(String(50), unique=True, nullable=False)
    stream_id = Column(String(50), nullable=False)
    creator_id = Column(String(50), nullable=False)
    last_editor_id = Column(String(50), nullable=False)

    metadata_ = Column("metadata", JSON, nullable=False, default={})
    # ts in ms, postgres Integers are limited to 2147483647
    creation_date = Column(BigInteger, nullable=False)
    last_edit_date = Column(BigInteger, nullable=False)
    generated_date = Column(BigInteger, nullable=False)

    tags = Column(JSON, nullable=False, default={})
    elems = Column(JSON, nullable=False, default={})
    # optional values
    location = Column(Text, nullable=True)
    hash = Column(Text, nullable=True)
    path = Column(Text, nullable=True)
