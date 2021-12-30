# coding: utf-8

from flask_restful import Resource, reqparse
from model import return_info
from database.sql_process import BuildingCategory

class GetBuildingListOfCategory(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("cateid",type=int,location="args")
        super(GetBuildingListOfCategory,self).__init__()
    
    def get(self):
        args=self.parser.parse_args()
        cateid=args["cateid"]
        if not cateid:
            return return_info.DATA_ERR,404
        query_status,list_=BuildingCategory.get_building_list_by_category_id(cateid)
        if query_status:
            return list_
        else:
            return return_info.QUERY_FAILED,404

class AddBuildingToCategory(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("cateid",type=int,location="form")
        self.parser.add_argument("buildingid",type=int,location="form")
        super(AddBuildingToCategory,self).__init__()
    
    def post(self):
        args=self.parser.parse_args()
        cate_id=args["cateid"]
        building_id=args["building_id"]
        for _,value in args.items():
            if not value:
                return return_info.DATA_ERR,404
        if BuildingCategory.add_building_to_category(building_id,cate_id):
            return {"status":"OK"},200
        else:
            return return_info.SERVER_ERR,503