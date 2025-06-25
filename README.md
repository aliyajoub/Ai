# نظام التحقق من الهوية باستخدام التعرف على الوجه
# Face Recognition Authentication System

## نظرة عامة | Overview

هذا المشروع عبارة عن نظام للتحقق من الهوية باستخدام تقنية التعرف على الوجه، مصمم للتحكم في الوصول إلى المناطق المقيدة. يستخدم النظام تقنيات رؤية الكمبيوتر والتعلم الآلي للتعرف على الوجوه وتحديد ما إذا كان الشخص مصرحًا له بالدخول.

This project is a face recognition authentication system designed for controlling access to restricted areas. The system uses computer vision and machine learning techniques to recognize faces and determine if a person is authorized for entry.

## المميزات | Features

- **التعرف على الوجه في الوقت الحقيقي** | **Real-time Face Recognition**: اكتشاف ومطابقة الوجوه في الوقت الحقيقي باستخدام تقنيات متقدمة | Detect and match faces in real-time using advanced techniques
- **واجهة ويب سهلة الاستخدام** | **User-friendly Web Interface**: إدارة المستخدمين وعرض سجلات الوصول | Manage users and view access logs
- **لوحة تحكم للمسؤول** | **Admin Dashboard**: إدارة المستخدمين والإعدادات | Manage users and settings
- **تسجيل الأحداث** | **Event Logging**: تسجيل جميع محاولات الوصول للمراجعة الأمنية | Log all access attempts for security review
- **التحكم في الأبواب** | **Door Control**: دعم للتحكم في أجهزة الأبواب الإلكترونية | Support for electronic door control devices
- **إشعارات** | **Notifications**: إشعارات عبر البريد الإلكتروني وتيليجرام للأحداث الأمنية | Email and Telegram notifications for security events

## هيكل المشروع | Project Structure

```
├── face_recognition/              # وحدة التعرف على الوجه | Face recognition module
│   ├── detector.py                # اكتشاف الوجوه في الصور | Face detection in images
│   ├── aligner.py                 # محاذاة الوجوه المكتشفة | Align detected faces
│   ├── embedder.py                # استخراج المتجهات المضمنة للوجوه | Extract face embeddings
│   ├── matcher.py                 # مقارنة المتجهات المضمنة | Compare embeddings
│   └── camera.py                  # التعامل مع الكاميرا | Camera handling
│
├── backend/                       # الخادم المركزي/الباك إند | Backend server
│   ├── app.py                     # تطبيق Flask الرئيسي | Main Flask application
│   ├── models.py                  # نماذج قاعدة البيانات | Database models
│   ├── routes.py                  # مسارات API | API routes
│   ├── auth.py                    # التحقق من الهوية والصلاحيات | Authentication and authorization
│   └── notifications/             # وحدة الإشعارات | Notifications module
│
├── door_control/                  # وحدة التحكم بالباب | Door control module
│   ├── gpio_handler.py            # التعامل مع GPIO | GPIO handling
│   └── relay.py                   # التحكم بالريليه | Relay control
│
├── database/                      # وحدة قاعدة البيانات | Database module
│   ├── db_manager.py              # مدير قاعدة البيانات | Database manager
│   ├── schema.sql                 # مخطط قاعدة البيانات | Database schema
│   └── migrations/                # ترحيلات قاعدة البيانات | Database migrations
│
├── utils/                         # أدوات مساعدة | Utilities
│   ├── logger.py                  # تسجيل الأحداث | Event logging
│   └── helpers.py                 # دوال مساعدة | Helper functions
│
├── admin_dashboard/               # لوحة تحكم المسؤول | Admin dashboard
│   ├── views.py                   # عرض صفحات لوحة التحكم | Dashboard views
│   └── forms.py                   # نماذج لوحة التحكم | Dashboard forms
│
├── templates/                     # قوالب HTML | HTML templates
├── static/                        # ملفات ثابتة (CSS، JS) | Static files (CSS, JS)
├── uploads/                       # مجلد التحميلات | Uploads folder
├── logs/                          # سجلات التطبيق | Application logs
├── tests/                         # اختبارات | Tests
├── config.py                      # إعدادات التطبيق | Application settings
├── .env                           # متغيرات البيئة | Environment variables
└── run.py                         # نقطة بدء التطبيق | Application entry point
```

## متطلبات النظام | System Requirements

- Python 3.8+
- OpenCV
- TensorFlow/Keras
- Flask
- SQLite/PostgreSQL
- dlib (اختياري للكشف المتقدم عن الوجه) | (optional for advanced face detection)

