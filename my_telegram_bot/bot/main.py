import logging
import os
from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from config import settings
from bot.handlers.start import start_command, help_command, history_command, stats_command
from bot.handlers.other import photo_handler, text_handler, unknown_command
from bot.utils.logger import setup_logger

# راه‌اندازی سیستم لاگ
logger = setup_logger()

async def initialize_bot():
    """راه‌اندازی و پیکربندی ربات"""
    # بررسی توکن
    if not settings.telegram_token:
        logger.error("توکن تلگرام تنظیم نشده است! لطفاً فایل تنظیمات را بررسی کنید.")
        return None
    
    # ایجاد برنامه
    application = Application.builder().token(settings.telegram_token).build()
    
    # ذخیره آی‌دی ادمین‌ها در داده‌های ربات
    application.bot_data["admin_ids"] = settings.admin_ids
    
    # ثبت هندلرهای دستورات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # ثبت هندلر تصاویر
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    
    # ثبت هندلر متن‌ها
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    # ثبت هندلر دستورات ناشناخته
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # ثبت خطاها
    application.add_error_handler(error_handler)
    
    return application

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاهای ربات"""
    logger.error(f"خطا در حین پردازش آپدیت: {context.error}")
    
    # اگر آپدیت معتبر باشد و پیام داشته باشد، به کاربر اطلاع می‌دهیم
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "متأسفانه خطایی رخ داد. لطفاً بعداً دوباره تلاش کنید."
        )

def main():
    """تابع اصلی برنامه"""
    try:
        # اطمینان از وجود پوشه‌های مورد نیاز
        os.makedirs(settings.images_dir, exist_ok=True)
        
        # ایجاد و اجرای برنامه
        app = Application.builder().token(settings.telegram_token).build()
        
        # ذخیره آی‌دی ادمین‌ها در داده‌های ربات
        app.bot_data["admin_ids"] = settings.admin_ids
        
        # ثبت هندلرهای دستورات
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("history", history_command))
        app.add_handler(CommandHandler("stats", stats_command))
        
        # ثبت هندلر تصاویر
        app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        
        # ثبت هندلر متن‌ها
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        
        # ثبت هندلر دستورات ناشناخته
        app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
        
        # ثبت خطاها
        app.add_error_handler(error_handler)
        
        # گرفتن و نمایش نام کاربری ربات
        async def log_bot_info(application):
            bot_info = await application.bot.get_me()
            logger.info(f"ربات با نام کاربری @{bot_info.username} راه‌اندازی شد")
        
        app.post_init = log_bot_info
        
        # شروع پردازش پیام‌ها با API جدید
        logger.info("در حال شروع ربات...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"خطای اصلی برنامه: {str(e)}")

if __name__ == "__main__":
    main() 