import tkinter as tk
import speech_recognition as sr
import gui
import func

def initialize_recognizer():
    r = sr.Recognizer()
    r.energy_threshold = 4000  # 배경 소음 환경에 맞게 조정
    r.dynamic_energy_threshold = False
    return r

r = initialize_recognizer()
func.filtering_noise(r)

try:
    gui.make_gui(r)


except Exception as e:
    print(f"[ERROR] 에러: {e}")