from typing import List
from typing import Optional, Dict, Any
from sqlalchemy import BigInteger, JSON, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from db_manager import Base

class Logs(Base):
    # postgres table name
    __tablename__ = "logs"
    
    # primary key
    # id -> object attribute representing a table column
    # Mapped[int] -> SQLAlchemy specific, maps the attribute to a column + defining the attribute type
    # mapped_column -> column specifications
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)    
    
    # id in octave api
    octave_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    stream_id: Mapped[str] = mapped_column(String(50), nullable=False)
    creator_id: Mapped[str] = mapped_column(String(50), nullable=False)
    last_editor_id: Mapped[str] = mapped_column(String(50), nullable=False)

    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default={})
    # ts in ms, postgres Integers are limited to 2147483647
    creation_date: Mapped[int] = mapped_column(BigInteger, nullable=False)
    last_edit_date: Mapped[int] = mapped_column(BigInteger, nullable=False)
    generated_date: Mapped[int] = mapped_column(BigInteger, nullable=False)

    tags: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default={})
    elems: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default={})
    # optional values
    location: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hash: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<EventLog(id={self.id}, octave_id={self.octave_id})>"