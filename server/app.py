#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/baked_goods', methods = ['POST'])
def baked_goods():
    newBakedGood = BakedGood(
        name=request.form.get("name"),
        price=request.form.get("price"),
        created_at=request.form.get("created_at"),
        updated_at=request.form.get("updated_at"),
        bakery_id=request.form.get("bakery_id")
    )

    db.session.add(newBakedGood)
    db.session.commit()

    review_dict = newBakedGood.to_dict()

    response = make_response(
        review_dict,
        201
    )

    return response

@app.route('/bakeries', methods = ['GET', 'PATCH'])
def bakeries():
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return make_response(  bakeries,   200  )
   

@app.route('/bakeries/<int:id>', methods = ['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if request.method == 'GET':
        
        bakery_serialized = bakery.to_dict()
        response = make_response(
            bakery_serialized,
            200
        )
        return response

    elif request.method == 'PATCH':
        # Update bakery name
        new_name = request.form.get('name')
        if new_name:
            bakery.name = new_name
            db.session.commit()
            return bakery.to_dict(), 200
        else:
            return {"error": "New name not provided"}, 400


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

@app.route('/baked_goods/<int:id>', methods = ['DELETE'])

def baked_goods_delete(id):
    baked_goods = BakedGood.query.filter_by(id=id).first()
    db.session.delete(baked_goods)
    db.session.commit()

    response_body = {
        "delete_successful": True,
        "message": "Review deleted."
    }

    response = make_response(
        response_body,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)