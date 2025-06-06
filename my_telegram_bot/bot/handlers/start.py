from telegram import Update
from telegram.ext import ContextTypes
from bot.services.db_service import db_service
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخگویی به دستور /start"""
    user = update.effective_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    
    # ذخیره یا به‌روزرسانی اطلاعات کاربر در دیتابیس
    try:
        db_service.get_or_create_user(user_id, username, first_name, last_name)
        logger.info(f"کاربر {user_id} ربات را شروع کرد")
    except Exception as e:
        logger.error(f"خطا در ثبت کاربر: {str(e)}")
    
    # ارسال پیام خوش‌آمدگویی
    welcome_message = (
        f"سلام {first_name}! 👋\n\n"
        "به ربات تشخیص تصویر خوش آمدید! 🤖\n\n"
        "📸 *قابلیت‌های این ربات:*\n"
        "• تشخیص اشیاء در تصاویر\n"
        "• طبقه‌بندی تصاویر\n"
        "• ذخیره نتایج در دیتابیس\n\n"
        "برای شروع، یک تصویر برای من بفرستید تا آن را تحلیل کنم."
    )
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخگویی به دستور /help"""
    help_message = (
        "🔍 *راهنمای استفاده از ربات:*\n\n"
        "• یک تصویر برای ربات ارسال کنید\n"
        "• ربات تصویر را تحلیل و نتیجه را ارسال می‌کند\n"
        "• از دستور /history برای مشاهده تاریخچه تحلیل‌ها استفاده کنید\n\n"
        
        "📋 *دستورات موجود:*\n"
        "/start - شروع مجدد ربات\n"
        "/help - نمایش این راهنما\n"
        "/history - مشاهده تاریخچه تحلیل‌های شما\n"
        "/stats - مشاهده آمار (فقط برای ادمین‌ها آزاد است)\n\n"
        


    )
    
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش تاریخچه تحلیل‌های کاربر"""
    user_id = update.effective_user.id
    
    try:
        # دریافت 5 تحلیل اخیر کاربر
        analyses = db_service.get_user_analyses(user_id, 5)
        
        if not analyses:
            await update.message.reply_text("شما هنوز هیچ تصویری ارسال نکرده‌اید!")
            return
        
        history_message = "📊 *تاریخچه تحلیل‌های شما:*\n\n"
        
        for i, analysis in enumerate(analyses, 1):
            history_message += (
                f"{i}. تاریخ: {analysis.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                f"   تشخیص: {analysis.label}\n"
                f"   اطمینان: {analysis.confidence}\n\n"
            )
        
        await update.message.reply_text(history_message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"خطا در دریافت تاریخچه: {str(e)}")
        await update.message.reply_text("خطایی در دریافت تاریخچه رخ داد. لطفاً بعداً دوباره تلاش کنید.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار برای ادمین‌ها"""
    user_id = update.effective_user.id
    
    # بررسی دسترسی ادمین
    if user_id not in context.bot_data.get("admin_ids", []):
        await update.message.reply_text("شما دسترسی لازم برای این دستور را ندارید.")
        return
    
    try:
        # دریافت آمار از دیتابیس
        stats = db_service.get_statistics()
        
        stats_message = (
            "📈 *آمار ربات:*\n\n"
            f"• تعداد کل کاربران: {stats['total_users']}\n"
            f"• تعداد کل تحلیل‌ها: {stats['total_analyses']}\n\n"
        )
        
        # افزودن بخش برچسب‌های پرتکرار
        if stats.get('top_labels'):
            stats_message += "🔝 *برچسب‌های پرتکرار:*\n"
            for i, (label, count) in enumerate(stats.get('top_labels', []), 1):
                stats_message += f"{i}. {label}: {count} بار\n"
        else:
            stats_message += "🔝 *برچسب‌های پرتکرار:*\n  هنوز هیچ تحلیلی انجام نشده است."
        
        await update.message.reply_text(stats_message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"خطا در دریافت آمار: {str(e)}")
        await update.message.reply_text("خطایی در دریافت آمار رخ داد. لطفاً بعداً دوباره تلاش کنید.") 