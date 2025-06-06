from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from config import settings
from bot.models.user import Base, User, ImageAnalysis
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.init_db()
    
    def init_db(self):
        """اتصال به دیتابیس و ایجاد جداول در صورت لزوم"""
        try:
            self.engine = create_engine(
                settings.db_connection_string,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30
            )
            self.Session = sessionmaker(bind=self.engine)
            
            # ایجاد جداول در صورت عدم وجود
            Base.metadata.create_all(self.engine)
            logger.info(f"اتصال به دیتابیس {settings.db_type} با موفقیت انجام شد")
        except Exception as e:
            logger.error(f"خطا در اتصال به دیتابیس: {str(e)}")
            raise
    
    def get_session(self):
        """ایجاد یک نشست دیتابیس جدید"""
        return self.Session()
    
    def get_or_create_user(self, user_id, username=None, first_name=None, last_name=None):
        """دریافت کاربر از دیتابیس یا ایجاد آن در صورت عدم وجود"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                user = User(
                    user_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)
                session.commit()
                logger.info(f"کاربر جدید ایجاد شد: {user_id}")
            return user
        except Exception as e:
            session.rollback()
            logger.error(f"خطا در ایجاد یا دریافت کاربر: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_image_analysis(self, user_id, file_path, file_id, label, confidence):
        """ذخیره نتیجه تحلیل تصویر در دیتابیس"""
        session = self.get_session()
        try:
            image_analysis = ImageAnalysis(
                user_id=user_id,
                file_path=file_path,
                file_id=file_id,
                label=label,
                confidence=confidence
            )
            session.add(image_analysis)
            session.commit()
            logger.info(f"تحلیل تصویر ذخیره شد: {file_path}")
            return image_analysis.id
        except Exception as e:
            session.rollback()
            logger.error(f"خطا در ذخیره تحلیل تصویر: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_user_analyses(self, user_id, limit=10):
        """دریافت تحلیل‌های اخیر کاربر"""
        session = self.get_session()
        try:
            analyses = session.query(ImageAnalysis)\
                .filter(ImageAnalysis.user_id == user_id)\
                .order_by(ImageAnalysis.created_at.desc())\
                .limit(limit).all()
            return analyses
        except Exception as e:
            logger.error(f"خطا در دریافت تحلیل‌های کاربر: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_statistics(self):
        """دریافت آمار برای ادمین"""
        session = self.get_session()
        try:
            total_users = session.query(User).count()
            total_analyses = session.query(ImageAnalysis).count()
            
            # دریافت شایع‌ترین برچسب‌ها
            # این کوئری می‌تواند برای انواع مختلف دیتابیس متفاوت باشد
            # اینجا از سینتکس عمومی استفاده می‌کنیم
            if total_analyses > 0:
                # در صورتی که تحلیلی وجود داشته باشد
                top_labels_query = session.query(
                    ImageAnalysis.label, 
                    func.count(ImageAnalysis.id).label("count")
                ).group_by(ImageAnalysis.label)\
                .order_by(func.count(ImageAnalysis.id).desc())\
                .limit(5).all()
                
                top_labels = []
                for label, count in top_labels_query:
                    top_labels.append((label or "بدون برچسب", count))
            else:
                # در صورتی که هیچ تحلیلی وجود نداشته باشد
                top_labels = []
            
            stats = {
                "total_users": total_users,
                "total_analyses": total_analyses,
                "top_labels": top_labels
            }
            
            logger.info(f"آمار دریافت شد: {stats}")
            return stats
        except Exception as e:
            logger.error(f"خطا در دریافت آمار: {str(e)}")
            # حتی در صورت خطا، آمار پایه را برمی‌گردانیم
            return {
                "total_users": 0,
                "total_analyses": 0,
                "top_labels": []
            }
        finally:
            session.close()

# ایجاد یک نمونه از سرویس دیتابیس برای استفاده در سایر ماژول‌ها
db_service = DatabaseService() 