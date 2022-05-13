from interfaces.post_repository_interface import IPostRepository
from interfaces.user_repository_interface import IUserRepository
from interfaces.user_statistics_interface import IUserStatistics
from models.dtos.data_statistics import DataStatistics


class UserStatistics(IUserStatistics):

    def __init__(self, post_repo: IPostRepository, user_repo: IUserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get(self):
        per_page = None
        offset = 0
        users = self.user_repo.get_all()
        datas = []
        for user in users:
            posts_per_user = self.post_repo.get_all(per_page, offset, user.id)
            count = 0
            for post in posts_per_user:
                date = post.created_at.strftime(
                        "%B") + '-' + post.created_at.strftime("%Y")
                if any(data.user_name == user.name and data.date == date for data in datas) is False:
                    count = 0
                    datas.append(DataStatistics(user.name, date, count))
                count += 1
                self.__update_count(count, datas, user.name, date)
        return datas

    def __update_count(self, count, datas, user, date):
        for data in datas:
            if data.user_name == user and data.date == date:
                data.count = count
