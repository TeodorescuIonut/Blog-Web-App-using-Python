from datetime import datetime
from interfaces.user_repository_interface import IUserRepository
from interfaces.database_interface import IDatabase
from models.user import User


class UserDbRepo(IUserRepository):
    users = list()
    no_users = 0

    def __init__(self, database: IDatabase):
        self.database = database

    def create(self, user: User) -> None:
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute("""INSERT INTO users (user_name, user_email, user_password, admin)
        VALUES (%s, %s, %s, %s) RETURNING user_id""",
                    (user.name, user.email, user.password, user.admin),
                    )
        user.id = cur.fetchone()[0]
        self.users.append(user)
        self.database.close_and_save(conn, cur)

    def get_all(self) -> []:
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute("""SELECT user_id,user_date_creation,
        user_date_modification, user_name, user_email, user_password, admin
        FROM users ORDER BY user_date_creation DESC""")
        rows = cur.fetchall()
        self.users.clear()
        for row in rows:
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
        self.database.close_and_save(conn, cur)
        return self.users

    def check_user_id(self, user_to_check: User) -> bool:
        if len(self.users) > 0:
            for user in self.users:
                if user_to_check.id == user.id:
                    return True
        return False

    def check_user_email(self, user_to_check: User) -> bool:
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute("""SELECT user_id,to_char(user_date_creation, 'dd/mm/yyyy HH24:MI'),
        to_char(user_date_modification, 'dd/mm/yyyy HH24:MI'), 
        user_name, user_email, user_password
        FROM users WHERE user_email = %s""", (user_to_check.email,))
        return cur.rowcount > 0

    def get_by_id(self, user_id: int) -> User:
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute("""SELECT user_id,to_char(user_date_creation, 'dd/mm/yyyy HH24:MI'), to_char(
        user_date_modification, 'dd/mm/yyyy HH24:MI'), user_name, user_email, user_password ,
        admin FROM users WHERE user_id = %s""", (user_id,))
        data = cur.fetchone()
        if data is None:
            return None
        user = User("", "", "")
        user.id = data[0]
        user.created_at = data[1]
        user.modified_at = data[2]
        user.name = data[3]
        user.email = data[4]
        user.password = data[5]
        user.admin = data[6]
        self.database.close_and_save(conn, cur)
        return user

    def update(self, user: User) -> None:
        conn = self.database.create_conn()
        cur = conn.cursor()
        id_user = user.id
        index_user = self.get_user_index(id_user)
        if index_user is not None:
            self.users.remove(self.users[index_user])
        self.users.append(user)
        user_date_modification = datetime.now().strftime("%B %d %Y %H:%M:%S")
        cur.execute("""
        UPDATE users
        SET user_name = %s,
            user_date_modification = %s,
            user_email = %s,
            user_password = %s,
            admin = %s
        WHERE user_id = %s
        """, (user.name,
              user_date_modification,
              user.email,
              user.password,
              user.admin, user.id))
        self.database.close_and_save(conn, cur)

    def delete(self, user: User) -> None:
        conn = self.database.create_conn()
        cur = conn.cursor()
        id_user = user.id
        cur.execute('DELETE FROM users WHERE user_id= %s', (id_user,))
        self.database.close_and_save(conn, cur)
        user_index = self.get_user_index(id_user)
        if user_index is not None:
            self.users.remove(self.users[user_index])

    def get_user_index(self, id_user) -> int:
        for user in self.users:
            if id_user == user.id:
                return self.users.index(user)

    def get_user_by_email(self, user_email):
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
        data = cur.fetchone()
        if data is not None:
            user = User("", "", "", "")
            user.id = data[0]
            user.created_at = data[1]
            user.modified_at = data[2]
            user.name = data[3]
            user.email = data[4]
            user.password = data[5]
            user.admin = data[6]
            self.database.close_and_save(conn, cur)
            return user
