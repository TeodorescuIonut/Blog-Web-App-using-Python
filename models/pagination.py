class Pagination:
    def __init__(self,current_page,no_per_page,count,last_page) -> None:
        self.current_page = current_page
        self.no_per_page = no_per_page
        self.count = count
        self.last_page = last_page
        