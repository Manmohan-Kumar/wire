'''
Created on May 20, 2018

@author: mac
'''
from sqlalchemy import Column, String, Text, Integer
from .entity import Entity, Base
from marshmallow import fields, Schema

class Chat(Entity, Base):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True)
    message = Column(Text)
    sender_id_fk  = Column(Integer)
    receiver_id_fk  = Column(String(5))
    
    def __init__(self, message, sender_id_fk, receiver_id_fk):
        Entity.__init__(self)
#         self.chat_id = chat_id        
        self.message = message
        self.sender_id_fk = sender_id_fk
        self.receiver_id_fk = receiver_id_fk        
        
class ChatSchema (Schema):
    chat_id = fields.Integer()
    message = fields.Str()
    phone_number  = fields.Str()
    sender_id_fk  = fields.Integer()
    receiver_id_fk = fields.Integer()    
    create_date = fields.DateTime()
    #updated_date = fields.DateTime()
