import os
import uuid
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from app.products import product_bp
from app.products.forms import ProductForm

def get_db():
    return TinyDB('data/products.json')

def save_image(file):
    if not file:
        return None
    ext = os.path.splitext(secure_filename(file.filename))[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, filename))
    return f"uploads/{filename}"

@product_bp.route("/")
def all_products():
    db = get_db()
    products = db.all()
    return render_template("products/products.html", products=products)

@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    db = get_db()
    Product = Query()
    product = db.get(Product.id == product_id)
    if not product:
        abort(404)
    return render_template("products/detail_product.html", product=product)

@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        db = get_db()
        # Генерація нового унікального id
        existing_ids = [p['id'] for p in db.all() if 'id' in p]
        new_id = max(existing_ids, default=0) + 1
        
        img_path = save_image(form.image.data)
        
        new_product = {
            "id": new_id,
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": int(form.quantity.data),
            "image": img_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.insert(new_product)
        flash(f"Товар '{form.name.data}' успішно додано!", "success")
        return redirect(url_for('products.all_products'))
        
    return render_template("products/product_form.html", form=form, title="Додати товар")

@product_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    db = get_db()
    Product = Query()
    product = db.get(Product.id == product_id)
    if not product:
        abort(404)

    form = ProductForm(data=product)
    if form.validate_on_submit():
        updated_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": int(form.quantity.data)
        }
        # Якщо користувач завантажив нове фото — замінюємо, інакше лишаємо старе
        if form.image.data:
            updated_data["image"] = save_image(form.image.data)

        db.update(updated_data, Product.id == product_id)
        flash("Дані товару успішно оновлено!", "info")
        return redirect(url_for('products.product_detail', product_id=product_id))

    return render_template("products/product_form.html", form=form, title="Редагувати товар", product=product)

@product_bp.route("/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    db = get_db()
    Product = Query()
    product = db.get(Product.id == product_id)
    if not product:
        abort(404)
        
    db.remove(Product.id == product_id)
    flash(f"Товар #{product_id} видалено!", "warning")
    return redirect(url_for('products.all_products'))