from sqlalchemy import Column, String
from database import Base

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
