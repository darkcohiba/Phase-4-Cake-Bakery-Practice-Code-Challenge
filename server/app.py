#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Cake, Bakery, CakeBakery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('./bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    data = [bakeries.to_dict(only=('id', 'name', 'address'))for bakeries in bakeries]

    return make_response(
        jsonify(data),
        200
    )

@app.get('/bakeries/<int:id>')
def get_bakeries_by_id(id):
    bakery = Bakery.query.filter(
        Bakery.id == id
    ).first()

    if not bakery:
        return make_response(
            jsonify({'error': 'bakery not found'}),404
        )
    
    return make_response(
        jsonify(bakery.to_dict(only = ('id','name','address','cakes')),200)
    )

@app.delete('/bakeries/<int:id>')
def delete_bakery(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if not bakery:
        return make_response(
            jsonify({'error': 'bakery not found'}), 404
        )
    db.session.delete(bakery)
    db.session.commit()

    return make_response(jsonify({}), 204)

@app.get('/cakes')
def get_cakes():
    cake = [c.to_dict(only=('id','name','description')) for c in Cake.query.all()]
    return make_response(cake, 200)

@app.post('/cake_bakery')
def post_bakery():
    data = request.get_json()
    try:
        new_bakery = CakeBakery(
        price = data['price'],
        cake_id = data['cake_id'],
        bakery_id = data['bakery_id']
        )
    except Exception:
        return "error error error"
    db.session.add(new_bakery)
    db.session.commit()
    return make_response(jsonify(new_bakery.to_dict()),200)










if __name__ == '__main__':
    app.run(port=5555, debug=True)