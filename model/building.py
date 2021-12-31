# coding: utf-8

from flask_restful import Resource,reqparse
from model import return_info
from database.sql_process import Buildings

class GetHomepageBuildingInfo(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        super(GetHomepageBuildingInfo,self).__init__()

    def get(self):
        all_homepage_building_info=Buildings.get_homepage_buildings_info()
        return all_homepage_building_info

class GetBuildingByID(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("buildingid",type=int,location="args")
        super(GetBuildingByID,self).__init__()
    
    def get(self):
        args=self.parser.parse_args()
        building_id=args["buildingid"]
        if not building_id:
            return return_info.DATA_ERR,404
        query_status,building=Buildings.get_building_by_id(building_id)
        if query_status:
            return building,200
        else:
            return return_info.QUERY_FAILED,404

class AddNewBuilding(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("buildingid", type=int, location="form")
        self.parser.add_argument("buildingname",type=str,location="form")
        self.parser.add_argument("buildingimg",type=str,location="form")
        self.parser.add_argument("accessway",type=str,location="form")
        super(AddNewBuilding, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        building_id=args["buildingid"]
        building_name=args["buildingname"]
        building_img=args["buildingimg"]
        building_access_way=args["accessway"]
        for _, value in args.items():
            if not value:
                return return_info.DATA_ERR, 404
        if Buildings.add_building(building_id,building_name,building_img,building_access_way):
            return {"status": "OK"}, 200
        else:
            return return_info.SERVER_ERR, 503

class RemoveBuilding(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("buildingid", type=int, location="args")

    def get(self):
        args = self.parser.parse_args()
        building_id = args["buildingid"]
        if not building_id:
            return return_info.DATA_ERR, 404
        status = Buildings.remove_building(building_id)
        if status:
            return {"status": "OK"}, 200
        else:
            return return_info.REMOVE_FAILED, 503
