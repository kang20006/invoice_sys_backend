from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restful import abort
from project.models import Item, item_schema, items_schema, Activity
from project import db, app
import pandas as pd
from datetime import datetime

item = Blueprint('item', '__name__')

# Get All item
@item.route("/", methods=['GET'])
def all_item():
    all_item = Item.query.all()
    result = items_schema.dump(all_item)
    data = pd.DataFrame(result)
    data["price"]= data["price"].apply(lambda x: round(float(x),2))
    data["label"] = data["name"] + " RM" + data["price"].astype(str) 
    return (data.to_json(orient='records'))

# Get Single item
@item.route("/<id>", methods=['GET'])
def get_item(id):
    item = Item.query.filter_by(id=id).first()
    result = item_schema.dump(item)
    if not result:
        abort(404, message="Could not find Company with this ID")
    return jsonify(result)

# Add New items
# {
# "NewList":[
#     {
#         "key" : "myvalue1",
#         "value" : "value1"
#     },
#     {
#         "key" : "myvalue2",
#         "value" : "value2"
#     },
#     {
#         "key" : "myvalu3",
#         "value" : "value4"
#     }
# ]
# }
@item.route("/", methods=['POST'])
def add_items():
    jdata=request.json['NewList']
    for data in jdata:
        name1 = data['name']
        unit1 = data['unit']
        price1 =data['price']

        check_repeat = Item.query.filter_by(name=name1,price=price1).first()
        if check_repeat:
            print (check_repeat)
        else:
            new_item = Item(name=name1,unit=unit1,price=price1)
            db.session.add(new_item)
            db.session.commit()

    return jsonify({
        'message': "Items Created"
    })

# DELETE item
@item.route("/<id>", methods=["DELETE"])
def delete_item(id):
    name= Item.query.filter_by(id=id).first()
    # name=name.name
    remark = Item.query.filter_by(id=id).delete()
    db.session.commit()

    my_date = datetime.now()
    ###
    new_activity=Activity(activity_dt=my_date,activity="Delete item",act_description="Deleted item")
    db.session.add(new_activity)
    db.session.commit()
    
    return jsonify({"message":"Item has been deleted"}), 204

# update Item
@item.route("/<id>", methods=["PUT"])
def update_item(id):
    item_new = request.get_json()
    item = Item.query.filter(Item.id==id).update(item_new)
    result = item_schema.dump(item)
    db.session.commit()

    name= Item.query.filter_by(id=id).first()
    # name=name.name
    my_date = datetime.now()
    ###
    new_activity=Activity(activity_dt=my_date,activity="Update item",act_description="Updated item")
    db.session.add(new_activity)
    db.session.commit()

    return jsonify({'message': "Updated",
                    'data': result})
