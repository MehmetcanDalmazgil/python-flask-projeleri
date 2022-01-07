import sqlite3

from db import db
# API nin düşünmediği, yani get, post, put, delete gerçekleşmeyen API'ye yardımcı dosyalar model olarak adlandırılmaktadır.
# Model bir yardımcıdır. Kaynağı kirletmemizi engeller.
# Müşterinin doğrudan etkileşimde bulunmadığı API'ye yardımcı metodlar.
# Doğrudan API tarafından çağrılmayan metodlar.

class UserModel(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id = _id).first()
    
    """
    @classmethod # Metod içerisinde User sınıfı kullanıldığı için bu şekilde tanımladık.
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
            # user = cls(row[0], row[1], row[2])

        else:
            user = None

        connection.close()
        return user
    
    @classmethod # Metod içerisinde User sınıfı kullanıldığı için bu şekilde tanımladık.
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
            # user = cls(row[0], row[1], row[2])

        else:
            user = None

        connection.close()
        return user
    """