## التثبيت | Installation

1. **استنساخ المستودع** | **Clone the repository**:

```bash
git clone https://github.com/yourusername/face-recognition-auth.git
cd face-recognition-auth
```

2. **إنشاء بيئة افتراضية** | **Create a virtual environment**:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **تثبيت المتطلبات** | **Install requirements**:

```bash
pip install -r requirements.txt
```

4. **تثبيت dlib (اختياري)** | **Install dlib (optional)**:
   - راجع ملف `DLIB_INSTALLATION.md` للحصول على تعليمات التثبيت | See `DLIB_INSTALLATION.md` for installation instructions

5. **إعداد ملف البيئة** | **Set up environment file**:
   - انسخ ملف `.env.example` إلى `.env` وقم بتعديل الإعدادات حسب الحاجة | Copy `.env.example` to `.env` and modify settings as needed

6. **تهيئة قاعدة البيانات** | **Initialize the database**:

```bash
python rebuild_db.py
```

## التشغيل | Running

```bash
python run.py
```

افتح المتصفح على العنوان `http://localhost:5000` | Open your browser at `http://localhost:5000`

## الاستخدام | Usage

1. **تسجيل الدخول كمسؤول** | **Login as admin**:
   - استخدم اسم المستخدم وكلمة المرور الافتراضية: `admin/admin` | Use default username and password: `admin/admin`

2. **إضافة مستخدمين** | **Add users**:
   - انتقل إلى لوحة التحكم > المستخدمين > إضافة مستخدم جديد | Go to Dashboard > Users > Add New User

3. **إضافة صور الوجه** | **Add face images**:
   - انتقل إلى صفحة المستخدم > إضافة صورة وجه | Go to User Page > Add Face Image

4. **اختبار التعرف على الوجه** | **Test face recognition**:
   - انتقل إلى العرض المباشر للكاميرا | Go to Live Camera View

## التكوين | Configuration

يمكن تعديل إعدادات التطبيق في ملف `config.py` وملف `.env` | Application settings can be modified in `config.py` and `.env` file.

## المساهمة | Contributing

نرحب بالمساهمات! يرجى اتباع هذه الخطوات | Contributions are welcome! Please follow these steps:

1. Fork المشروع | Fork the project
2. إنشاء فرع للميزة الخاصة بك | Create your feature branch
3. Commit التغييرات الخاصة بك | Commit your changes
4. Push إلى الفرع | Push to the branch
5. فتح طلب سحب | Open a pull request

## الترخيص | License

هذا المشروع مرخص بموجب رخصة MIT - انظر ملف LICENSE للحصول على التفاصيل | This project is licensed under the MIT License - see the LICENSE file for details.

## الاتصال | Contact

للأسئلة أو الدعم، يرجى التواصل مع [اسمك/بريدك الإلكتروني] | For questions or support, please contact [your name/email].
# نظام الأمن والمراقبة الذكي

هذا النظام يستخدم الذكاء الاصطناعي للكشف عن الأسلحة والتعرف على الوجوه للمراقبة الأمنية.

## المتطلبات

1. Python 3.7 أو أحدث
2. كاميرا ويب
3. ملفات نموذج YOLO (yolov3.weights و yolov3.cfg)

## التثبيت

1. قم بتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

2. قم بتحميل ملفات نموذج YOLO:
- قم بتحميل `yolov3.weights` و `yolov3.cfg` من موقع YOLO الرسمي
- ضع الملفات في نفس مجلد المشروع

## الإعداد

1. قم بتعديل إعدادات البريد الإلكتروني في `security_system.py`:
- `email_from`: عنوان البريد الإلكتروني المرسل
- `email_password`: كلمة مرور البريد الإلكتروني
- `email_to`: عنوان البريد الإلكتروني المستلم

2. قم بتعديل إعدادات API في `security_system.py`:
- `api_url`: عنوان API الخاص بنظام الإنذار

## تدريب النظام على الوجوه

1. قم بإنشاء مجلد للصور التدريبية لكل شخص
2. استخدم الدالة `train_face` لتدريب النظام:
```python
security_system.train_face(person_id, person_name, "path/to/images_folder")
```

## تشغيل النظام

```python
security_system = SecuritySystem()
security_system.run()
```

## الميزات

- الكشف عن الأسلحة باستخدام YOLO
- التعرف على الوجوه
- إرسال تنبيهات عبر البريد الإلكتروني
- إرسال تنبيهات عبر API
- التحكم في الأبواب بناءً على التعرف على الوجوه 
