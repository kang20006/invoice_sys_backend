from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restful import abort
from project.models import InvoiceItem, Invoice, Item,summarys_schema,Company,summary2_schema,summarys2_schema, invoices_schema, companys_schema
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
        Invoice.remark,
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
    data=pd.DataFrame(result2)
    data['total']=data['quantity']*data['price']
    sum = data.groupby('invoice_id')["total"].sum()
    total={'total': (float(sum[0]))}
    result2={'itemlist': result2}


    return jsonify({**result, **result2,**total})

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

@summary.route("/new_info", methods=['GET'])
def new():
    all_invoice = db.session.query(Invoice).add_columns(Invoice.id).all()
    result=invoices_schema.dump(all_invoice)
    data_invoice=pd.DataFrame(result)
    ##### remember to change to P00000
    data_invoice['id']=data_invoice['id'].str.replace('P000', '')
    data_invoice['id'] = pd.to_numeric(data_invoice['id'])
    max_value = data_invoice['id']. max() 
    all_company = db.session.query(Company).add_columns(
        Company.name).all()
    result2=companys_schema.dump(all_company)
    
    return (jsonify({'invoice_id': 'P000'+ str(max_value+1),
    'company_name':result2}))

#filter by company id
@summary.route("/invoice_s/<id>", methods=['GET'])
def all_invoices_by_company(id):
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
    company_name=Company.query.filter(Company.id==id).first()
    company_name=company_name.name
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
    data4=data4[data4['name'].isin([company_name])]
    return (data4.to_json(orient='records'))