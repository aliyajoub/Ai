import cv2
import numpy as np
import time
import os
import smtplib
from email.message import EmailMessage
import threading
from ultralytics import YOLO
import requests
import torch
import gc

class SecuritySystem:
    def __init__(self):
        # Initialize basic variables
        self.camera = None
        self.model = None
        self.alarm_active = False
        self.last_alert_time = 0
        self.alert_cooldown = 60  # seconds between alerts
        self.authorized_faces = {}  # dictionary for authorized faces
        self.face_recognizer = None
        self.save_frames = True  # Flag to save frames instead of displaying
        self.frame_save_interval = 5  # Save every 5th frame
        self.output_dir = "output_frames"  # Directory to save frames
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Setup object detection (YOLOv8)
        self.setup_object_detection()
        
        # Setup face recognition
        self.setup_face_recognition()
    
    def setup_object_detection(self):
        try:
            import torch
            # Set memory settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = True
            
            # استخدام نموذج YOLOv8n (النسخة الأصغر والأسرع)
            device = 'cpu'  # استخدام CPU لتجنب مشاكل الذاكرة
            self.model = YOLO('yolov8n.pt').to(device)  # استخدام النموذج الصغير للسرعة
            
            # تعيين اللغة الإنجليزية للإخراج
            self.output_language = "english"
            
            print("YOLO model loaded successfully on CPU")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            try:
                # محاولة تحميل النموذج الصغير كخطة بديلة
                self.model = YOLO('yolov8n.pt').to('cpu')
                print("Smaller YOLO model loaded as fallback")
            except:
                raise Exception("Failed to load any YOLO model")
    
    def setup_face_recognition(self):
        """إعداد نظام التعرف على الوجوه"""
        try:
            print("جاري إعداد نظام التعرف على الوجوه...")
            # يمكنك تنفيذ التعرف على الوجوه هنا في المستقبل
            # على سبيل المثال باستخدام face_recognition أو dlib أو OpenCV
            
            # حاليًا، سنقوم فقط بتهيئة المتغيرات الأساسية
            self.face_recognizer = None  # سيتم استبدالها بنموذج التعرف على الوجوه لاحقًا
            print("تم إعداد نظام التعرف على الوجوه بنجاح")
        except Exception as e:
            print(f"تحذير: فشل في إعداد نظام التعرف على الوجوه: {e}")
            print("سيستمر النظام بدون ميزة التعرف على الوجوه")
            # لا نقوم برفع استثناء هنا للسماح للنظام بالعمل بدون التعرف على الوجوه
    
    def start_camera(self, camera_id=0):
        """بدء تشغيل الكاميرا باستخدام معرف الكاميرا المحدد"""
        try:
            print(f"جاري بدء تشغيل الكاميرا على المنفذ {camera_id}...")
            self.camera = cv2.VideoCapture(camera_id)
            
            # تقليل دقة الكاميرا لتحسين الأداء
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            # تقليل معدل الإطارات لتخفيف الحمل
            self.camera.set(cv2.CAP_PROP_FPS, 10)
            
            if not self.camera.isOpened():
                raise Exception(f"فشل في فتح الكاميرا على المنفذ {camera_id}")
                
            # التحقق من أن الكاميرا تعمل بشكل صحيح
            ret, test_frame = self.camera.read()
            if not ret or test_frame is None:
                raise Exception("فشل في قراءة الإطار من الكاميرا")
                
            print(f"تم بدء تشغيل الكاميرا بنجاح على المنفذ {camera_id}")
            print(f"دقة الإطار: {test_frame.shape[1]}x{test_frame.shape[0]}")
            
        except Exception as e:
            print(f"خطأ في بدء تشغيل الكاميرا: {e}")
            if self.camera is not None:
                self.camera.release()
                self.camera = None
            raise Exception(f"فشل في بدء تشغيل الكاميرا: {e}")

    def process_frame(self, frame):
        # Resize frame to smaller dimensions
        frame = cv2.resize(frame, (320, 240))  # تقليل حجم الإطار
        
        # Convert to RGB for YOLO
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # التنبؤ مع تحسين استخدام الذاكرة
        with torch.no_grad():  # تعطيل حساب التدرج لتوفير الذاكرة
            results = self.model.predict(
                source=rgb_frame,
                imgsz=640,  # حجم الصورة المدخلة
                conf=0.2,   # تخفيض عتبة الثقة لزيادة احتمالية الكشف
                verbose=False,
                max_det=20  # زيادة الحد الأقصى للكشف
            )
        
        weapons_detected = False
        weapons_info = []
    
        # قائمة موسعة من أنواع الأسلحة للبحث عنها
        weapon_types = ["knife", "gun", "rifle", "pistol", "weapon", "firearm", "blade", 
                       "handgun", "shotgun", "revolver", "sword", "dagger", "machete",
                       "scissors", "axe"]
        
        # أرقام الفئات المعروفة للأسلحة في COCO dataset
        weapon_class_ids = [0, 43, 45, 56, 67]  # person, knife, bottle, chair, cell phone
    
        # طباعة جميع الفئات المكتشفة للتشخيص
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = self.model.names[class_id]
                
                # طباعة كل الأشياء المكتشفة للتشخيص
                print(f"Detected: {label} with confidence {confidence:.2f}")
                
                # تحقق من الفئات المشابهة للأسلحة أو الفئات المعروفة
                is_weapon = any(weapon in label.lower() for weapon in weapon_types) or class_id in weapon_class_ids
                
                # للأشخاص والهواتف، نطلب ثقة أعلى لتجنب الإنذارات الخاطئة
                if class_id == 0 and confidence < 0.5:  # person - تخفيض العتبة
                    is_weapon = False
                if class_id == 67 and confidence < 0.5:  # cell phone - تخفيض العتبة
                    is_weapon = False
                    
                # تجربة: اعتبار كل الأشياء المكتشفة كأسلحة مؤقتًا للاختبار
                # is_weapon = True  # أزل التعليق لاختبار رسم الإطارات لكل الأشياء المكتشفة
                    
                if is_weapon:
                    weapons_detected = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
            
                    weapons_info.append({
                        "type": label,
                        "confidence": confidence,
                        "position": (x1, y1, x2 - x1, y2 - y1)
                    })
            
                    # تمييز الأسلحة في الإطار بشكل أكثر وضوحًا
                    color = (0, 0, 255)  # أحمر للأسلحة
                    thickness = 3  # زيادة سمك الإطار
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                    
                    # إضافة خلفية للنص لتحسين الرؤية
                    text = f"{label} {confidence:.2f}"
                    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                    cv2.rectangle(frame, (x1, y1 - text_size[1] - 10), (x1 + text_size[0], y1), color, -1)
                    cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                    
                    print(f"WEAPON DETECTED: {label} with confidence {confidence:.2f}")
            
        # تفعيل الإنذار عند كشف الأسلحة
        current_time = time.time()
        if weapons_detected and (current_time - self.last_alert_time > self.alert_cooldown):
            self.trigger_alarm(weapons_info, [], frame)
            self.last_alert_time = current_time
            print("ALARM TRIGGERED: Weapon detected!")
        
        return frame

    def run(self):
        print("\n" + "=" * 50)
        print("SECURITY SYSTEM STARTED")
        print("Press 'q' to quit")
        print("=" * 50 + "\n")
        
        frame_count = 0
        start_time = time.time()
        last_memory_cleanup = time.time()
        skip_frames = 5  # معالجة إطار واحد من كل 5 إطارات
        
        try:
            while self.camera.isOpened():
                ret, frame = self.camera.read()
                if not ret or frame is None:
                    print("Failed to read frame from camera, trying to reconnect...")
                    time.sleep(1)
                    continue
                
                # تقليل حجم الإطار لتحسين الأداء
                frame = cv2.resize(frame, (320, 240))
                
                # معالجة إطار واحد من كل skip_frames إطارات لتحسين الأداء
                process_this_frame = (frame_count % skip_frames == 0)
                
                if process_this_frame:
                    processed_frame = self.process_frame(frame)
                else:
                    processed_frame = frame
                
                # عرض الإطار على الشاشة
                cv2.imshow("Security System", processed_frame)
                
                # حفظ الإطار في مجلد الإخراج (فقط للإطارات المعالجة)
                if self.save_frames and process_this_frame and frame_count % self.frame_save_interval == 0:
                    output_path = os.path.join(self.output_dir, f"frame_{int(time.time())}_{frame_count}.jpg")
                    cv2.imwrite(output_path, processed_frame)
                
                # تنظيف الذاكرة كل 15 ثانية
                current_time = time.time()
                if current_time - last_memory_cleanup > 15:
                    gc.collect()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                    last_memory_cleanup = current_time
                    print("Memory cleaned")
                
                # حساب وطباعة FPS كل 30 إطار
                frame_count += 1
                if frame_count % 30 == 0:
                    fps = 30 / (time.time() - start_time)
                    print(f"FPS: {fps:.2f}")
                    start_time = time.time()
                
                # انتظار مفتاح للخروج
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("User requested exit")
                    break
                
                # التحقق من وجود إشارة توقف من ملف
                if os.path.exists("stop_signal.txt"):
                    print("Stop signal received")
                    break
                
        except Exception as e:
            print(f"Error in main loop: {e}")
            self.camera.release()
            print("System stopped and resources released")
            try:
                cv2.destroyAllWindows()
            except:
                pass

    def trigger_alarm(self, weapons_info, unauthorized_persons, frame):
        try:
            # حفظ صورة التنبيه
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            alert_filename = f"alert_{timestamp}.jpg"
            cv2.imwrite(alert_filename, frame)
            
            # طباعة معلومات التنبيه باللغة الإنجليزية
            print("\n" + "=" * 50)
            print("SECURITY ALERT!")
            print("=" * 50)
            
            if weapons_info:
                print("Weapons detected:")
                for weapon in weapons_info:
                    print(f"- {weapon['type']} (Confidence: {weapon['confidence']:.2f})")
            
            if unauthorized_persons:
                print("Unauthorized persons detected:")
                for person in unauthorized_persons:
                    print(f"- {person}")
                    
            print(f"Alert image saved as: {alert_filename}")
            print("=" * 50 + "\n")
            
            # يمكن إضافة المزيد من آليات التنبيه هنا (مثل إرسال بريد إلكتروني أو رسالة نصية)
            
        except Exception as e:
            print(f"Error triggering alarm: {e}")
# How to use the system
if __name__ == "__main__":
    # Create security system
    security_system = SecuritySystem()
    
    # Add authorized person (example)
    # security_system.train_face(1, "John Doe", "faces/john")
    
    # Run system
    security_system.run()