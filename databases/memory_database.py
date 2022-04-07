from interfaces.database_interface import IDatabase


class MemoryDatabase(IDatabase):
    def create_conn(self):
        pass

    def create_cursor(self):
        pass
    def close_and_save(self, conn, cur):
        pass
    def create_table(self):
        pass
    