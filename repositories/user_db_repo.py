from datetime import datetime
import sys
import os
from pathlib import Path

from interfaces.user_repository_interface import IUserRepository


myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from models.user import User
from interfaces.database_interface import IDatabase

class UserDbRepo(IUserRepository):
    users = list()
    def __init__(self, db:IDatabase):
        self.db = db
    def create(self, user:User) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor()
        cur.execute(
                "INSERT INTO users (user_name, user_email, user_password, admin) VALUES (%s, %s, %s, %s) RETURNING user_id",
                (user.user_name, user.user_email, user.user_password, False),
            )
        user.user_id = cur.fetchone()[0]
        self.users.append(user)
        self.db.close_and_save(conn,cur)


    def get_all(self) -> list():
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute("SELECT user_id,user_date_creation,user_date_modification, user_name, user_email, user_password  FROM users ORDER BY user_date_creation DESC")
        rows = cur.fetchall()
        for row in rows:
            user =User("", "", "")
            user.user_id = row[0]
            user.user_date_creation = row[1]
            user.user_date_modification = row[2]
            user.user_name= row[3]
            user.user_email= row[4]
            user.user_password= row[5]
            if self.check_user_id(user) is False:
                self.users.append(user)
        self.db.close_and_save(conn, cur)
        return self.users


    def check_user_id(self,user_to_check:User)-> bool:
        if len(self.users) > 0:
            for user in self.users:
                if user_to_check.user_id == user.user_id:
                    return True
        return False
    def check_user_email(self,user_to_check:User)-> bool:
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute("SELECT user_id,to_char(user_date_creation, 'dd/mm/yyyy HH24:MI'),to_char(user_date_modification, 'dd/mm/yyyy HH24:MI'), user_name, user_email, user_password FROM users WHERE user_email = %s", (user_to_check.user_email,))
        return cur.rowcount > 0
    def get_by_id(self, user_id:int) -> User:
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute("SELECT user_id,to_char(user_date_creation, 'dd/mm/yyyy HH24:MI'),to_char(user_date_modification, 'dd/mm/yyyy HH24:MI'), user_name, user_email, user_password FROM users WHERE user_id = %s", (user_id,))
        data = cur.fetchone()
        if data is None:
            return None
        user =User("", "", "")
        user.user_id = data[0]
        user.user_date_creation = data[1]
        user.user_date_modification = data[2]
        user.user_name= data[3]
        user.user_email= data[4]
        user.user_password= data[5]
        self.db.close_and_save(conn, cur)
        return user
    def update(self, user:User) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor() 
        id = user.user_id
        index_user = self.get_user_index(id)
        if index_user is not None:
            self.users.remove(self.users[user_index])
        self.users.append(user) 
        user_date_modification = datetime.now().strftime("%B %d %Y %H:%M:%S")     
        cur.execute("""
        UPDATE users
        SET user_name = %s,
            user_date_modification = %s,
            user_email = %s,
            user_password = %s
        WHERE user_id = %s
        """,(user.user_name,user_date_modification, user.user_email,user.user_password, user.user_id))
        self.db.close_and_save(conn, cur)
        
    def delete(self, user:User) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor()
        id = user.user_id 
        cur.execute('DELETE FROM users WHERE user_id= %s', (id,)) 
        cur.execute('DELETE FROM posts WHERE owner_id= %s', (id,))
        self.db.close_and_save(conn, cur)
        user_index = self.get_user_index(id)
        if user_index is not None:
            self.users.remove(self.users[user_index])


    def get_user_index(self, id)-> int:
        for user in self.users:
            if id == user.user_id:
                return self.users.index(user)
    
    def get_user_by_email(self, user_email):
        conn = self.db.create_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
        data = cur.fetchone()
        if data is not None:
            user =User("", "", "", "")
            user.user_id = data[0]
            user.user_date_creation = data[1]
            user.user_date_modification = data[2]
            user.user_name= data[3]
            user.user_email= data[4]
            user.user_password= data[5]
            user.admin = data[6]
            self.db.close_and_save(conn, cur)
            return user