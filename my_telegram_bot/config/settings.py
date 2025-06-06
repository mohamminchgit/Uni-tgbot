import os
from pathlib import Path

# TELEGRAM_TOKEN=7584204554:AAFoH72raVZk-dhl7YZ9iLN3SLFwfp8J7TE
# DB_TYPE=7534724248
# DB_CONNECTION_STRING=sqlite:///db.sqlite3
# MODEL_TYPE=mobilenet
# CUSTOM_MODEL_PATH=
# ADMIN_IDS=87654321
# LOG_LEVEL=INFO
# GEMINI_API_KEY=AIzaSyD-mz2hJzAdu8lroCaQtQR1eOPm9jXAmgk
# MODEL_TYPE=gemini


# تنظیمات پایه
BASE_DIR = Path(__file__).resolve().parent.parent

# تنظیمات تلگرام - لطفاً این مقدار را تغییر دهید
TELEGRAM_TOKEN = "7584204554:AAFoH72raVZk-dhl7YZ9iLN3SLFwfp8J7TE"

# تنظیمات دیتابیس
DB_TYPE = "sqlite"
DB_CONNECTION_STRING = f"sqlite:///{BASE_DIR}/db.sqlite3"

# تنظیمات مدل هوش مصنوعی
MODEL_TYPE = "gemini"
CUSTOM_MODEL_PATH = ""

# تنظیمات API جمنای - لطفاً این مقدار را تغییر دهید
GEMINI_API_KEY = "AIzaSyD-mz2hJzAdu8lroCaQtQR1eOPm9jXAmgk"

# مسیر ذخیره‌سازی تصاویر
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# تنظیمات لاگ
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, "bot.log")

# آی‌دی ادمین‌ها (برای گزارش‌گیری)
ADMIN_IDS = [87654321]  # لطفاً این مقدار را با آی‌دی تلگرام خود جایگزین کنید

# کلاس تنظیمات
class Settings:
    def __init__(self):
        self.telegram_token = TELEGRAM_TOKEN
        self.db_type = DB_TYPE
        self.db_connection_string = DB_CONNECTION_STRING
        self.model_type = MODEL_TYPE
        self.custom_model_path = CUSTOM_MODEL_PATH
        self.gemini_api_key = GEMINI_API_KEY
        self.images_dir = IMAGES_DIR
        self.log_level = LOG_LEVEL
        self.log_file = LOG_FILE
        self.admin_ids = ADMIN_IDS
        self.base_dir = BASE_DIR

settings = Settings() 