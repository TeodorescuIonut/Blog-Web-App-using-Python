from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from interfaces.db_config_interface import IDatabaseConfig
from interfaces.databse_sqlalchemy_interface import IDatabaseAlchemy


class SQLAlchemyDatabase(IDatabaseAlchemy):
    def __init__(self, db_config: IDatabaseConfig):
        self.db_config = db_config

    def generate_engine(self):
        db_settings = self.db_config.load()
        engine = create_engine(
            f"""postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}/
            {db_settings.database}""",
            echo=True)
        return engine

    def generate_session(self):
        engine = self.generate_engine()
        session = sessionmaker(bind=engine)
        return session

    def create_conn(self):
        session = self.generate_session()
        return session()

    def close_and_save(self, conn):
        conn.commit()
        conn.close()
