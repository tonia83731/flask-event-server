from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate
from app.lib.auth_handling import admin_authentication
from app.model.users_schema import UserSchema
from app.model.category_schema import CategorySchema
from app import db
from sqlalchemy import or_

class CategoryValidate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=100))
    code = name = fields.String(required=True)

class AdminCategories(Resource): 
    @jwt_required()
    def get(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        
        categories = db.session.query(CategorySchema).all()
        return {
            "data": [c.to_dict() for c in categories]
        }, 200
    
    @jwt_required()
    def post(self, admin_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        
        user = db.session.query(UserSchema).filter(UserSchema.id == admin_id).first()
        if user.email != "admin@example.com":
            return {
                "message": "Permission deined"
            }, 400
        input = CategoryValidate()
        errors = input.validate(request.json)

        if errors: 
            return {
                "message": errors
            }, 400
        
        data = input.load(request.json)

        is_existed = db.session.query(CategorySchema).filter(
        CategorySchema.code == data['code']
        ).first()
        if is_existed:
            return {
                "message": "Category with this code already exists"
            }, 400

        category = CategorySchema(**data)
        category.created()

        return {
            "data": category.to_dict()
        }, 201
    
class AdminCategory(Resource):
    @jwt_required()
    def get(self, admin_id, category_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        category = db.session.query(CategorySchema).filter(CategorySchema.id == category_id).first()
        if not category:
            return {
                "message": "Category not found"
            }, 404
        return {
            "data": category.to_dict()
        }, 200

    @jwt_required()
    def put(self, admin_id, category_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        user = db.session.query(UserSchema).filter(UserSchema.id == admin_id).first()
        if user.email != "admin@example.com":
            return {
                "message": "Permission deined"
            }, 400
        category = db.session.query(CategorySchema).filter(CategorySchema.id == category_id).first()
        if not category:
            return {
                "message": "Category not found"
            }, 404

        input = CategoryValidate()
        errors = input.validate(request.json)

        if errors: 
            return {
                "message": errors
            }, 400
        
        data = input.load(request.json)

        is_existed = db.session.query(CategorySchema).filter(
            CategorySchema.code == data['code']
        ).first()
        if is_existed and is_existed.id != category_id:
            return {
                "message": "Category with this code already exists"
            }, 400
    
        category.name = data["name"]
        category.code = data["code"]

        db.session.commit()
        return {
            "data": category.to_dict()
        }, 200
        

    @jwt_required()
    def delete(self, admin_id, category_id):
        if not admin_authentication(admin_id):
            return {
                "message": "Permission deined"
            }, 400
        user = db.session.query(UserSchema).filter(UserSchema.id == admin_id).first()
        if user.email != "admin@example.com":
            return {
                "message": "Permission deined"
            }, 400   
        category = db.session.query(CategorySchema).filter(CategorySchema.id == category_id).first()
        if not category:
            return {
                "message": "Category not found"
            }, 404
        
        category.deleted()
        return {
            "message": "Category deleted",
        }, 200