import RPi.GPIO as GPIO
import time
import cv2

class Servo():
    def __init__(self):
        self.servo_pin = 22
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin,GPIO.OUT)
        self.servo = GPIO.PWM(self.servo_pin,50)
        self.servo.start(7.5)
        try:
            self.servo.ChangeDutyCycle(7.5)
        except KeyboardInterrupt:
            GPIO.cleanup()
        
    def change_position(self, position):
        try:
            self.servo.ChangeDutyCycle(position)
        except KeyboardInterrupt:
            GPIO.cleanup()
    
    def stop(self):
        try:
            self.servo.ChangeDutyCycle(7.5)
        except KeyboardInterrupt:
            GPIO.cleanup()
        
        self.servo.stop()
        GPIO.cleanup()
    
def get_position(img_width, face_x, face_width):    
    face_mid = face_x + face_width / 2
    ratio = face_mid / img_width
    position = 15 - (2 * ratio + 0.5) / 20 * 100
    return position
