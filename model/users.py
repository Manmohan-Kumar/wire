'''
Created on May 20, 2018

@author: mac
'''
from sqlalchemy import Column, String, Text, Integer
from .entity import Entity, Base
from marshmallow import fields, Schema
from sqlalchemy.sql.schema import UniqueConstraint

class Users(Entity, Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    contact_id = Column(Integer)
    display_name = Column(String(50))
    phone_number  = Column(String(12))
    country_phone_code  = Column(String(5))
    callback_url = Column(String(5)) 
    password = Column(String(20)) 
    telesign_api_key = Column(Text)
    telesign_customer_id = Column(Text)
    
    __table_args__ = (UniqueConstraint('phone_number', 'display_name', name='_phone_display_uc'),  )    

    def __init__(self, display_name, phone_number, country_code, callback_url=None, password='default', ts_api_key=None, ts_cust_id=None, contact_id = None):
        Entity.__init__(self)
        #self.user_id = user_id        
        self.display_name = display_name
        self.phone_number = phone_number + country_code
        self.country_phone_code = country_code
        self.callback_url = callback_url
        self.password = password
        self.telesign_api_key = ts_api_key
        self.telesign_customer_id = ts_cust_id
        self.contact_id = contact_id
        
class UserSchema (Schema):
    user_id = fields.Integer()
    contact_id = fields.Integer()
    display_name = fields.Str()
    phone_number  = fields.Str()
    country_phone_code  = fields.Str()
    callback_url = fields.Str()
    password = fields.Str()
    telesign_api_key = fields.Str()
    telesign_customer_id = fields.Str()
    create_date = fields.DateTime()
    updated_date = fields.DateTime()