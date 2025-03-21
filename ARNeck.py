from flask import Blueprint, request, jsonify, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import logging, subprocess

logging.basicConfig(level=logging.DEBUG)

ar_blueprint = Blueprint("ar", __name__)

DATABASE_URL = "mysql+pymysql://root@127.0.0.1:3306/arihant"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class ProcessedImage(Base):
    __tablename__ = 'processed_images'
    png_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.product_id', ondelete='CASCADE'), nullable=False)
    png_image = Column(String(255), nullable=False)

class Product(Base):
    __tablename__ = 'Products'
    product_id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)  # Add a category field

@ar_blueprint.route("/get-product-details", methods=["POST"])
def get_product_details():
    """Fetch image path and category for a given product_id."""
    data = request.json
    product_id = data.get("product_id")

    logging.debug(f"Received product_id: {product_id}")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    image_record = session.query(ProcessedImage).filter_by(product_id=product_id).first()
    product_record = session.query(Product).filter_by(product_id=product_id).first()

    if image_record and product_record:
        logging.debug(f"Image found: {image_record.png_image}, Category: {product_record.category}")
        return jsonify({"image_path": image_record.png_image, "category": product_record.category})
    else:
        logging.debug("Image or category not found in database")
        return jsonify({"error": "Image or category not found"}), 404

@ar_blueprint.route("/start-ar")
def start_ar():
    """Run different scripts based on category."""
    image_path = request.args.get("image")
    category = request.args.get("category")

    if not image_path or not category:
        return "Missing image or category", 400

    logging.debug(f"Starting AR with image: {image_path} and category: {category}")

    # Determine which script to run
    script_to_run = (
    "main.py" if category.lower() == "necklace" else 
    "AREarrings.py" if category.lower() == "earrings" else 
    "ARBracelete.py" if category.lower() == "bracelete" else 
    "ARRing.py" if category.lower() == "ring" else 
    None
)

    subprocess.Popen(["python", script_to_run, image_path])

    return f"AR process started successfully with {script_to_run}!"
