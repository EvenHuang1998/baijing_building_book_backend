# -*- coding:utf-8 -*-
from flask import Flask, send_file, request
from flask_restful import Api
from database.sql_process import Session

app=Flask(__name__)
api=Api(app)

@app.teardown_request
def shutdown_session(exception=None):
    Session.remove()

#buildings
from model.building import GetHomepageBuildingInfo
api.add_resource(GetHomepageBuildingInfo,"/showAllBuildings")

if __name__ == "__main__":
    app.run(debug=True)
