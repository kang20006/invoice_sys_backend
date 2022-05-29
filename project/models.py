from enum import unique
from sqlalchemy.orm import backref
from project import  db, ma
from datetime import datetime
from sqlalchemy import funcfilter, func, and_

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50),unique=True, nullable=False)
    attention=db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    fax = db.Column(db.String(100), nullable=True)
    
    def __init__ (self,name,attention,address,phone,fax):
        self.name=name
        self.address=address
        self.phone=phone
        self.fax=fax
        self.attention=attention

#the ways how the data print out
class CompanySchema(ma.Schema):
    class Meta:
        fields=('id','name','address','phone','attention','fax')

#Initialize Schema
company_schema=CompanySchema()
companys_schema=CompanySchema(many=True)

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id =  db.Column(db.String(100), db.ForeignKey('invoice.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity= db.Column(db.Numeric(5000))
    invoice = db.relationship("Invoice", backref="invoice_item")
    item = db.relationship("Item", backref="invoice_item")

class InvoiceItemSchema(ma.Schema):
    class Meta:
        fields=('invoice_id','item_id','quantity')

invoice_item_schema=InvoiceItemSchema()
invoice_items_schema=InvoiceItemSchema(many=True)


class Invoice(db.Model):
    id = db.Column(db.String(100),nullable=False, primary_key=True)
    sub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    remark= db.Column(db.String(500),nullable=True)
    company_id=db.Column(db.String(100),db.ForeignKey('company.id'),nullable=False)
    company = db.relationship('Company', backref='invoice')

    item=db.relationship('Item',secondary='invoice_item')

    def __init__ (self,id,sub_date,company_id,remark):
        self.id=id
        self.sub_date=sub_date
        self.company_id=company_id
        self.remark=remark

#Invoice schema
class InvoiceSchema(ma.Schema):
    class Meta:
        fields=('id','sub_date','company_id')

#initialize schema
invoice_schema=InvoiceSchema()
invoices_schema=InvoiceSchema(many=True)    

class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(3000))
    unit=db.Column(db.String(50),nullable=False)
    price=db.Column(db.Numeric(50000))
    
    def __init__ (self,name,unit,price):
        self.name=name
        self.unit=unit
        self.price=price
       
#item schema
class ItemSchema(ma.Schema):
    class Meta:
        fields=('id','name','unit','price')

#initialize schema
item_schema=ItemSchema()
items_schema=ItemSchema(many=True)  


class Activity(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    activity_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    invoice_id=db.Column(db.String(100),db.ForeignKey('invoice.id'),nullable=False)
    activity=db.Column(db.String(500))
    act_description=db.Column(db.String(1000))
   
    #relationships:
    invoice = db.relationship('Invoice', backref='activity')
    
    def __init__(self,activity_dt,invoice_id,activity,act_description):
        self.activity_dt=activity_dt
        self.invoice_id=invoice_id
        self.activity=activity
        self.act_description=act_description
       
class ActivitySchema(ma.Schema):
    class Meta:
        fields=('id','activity_dt','invoice_id','activity','act_description')

activity_schema=ActivitySchema()
activitys_schema=ActivitySchema(many=True)        


class SummarySchema(ma.Schema):
    class Meta:
        fields = ('id',
                  'quantity',
                  'invoice_id',
                  'sub_date',
                  'name',
                  'price',
                  'unit',
                  'total'
        )
summary_schema = SummarySchema()
summarys_schema = SummarySchema(many=True)

class Summary2Schema(ma.Schema):
    class Meta:
        fields = ('id',
                  'sub_date',
                  'name',
                  'attention',
                  'address',
                  'phone',
                  'fax',
                  'name'
        )
summary2_schema = Summary2Schema()
summarys2_schema = Summary2Schema(many=True)


