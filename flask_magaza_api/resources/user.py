import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.user import UserModel
from blocklist import BLOCKLIST

# _ ile adlandırma private değişken olduğunun göstergesidir.
_user_parser = reqparse.RequestParser()

_user_parser.add_argument('username',
    type = str,
    required = True,
    help = "Bu alan bos birakilamaz!"
)

_user_parser.add_argument('password',
    type = str,
    required = True,
    help = "Bu alan bos birakilamaz!"
)

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'Bir kullanici bu ismi zaten kullaniyor.'}, 400
        
        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "Kullanici basariyla kaydedildi."}, 201

    """
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'Bir kullanici bu ismi zaten kullaniyor.'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        # id değeri otomatik artmaktadır. (bkz. create_tables.py)
        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "Kullanici basariyla kaydedildi."}, 201
    """


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'Kullanici Bulanamadi.'}, 404 
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'Kullanici Bulanamadi.'}, 404 
        user.delete_from_db()
        return {'message': 'Kullanici Silindi.'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # Parser(Ayrıştırıcı) üzerinden veri alacak
        data = _user_parser.parse_args()

        # Kullanıcıyı veri tabanında bulacak
        user = UserModel.find_by_username(data['username'])

        # Password kontrolü (authentication() metodunun yaptığı işlem)
        if user and safe_str_cmp(user.password, data['password']):
            # identity() metodunun yaptığı işlem
            access_token = create_access_token(identity = user.id, fresh = True) # fresh = tokenize refreshing ile alakalı.
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Gecersiz Kimlik Bilgileri'}

        # Erişim token'ı oluşturacak
        # Yenileme token'ı oluşturacak (Bakılacak)


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti, bir jwt için benzersiz bir tanımlayıcıdır. Bu şekilde kullanıcıyı silmeden kullanıcı girişine ait access token'ı kaldırmış oluruz.
        BLOCKLIST.add(jti)
        return {'message': "Basariyla cikis gerceklestirildi."}, 200


class TokenRefresh(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) # True olunca oluşturulan access token'ı tekrar post için kullanabiliyoruz.
        return {'access_token': new_token}, 200