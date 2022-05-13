from flask import request
from interfaces.filtering_interface import IFiltering
from interfaces.user_repository_interface import IUserRepository
from models.dtos.filter import Filter


class Filtering(IFiltering):
    def __init__(self, users_repo: IUserRepository):
        self.repo = users_repo
        self.selected_owner_id = 0

    def get_owner_id(self) -> int:
        self.selected_owner_id = request.args.get('selected_owner_id')
        if self.selected_owner_id is None:
            self.selected_owner_id = -1
        return int(self.selected_owner_id)

    def return_filter(self):
        owner_id = self.get_owner_id()
        owners = self.repo.get_all()
        return Filter(owner_id, owners)
