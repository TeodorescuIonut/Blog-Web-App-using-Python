from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, Boolean
from models.post_sqlalchemy import Base


class UserSQLAlchemy(Base):
    __tablename__ = "users"
    user_id = Column("user_id", Integer, primary_key=True)
    user_name = Column("user_name", VARCHAR(255))
    user_email = Column("user_email", VARCHAR(255))
    user_password = Column("user_password", VARCHAR(255))
    user_date_creation = Column("user_date_creation", TIMESTAMP)
    user_date_modification = Column("user_date_modification", TIMESTAMP)
    admin = Column("admin", Boolean)
