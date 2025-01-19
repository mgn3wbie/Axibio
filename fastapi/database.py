from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import models
import jsons
import json
import os

class Manager:
    # creates db engine
    engine = create_engine(os.environ["DB_URL"])
    # creates session
    Session = sessionmaker(bind=engine)
    session = Session()

    # todo : error handling
    def persist_items_from_model(self, items, cls):
        '''takes a list of dicts and persists them to the db as the objects they represent'''
        for item in items:
            log = jsons.loads(json.dumps(item), cls=cls)
            self.session.merge(log)
        self.session.commit()

    # todo : error handling
    def create_missing_tables(self):
        '''generates all tables in the db (doesnt recreate existing)'''
        models.Base.metadata.create_all(bind=self.engine)
        self.session.commit()
    
    GAIAPASS = "gaiapass"
    EVENTLOG = "eventlog"
    # todo : error handling
    def get_all_events_with_name(self, event_name):
        query = select(models.Logs.id, models.Logs.elems).where(models.Logs.elems[self.GAIAPASS][self.EVENTLOG].has_key(event_name))
        results = self.session.execute(query).fetchall()
        return results
