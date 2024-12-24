from .user import User
from .reviews import Review
from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod

class ReviewImage(db.Model):
    __tablename__ = 'review_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('review.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    url = db.Column(db.String)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Define the relationship with Review (optional if you need access to the associated review object)
    review = db.relationship('Review', back_populates='review_images') 
    images = db.relationship('ReviewImage', back_populates='review')

   
    def to_dict(self):
        return {
            'id': self.id,
            'review_id': self.review_id,
            'user_id': self.user_id,
            'url': self.restaurant_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'review': self.review.to_dict() if self.review else None,
            'user': self.user.to_dict() if self.user else None
        }