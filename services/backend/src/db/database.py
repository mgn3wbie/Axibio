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

    # todo : error handling
    def persist_dicts_from_model(dicts_list, cls):
        '''takes a list of dicts and persists them to the db as the objects they represent'''
        for dict_item in dicts_list:
            db_item = jsons.loads(json.dumps(dict_item), cls=cls)
            session.merge(db_item)
        session.commit()

    def persist_item(item):
        '''persist a modelled object to the db'''
        session.merge(item)
        session.commit()

    def persist_items(items):
        '''persist a list of modelled objects to the db'''
        for item in items:
            session.merge(item)
        session.commit()

    # todo : error handling
    def create_missing_tables():
        '''generates all tables in the db (doesnt recreate existing)'''
        models.Base.metadata.create_all(bind=engine)
        session.commit()
    
    def create_fake_users():
        fake_users = [
            models.User(email="julien@email.com", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", disabled=False),
            models.User(email="pirate@email.com", hashed_password="fakehashedsecret", disabled=True)
        ]
        DBManager.persist_items(fake_users)


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
