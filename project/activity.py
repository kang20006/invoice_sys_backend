from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restful import abort
from project.models import Activity, activitys_schema
from project import db, app
import pandas as pd

activity = Blueprint('activity', '__name__')

# Get All Activity
@activity.route("/", methods=['GET'])
def all_activity():
    all_activity = Activity.query.all()
    result = activitys_schema.dump(all_activity)
    data=pd.DataFrame(result)
    data['start']=data["activity_dt"]
    data['title']=data["activity"]
    del data["activity_dt"]
    del data["activity"]
    return (data.to_json(orient='records'))