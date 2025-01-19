from sqlalchemy import Column, Integer, BigInteger, JSON, String, Text
from sqlalchemy.orm import declarative_base
 
# all model classes must inherit from this
print('creating Base')
Base = declarative_base()

class Logs(Base):
    # postgres table name
    __tablename__ = "logs"
    
    # primary key
    id = Column(String(50), primary_key=True, index=True)
    stream_id = Column("streamId", String(50), nullable=False, index=True)
    creator_id = Column("creatorId", String(50), nullable=False, index=True)
    last_editor_id = Column("lastEditorId", String(50), nullable=False, index=True)

    metadata_ = Column("metadata", JSON, nullable=False, default={})
    # ts in ms, postgres Integers are limited to 2147483647
    creation_date = Column("creationDate", BigInteger, nullable=False, index=True)
    last_edit_date = Column("lastEditDate", BigInteger, nullable=False, index=True)
    generated_date = Column("generatedDate", BigInteger, nullable=False, index=True)

    tags = Column(JSON, nullable=False, default={})
    elems = Column(JSON, nullable=False, default={})

    # optional values
    location = Column(Text, nullable=True)
    hash = Column(Text, nullable=True)
    path = Column(Text, nullable=True)
