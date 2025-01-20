from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import src.db.models as models
import jsons
import json
import os

# creates db engine
engine = create_engine(os.environ["DB_URL"])
# creates session
Session = sessionmaker(bind=engine)
session = Session()

class DBManager:

    # ---------------------- table creation ----------------------
    # todo : error handling
    def create_missing_tables():
        '''generates all tables in the db (doesnt recreate existing)'''
        models.Base.metadata.create_all(bind=engine)
        session.commit()

    # ---------------------- creation ----------------------
    # todo : error handling
    def add_or_update_dicts_from_model_with_ids(dicts_list, cls):
        '''takes a list of dicts and persists them to the db as the objects they represent'''
        for dict_item in dicts_list:
            db_item = jsons.loads(json.dumps(dict_item), cls=cls)
            session.merge(db_item)
        session.commit()

    def add_new_item(item):
        '''persist a modelled object to the db'''
        session.add(item)
        session.commit()

    def add_items_if_not_existing(items, condition_column):
        '''persist a list of modelled objects to the db if they don't already exist'''
        for item in items:
            DBManager.add_item_if_doesnt_exist(item, condition_column)

    def add_item_if_doesnt_exist(item, condition_column):
        '''persist a modelled object to the db if it doesn't already exist'''
        query = select(item.__class__).where(getattr(item.__class__, condition_column) == item.__dict__[condition_column])
        result = session.execute(query).first()
        if result is None:
            session.add(item)
            session.commit()

    # ---------------------- read ----------------------
    GAIAPASS = "gaiapass"
    EVENTLOG = "eventlog"
    # todo : error handling
    def get_all_events_with_name(event_name):
        query = select(models.Logs.id, models.Logs.elems).where(models.Logs.elems[DBManager.GAIAPASS][DBManager.EVENTLOG].has_key(event_name))
        results = session.execute(query).fetchall()
        return results

    def get_user_for_email(user_email) -> models.User:
        query = select(models.User).where(models.User.email == user_email)
        result = session.execute(query).first()
        return result[0] if result else None

    # ---------------------- update ----------------------
    def update_item_with_id(item):
        '''update a modelled object in the db'''
        session.merge(item)
        session.commit()

    def update_items_with_ids(items):
        '''update modelled objects in the db'''
        for item in items:
            session.merge(item)
        session.commit()
