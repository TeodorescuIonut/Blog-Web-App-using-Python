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
                "INSERT INTO users (user_name, user_email, user_password) VALUES (%s, %s, %s) RETURNING user_id",
                (user.user_name, user.user_email, user.user_password),
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
            if self.check_user_exists(user) is False:
                self.users.append(user)
        self.db.close_and_save(conn, cur)
        return self.users

    def check_user_exists(self,user_to_check:User)-> bool:
        if len(self.users) > 0:
            for user in self.users:
                if user_to_check.user_id == user.user_id:
                    return True
        return False
        


    def get_by_id(self, user_id:int) -> User:
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        data = cur.fetchall()[0]
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
        self.users.remove(self.users[index_user])
        self.users.append(user)      
        cur.execute("""
        UPDATE users
        SET user_name = %s,
            user_email = %s,
            user_password = %s
        WHERE user_id = %s RETURNING *
        """,(user.user_name, user.user_email, user.user_password, user.user_id))
        self.db.close_and_save(conn, cur)
        
        
        
    
    def delete(self, user:User) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor()
        id = user.user_id 
        cur.execute('DELETE FROM users WHERE user_id= %s', (id,)) 
        self.db.close_and_save(conn, cur)
        user_index = self.get_user_index(id)
        self.users.remove(self.users[user_index])


    def get_user_index(self, id: int)-> int:
        for user in self.users:
            if user.user_id == id:
                return self.users.index(user)
    
