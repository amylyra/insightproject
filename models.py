from sqlalchemy import Column, String
from database import Base

class Product(Base):
    __tablename__ = 'products'

    brand = Column(String(50), primary_key=True)
    name = Column(String(100))
    ingredients = Column (Ingredient)
    listPrice = Column(String(10))
    size = Column(String(10))
    rating = Column(String(10))

    def __init__(self, brand=None, name=None, ingredients=None,
                 listPrice=None,size=None,rating=None):
        self.brand = brand
        self.name = name
        self.ingredients= ingredients
        self.listPrice = listPrice
        self.size = size
        self.rating = rating


    def __repr__(self):
        return '<Product %r>' % (self.name)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    name = Column(String(100), primary_key=True)
    about = Column(String(1000))
    safety = Column(String(2))
    function = Column(String(500))

    def __init__(self, name=None, about=None, safety=None,
                 function=None):
        self.name = name
        self.about = about
        self.safety = safety
        self.function = function

    def __repr__(self):
        return '<Ingredient %r>' % (self.name)
