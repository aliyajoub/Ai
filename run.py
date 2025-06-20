from security_system import SecuritySystem
import cv2
import time
import os
import threading

def check_camera():
    """Check available cameras"""
    print("جاري التحقق من الكاميرات المتاحة...")
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"تم العثور على كاميرا في المنفذ {i}")
                cap.release()
                return i
            cap.release()
    return 0  # Use default port if no camera found

# أضف هذا الاستيراد في بداية الملف
import tkinter as tk

def create_control_ui(security_system):
    """Create a simple UI for controlling the security system"""
    root = tk.Tk()
    root.title("نظام الأمان")
    root.geometry("300x200")
    
    def exit_app():
        with open("stop_signal.txt", "w") as f:
            f.write("stop")
        print("تم إرسال إشارة التوقف")
        root.destroy()
    
    def train_face():
        print("وضع تدريب الوجه (غير مدعوم في هذا الإصدار)")
    
    def save_alert():
        print("تم طلب حفظ صورة التنبيه")
    
    # Create buttons
    exit_btn = tk.Button(root, text="خروج (q)", command=exit_app)
    exit_btn.pack(pady=10)
    
    train_btn = tk.Button(root, text="تدريب وجه جديد (t)", command=train_face)
    train_btn.pack(pady=10)
    
    save_btn = tk.Button(root, text="حفظ صورة التنبيه (s)", command=save_alert)
    save_btn.pack(pady=10)
    
    # Start the UI loop in a separate thread
    def ui_thread():
        root.mainloop()
    
    ui_thread = threading.Thread(target=ui_thread)
    ui_thread.daemon = True
    ui_thread.start()
    
    return root

# ثم استبدل تشغيل keyboard_listener في الدالة main بـ:
# create_control_ui(security_system)
def keyboard_listener():
    """Listen for keyboard events"""
    print("اضغط 'q' للخروج، 't' لتدريب وجه جديد، 's' لحفظ صورة التنبيه")
    
    def on_key_press(key):
        if key.name == 'q':
            # Create a signal file to stop the main loop
            with open("stop_signal.txt", "w") as f:
                f.write("stop")
            print("تم إرسال إشارة التوقف")
            return False  # Stop listener
        elif key.name == 't':
            print("وضع تدريب الوجه (غير مدعوم في هذا الإصدار)")
        elif key.name == 's':
            print("تم طلب حفظ صورة التنبيه")
    
    # Start listening for key presses
    keyboard.on_press(on_key_press)
    keyboard.wait('q')  # Wait until 'q' is pressed

def file_based_control():
    """Monitor a control file for commands"""
    control_file = "control_commands.txt"
    # Create empty control file if it doesn't exist
    if not os.path.exists(control_file):
        with open(control_file, "w") as f:
            f.write("")
    
    last_modified = os.path.getmtime(control_file)
    
    while True:
        time.sleep(1)  # Check every second
        
        # Check if file was modified
        current_modified = os.path.getmtime(control_file)
        if current_modified > last_modified:
            last_modified = current_modified
            
            # Read command from file
            with open(control_file, "r+") as f:
                cmd = f.read().strip().lower()
                # Clear the file
                f.seek(0)
                f.truncate()
            
            if cmd == 'q':
                with open("stop_signal.txt", "w") as f:
                    f.write("stop")
                print("تم إرسال إشارة التوقف")
                break
            elif cmd == 't':
                print("وضع تدريب الوجه (غير مدعوم في هذا الإصدار)")
            elif cmd == 's':
                print("تم طلب حفظ صورة التنبيه")

def main():
    import torch
    import gc
    security_system = None
    
    # Remove stop signal file if it exists
    if os.path.exists("stop_signal.txt"):
        os.remove("stop_signal.txt")
    
    try:
        # Free memory before starting
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        camera_id = check_camera()
        print(f"استخدام الكاميرا على المنفذ {camera_id}")
        
        security_system = SecuritySystem()
        security_system.start_camera(camera_id)
        
        print("""
        أوامر التحكم (اكتب الأمر في ملف control_commands.txt):
        1. اكتب 'q' للخروج
        2. اكتب 't' لتدريب وجه جديد
        3. اكتب 's' لحفظ صورة التنبيه
        """)
        
        # استخدام التحكم القائم على الملفات بدلاً من keyboard_listener
        control_thread = threading.Thread(target=file_based_control)
        control_thread.daemon = True
        control_thread.start()
        
        security_system.run()
        
    except Exception as e:
        print(f"خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure proper cleanup
        if security_system is not None:
            if hasattr(security_system, 'camera') and security_system.camera is not None:
                security_system.camera.release()
            if hasattr(security_system, 'model'):
                del security_system.model
        # Final memory cleanup
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        # Remove stop signal file
        if os.path.exists("stop_signal.txt"):
            os.remove("stop_signal.txt")

if __name__ == "__main__":
    main()