import math
from flask import request
from interfaces.pagination_interface import IPagination
from models.dtos.pagination import Pagination


class Paginate(IPagination):

    def __init__(self, no_per_page=4):
        self.no_per_page = no_per_page

    def offset(self):
        page = self.current_page()
        offset = (page - 1) * self.no_per_page
        return offset

    def current_page(self):
        page = request.args.get("page", type=int, default=1)
        return page

    def get_last_page_index(self, count):
        index_page = math.ceil(count / self.no_per_page)
        return index_page

    def set_no_per_page(self, no_per_page):
        self.no_per_page = no_per_page

    def set_pagination(self, count):
        page = self.current_page()
        last_page = self.get_last_page_index(count)
        return Pagination(page,
                          self.no_per_page, count, last_page)
