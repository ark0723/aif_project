from sqlalchemy.orm import relationship, as_declarative
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    SmallInteger,
    CheckConstraint,
    Boolean,
)
from datetime import datetime, timedelta
from database import Base
import uuid


# Base class override
@as_declarative()
class Base:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    __name__: str


class User(Base):
    __tablename__ = "member_member"

    member_id = Column(Integer, primary_key=True, index=True)
    member_email = Column(String(length=100), nullable=False, index=True)
    member_password = Column(String(255), nullable=True)
    img_uuid = Column(String(36), default=str(uuid.uuid4()))
    img_generate_count = Column(SmallInteger, default=0)
    auth_group = Column(String(10), default="general")
    is_admin = Column(Boolean, default=False)
    mem_waiting = Column(Boolean, default=False)
    mem_number = Column(String(20), nullable=True)

    # define a checkconstraint for generating_count column
    # __table_args__ = (
    #     CheckConstraint("img_generate_count <=2", name="max_count_constraint"),
    # )
    def __repr__(self):
        return f"<Member(member_email='{self.member_email}', is_admin={self.is_admin})>"


class Image(Base):
    __tablename__ = "member_image"
    img_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member_member.member_id"))
    img_url = Column(String(length=255))
    keyword_input = Column(Text)
    generating_count = Column(SmallInteger, default=0)
    style_code = Column(String(length=20))
    expiration_date = Column(DateTime, default=datetime.now() + timedelta(days=7))

    # User table 참조: Image 객체(예: img)에서 연결된 user의 id를 참조할수 있음 -> img.member.member_id
    # User에 해당하는 객체가 user일떄: user.images -> user가 만든 이미지들을 참조할수 있음
    member = relationship("User", backref="images")
