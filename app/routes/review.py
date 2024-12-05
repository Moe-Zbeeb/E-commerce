from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Review

# Define blueprint
review_bp = Blueprint('review_bp', __name__, url_prefix='/api/reviews')

# ===============================
# Service 4 - Review Endpoints
# ===============================

# 1. Submit a new review
@review_bp.route('/', methods=['POST'])
def submit_review():
    data = request.get_json()
    try:
        new_review = Review(
            product_id=data['product_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({
            'id': new_review.id,
            'product_id': new_review.product_id,
            'user_id': new_review.user_id,
            'rating': new_review.rating,
            'comment': new_review.comment
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 2. Update a review
@review_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = Review.query.get(review_id)
    if review:
        try:
            review.rating = data.get('rating', review.rating)
            review.comment = data.get('comment', review.comment)
            db.session.commit()
            return jsonify({
                'id': review.id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Review not found'}), 404

# 3. Delete a review
@review_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted successfully'}), 204
    else:
        return jsonify({'error': 'Review not found'}), 404

# 4. Get all reviews for a product
@review_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([
        {
            'id': review.id,
            'user_id': review.user_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews
    ]), 200

# 5. Get all reviews by a user
@review_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': review.id,
            'product_id': review.product_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews
    ]), 200
    
@review_bp.route('/health', methods=['GET'])
def review_health_check():
    """Check if the Review Service is healthy."""
    try:
        # Example: Check database connectivity
        db.session.execute('SELECT 1')
        return {"status": "ok", "service": "Review Service"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500