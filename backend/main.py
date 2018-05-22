'''
Created on May 20, 2018

@author: mac
'''
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from sqlalchemy.orm.util import aliased
from requests import post
from model.entity import Session, engine, Base
from model.users import Users, UserSchema
from model.chat import Chat, ChatSchema
from model.contacts import Contacts, ContactsSchema
from model.countries import Country, CountrySchema
import json
import base64 




# generate database schema
#Base.metadata.create_all(engine)

app = Flask(__name__)
api = Api(app)
CORS(app)

# start session
session = Session()

# check for existing data
users = session.query(Users).all()
print('### Users:')
for user in users:
    #print(user)
    print('({user.user_id}) {user.display_name} - {user.phone_number}')
    
    
@app.route("/fetchUsers")
def fetchUsers():
    '''
    fetch all users data
    '''
    # fetching from the database
    session = Session()
    user_objects = session.query(Users).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    userList = schema.dump(user_objects)

    # serializing as JSON
    session.close()
    return json.dumps(userList.data)

@app.route("/getContacts")
def getContacts(displayName = 'Krishna', phoneNum = '8427434777'):
    '''
    Fetch list of contacts for a user
    '''
    session = Session()
    uAlias = aliased(Users)
    cAlias = aliased(Contacts)
    contact_objects = session.query(cAlias.contact_country_code,cAlias.contact_phone_num,  cAlias.update_date).\
    join(uAlias, (cAlias.user_id == uAlias.user_id)).\
    filter(uAlias.display_name.like(displayName) & uAlias.phone_number.like(phoneNum) ).all()
    
    schema = ContactsSchema(many = True)
    contactList = schema.dump(contact_objects)
    
    session.close()
    return json.dumps(contactList.data)

@app.route("/getChatHistory")
def getChatHistory(senderId = 3, receiverId = 4):
    '''
    Fetch list of contacts for a user
    '''
    session = Session()
    
    chat_objects = session.query(Chat).\
    filter(Chat.sender_id_fk.in_((senderId, receiverId)) & Chat.receiver_id_fk.in_((senderId,receiverId))).all()
    schema = ChatSchema(many = True)
    chatList = schema.dump(chat_objects)
    
    session.close()
    return json.dumps(chatList.data)
    
@app.route("/getCountries")
def getCountries():
    '''
    fetch all country data
    '''
    # fetching from the database
    session = Session()
    country_objects = session.query(Country).all()

    # transforming into JSON-serializable objects
    schema = CountrySchema(many=True)
    countryList = schema.dump(country_objects)

    # serializing as JSON
    session.close()
    return json.dumps(countryList.data)

@app.route("/send-message")
def sendMessage(displayName, phoneNum, message):
    '''
    1. Hit the user table get customerId API key
    2. send the sms
    3. save message in chat table with sender and receiver
    4. optional: do a getrequest to check whether user has received the message    
    '''
    customerID = 'ddhgkjdfhgkjdf'
    APIkey = 'hfksjdfhksjdhfks'
    url = 'https://rest-ww.telesign.com/v1/messaging'
    #phoneNumber = '919023051078'
    message = 'Hi I want to order pepperoni pizza'
    messagetype = 'ARN'
    
    data= {'phone_number':phoneNum, 'message':message, 'message_type':messagetype}
    
    encode = (customerID + ':' + APIkey).encode('utf-8')
    b64encoded = base64.urlsafe_b64encode(encode).decode('ascii')
    header = {'Authorization' : 'Basic ' + b64encoded}
    
    response = post(url, data=data, headers=header)
    jsonResponse = json.loads(response.content)
    print(jsonify(jsonResponse))
    
    '''
    json to be returned having
    Message-sent: yes
    Timestamp : dd-mm-yy hh:mm
    Error: only if there is some error otherwise empty
    
    In DB save:
    message
    from phone
    To phone
    Timestamp    
    '''
    return jsonify(jsonResponse)
    
class Employees(Resource):
    def get(self):        
        # fetching from the database
        session = Session()
        user_objects = session.query(Users).all()
    
        # transforming into JSON-serializable objects
        schema = UserSchema(many=True)
        userList = schema.dump(user_objects)
    
        # serializing as JSON
        session.close()
        return json.dumps(userList.data)

api.add_resource(Employees, '/employees') # Route_1

    
    
if __name__ == '__main__':
    app.run()