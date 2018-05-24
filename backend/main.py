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

@app.route("/getCurrentUser", methods=['POST'])
def getCurrentUser():
    '''
    send json post request example:
    {
      "displayName": "Manmohan",
      "phoneNum": "9023051078"
    }
    fetch current user data
    '''    
    #     displayName = request.args.get('displayName')
    #     phoneNum = request.args.get('phoneNum')

    req_json = request.get_json()
    displayName = req_json['displayName']
    phoneNum = req_json['phoneNum']
    # fetching from the database
    session = Session()
    user_objects = session.query(Users.user_id, Users.display_name, Users.callback_url, Users.country_phone_code, Users.create_date, Users.phone_number ).\
    filter(Users.display_name.like(displayName) & Users.phone_number.like(phoneNum)).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    userList = schema.dump(user_objects)

    # serializing as JSON
    session.close()
    return json.dumps(userList.data)

@app.route("/getContacts", methods=['POST'])
def getContacts(displayName = 'Krishna', phoneNum = '8427434777'):
    '''
    Fetch list of contacts for a user
    {
      "displayName": "Manmohan",
      "phoneNum": "9023051078",
      "user_id": "4"
    }
    '''
    req_json = request.get_json()
    displayName = req_json['displayName']
    phoneNum = req_json['phoneNum']
    sender_id = req_json['sender_id']
    
    session = Session()
    u = aliased(Users)
    '''
    uAlias = aliased(Users)
    cAlias = aliased(Contacts)

    contact_objects = session.query(cAlias.contact_country_code,cAlias.contact_phone_num,  cAlias.update_date).\
    join(uAlias, (cAlias.user_id == uAlias.user_id)).\
    filter(uAlias.display_name.like(displayName) & uAlias.phone_number.like(phoneNum) ).all()
    '''
    contact_objects = session.query(u.user_id, u.display_name, u.callback_url, u.country_phone_code, u.create_date, u.phone_number).\
    filter(u.contact_id == sender_id).all()
    schema = UserSchema(many = True)
    contactList = schema.dump(contact_objects)
    
    session.close()
    return json.dumps(contactList.data)

@app.route("/addContact", methods=['POST'])
def addContact():
    '''
    Add a contact
    {
      "sender_id": "4",
      "displayName": "Mohit",
      "phoneNum": "8427434777",
      "countryPhoneCode":"91"  
    }
    '''
    req_json = request.get_json()
    sender_id = req_json['sender_id']
    con_displayName = req_json['displayName']
    con_phone_Num = req_json['phoneNum']
    country_phone_code = req_json['country_phone_code']
    session = Session()
    contact = Users(display_name = con_displayName, phone_number= con_phone_Num, country_code = country_phone_code, contact_id = sender_id)
    session.add(contact)
    session.commit()
    session.close()    
    return  "Contact added Successfully"
'''
#    with session.begin(nested=True):            
    contact=session.query(Users).\
    filter(Users.display_name.like(con_displayName) & Users.phone_number.like(con_phone_Num)).first()
    if not contact:
#            try:
        contact = Users(display_name = con_displayName, phone_number= con_phone_Num, country_code = country_phone_code)
        session.add(contact)
        session.commit()
        session.begin(subtransactions=True)
        receiver_id = contact.user_id                
        empty_chat = Chat (message = None, sender_id_fk = sender_id, receiver_id_fk = receiver_id) 
        session.add(empty_chat)
        session.commit()
#                session.close()
        return "Contact added Successfully"
#           except:
#              pass
#         finally:
#            session.close_all()
    else:
        return "Contact already exists"
'''

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

@app.route("/send-message", methods=['POST'])
def sendMessage():
    
    '''
    example post request:
        {
          "displayName": "Manmohan",
          "phoneNum": "9023051078",
          "countryPhoneCode":"91",
          "message":"Be grateful to the great Thanos."  
        }
    '''

    req_json = request.get_json()
    sender_displayName = req_json['currentUser_displayName']
    receiver_displayName = req_json['receiver_displayName']
    sender_phoneNum = req_json['sender_phoneNum']
    receiver_countryPhoneCode = req_json['receiver_countryPhoneCode']
    receiver_phoneNum = req_json['receiver_phoneNum']
    message = req_json['message']
    '''
    1. Hit the user table get customerId API key
    2. send the sms
    3. save message in chat table with sender and receiver
    4. optional: do a getrequest to check whether user has received the message    
    '''
    # fetching from the database
    session = Session()
    user_objects = session.query( Users.telesign_customer_id, Users.telesign_api_key, Users.user_id ).\
    filter(Users.display_name.like(sender_displayName) & Users.phone_number.like(sender_phoneNum)).all()


    APIkey = user_objects[0].telesign_api_key
    customerID = user_objects[0].telesign_customer_id
    sender_id = user_objects[0].user_id
    
    
    '''
    fetch receiver_id_fk by querying user table 
    Save message data 
    '''
    receiver_objects = session.query( Users.user_id ).\
    filter(Users.display_name.like(receiver_displayName) & Users.phone_number.like(receiver_phoneNum)).all()
    receiver_id = receiver_objects[0].user_id

    iMessage = Chat (message = message, sender_id_fk = sender_id, receiver_id_fk = receiver_id) 
    
    session.add(iMessage)
    session.commit()

    # serializing as JSON
    session.close()
    #customerID = '0E09D1B5-86CB-4E89-828E-CA61C850BA06'
    #APIkey = 'M4hajYKMhoXrFnXsg84yMm+FeeSU8Jjoi3JMZVOiMysXXpPvnBv+pxNTss++zrobMxGSc8lcN8ib4elemPPBHw=='
    url = 'https://rest-ww.telesign.com/v1/messaging'
    #phoneNumber = '919023051078'
    #message = 'Hi I want to order pepperoni pizza'
    messagetype = 'ARN'
    
    data= {'phone_number':receiver_countryPhoneCode + receiver_phoneNum, 'message':message, 'message_type':messagetype}
    
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
    
# class Employees(Resource):
#     def get(self):        
#         # fetching from the database
#         session = Session()
#         user_objects = session.query(Users).all()
#     
#         # transforming into JSON-serializable objects
#         schema = UserSchema(many=True)
#         userList = schema.dump(user_objects)
#     
#         # serializing as JSON
#         session.close()
#         return json.dumps(userList.data)
# 
# api.add_resource(Employees, '/employees') # Route_1
# 
# @app.route('/form-example', methods=['POST']) #allow both GET and POST requests
# def form_example():
#     req_data = request.get_json()
#     language = req_data['language']
#     framework = req_data['framework']
#     python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
#     example = req_data['examples'][0] #an index is needed because of the array
#     boolean_test = req_data['boolean_test']
# 
#     return '''
#            The language value is: {}
#            The framework value is: {}
#            The Python version is: {}
#            The item at index 0 in the example list is: {}
#            The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)
    # addContact
    # 
    
if __name__ == '__main__':
    app.run()