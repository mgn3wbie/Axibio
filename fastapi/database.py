from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import os

class Manager:
    # creates db engine
    engine = create_engine(os.environ["DB_URL"])

    def _get_connection(self):
        print("Attempting to connect to db")
        try:
            db_connection = self.engine.connect()
            print("Connection succeeded !")
        except Exception as e:
            print("Connection failed : " + str(e))
        return db_connection


    # generates all tables in the db (doesnt recreate existing)
    def create_missing_tables(self):
        connection = self._get_connection()
        models.Base.metadata.create_all(bind=connection)

        connection.commit()
        # return inspect(connection).has_table("logs")

    # def has_table_logs(self):
    #     connection = self._get_connection()