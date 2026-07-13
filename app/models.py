from .database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,ForeignKey,Boolean
from sqlalchemy.sql.expression import null,text
from sqlalchemy.orm import relationship

class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer,primary_key=True,nullable=False)
    url = Column(String,nullable=False, unique=True)
    short_code = Column(String, nullable=True, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    expires_at  = Column(TIMESTAMP(timezone=True), nullable=True,server_default=text("now() + interval '1 year'"))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False, index=True)
    click_count = Column(Integer, nullable=False, server_default="0")
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True , nullable=False)
    username = Column(String, nullable=False, unique=True)
    email_id = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean,nullable=False,server_default="false")
    
