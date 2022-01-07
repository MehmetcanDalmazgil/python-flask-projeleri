from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': "Magaza bulunamadi."}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"{name} adli magaa onceden olusturulmus."}, 400
        
        store = StoreModel(name)

        try:
            store.save_to_db() 
        except:
            return {'message': "Magaza olusturulurken bilinmedik bir hata ile karsilasildi."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {'message': "Magaza silindi."}
    
class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.find_all()]} # Daha Pythonic 
    # query.all => query'i find_by_name yerine de kullanabiliriz fakat db'ye sorgu atarak işlem gerçekleştirdiğiniden kaynak olarak ağırlaşmaktadır.