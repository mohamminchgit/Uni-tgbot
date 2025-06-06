import logging
import os
from logging.handlers import RotatingFileHandler
from config import settings

def setup_logger():
    """راه‌اندازی سیستم لاگ"""
    # تبدیل سطح لاگ از رشته به ثابت
    log_level_str = settings.log_level.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # فرمت لاگ
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # پیکربندی اصلی
    logging.basicConfig(
        level=log_level,
        format=log_format,
    )
    
    # مسیر فایل لاگ
    log_file = settings.log_file
    
    # اطمینان از وجود دایرکتوری لاگ
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # افزودن handler فایل چرخشی (با حداکثر 5 فایل 5 مگابایتی)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5 مگابایت
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # افزودن هندلر به logger اصلی
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # ایجاد logger مخصوص برنامه
    logger = logging.getLogger('telegram_bot')
    logger.setLevel(log_level)
    
    # تنظیم سطح لاگ کتابخانه‌های خارجی
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    
    logger.info("سیستم لاگ راه‌اندازی شد")
    return logger 