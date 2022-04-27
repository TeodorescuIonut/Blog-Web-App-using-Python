import datetime
from interfaces.post_repository_interface import IPostRepository
from interfaces.user_repository_interface import IUserRepository
from interfaces.user_statistics_interface import IUserStatistics
from models.data_statistics import DataStatistics
from repositories.sql_alchemy_post_repo import SQLAlchemyPostRepo


class UserStatistics(IUserStatistics):

    def __init__(self, post_repo: IPostRepository, user_repo: IUserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get_statistics(self):
        per_page = 'ALL'
        if isinstance(self.post_repo, SQLAlchemyPostRepo):
            per_page = None
        offset = 0
        users = self.user_repo.get_all()
        datas = []
        for user in users:
            posts_per_user = self.post_repo.get_all(per_page, offset, user.user_id)
            count = 0
            for post in posts_per_user:
                if post.post_owner == user.user_name:
                    if type(post.post_date_creation) is str:
                        post.post_date_creation = datetime.datetime.strptime(post.post_date_creation, '%B %d %Y %H:%M:%S')
                    date = post.post_date_creation.strftime(
                        "%B") + '-' + post.post_date_creation.strftime("%Y")
                    if any(data.user_name == user.user_name and data.date == date for data in datas) is False:
                        count = 0
                        datas.append(DataStatistics(user.user_name, date, count))
                    count += 1
                self.__update_count(count, datas, user.user_name, date)
        return datas

    def __update_count(self, count, datas, user, date):
        for data in datas:
            if data.user_name == user and data.date == date:
                data.count = count
