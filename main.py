from flask import Flask
from models import db, ma


UPLOAD_FOLDER = './static/images/products/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
app.app_context().push()

ma.init_app(app)


import views
import rest


if __name__ == '__mane__':
    app.run(debug=True)

