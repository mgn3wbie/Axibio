from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import models
import jsons
import json
import os
from pprint import pprint

class Manager:
    # creates db engine
    engine = create_engine(os.environ["DB_URL"])
    Session = sessionmaker(bind=engine)
    session = Session()

    def persist_items_from_model(self, items, cls):
        '''takes a list of dicts and persists them to the db as the objects they represent'''
        for item in items:
            log = jsons.loads(json.dumps(item), cls=cls)
            pprint(vars(log))
            self.session.merge(log)
        self.session.commit()

    def create_missing_tables(self):
        '''generates all tables in the db (doesnt recreate existing)'''
        models.Base.metadata.create_all(bind=self.engine)
        self.session.commit()
        return inspect(self.engine).has_table("logs")