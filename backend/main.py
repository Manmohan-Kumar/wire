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
#from model.contacts import Contacts, ContactsSchema
from model.countries import Country, CountrySchema
import json
import base64 
from backend.mainHelper import JWTHelper




# generate database schema
#Base.metadata.create_all(engine)

app = Flask(__name__)
api = Api(app)
CORS(app)

SECRETKEY = 'qE8MkAYuNl6MGO9HRAVNiIeiYRqKxUXMIAvRczROlwuAv'
jwtUtil = JWTHelper()

# start session
session = Session()

'''
# check for existing data
users = session.query(Users).all()
print('### Users:')
for user in users:
    #print(user)
    print(f'({user.user_id}) {user.display_name} - {user.phone_number}')
''' 
    
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

@app.route("/login", methods=['POST'])
def login():
    '''
    send json post request example:
    {
      "display_name": "admin",
      "password": "123456"
    }
    fetch current user data
    '''
#     request.headers.get('Authorization').split()[1]
    req_json = request.get_json()
    displayName = req_json['display_name']
    password = req_json['password']
    # fetching from the database
    session = Session()
    user_objects = session.query(Users.user_id, Users.display_name, Users.callback_url, Users.country_phone_code, Users.create_date, Users.phone_number ).\
    filter(Users.display_name.like(displayName) & Users.password.like(password)).all()
    schema = UserSchema(many=True)
    userList = schema.dump(user_objects)
    responseObject = userList.data
    
    if(len(user_objects) > 0 and user_objects[0].display_name != ""):
        display_name_db = user_objects[0].display_name
        jwt_token = jwtUtil.encode_auth_token(display_name_db, SECRETKEY)
        responseObject = {'user': responseObject, 'message': 'SUCCESS'}
        responseObject.update(jwt_token)
        print(responseObject)    

    # serializing as JSON
    session.close()
    return json.dumps(responseObject)

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

@app.route("/register", methods=['POST'])
def register():
    '''
    Add a User
    {
      
      "display_name": "Mohit",
      "phone_number": "8427434777",
      "country_phone_code":"91",
      callback_url : "hdjkfhkdjsf",
      telesign_customer_id : "ghdkjafhjd",
      telesign_api_key : "jsdhfjkhsdfkj",
      password : "ghdfhsdj"
          }
    '''
    req_json = request.get_json()
    returnStatus = "status: User created successfully"
    session = Session()
    try:
        userJson = req_json['contact']  
        user_displayName = userJson['display_name']
        phone_Num = userJson['phone_number']
        country_phone_code = userJson['country_phone_code']
        callback_url = userJson['callback_url']
        telesign_customer_id = userJson['telesign_customer_id']
        telesign_api_key = userJson['telesign_api_key']
        password = userJson['password']
        
        newUser = Users(display_name = user_displayName, phone_number= phone_Num, country_code = country_phone_code, callback_url = callback_url, ts_cust_id=telesign_customer_id, ts_api_key= telesign_api_key, password= password)
        session.add(newUser)
        session.commit()
    except Exception as e:
        print(e)
        returnStatus = "status: Some problem while registering user, please check for duplicity"
    finally:
        returnStatus = "status: Registration successfull"
        #returnStatus = "Contact {0} added success fully".format(contact.user_id)
        session.close()    
    return json.dumps(returnStatus)

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
    #displayName = req_json['displayName']
    #phoneNum = req_json['phoneNum']
    sender_id = req_json['sender_id']    
    
    auth_header = request.headers.get('Authorization')
    sub = jwtUtil.parse_decode_auth_token(auth_header, SECRETKEY)
    if('INVALID' == sub):
        return json.dumps({'status':'Logged Out'}) 
    
    session = Session()
    u = aliased(Users)

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
    auth_header = request.headers.get('Authorization')
    sub = jwtUtil.parse_decode_auth_token(auth_header, SECRETKEY)
    
    req_json = request.get_json()
    returnStatus = {"status": "Contact added successfully"}
    session = Session()
    try:
        contactJson = req_json['contact']  
        sender_id = contactJson['sender_id']
        sender_name = contactJson['sender_name']
        con_displayName = contactJson['display_name']
        con_phone_Num = contactJson['phone_number']
        country_phone_code = contactJson['country_phone_code']
        
        if(sender_name == sub):                        
            contact = Users(display_name = con_displayName, phone_number= con_phone_Num, country_code = country_phone_code, contact_id = sender_id)
            session.add(contact)
            session.commit()
            session.refresh(contact)
    #         schema = UserSchema(many = True)
    #         contactList = schema.dump(contact)
            returnStatus.update({"contact_id": contact.user_id})
            print(contact.user_id)
        else:
            returnStatus = {"status":"FAILURE"}
    except Exception as e:
        print(e)
        returnStatus = {"status": "Some problem while adding contact, please check for duplicity"}
    finally:        
        #returnStatus = "Contact {0} added success fully".format(contact.user_id)
        session.close()    
    return  json.dumps(returnStatus)
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

@app.route("/getChatHistory", methods=['GET'])
def getChatHistory(senderId = 3, receiverId = 4):
    '''
    Fetch list of contacts for a user
    '''
    
#     req_json = request.get_json()
    senderId = request.args.get('sender_id')
    receiverId = request.args.get('receiver_id')
    
    session = Session()
    
    chat_objects = session.query(Chat).\
    filter(Chat.sender_id_fk.in_((senderId, receiverId)) & Chat.receiver_id_fk.in_((senderId,receiverId))).order_by(Chat.create_date.asc()).all()
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
          "currentUser_displayName": "Manmohan",
          "receiver_displayName": "Bala",
          "sender_phoneNum": "9023051078",
          "receiver_phoneNum": "7009600580",
          "receiver_countryPhoneCode":"91",
          "message":"Be grateful to the great Thanos."  
        }
    '''
    req_json = request.get_json()
    ''' 1    
    sender_displayName = req_json['currentUser_displayName']
    receiver_displayName = req_json['receiver_displayName']
    sender_phoneNum = req_json['sender_phoneNum']
    '''
    sender_id = req_json['sender_id']
    receiver_id = req_json['receiver_id']
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
    ''' 1
        user_objects = session.query( Users.telesign_customer_id, Users.telesign_api_key, Users.user_id ).\
        filter(Users.display_name.like(sender_displayName) & Users.phone_number.like(sender_phoneNum)).all()
    '''
    user_objects = session.query( Users.telesign_customer_id, Users.telesign_api_key, Users.user_id ).\
    filter(Users.user_id.like(sender_id)).all()


    APIkey = user_objects[0].telesign_api_key
    customerID = user_objects[0].telesign_customer_id
    ''' 2
     sender_id = user_objects[0].user_id
    '''
    
    
    '''
    3
    fetch receiver_id_fk by querying user table 
    Save message data 
    
    receiver_objects = session.query( Users.user_id ).\
    filter(Users.display_name.like(receiver_displayName) & Users.phone_number.like(receiver_phoneNum)).all()
    receiver_id = receiver_objects[0].user_id
    '''    

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

# send CORS headers
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     if request.method == 'OPTIONS':
#         response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
#         headers = request.headers.get('Access-Control-Request-Headers')
#         if headers:
#             response.headers['Access-Control-Allow-Headers'] = headers
#     return response
    
if __name__ == '__main__':
    app.run(debug=True)