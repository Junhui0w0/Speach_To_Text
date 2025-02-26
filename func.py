import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

# 최초 1회만 소음 적응 수행
def filtering_noise(recognizer):
    with sr.Microphone() as source:
        print("\n[디버깅] 배경 소음 분석 중..")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("[디버깅] 배경 소음 분석 완료!")

# 음성 캡처 함수
def capture_audio(recognizer):
    try:
        with sr.Microphone() as source:
            print("[디버깅] 음성인식 수행중...")
            return recognizer.listen(source, timeout=10, phrase_time_limit=20)
        
    except sr.UnknownValueError:
        print("[디버깅] 음성을 이해할 수 없습니다")
    except sr.RequestError as e:
        print(f"[디버깅] Google API 요청 실패: {e}")
    except KeyboardInterrupt:
        print("[디버깅] 프로그램 종료")        
    except Exception:
        messagebox.showinfo("알림", "[Error] 음성 인식 실패")
        print("[디버깅-Error] 음성 인식 실패")

# Speach To Text
def minning_word(recognizer, audio):
    print(f"[디버깅] audio 타입: {type(audio)}")
    text = recognizer.recognize_google(audio, language='ko-KR')
    print(f"[디버깅] 인식된 텍스트: {text}")
    return text