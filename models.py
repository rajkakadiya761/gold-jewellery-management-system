# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    size = db.Column(
        db.Enum('small', 'medium', 'large', name='size_enum'),
        nullable=False
    )
    category = db.Column(
        db.Enum('ring', 'necklace', 'earring', 'bracelet', name='category_enum'),
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

