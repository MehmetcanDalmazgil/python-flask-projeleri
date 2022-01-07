# https://www.getpostman.com/collections/a85d3f1fa722d6a21d93

from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blocklist import BLOCKLIST

from db import db

app = Flask(__name__)
# config = yapılandırma
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Flask-SQLAlchemy nesnelerin değişikliklerini izler ve sinyal yayar. Bu, ek bellek gerektirir ve gerekmediğinde devre dışı bırakılabilir.
app.config['PROPAGATE_EXCEPTIPNS'] = True
app.config['JWT_SECRET_KEY'] = 'thekoyu' # app.secret_key = 'thekoyu'

api = Api(app) # API metodlarını kullanmamızı kolay hale getirecek.

# Veri tabanı ve tabloları oluşturan kod parçacığı
@app.before_first_request # decorator
def create_tables():
    db.create_all()

# Kullanıcı Girişi Kontrolü
# Bir kullanıcı token oluşmaktadır. Bu değer ile jwt_required() istenilen istekler gerçekleştirilebilir.
# jwt = JWT(app, authenticate, identity) # /auth

jwt = JWTManager(app) # /auth endpoint'ini oluşturmamaktadır. JWT'den farklı bir kütüphanedir.

@jwt.additional_claims_loader # Eski adı @jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # id'si 1 olan kullanıcı kullanabilir.
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader # Access token'nin ait olduğu kullanıcı id blocklist içerisinde yer alıyorsa bu token'ı revoked_token_callback metoduna göndererek iptal etmektedir.
def check_if_token_in_blacklist(jwt_header, jwt_payload): 
    return jwt_payload['jti'] in BLOCKLIST

@jwt.expired_token_loader # Token süresinin dolup dolmadığına bakan decorator.
def expired_token_callback():
    return jsonify({
        'description': "Token Suresi Doldu", # The token has expired
        'error': "token_expired"
    }), 401

@jwt.invalid_token_loader # Geçersiz token değeri girilip girilmediğine bakan decorator.
def invalid_token_callback(error): 
    return jsonify({
        'description': "Imza Dogrulama Basarsiziz", # Signature verification failid
        'error': "invalid_token"
    }), 401

@jwt.unauthorized_loader # Access token içermesi gereken isteğin token'ı içerip içermediğini kontrol eden decorator.
def missing_token_callback(error):
    return jsonify({
        'description': "Istek access token icermiyor", # Request does not contain an access token
        'error': "authorization_required"
    }), 401

@jwt.needs_fresh_token_loader # refresh işlemiyle üretilen yeni token'nın kullanılıp kullanılmadığını kontrol eden decorator.
def token_not_fresh_callback():
    return jsonify({
        'description': "Bu token bir fresh token degil", # The token is not fresh
        'error' : "fresh_token_required"
    }), 401

@jwt.revoked_token_loader # Kullanıcı çıkış yaptıktan sonra kullanıcıya ait access point'i iptal eden decorator
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': "Token iptal edildi.", # Token has been revoked
        'message': "token_revoked"
    }), 401

#app.route() yerine bu şekilde bir kullanım sağlıyor.
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/ayakkabı
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug = True)

