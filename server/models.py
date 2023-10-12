from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Cake(db.Model, SerializerMixin):
    __tablename__ = 'cake_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    cakebakery_c_relationship = db.relationship('CakeBakery', back_populates='cake_relationship')


class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakery_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    cakebakery_b_relationship = db.relationship('CakeBakery', back_populates='bakery_relationship')

class CakeBakery(db.Model, SerializerMixin):
    __tablename__ = 'cakebakery_table'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)

    cake_id = db.Column(db.Integer, db.ForeignKey('cake_table.id'))
    cake_relationship = db.relationship('Cake', back_populates='')

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakery_table.id'))
    bakery_relationship = db.relationship('Bakery', back_populates='')

    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    @validates('price')
    def validate_price(self, key, price):
        if 0 < price <= 1000:
            return price
        else:
            raise ValueError("Price is not correct.")






