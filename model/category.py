# coding: utf-8

from flask_restful import Resource,reqparse
from model import return_info
from database.sql_process import Categories

class AddNewCategory(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catename",type=str,location="form")
        self.parser.add_argument("cateid",type=int,location="form")
        super(AddNewCategory,self).__init__()
    
    def post(self):
        args=self.parser.parse_args()
        catename=args["catename"]
        cateid=args["cateid"]
        for _,value in args.items():
            if not value:
                return return_info.DATA_ERR,404
        if Categories.add_category(cateid,catename):
            return {"status":"OK"},200
        else:
            return return_info.SERVER_ERR,503
    
class GetAllCategories(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        super(GetAllCategories,self).__init__()
    
    def get(self):
        all_categories=Categories.get_categories()
        return all_categories

class GetCategoryByID(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("cateid",type=int,location="args")
        super(GetAllCategories,self).__init__()

    def get(self):
        args=self.parser.parse_args()
        cateid=args["cateid"]
        if not cateid:
            return return_info.DATA_ERR,404
        query_status,category=Categories.get_category_by_id(cateid)
        if query_status:
            return category,200
        else:
            return return_info.QUERY_FAILED,404

class RemoveCategory(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("cateid",type=int,location="args")

    def get(self):
        args=self.parser.parse_args()
        cateid=args["cateid"]
        if not cateid:
            return return_info.DATA_ERR,404
        status=Categories.remove_category(cateid)
        if status:
            return {"status":"OK"},200
        else:
            return return_info.REMOVE_FAILED,503
