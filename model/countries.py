'''
Created on May 20, 2018

@author: mac
'''
from sqlalchemy import Column, String, Text, Integer, CHAR
from .entity import Entity, Base
from marshmallow import fields, Schema

class Country(Entity, Base):
    __tablename__ = 'country'   
    id = Column(Integer, primary_key=True)
    iso = Column(CHAR(2))
    name  = Column(String(80))
    nicename  = Column(String(80))
    iso3 = Column(CHAR(3))
    numcode = Column(Integer)
    phonecode = Column(Integer)
    
    def __init__(self, id, iso, name, nicename, iso3, numcode, phonecode):
        #Entity.__init__(self)
        self.id = id        
        self.iso = iso
        self.name = name
        self.nicename = nicename
        self.iso3 = iso3
        self.numcode = numcode
        self.phonecode = phonecode
                
        
class CountrySchema (Schema):
    id = fields.Integer()
    iso = fields.Str()
    name  = fields.Str()
    nicename = fields.Str()
    iso3 = fields.Str()
    numcode  = fields.Integer()
    phonecode = fields.Integer()   
    