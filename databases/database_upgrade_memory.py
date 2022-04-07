from interfaces.database_upgrade_interface import IDatabaseUpgrade


class MemoryDBUpgrade(IDatabaseUpgrade):
    def upgrade_db(self):
        pass

    def is_latest_db_version(self):
        pass
