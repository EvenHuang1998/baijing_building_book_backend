# -*- coding:utf-8 -*-
from flask import Flask, send_file, request
from flask_restful import Api
from database.sql_process import Session

app=Flask(__name__)
api=Api(app)

@app.teardown_request
def shutdown_session(exception=None):
    Session.remove()

# 添加header解决跨域


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
    return response

#buildings
from model.building import GetHomepageBuildingInfo
api.add_resource(GetHomepageBuildingInfo,"/building/showHomepageBuildings")
from model.building import GetBuildingByID
api.add_resource(GetBuildingByID,"/building/getBuilding")
from model.building import AddNewBuilding
api.add_resource(AddNewBuilding,"/building/addNewBuilding")
from model.building import RemoveBuilding
api.add_resource(RemoveBuilding,"/building/removeBuilding")

#categories
from model.category import GetAllCategories
api.add_resource(GetAllCategories,"/category/getAllCategories")

if __name__ == "__main__":
    app.run(debug=True)
