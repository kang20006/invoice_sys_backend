from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restful import abort
from project.models import Invoice, invoice_schema, invoices_schema, Item, InvoiceItem
from project import db, app

invoice = Blueprint('invoice', '__name__')

# Get All Invoice
@invoice.route("/", methods=['GET'])
def all_invoice():
    all_invoice = Invoice.query.all()
    result = invoices_schema.dump(all_invoice)
    return jsonify({'data': result})

# Get Single Invoice
@invoice.route("/<id>", methods=['GET'])
def get_invoice(id):
    invoice = Invoice.query.filter_by(id=id).first()
    result = invoice_schema.dump(invoice)
    if not result:
        abort(404, message="Could not find Invoice with this ID")
    return jsonify(result)

from datetime import datetime

# {"id":"P00011",
# "sub_date": "03/10/22 13:14:00",
# "remark":"eirhiohfe",
# "company_id":1,
#  "NewList":[
#      {
#          "name" : "railing1",
#          "price" : 18,
#          "unit": "m",
#          "quantity": 100
#      },
#      {
#          "name" : "bill board2",
#          "price" : 1800,
#          "unit": "NOS",
#          "quantity": 100
#      },
#      {
#          "name" : "gating",
#          "price" : 2000,
#          "unit": "NOS",
#          "quantity": 100
#      }
#  ]
#  }

# Add New Invoice
@invoice.route("/", methods=['POST'])
def add_invoice():
    id = request.json['id']
    sub_date = request.json['sub_date']
    datetime_object = datetime.strptime(sub_date, '%m/%d/%y %H:%M:%S')
    remark= request.json['remark']
    company_id= request.json['company_id']
    jdata=request.json['NewList']
    new_invoice = Invoice(id=id,sub_date=datetime_object, company_id=company_id,
                              remark=remark)
    db.session.add(new_invoice)
    db.session.commit()
    for data in jdata:
        name = data['name']
        unit = data['unit']
        price =data['price']
        quantity=data['quantity']
        check_repeat = Item.query.filter_by(name=name,price=price).first()
        if check_repeat:
            pass
        else:
            new_item = Item(name=name,unit=unit,price=price)
            db.session.add(new_item)
            db.session.commit()
        purchased_item=db.session.query(Item.id).filter_by(name=name,price=price).first()
        new_invoiceitem=InvoiceItem(invoice_id=id,item_id=purchased_item[0],quantity=quantity)
        db.session.add(new_invoiceitem)
        db.session.commit()    
    return jsonify({
        'message': "Invoice Created",
    })

# DELETE invoice
@invoice.route("/<id>", methods=["DELETE"])
def delete_invoice(id):
    invoiceitem=InvoiceItem.query.filter_by(invoice_id=id).delete()
    invoice = Invoice.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"Invoice and InvoiceItem has been deleted"}), 204

# update invoice
@invoice.route("/<id>", methods=["PUT"])
def update_invoice(id):
    invoice = Invoice.query.filter_by(id=id).delete()
    id = request.json['id']
    sub_date = request.json['sub_date']
    datetime_object = datetime.strptime(sub_date, '%m/%d/%y %H:%M:%S')
    remark= request.json['remark']
    company_id= request.json['company_id']
    jdata=request.json['NewList']
    new_invoice = Invoice(id=id,sub_date=datetime_object, company_id=company_id,
                              remark=remark)
    db.session.add(new_invoice)
    db.session.commit()
    invoiceitem=InvoiceItem.query.filter_by(invoice_id=id).delete()
    db.session.commit()
    jdata=request.json['NewList']
    for data in jdata:
        name = data['name']
        unit = data['unit']
        price =data['price']
        quantity=data['quantity']
        check_repeat = Item.query.filter_by(name=name,price=price).first()
        if check_repeat:
            pass
        else:
            new_item = Item(name=name,unit=unit,price=price)
            db.session.add(new_item)
            db.session.commit()
        purchased_item=db.session.query(Item.id).filter_by(name=name,price=price).first()
        new_invoiceitem=InvoiceItem(invoice_id=id,item_id=purchased_item[0],quantity=quantity)
        db.session.add(new_invoiceitem)
        db.session.commit()    
    return jsonify({'message': "Updated"
                    })
