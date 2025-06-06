from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

Base = declarative_base()

class User(Base):
    """مدل داده کاربر تلگرام"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    last_activity = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username})>"


class ImageAnalysis(Base):
    """مدل داده تحلیل تصویر"""
    __tablename__ = 'image_analyses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    file_path = Column(String(255), nullable=False)
    file_id = Column(String(255), nullable=True)  # آی‌دی فایل در تلگرام
    label = Column(String(100), nullable=True)    # برچسب تشخیص داده شده
    confidence = Column(String(20), nullable=True) # درصد اطمینان
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<ImageAnalysis(id={self.id}, user_id={self.user_id}, label={self.label})>" 