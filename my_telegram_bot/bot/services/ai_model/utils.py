import os
import json
import logging
import requests
from config import settings

logger = logging.getLogger(__name__)

def get_imagenet_labels():
    """دریافت برچسب‌های مدل ImageNet"""
    # لیست برچسب‌های ImageNet
    labels_path = os.path.join(os.path.dirname(__file__), 'imagenet_labels.json')
    
    # اگر فایل برچسب‌ها وجود نداشت، یک نمونه کوچک ایجاد می‌کنیم
    if not os.path.exists(labels_path):
        # این یک نمونه کوچک از برچسب‌های ImageNet است 
        # در یک پروژه واقعی باید فایل کامل را دانلود کنید
        sample_labels = {
            0: "tench, Tinca tinca",
            1: "goldfish, Carassius auratus",
            2: "great white shark, white shark",
            3: "tiger shark, Galeocerdo cuvieri",
            4: "hammerhead, hammerhead shark",
            5: "electric ray, crampfish",
            6: "stingray",
            7: "cock",
            8: "hen",
            9: "ostrich, Struthio camelus",
            10: "brambling, Fringilla montifringilla",
            # ... و غیره
        }
        
        # ذخیره نمونه برچسب‌ها در فایل
        try:
            with open(labels_path, 'w', encoding='utf-8') as f:
                json.dump(sample_labels, f, ensure_ascii=False, indent=4)
            logger.info(f"فایل نمونه برچسب‌ها ایجاد شد: {labels_path}")
        except Exception as e:
            logger.error(f"خطا در ایجاد فایل برچسب‌ها: {str(e)}")
    
    # خواندن برچسب‌ها از فایل
    try:
        with open(labels_path, 'r', encoding='utf-8') as f:
            labels = json.load(f)
        # تبدیل کلیدها به عدد (در صورتی که به صورت رشته ذخیره شده باشند)
        labels = {int(k): v for k, v in labels.items()}
        return labels
    except Exception as e:
        logger.error(f"خطا در خواندن برچسب‌ها: {str(e)}")
        # در صورت خطا، یک دیکشنری خالی برمی‌گردانیم
        return {}

def create_imagenet_labels_file():
    """ایجاد فایل برچسب‌های ImageNet"""
    # این تابع در یک پروژه واقعی می‌تواند برچسب‌ها را از اینترنت دانلود کند
    # اما برای ساده‌سازی، فقط چند برچسب نمونه ایجاد می‌کنیم
    sample_labels = {i: f"label_{i}" for i in range(1000)}
    
    labels_path = os.path.join(os.path.dirname(__file__), 'imagenet_labels.json')
    try:
        with open(labels_path, 'w', encoding='utf-8') as f:
            json.dump(sample_labels, f, ensure_ascii=False, indent=4)
        logger.info(f"فایل برچسب‌های ImageNet ایجاد شد: {labels_path}")
    except Exception as e:
        logger.error(f"خطا در ایجاد فایل برچسب‌های ImageNet: {str(e)}")

def translate_label(label, target_lang='fa'):
    """ترجمه برچسب (اختیاری برای پروژه‌های پیشرفته‌تر)"""
    # این تابع می‌تواند در نسخه‌های پیشرفته‌تر پروژه پیاده‌سازی شود
    # برای مثال، با استفاده از یک API ترجمه یا یک دیکشنری از پیش تعریف شده
    # در اینجا فقط برچسب اصلی را برمی‌گردانیم
    return label

def format_gemini_response(response_text):
    """فرمت‌بندی پاسخ جمنای برای نمایش به کاربر"""
    try:
        # اگر پاسخ فرمت JSON داشته باشد
        import re
        json_match = re.search(r'({.*})', response_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(1)
            result_dict = json.loads(json_str)
            
            formatted_response = "🔍 *نتایج تحلیل تصویر:*\n\n"
            
            # افزودن شیء اصلی
            if 'main_object' in result_dict:
                main_obj = result_dict['main_object']
                formatted_response += f"📌 *شیء اصلی:* {main_obj.get('label', 'نامشخص')}\n"
                formatted_response += f"   اطمینان: {main_obj.get('confidence', 'نامشخص')}\n\n"
            
            # افزودن سایر اشیاء
            if 'other_objects' in result_dict and result_dict['other_objects']:
                formatted_response += "✨ *سایر اشیاء شناسایی شده:*\n"
                for i, obj in enumerate(result_dict['other_objects'], 1):
                    formatted_response += f"  {i}. {obj.get('label', 'نامشخص')} "
                    formatted_response += f"({obj.get('confidence', 'نامشخص')})\n"
            
            return formatted_response
        else:
            # اگر پاسخ فرمت JSON نداشته باشد، متن خام را برمی‌گردانیم
            return f"🔍 *نتایج تحلیل تصویر:*\n\n{response_text}"
    except Exception as e:
        logger.error(f"خطا در فرمت‌بندی پاسخ جمنای: {str(e)}")
        return response_text

def test_gemini_api_key():
    """تست اعتبار کلید API جمنای"""
    if not settings.gemini_api_key:
        logger.error("کلید API جمنای تنظیم نشده است!")
        return False
    
    try:
        # تست ساده برای بررسی اعتبار کلید API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": "سلام"}]}],
            "generationConfig": {"maxOutputTokens": 50}
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info("کلید API جمنای معتبر است.")
            return True
        else:
            logger.error(f"کلید API جمنای نامعتبر است: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"خطا در تست کلید API جمنای: {str(e)}")
        return False

def enhance_image(image_path):
    """بهبود کیفیت تصویر با استفاده از OpenCV (نمونه)"""
    # این تابع می‌تواند در نسخه‌های پیشرفته‌تر پروژه پیاده‌سازی شود
    # برای بهبود کیفیت تصاویر قبل از تحلیل
    # می‌توان از کتابخانه OpenCV استفاده کرد
    return image_path 