import sqlite3

from models.item import ItemModel

# API nin yanıt verdiği, düşündüğü dosyalar resource klasörü altında yer almaktadır. 

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

# CRUD API
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help =  "Bu alan boş birakilamaz!")
    
    parser.add_argument('store_id',
        type = int,
        required = True,
        help =  "Tum esyalar store id'ye ihtiyac duymaktadir.")

    @jwt_required()
    def get(self,name):        
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # Şu an geriye sözlük yerine class nesnesi döndüğünden .json() yapmamız gerekti.
        return {'message': 'Esya bulunamadi.'}
    
    @jwt_required(fresh=True) # Eğer refresh endpoint çalıştıysa yani access token değiştiyse tekrar giriş yapmamızı istemektedir.
    def post(self,name):
        # force = True -> Headers'a bakmadan işlemi gerçekleştirmektedir.
        # silent = True -> Hata döndürmesini engellemektedir.
        if ItemModel.find_by_name(name):
            return {'message': f"{name} adıyla bir item bulunmaktadır."}, 400
    
        data = Item.parser.parse_args()
        # item = {"name": name, "price": data['price']}
        item = ItemModel(name,**data) # data['price'], data['store_id']

        try:
            # ItemModel.insert(item)
            item.save_to_db()

        except:
            return{'message': "Oge eklenirken bir hata olustu."}, 500

        return item.json(), 201
    
    @jwt_required() # Kullanıcın bu işlemi gerçekleştirebilmesi için admin kimliğne sahip olma şartı getiriyoruz.
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': "Yoneticilik gerekmektedir."}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Esya Silindi.'}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()

    """
    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Esya Silindi.'}
    
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "Oge eklenirken bir hata olustu."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "Oge guncellenirken bir hata olustu."}, 500
        return updated_item.json()
    """


class ItemList(Resource):
    @jwt_required(optional=True) # Kullanıcnın giriş yapıp yapadığına göre response ifadesini değiştiriyoruz.
    def get(self):
        user_id = get_jwt_identity() #Oturum açan kullanıcının kim olduğunu görmemizi sağlar.
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items': items},200
        return {
            'items': [item['name'] for item in items],
            'message': 'Eger oturum acarsaniz daha fazla urun gorebilirsiniz.'
        }, 200

        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # return {'items': [x.json() for x in ItemModel.find_all()]} # Daha Pythonic, Daha Hızlı, Daha Okunulabilir
        #query.all() => find_all()

    """
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query,)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {'items': items}
    """