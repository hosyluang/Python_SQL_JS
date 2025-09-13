from flask import Blueprint, render_template, session, request, jsonify
from db_config import get_db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart(): 
    return render_template('layout/cart.html')

@cart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    db = get_db()
    product = db.execute("SELECT * FROM product WHERE id = ?", (product_id,)).fetchone()
    cart = session.get('cart', [])
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['qty'] += 1
            found = True
            break
    if not found:
        product_data = {
            'price': product['price'],
            'image': product['image'],
            'name': product['title'],
            'qty': 1,
            'id': product['id'],
        }
        cart.append(product_data)
    session['cart'] = cart

    return jsonify({'status': 'success', 'product': session['cart']})


@cart_bp.route('/show-cart')
def show_cart():
    cart = session.get('cart', [])
    return render_template('layout/cart.html', products=cart)
