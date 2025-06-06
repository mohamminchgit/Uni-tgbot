# ربات تلگرام تشخیص تصویر

این پروژه یک ربات تلگرامی مبتنی بر پایتون است که برای دریافت، تحلیل و طبقه‌بندی تصاویر با استفاده از مدل‌های هوش مصنوعی طراحی شده است.

## قابلیت‌ها

- دریافت تصویر از کاربر در تلگرام
- پیش‌پردازش تصویر با استفاده از کتابخانه‌های پایتون
- استفاده از مدل جمنای برای:
  - تشخیص و توصیف تصویر
  - طبقه‌بندی اشیاء موجود در تصویر
- ذخیره اطلاعات در پایگاه داده شامل:
  - نام کاربر
  - تاریخ و زمان ارسال
  - تصویر
  - نتیجه تحلیل مدل (برچسب و درصد اطمینان)
- پاسخ به کاربر با نتیجه تحلیل
- امکان دریافت گزارش آماری توسط ادمین

## نیازمندی‌ها

- پایتون 3.9 یا بالاتر
- کتابخانه‌های مورد نیاز در فایل `requirements.txt`
- کلید API جمنای (Google Gemini API)

## نصب و راه‌اندازی

1. کلون کردن مخزن:
```
git clone https://github.com/username/telegram-image-analysis-bot.git
cd telegram-image-analysis-bot
```

2. ایجاد و فعال‌سازی محیط مجازی:
```
python -m venv venv
# در ویندوز
venv\Scripts\activate
# در لینوکس و مک
source venv/bin/activate
```

3. نصب وابستگی‌ها:
```
pip install -r requirements.txt
```

4. کپی فایل `.env.example` به `.env` و ویرایش آن:
```
cp .env.example .env
```

5. ویرایش فایل `.env` و تنظیم توکن ربات تلگرام و کلید API جمنای:
```
TELEGRAM_TOKEN=your_telegram_token_here
GEMINI_API_KEY=your_gemini_api_key_here
MODEL_TYPE=gemini
```

6. اجرای ربات:
```
python -m bot.main
```

## دریافت کلید API جمنای

برای استفاده از مدل جمنای، نیاز به یک کلید API دارید. برای دریافت آن:

1. به [Google AI Studio](https://makersuite.google.com/) بروید
2. وارد حساب گوگل خود شوید
3. به بخش "API Key" بروید
4. یک کلید API جدید ایجاد کنید
5. کلید را در فایل `.env` در متغیر `GEMINI_API_KEY` قرار دهید

## ساختار پروژه

```
my_telegram_bot/
│
├── bot/
│   ├── handlers/         # هندلرهای تلگرام
│   ├── services/         # سرویس‌های مختلف مثل دیتابیس و مدل هوش مصنوعی
│   ├── models/           # مدل‌های داده
│   ├── utils/            # توابع کمکی
│   └── main.py           # نقطه شروع ربات
│
├── config/               # تنظیمات کلی
├── images/               # محل ذخیره تصاویر دریافتی
├── .env                  # متغیرهای محیطی
├── .env.example          # نمونه متغیرهای محیطی
├── requirements.txt      # وابستگی‌ها
└── README.md             # این فایل
```

## دستورات ربات

- `/start` - شروع ربات و دریافت پیام خوش‌آمدگویی
- `/help` - نمایش راهنما
- `/history` - مشاهده تاریخچه تحلیل‌ها
- `/stats` - مشاهده آمار (فقط برای ادمین‌ها)

## توسعه و مشارکت

توسعه‌دهندگان می‌توانند با انجام مراحل زیر در پروژه مشارکت کنند:

1. Fork کردن مخزن
2. ایجاد یک شاخه جدید (`git checkout -b feature/amazing-feature`)
3. Commit کردن تغییرات (`git commit -m 'Add some amazing feature'`)
4. Push کردن به شاخه (`git push origin feature/amazing-feature`)
5. ایجاد یک Pull Request 