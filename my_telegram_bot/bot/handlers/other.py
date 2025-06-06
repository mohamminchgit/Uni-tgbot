import os
import uuid
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.db_service import db_service
from bot.services.ai_model import ImageClassifier
from bot.services.ai_model.utils import format_gemini_response
import logging
from config import settings

logger = logging.getLogger(__name__)

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش تصاویر ارسالی کاربر"""
    user = update.effective_user
    user_id = user.id
    
    # ارسال پیام در حال پردازش
    processing_message = await update.message.reply_text("در حال پردازش تصویر... ⏳")
    
    try:
        # دریافت تصویر با بالاترین کیفیت
        photo = update.message.photo[-1]
        file_id = photo.file_id
        
        # دانلود فایل
        file = await context.bot.get_file(file_id)
        
        # ایجاد نام منحصر به فرد برای ذخیره تصویر
        file_extension = "jpg"  # معمولاً تلگرام تصاویر را با فرمت JPG می‌فرستد
        filename = f"{user_id}_{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(settings.images_dir, filename)
        
        # اطمینان از وجود دایرکتوری برای ذخیره تصاویر
        os.makedirs(settings.images_dir, exist_ok=True)
        
        # دانلود و ذخیره تصویر
        await file.download_to_drive(file_path)
        logger.info(f"تصویر ذخیره شد: {file_path}")
        
        # تحلیل تصویر با استفاده از مدل هوش مصنوعی
        from bot.services.ai_model.model import image_classifier
        results = image_classifier.classify_image(file_path)
        
        if not results:
            await processing_message.edit_text("متأسفانه نتوانستم چیزی در این تصویر تشخیص دهم. لطفاً تصویر دیگری ارسال کنید.")
            return
        
        # ذخیره نتیجه در دیتابیس
        top_result = results[0]
        db_service.save_image_analysis(
            user_id=user_id,
            file_path=file_path,
            file_id=file_id,
            label=top_result['label'],
            confidence=top_result['confidence']
        )
        
        # آماده‌سازی پاسخ
        if settings.model_type == 'gemini':
            # برای مدل جمنای، فرمت پاسخ متفاوت است
            response = ""
            for result in results:
                if 'label' in result and len(result['label']) > 100:
                    # اگر برچسب بسیار طولانی باشد، احتمالاً پاسخ کامل مدل است
                    raw_response = result['label']
                    response = format_gemini_response(raw_response)
                    break
            
            # اگر پاسخ خاصی نداشتیم، از فرمت معمول استفاده می‌کنیم
            if not response:
                response = "🔍 *نتایج تحلیل تصویر:*\n\n"
                for result in results[:3]:  # نمایش 3 نتیجه برتر
                    response += f"• {result['label']}\n  اطمینان: {result['confidence']}\n\n"
        else:
            # فرمت پاسخ برای مدل‌های دیگر
            response = "🔍 *نتایج تحلیل تصویر:*\n\n"
            for result in results[:3]:  # نمایش 3 نتیجه برتر
                response += f"• {result['label']}\n  اطمینان: {result['confidence']}\n\n"
        
        response += "می‌توانید تصویر دیگری ارسال کنید یا با استفاده از /history تاریخچه خود را ببینید."
        
        # ارسال پاسخ
        await processing_message.edit_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"خطا در پردازش تصویر: {str(e)}")
        await processing_message.edit_text(
            "متأسفانه در پردازش تصویر خطایی رخ داد. لطفاً دوباره تلاش کنید یا تصویر دیگری ارسال کنید."
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به پیام‌های متنی عادی"""
    text = update.message.text
    
    # اگر پیام با / شروع شود، آن را نادیده می‌گیریم (احتمالاً دستوری است که هندلر ندارد)
    if text.startswith('/'):
        return
    
    response = (
        "برای استفاده از ربات، لطفاً یک تصویر ارسال کنید. 📸\n\n"
        "من می‌توانم اشیاء، حیوانات، گیاهان و موارد دیگر را در تصاویر تشخیص دهم.\n\n"
        "برای مشاهده راهنما، از دستور /help استفاده کنید."
    )
    
    await update.message.reply_text(response)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستورات ناشناخته"""
    await update.message.reply_text(
        "متأسفانه این دستور را نمی‌شناسم. برای مشاهده لیست دستورات، /help را وارد کنید."
    ) 