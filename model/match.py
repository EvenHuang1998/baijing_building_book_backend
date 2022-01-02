# coding: utf-8
from flask_restful import Resource,reqparse
from model import return_info
from database.sql_process import BuildingMatch

class GetMatchOfBuilding(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("buildingid",type=int,location="args")
        super(GetMatchOfBuilding,self).__init__()

    def get(self):
        args=self.parser.parse_args()
        building_id=args["buildingid"]
        if not building_id:
            return return_info.DATA_ERR,404
        
        status,match=BuildingMatch.get_match_url_by_building_id(building_id)
        if status:
            return match,200
        else:
            return return_info.QUERY_FAILED,404
    
class AddMatch(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("buildingid",type=int,location="form")
        self.parser.add_argument("matchurl",type=str,location="form")
        super(AddMatch,self).__init__()
    
    def post(self):
        args=self.parser.parse_args()
        building_id=args["buildingid"]
        match_url=args["matchurl"]

        for _,value in args.items():
            if not value:
                return return_info.DATA_ERR,404
        if BuildingMatch.add_match(building_id,match_url):
            return {"status":"OK"},200
        else:
            return return_info.SERVER_ERR,503
        