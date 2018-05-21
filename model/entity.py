'''
Created on May 20, 2018
https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-apps-part-1/
https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
https://auth0.com/blog/developing-restful-apis-with-python-and-flask/

https://github.com/auth0-blog/flask-restful-apis/tree/master/cashman

@author: Manmohan
'''
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = '127.0.0.1:3306'
db_name = 'conversations'
db_user = 'Manmohan'
db_password = 'Manmohan@86'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_url}/{db_name}')

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Entity():
    #user_id = Column(Integer, primary_key=True)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    #last_updated_by = Column(String(16))

    def __init__(self):
        self.create_date = datetime.now()
        self.update_date = datetime.now()
        #self.last_updated_by = created_by
