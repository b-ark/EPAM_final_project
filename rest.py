"""Modules with RESTful service implementation"""
from datetime import datetime
from flask import request, jsonify
from models import Category, Product, CategorySchema, ProductSchema
from main import app
from service import db_add, get_item, check_request, db_commit, db_delete


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@app.route('/api/category', methods=['GET', 'POST', 'DELETE', 'PUT'])
def rest_category():
    """Operations with single category object"""
    if request.method == 'POST':
        title = request.args.get('title')
        description = request.args.get('description')
        item = Category(title=title, description=description)
        db_add(item)
    if request.method == 'GET':
        _id = request.args.get('id')
        item = get_item(Category, _id)
    if request.method == 'PUT':
        _id = request.args.get('id')
        item = get_item(Category, _id)
        if check_request(request.args.get('title')):
            item.title = request.args.get('title')
        if check_request(request.args.get('description')):
            item.description = request.args.get('description')
        db_commit()
    if request.method == 'DELETE':
        item = get_item(Category, request.args.get('id'))
        db_delete(item)
    return category_schema.jsonify(item)


@app.route('/api/product', methods=['GET', 'POST', 'DELETE', 'PUT'])
def rest_product():
    """Operations with single product object"""
    if request.method == 'POST':
        title = request.args.get('title')
        price = request.args.get('price')
        description = request.args.get('description')
        sales_start = datetime.strptime(request.args.get('sales_start'), '%Y-%m-%d').date()
        amount = request.args.get('amount')
        category_id = request.args.get('category_id')
        element = Product(title=title,
                          price=price,
                          description=description,
                          sales_start=sales_start,
                          amount=amount,
                          category_id=category_id)
        db_add(element)
        return product_schema.jsonify(element)

    if request.method == 'GET':
        _id = request.args.get('id')
        item = get_item(Product, _id)
        return product_schema.jsonify(item)

    if request.method == 'PUT':
        _id = request.args.get('id')
        item = get_item(Product, _id)

        if check_request(request.args.get('title')):
            item.title = request.args.get('title')
        if check_request(request.args.get('price')):
            item.price = request.args.get('price')
        if check_request(request.args.get('description')):
            item.description = request.args.get('description')
        if check_request(request.args.get('sales_start')):
            item.sales_start = datetime.strptime(request.args.get('sales_start'), '%Y-%m-%d').date()
        if check_request(request.args.get('amount')):
            item.amount = request.args.get('amount')
        if check_request(request.args.get('img_path')):
            item.img_path = request.args.get('img_path')
        if check_request(request.args.get('category_id')):
            item.category_id = request.args.get('category_id')
        db_commit()
        return product_schema.jsonify(item)

    if request.method == 'DELETE':
        item = get_item(Product, request.args.get('id'))
        db_delete(item)
        return product_schema.jsonify(item)


@app.route('/api/categories', methods=['GET'])
def rest_categories():
    """Operations with all category objects"""
    data = Category.query.all()
    return categories_schema.jsonify(data)


@app.route('/api/products', methods=['GET'])
def rest_products():
    """Operations with all product objects"""
    data = Product.query.all()
    return products_schema.jsonify(data)


@app.route('/api/category/sum', methods=['GET'])
def rest_products_sum():
    """Calculates the sum of all products in the certain category"""
    _id = request.args.get('id')
    item = get_item(Category, _id)
    result = 0
    print(item)
    for i in item.products:
        result += i.amount
    return jsonify({'sum': result})


@app.route('/api/search', methods=['GET'])
def rest_search():
    """Returns products, available by certain date"""
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d').date()
    data = Product.query.filter(Product.sales_start <= date)
    return products_schema.jsonify(data)
