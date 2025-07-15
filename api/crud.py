from sqlalchemy.orm import Session
from .models import Message, Detection
from sqlalchemy import func

def get_top_products(db: Session, limit=10):
    return db.query(Detection.detected_object_class, func.count().label("count"))\
             .group_by(Detection.detected_object_class)\
             .order_by(func.count().desc())\
             .limit(limit).all()

def get_channel_activity(db: Session, channel_name: str):
    return db.query(Message.channel, func.count().label("post_count"))\
             .filter(Message.channel == channel_name)\
             .group_by(Message.channel).first()

def search_messages(db: Session, query: str):
    return db.query(Message).filter(Message.message.ilike(f"%{query}%")).all()
