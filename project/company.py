from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restful import abort
from project.models import Company, company_schema, companys_schema
from project import db, app

company = Blueprint('company', '__name__')

# Get All Company


@company.route("/", methods=['GET'])
def all_company():
    all_user = Company.query.all()
    result = companys_schema.dump(all_user)
    return jsonify({'data': result})

# Get Single Company


@company.route("/<id>", methods=['GET'])
def get_company(id):
    Company = Company.query.filter_by(id=id).first()
    result = company_schema.dump(company)
    if not result:
        abort(404, message="Could not find Company with this ID")
    return jsonify(result)

# Add New Company


@company.route("/", methods=['POST'])
def add_company():
    name = request.json['name']
    attention = request.json['attention']
    fax = request.json['fax']
    address = request.json['address']
    phone = request.json['phone']

    check_name = Company.query.filter_by(name=name).first()

    if check_name:
        return jsonify({'error': 'Company name has been taken'}), 409
    else:
        new_company = Company(name=name, address=address,
                              phone=phone, fax=fax, attention=attention)
        db.session.add(new_company)
        db.session.commit()

    return jsonify({
        'message': "Company Created",
        'new_user': {
            'name': name, 'address': address, 'phone': phone, 'fax': fax, 'attention': attention
        }
    })


# DELETE Company
@company.route("/<id>", methods=["DELETE"])
def delete_company(id):
    remark = Company.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify({"Company has been deleted"}), 204

# update Company
@company.route("/<id>", methods=["PUT"])
def update_company(id):
    comp = Company.query.get(id)
    comp_new = request.get_json()
    comp = comp_new
    result = company_schema.dump(comp)
    db.session.commit()
    return jsonify({'message': "Updated",
                    'data': result})
