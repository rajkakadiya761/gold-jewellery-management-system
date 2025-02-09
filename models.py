from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import JSON

db = SQLAlchemy()

class HomeProduct(db.Model):
    __tablename__ = 'homeProducts'

    homeProduct_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    
    # Relationship definition
    product = db.relationship('Products', backref='home_products', lazy=True)

    def __repr__(self):
        return f"<HomeProduct {self.homeProduct_id}, Product {self.product_id}>"
    
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_confirmed = db.Column(db.Integer, default=0)  # Add confirmation status

    def __repr__(self):
        return f"<User {self.name}, {self.email}>"
    
class Complaints(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'inprocess', 'resolved'), default='pending')
    type = db.Column(db.Enum('delivery', 'product', 'packaging'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    product_weight = db.Column(db.Float, nullable=False)
    sizes = db.Column(db.String(50), nullable=False)  
    category = db.Column(
        db.Enum('ring', 'necklace', 'earrings', 'bracelete', name='category_enum'),
        nullable=False
    )
    photo1 = db.Column(db.String(255), nullable=False)
    photo2 = db.Column(db.String(255), nullable=False)

    # Define only the relationship
    product_materials = db.relationship('ProductMaterial', back_populates='product')

    def __repr__(self):
        return f"<Product {self.name}, {self.category}>"


class ProductMaterial(db.Model):
    __tablename__ = 'product_material'

    product_material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)

    # Define the other side of the relationship
    product = db.relationship('Products', back_populates='product_materials')
    material = db.relationship('Material', backref=db.backref('product_materials', lazy=True))

    def __repr__(self):
        return f"<ProductMaterial {self.product_id}, {self.material_id}>"


class Material(db.Model):
    __tablename__ = 'materials'

    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Material {self.material_name}>"


class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    ratings = db.Column(db.Integer, nullable=False)  # From 1 to 5
    message = db.Column(db.Text, nullable=False)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Users', backref='feedback')  
    product = db.relationship('Products', backref='feedback') 
    
class Cart(db.Model):
    __tablename__ = 'carts'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_ids = db.Column(JSON, nullable=False)  # Stores a list of product IDs

    # Relationship to User
    user = db.relationship('Users', backref=db.backref('cart', lazy=True))
