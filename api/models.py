from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime
from .database import Base

class Message(Base):
    __tablename__ = 'fct_messages'
    id = Column(BigInteger, primary_key=True)
    message = Column(String)
    date = Column(DateTime)
    channel = Column(String)

class Detection(Base):
    __tablename__ = 'fct_image_detections'
    message_id = Column(BigInteger, primary_key=True)
    detected_object_class = Column(String)
    confidence_score = Column(Float)
