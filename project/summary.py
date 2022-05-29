from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restful import abort
from project.models import InvoiceItem, Invoice, Item,summarys_schema,Company,summary2_schema,summarys2_schema
from project import db, app
from project import db, app
import pandas as pd
import json

summary = Blueprint('summary', '__name__')

#show all the invoiceitem
@summary.route("/invoiceitem", methods=['GET'])
def all_invoiceitem():
    all_invoice = db.session.query(InvoiceItem).join(Invoice).outerjoin(Item).add_columns(
        InvoiceItem.id,
        InvoiceItem.quantity,
        InvoiceItem.invoice_id,
        Invoice.sub_date,
        InvoiceItem.item_id,
        Item.name,
        Item.price,
        Item.unit,
    ).all()
    result = summarys_schema.dump(all_invoice)
    # data=pd.DataFrame(result).reset_index(drop=True)
    # data['total']=data['quantity']*data['price']
    
    return jsonify({'data': result})

#show invoice and items
@summary.route("/invoice/<id>", methods=['GET'])
def invoice_detail(id):
    invoice = Invoice.query.outerjoin(Company).add_columns(
        Invoice.id,
        Invoice.sub_date,
        Company.name,
        Company.attention,
        Company.address,
        Company.phone,
        Company.fax
    ).filter(Invoice.id==id).first()
    result = summary2_schema.dump(invoice)

    all_invoiceitem = db.session.query(InvoiceItem).join(Invoice).outerjoin(Item).add_columns(
        InvoiceItem.id,
        InvoiceItem.quantity,
        InvoiceItem.invoice_id,
        InvoiceItem.item_id,
        Item.name,
        Item.price,
        Item.unit,
    ).filter(Invoice.id==id).all()
   
    result2 = summarys_schema.dump(all_invoiceitem)

    result2={'itemlist': result2}

    return jsonify({**result, **result2})

#show all the invoice
@summary.route("/invoice_s", methods=['GET'])
def all_invoices():
    all_invoice = db.session.query(InvoiceItem).join(Invoice).outerjoin(Item).add_columns(
        InvoiceItem.id,
        InvoiceItem.quantity,
        InvoiceItem.invoice_id,
        Invoice.sub_date,
        InvoiceItem.item_id,
        Item.name,
        Item.price,
        Item.unit,
    ).all()
    result = summarys_schema.dump(all_invoice)

    invoice = Invoice.query.outerjoin(Company).add_columns(
        Invoice.id,
        Invoice.sub_date,
        Company.name,
    ).all()
    result2 = summarys2_schema.dump(invoice)
    data3=pd.DataFrame(result2)
    data=pd.DataFrame(result).reset_index(drop=True)
    data['total']=data['quantity']*data['price']
    data2 = data.groupby('invoice_id')["total"].sum()
    data4=pd.merge(data2, data3, left_on='invoice_id', right_on='id')
    return (data4.to_json(orient='records'))
