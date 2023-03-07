"""Modules with Web controllers / views"""
from datetime import datetime
import os
from flask import render_template, request, redirect
from main import app
from models import Category, Product, db
from service import POST_category, get_item, db_commit, db_delete, db_add


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/categories')
def categories():
    """Page with the list of categories and products"""
    data = Category.query.all()
    return render_template('categories.html', data=data)


@app.route('/products')
def products():
    """Page with the list of products"""
    data = Product.query.all()
    return render_template('products.html', data=data)


@app.route('/categories/new', methods=['POST', 'GET'])
def new_category():
    """Page with the form to add new category"""
    if request.method == 'POST':
        return POST_category(request)
    # request.method == 'GET'
    return render_template('create_category.html')


@app.route('/products/new', methods=['POST', 'GET'])
def new_product():
    """Page with the form to add new product"""
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        sales_start = datetime.strptime(request.form['sales_start'], '%Y-%m-%d').date()
        amount = request.form['amount']
        category_title = request.form['category_title']
        parent = Category.query.filter_by(title=category_title).first()

        product = Product(title=title,
                          price=price,
                          description=description,
                          sales_start=sales_start,
                          amount=amount,
                          category_id=parent.id)
        db_add(product)
        obj = Product.query.order_by(Product.id.desc()).first()
        if "file" not in request.files:
            return 'No file part'
        file = request.files['file']
        file.filename = str(obj.id) + '.' + file.filename.split('.')[1]
        path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path_to_file)
        obj.img_path = path_to_file
        db_commit()
        return redirect('/products')
    # request.method == 'GET'
    data = Category.query.all()
    return render_template('create_product.html', data=data)


@app.route('/product/<int:_id>', methods=['GET'])
def show_product(_id):
    """Page to show product by id"""
    item = get_item(Product, _id)
    return render_template('product.html', data=item)


@app.route('/category/<int:_id>', methods=['GET'])
def show_category(_id):
    """Page to show category by id"""
    item = get_item(Category, _id)
    return render_template('category.html', data=item)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Page to search for products, available by certain date"""
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        data = Product.query.filter(Product.sales_start <= date)
        return render_template('search.html', data=data)
    # request.method == 'GET'
    return render_template('search.html')


@app.route('/category/edit/<int:_id>', methods=['GET', 'POST'])
def edit_category(_id):
    """Page to edit category by id"""
    if request.method == 'POST':
        item = get_item(Category, _id)
        item.title = request.form['title']
        item.description = request.form['description']
        db_commit()
        return redirect('/categories')
    # request.method == 'GET'
    item = get_item(Category, _id)
    return render_template('edit_category.html', data=item)


@app.route('/product/edit/<int:_id>', methods=['GET', 'POST'])
def edit_product(_id):
    """Page to edit product by id"""
    if request.method == 'POST':
        item = get_item(Product, _id)
        item.title = request.form['title']
        item.description = request.form['description']
        db_commit()
        return redirect('/products')
    # request.method == 'GET' functionality
    item = get_item(Product, _id)
    cats = Category.query.all()
    return render_template('edit_product.html', data=[item] + [cats])


@app.route('/product/delete/<int:_id>', methods=['GET'])
def delete_product(_id):
    """Page to delete product by id"""
    item = get_item(Product, _id)
    db_delete(item)
    return redirect('/products')


@app.route('/category/delete/<int:_id>', methods=['GET'])
def delete_category(_id):
    """Page to delete category by id"""
    item = get_item(Category, _id)
    db_delete(item)
    return redirect('/categories')
