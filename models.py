from sqlalchemy import Column, String, Integer
from database import Base

class Product(Base):
    __tablename__ = 'products'

    brand = Column(String(50))
    product_name = Column(String(100),primary_key=True)
    ingredients = Column (String(1000))
    safety_score = Column (Integer)                      
    listPrice = Column(String(10))
    size = Column(String(10))
    rating = Column(String(10))

    def __init__(self, brand=None, product_name=None, ingredients=None,safety_score=None,
                 listPrice=None,size=None,rating=None):
        self.brand = brand
        self.product_name = product_name
        self.ingredients =ingredients
        self.safety_score= safety_score
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
