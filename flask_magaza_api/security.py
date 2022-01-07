# JWT ile kullandigimiz bu dosyayi JWT-Extended ile beraber kullanmaya gerek kalmadi.

from models.user import UserModel

from werkzeug.security import safe_str_cmp

# users = [
#     User(1,'mehmet','m123')
# ]

# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    # user = username_mapping.get(username, None)
    # if user and user.password == password:
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password): #utf-8 ve unicode konusunda karşılaşılacak sorunları engelledik.
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

# users = [
#     {
#         'id':1,
#         'username': 'mehmetcan',
#         'password': 'memo123'

#     }
# ]

# username_mapping = { 'mehmetcan': {
#     'id':1,
#     'username': 'mehmetcan',
#     'password': 'memo123'
# }}

# userid_mapping = {1: {
#     'id':1,
#     'username': 'mehmetcan',
#     'password': 'memo123'
# }}

