from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
# lazy='dynamic' makes items a query so you have to call .all to fetch all items, which it would otherwise do by default
# so creating the object is faster, calling the method is slower, opposite is true without the line

# an ORM such as SQLAlchemy makes it really easy to interact with other objects in your system via these relationships
# but the test stops becoming a unit test, so the json method can't be tested for example
# only the init method can be unit tested

    def __init__(self, name) -> object:
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}
    # returns all the items JSONs

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
