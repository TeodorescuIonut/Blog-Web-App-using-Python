from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, VARCHAR
from sqlalchemy.orm import declarative_base, column_property

Base = declarative_base()


class PostSQLAlchemy(Base):
    __tablename__ = 'posts'
    post_id = Column("post_id", Integer, primary_key=True)
    post_title = Column("post_title", VARCHAR(255))
    post_contents = Column("post_content", VARCHAR)
    post_date_creation = Column("post_created_on", TIMESTAMP)
    post_date_modification = Column("post_modified_on", TIMESTAMP)
    owner_id = Column("owner_id", Integer, ForeignKey("users.user_id"))
