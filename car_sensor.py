import serial
import time
import winsound

# تأكد من تغيير 'COM3' للمنفذ الصح عندك
ser = serial.Serial('COM3', 9600, timeout=0.1)
time.sleep(2)

BEEP_FREQUENCY = 1500  
BEEP_DURATION = 100    # قللنا مدة التيت شوية عشان تظبط مع السرعات العالية

while True:
    # تنظيف الطابور عشان ناخد أحدث قراءة وصلت حالاً
    ser.reset_input_buffer()
    time.sleep(0.05) # انتظار صغير جداً لتجميع قراءة جديدة
    
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        try:
            distance = float(line)
            
            # فلتر لو السنسور حدف قراءة غلط أو سالبة
            if distance <= 0 or distance > 400:
                continue
                
            print(f"المسافة الحالية: {distance:.1f} سم")
            
            # 1. المنطقة الآمنة
            if distance > 250:
                print("الوضع آمن")
                time.sleep(0.2)
                
            # 2. منطقة الاقتراب (الصوت المنتظم المتسارع)
            elif 100 < distance <= 250:
                # معادلة خطية دقيقة لحساب الانتظار بناءً على المسافة
                delay_time = ((distance - 100) / 150) * 0.5 + 0.05
                print(f"تحذير: اقتراب! الفاصل: {delay_time:.2f} ثانية")
                
                winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION)
                time.sleep(delay_time)
                
            # 3. منطقة الخطر الشديد
            elif distance <= 100:
                print("خطر: توقف فوراً!!!")
                winsound.Beep(BEEP_FREQUENCY, 150)
                time.sleep(0.05)
                
        except ValueError:
            pass