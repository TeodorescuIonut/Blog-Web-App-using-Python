from datetime import datetime
from sqlalchemy import desc, insert, update, delete
from interfaces.databse_sqlalchemy_interface import IDatabaseAlchemy
from interfaces.user_repository_interface import IUserRepository
from models.dtos.user import User
from models.data_models.user_sqlalchemy import UserSQLAlchemy


class SQLAlchemyUserRepo(IUserRepository):
    users = list()

    def __init__(self, database: IDatabaseAlchemy):
        self.database = database

    def get_all(self):
        conn = self.database.create_conn()
        res = conn.query(UserSQLAlchemy.user_id,
                         UserSQLAlchemy.user_date_creation,
                         UserSQLAlchemy.user_date_modification,
                         UserSQLAlchemy.user_name,
                         UserSQLAlchemy.user_email,
                         UserSQLAlchemy.user_password,
                         UserSQLAlchemy.admin). \
            order_by(desc(UserSQLAlchemy.user_date_creation)).all()
        self.users.clear()
        for row in res:
            user = User("", "", "")
            user.id = row[0]
            user.created_at = row[1]
            user.modified_at = row[2]
            user.name = row[3]
            user.email = row[4]
            user.password = row[5]
            user.admin = row[6]
            if self.check_user_id(user) is False:
                self.users.append(user)
        self.database.close_and_save(conn)
        return self.users

    def check_user_id(self, user_to_check: User) -> bool:
        if len(self.users) > 0:
            for user in self.users:
                if user_to_check.id == user.id:
                    return True
        return False

    def get_by_id(self, user_id):
        conn = self.database.create_conn()
        res = conn.query(UserSQLAlchemy).filter(UserSQLAlchemy.user_id == user_id).first()
        if res is None:
            return None
        user = User(res.user_name, res.user_email, res.user_password, res.admin, res.user_id)
        user.modified_at = res.user_date_modification
        self.database.close_and_save(conn)
        return user

    def create(self, user: User):
        conn = self.database.create_conn()
        users_table = UserSQLAlchemy.__table__
        stmt = (insert(users_table).values(user_name=user.name,
                                           user_email=user.email,
                                           user_password=user.password,
                                           admin=user.admin).returning(users_table.c.user_id))
        res = conn.execute(stmt).first()[0]
        user.id = res
        self.database.close_and_save(conn)

    def update(self, user: User):
        conn = self.database.create_conn()
        users_table = UserSQLAlchemy.__table__
        user_date_modification = datetime.now().strftime("%B %d %Y %H:%M:%S")
        stmt = (update(users_table).where(users_table.c.user_id == user.id).
                values(user_name=user.name,
                       user_date_modification=user_date_modification,
                       user_email=user.email,
                       user_password=user.password,
                       admin=user.admin))
        conn.execute(stmt)
        self.database.close_and_save(conn)

    def delete(self, user):
        conn = self.database.create_conn()
        users_table = UserSQLAlchemy.__table__
        stmt = (delete(users_table).where(users_table.c.user_id == user.id))
        conn.execute(stmt)
        self.database.close_and_save(conn)

    def get_user_by_email(self, user_email):
        conn = self.database.create_conn()
        res = conn.query(UserSQLAlchemy).filter(UserSQLAlchemy.user_email == user_email).first()
        user = None
        if res is not None:
            user = User(res.user_name, res.user_email, res.user_password, res.admin, res.user_id)
        self.database.close_and_save(conn)
        return user

    def check_user_email(self, user_to_check) -> bool:
        conn = self.database.create_conn()
        res = conn.query(UserSQLAlchemy). \
            filter(UserSQLAlchemy.user_email == user_to_check.email).first()
        self.database.close_and_save(conn)
        if res is not None:
            return True
