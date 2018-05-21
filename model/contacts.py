'''
Created on May 20, 2018

@author: mac
'''
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base
from marshmallow import fields, Schema

class Contacts(Entity, Base):
    __tablename__ = 'contacts'
    contact_id = Column(Integer, primary_key=True)    
    contact_phone_num  = Column(String(12))    
    contact_country_code  = Column(String(5))
    user_id = Column(Integer)
    
    def __init__(self, contact_id, contact_phone_num, contact_country_code, user_id):
        Entity.__init__(self)
        self.contact_id = contact_id
        self.contact_phone_num = contact_phone_num
        self.contact_country_code = contact_country_code
        self.user_id = user_id
        
class ContactsSchema(Schema):
    contact_id = fields.Integer()    
    contact_phone_num  = fields.Str()    
    contact_country_code  = fields.Str()
    user_id = fields.Integer()
    create_date = fields.DateTime()
    updated_date = fields.DateTime()