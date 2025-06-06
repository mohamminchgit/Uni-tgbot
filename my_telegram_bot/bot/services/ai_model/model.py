import os
import base64
import requests
import logging
from PIL import Image
from io import BytesIO
from config import settings

logger = logging.getLogger(__name__)

class ImageClassifier:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json",
        }
    
    def encode_image_to_base64(self, image_path):
        """تبدیل تصویر به فرمت Base64 برای ارسال به API"""
        try:
            # باز کردن و فشرده‌سازی تصویر برای کاهش حجم
            image = Image.open(image_path)
            
            # تغییر اندازه تصویر برای کاهش حجم (اختیاری)
            max_size = 800
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.LANCZOS)
            
            # تبدیل به Base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG", quality=80)
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return img_str
        except Exception as e:
            logger.error(f"خطا در تبدیل تصویر به Base64: {str(e)}")
            raise
    
    def classify_image(self, image_path):
        """تحلیل تصویر با استفاده از مدل جمنای"""
        try:
            # تبدیل تصویر به Base64
            base64_image = self.encode_image_to_base64(image_path)
            
            # آماده‌سازی درخواست
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "تصویر زیر را تحلیل کن و به من بگو چه چیزی در آن می‌بینی. لطفاً نام شیء اصلی و درصد اطمینان خود را بیان کن و پنج مورد از اشیاء دیگری که در تصویر می‌بینی را با درصد اطمینان فهرست کن. پاسخ را به صورت JSON با فرمت زیر برگردان: {\"main_object\": {\"label\": \"نام شیء\", \"confidence\": \"درصد اطمینان\"}, \"other_objects\": [{\"label\": \"نام شیء\", \"confidence\": \"درصد اطمینان\"}, ...]}"},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }],
                "generation_config": {
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "max_output_tokens": 1024
                }
            }
            
            # ارسال درخواست به API
            url = f"{self.api_url}?key={self.api_key}"
            response = requests.post(url, json=payload, headers=self.headers)
            
            # بررسی پاسخ
            if response.status_code != 200:
                logger.error(f"خطا در درخواست API: {response.status_code} - {response.text}")
                return []
            
            # استخراج پاسخ از JSON
            response_json = response.json()
            
            # استخراج متن پاسخ
            try:
                response_text = response_json['candidates'][0]['content']['parts'][0]['text']
                
                # استخراج بخش JSON از پاسخ (در صورتی که متن اضافی وجود داشته باشد)
                import json
                import re
                
                # تلاش برای پیدا کردن بخش JSON در پاسخ
                json_match = re.search(r'({.*})', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    result_dict = json.loads(json_str)
                else:
                    # اگر کل متن یک JSON معتبر باشد
                    try:
                        result_dict = json.loads(response_text)
                    except:
                        # در صورت خطا، یک ساختار پیش‌فرض برمی‌گردانیم
                        logger.warning("خطا در تجزیه JSON از پاسخ جمنای")
                        return self._format_default_response(response_text)
                
                # فرمت‌بندی نتایج
                results = []
                
                # افزودن شیء اصلی به نتایج
                if 'main_object' in result_dict:
                    main_obj = result_dict['main_object']
                    results.append({
                        'rank': 1,
                        'label': main_obj.get('label', 'نامشخص'),
                        'confidence': main_obj.get('confidence', '0%')
                    })
                
                # افزودن سایر اشیاء به نتایج
                if 'other_objects' in result_dict:
                    for i, obj in enumerate(result_dict['other_objects'], 2):
                        results.append({
                            'rank': i,
                            'label': obj.get('label', 'نامشخص'),
                            'confidence': obj.get('confidence', '0%')
                        })
                
                return results
            except Exception as e:
                logger.error(f"خطا در پردازش پاسخ API: {str(e)}")
                # در صورت خطا، متن کامل پاسخ را برمی‌گردانیم
                return self._format_default_response(response_text)
                
        except Exception as e:
            logger.error(f"خطا در طبقه‌بندی تصویر: {str(e)}")
            raise
    
    def _format_default_response(self, text):
        """ایجاد یک پاسخ پیش‌فرض در صورت خطا در تجزیه JSON"""
        return [{
            'rank': 1,
            'label': text[:100] + ('...' if len(text) > 100 else ''),
            'confidence': 'نامشخص'
        }]

# ایجاد یک نمونه از کلاس برای استفاده در سایر ماژول‌ها
image_classifier = ImageClassifier() 