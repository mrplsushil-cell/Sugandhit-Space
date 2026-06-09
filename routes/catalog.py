from flask import Blueprint, render_template, request, jsonify, session
from models import db, Plant, ReviewRating
from flask_login import current_user

catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    
    query = Plant.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            Plant.name.ilike(f'%{search}%') | 
            Plant.description.ilike(f'%{search}%')
        )
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(Plant.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Plant.price.desc())
    else:
        query = query.order_by(Plant.name.asc())
    
    plants = query.paginate(page=page, per_page=12)
    categories = db.session.query(Plant.category).filter_by(is_active=True).distinct().all()
    
    return render_template('catalog/index.html',
                         plants=plants,
                         categories=[c[0] for c in categories if c[0]],
                         selected_category=category,
                         search_query=search,
                         sort_by=sort_by)

@catalog_bp.route('/<int:plant_id>')
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    # Get reviews
    reviews = ReviewRating.query.filter_by(plant_id=plant_id).all()
    
    # Get related plants (same category)
    related_plants = Plant.query.filter(
        Plant.category == plant.category,
        Plant.id != plant_id,
        Plant.is_active == True
    ).limit(4).all()
    
    avg_rating = 0
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    
    return render_template('catalog/plant_detail.html',
                         plant=plant,
                         reviews=reviews,
                         avg_rating=avg_rating,
                         related_plants=related_plants)

@catalog_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    plant_id = data.get('plant_id')
    quantity = data.get('quantity', 1)
    
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'success': False, 'message': 'Plant not found'}), 404
    
    if not quantity or quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    
    if 'cart' not in session:
        session['cart'] = {}
    
    plant_key = str(plant_id)
    
    if plant_key in session['cart']:
        session['cart'][plant_key]['quantity'] += quantity
    else:
        session['cart'][plant_key] = {
            'name': plant.name,
            'price': float(plant.price),
            'quantity': quantity,
            'image': plant.image
        }
    
    session.modified = True
    
    cart_count = sum(item['quantity'] for item in session['cart'].values())
    
    return jsonify({
        'success': True,
        'message': f'{plant.name} added to cart!',
        'cart_count': cart_count
    })

@catalog_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    
    total_amount = 0
    cart_items = []
    
    for plant_id, item in cart.items():
        item_total = item['price'] * item['quantity']
        total_amount += item_total
        cart_items.append({
            'plant_id': plant_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'total': item_total
        })
    
    return render_template('catalog/cart.html',
                         cart_items=cart_items,
                         total_amount=total_amount)

@catalog_bp.route('/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    plant_id = str(data.get('plant_id'))
    quantity = data.get('quantity', 0)
    
    if 'cart' not in session:
        return jsonify({'success': False}), 404
    
    if quantity <= 0:
        if plant_id in session['cart']:
            del session['cart'][plant_id]
    else:
        if plant_id in session['cart']:
            session['cart'][plant_id]['quantity'] = quantity
    
    session.modified = True
    return jsonify({'success': True})

@catalog_bp.route('/cart/remove/<plant_id>', methods=['POST'])
def remove_from_cart(plant_id):
    if 'cart' in session and str(plant_id) in session['cart']:
        del session['cart'][str(plant_id)]
        session.modified = True
    
    return jsonify({'success': True})

@catalog_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    session.modified = True
    return jsonify({'success': True})

@catalog_bp.route('/review/<int:plant_id>', methods=['POST'])
def add_review(plant_id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Please login to add a review'}), 401
    
    data = request.get_json()
    rating = data.get('rating')
    review_text = data.get('review_text', '')
    
    if not rating or rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Invalid rating'}), 400
    
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'success': False, 'message': 'Plant not found'}), 404
    
    review = ReviewRating(
        user_id=current_user.id,
        plant_id=plant_id,
        rating=rating,
        review_text=review_text
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Review added successfully!'})
