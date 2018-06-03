'''
Created on Jun 3, 2018

@author: mac
'''
from datetime import datetime, timedelta
import jwt
from passlib.hash import pbkdf2_sha256 as sha256
import json
class JWTHelper:   
    JWT_EXP_DELTA_SECONDS=120
    def encode_auth_token(self, display_name, secretkey):
        '''
        Generates auth token
        :return: string
        '''
        try:
            exp = datetime.utcnow() + timedelta(seconds=JWTHelper.JWT_EXP_DELTA_SECONDS)
            
            payload = {
                'exp': exp,
                'iat': datetime.utcnow(),
                'sub': display_name
                }
            jwt_token = jwt.encode(payload, secretkey, algorithm='HS256')
            return {'jwt_token':jwt_token.decode('UTF8'), 'expiresIn': exp.strftime("%Y-%m-%d %H:%M:%S")}
        except Exception as e:
            return e
        
    def parse_decode_auth_token(self, auth_header, secretkey):
        if auth_header:
            token = auth_header.split(" ")[1] 
            try:
                payload = jwt.decode(token, secretkey, algorithm='HS256')
                return  payload['sub']
            except jwt.ExpiredSignatureError:
                return 'INVALID'
            except jwt.InvalidTokenError:
                return 'INVALID'
        else:
            return 'Failure'   
        
    def generateHash(self, passwd):
        return sha256.hash(passwd)
    
    def verifyHash(self, passwd, hashedPasswd):
        return sha256.verify(passwd, hashedPasswd)