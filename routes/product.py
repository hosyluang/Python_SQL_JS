import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app, session
from db_config import get_db


product_bp = Blueprint('product', __name__)

@product_bp.route('/my-product')
def my_product():
    db = get_db()
    user_id = session.get('user_id')
    products = db.execute('SELECT * FROM product WHERE id_user = ?', (user_id,)).fetchall()
    return render_template('layout/my-product.html', products=products)

@product_bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    ketqua = ""
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        file = request.files.get('image')
        id_user = session.get('user_id')
        db = get_db()
        db.execute('insert into product (title, price, image, id_user) values (?, ?, ?, ?)', (title, price, file.filename, id_user))
        db.commit()
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return redirect(url_for('product.my_product'))
    return render_template('layout/add-product.html', ketqua=ketqua)
@product_bp.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        file = request.files.get('image')
        db.execute('UPDATE product SET title = ?, price = ?, image = ? WHERE id = ?', (title, price, file.filename, id))
        db.commit()
        return redirect(url_for('product.my_product'))
    product = db.execute('SELECT * FROM product WHERE id = ?', (id,)).fetchone()
    return render_template('layout/edit-product.html', product=product)

@product_bp.route('/delete-product/<int:id>')
def delete_product(id):
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('product.my_product'))