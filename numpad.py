import tkinter as tk
from tkinter import Toplevel, messagebox

# 연락처 데이터 저장 변수
contact_number = ""  # 현재 연락처 데이터

def start_voice_recognition(options_window):
    """음성인식 선택"""
    global contact_number
    if contact_number:
        # 이미 데이터가 있는 경우 경고 메시지 표시
        overwrite = messagebox.askyesno("경고", "이미 연락처 데이터가 저장되어 있습니다. \n음성인식을 다시 진행하시겠습니까?")
        if not overwrite: #기존 전화번호 유지
            print(f"[DEBUG] 기존 연락처 데이터 유지")# 사용자가 취소를 선택한 경우 함수 종료
        
        else:
            contact_number = "voice_start"
            print(f"[DEBUG] 기존 데이터 삭제 후 음성인식 시작: {contact_number}")

    else:
        contact_number = "voice_start"
        print(f"[DEBUG] 음성인식 시작: {contact_number}")

    options_window.destroy()  # 창 닫기

def open_numpad(root, options_window):
    """넘패드 선택"""
    global contact_number

    def add_digit(digit):
        current = phone_var.get()
        phone_var.set(current + digit)

    def clear_entry():
        phone_var.set("")

    def delete_last():
        current = phone_var.get()
        phone_var.set(current[:-1])

    def confirm_input():
        global contact_number
        contact_number = phone_var.get()
        print(f"[DEBUG] options_window 타입: {type(options_window)}")
        print(f"[DEBUG] 입력된 연락처: {contact_number}")
        numpad.destroy()  # 넘패드 창 닫기
        options_window.destroy()  # 옵션 창도 닫기

    def format_phone_number(*args):
        """휴대폰 번호를 자동으로 하이픈(-) 형식으로 변환"""
        input_value = phone_var.get().replace("-", "")  # 기존 하이픈 제거
        formatted_value = ""

        # 번호 길이에 따라 하이픈 추가
        if input_value.startswith(("010", "031", "032", "051","053","062","042","052","044","033","043","041","051","063","061","054","055","064")) and len(input_value) > 3:
            # 일반 휴대폰 번호 (010-XXXX-XXXX)
            if len(input_value) <= 7:
                formatted_value = f"{input_value[:3]}-{input_value[3:]}"
            else:
                formatted_value = f"{input_value[:3]}-{input_value[3:7]}-{input_value[7:]}"
        elif input_value.startswith("02") and len(input_value) > 2:
            # 서울 지역번호 (02-XXXX-XXXX)
            if len(input_value) <= 6:
                formatted_value = f"{input_value[:2]}-{input_value[2:]}"
            else:
                formatted_value = f"{input_value[:2]}-{input_value[2:6]}-{input_value[6:]}"
        else:
            # 기타 번호는 그대로 유지
            formatted_value = input_value

        # 변환된 값 설정
        phone_var.set(formatted_value)


    numpad = Toplevel(root)
    numpad.title("넘패드")
    numpad.geometry("400x400")
    numpad.resizable(False, False)

        # root 창의 크기와 위치 가져오기
    root.update_idletasks()  # 현재 창 크기를 정확히 계산하기 위해 필요
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # options_window 크기 설정
    window_width = 400
    window_height = 400

    # 정중앙 위치 계산
    pos_x = root_x + (root_width // 2) - (window_width // 2)
    pos_y = root_y + (root_height // 2) - (window_height // 2)

    # 창 위치 및 크기 설정
    numpad.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    phone_var = tk.StringVar(value=contact_number)
    phone_var.trace_add("write", format_phone_number)  # 값 변경 시 format_phone_number 호출
    entry = tk.Entry(numpad, textvariable=phone_var, font=("맑은고딕", 20), justify="center")
    entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


    buttons = [
        ("1", 1, 0), ("2", 1, 1), ("3", 1, 2),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2),
        ("7", 3, 0), ("8", 3, 1), ("9", 3, 2),
        ("0", 4, 1)
    ]
    for (text, row, col) in buttons:
        tk.Button(
            numpad,
            text=text,
            font=("맑은고딕", 20),
            command=lambda t=text: add_digit(t),
            width=5,
            height=2
        ).grid(row=row, column=col)

    tk.Button(
        numpad,
        text="전부\n지우기",
        font=("맑은고딕", 15),
        command=clear_entry,
        width=7,
        height=2
    ).grid(row=4, column=0)

    tk.Button(
        numpad,
        text="지우기",
        font=("맑은고딕", 15),
        command=delete_last,
        width=5,
        height=2
    ).grid(row=4, column=2)

    tk.Button(
        numpad,
        text="확인",
        font=("맑은고딕", 15),
        command=confirm_input,
        width=15,
        height=2
    ).grid(row=5, column=0, columnspan=3)

def open_contact_options(root, cur_num):
    """연락처 옵션 GUI"""
    global contact_number
    contact_number = cur_num

    # 팝업 창 생성
    options_window = Toplevel(root)
    options_window.title("연락처 옵션")
    options_window.resizable(False, False)

    # root 창의 크기와 위치 가져오기
    root.update_idletasks()  # 현재 창 크기를 정확히 계산하기 위해 필요
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # options_window 크기 설정
    window_width = 300
    window_height = 200

    # 정중앙 위치 계산
    pos_x = root_x + (root_width // 2) - (window_width // 2)
    pos_y = root_y + (root_height // 2) - (window_height // 2)

    # 창 위치 및 크기 설정
    options_window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    # 버튼 추가
    tk.Button(
        options_window,
        text="음성인식",
        font=("맑은고딕", 15),
        command=lambda: start_voice_recognition(options_window),
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        options_window,
        text="키패드",
        font=("맑은고딕", 15),
        command=lambda: open_numpad(root, options_window),
        width=20,
        height=2
    ).pack(pady=10)

    # 창이 닫힐 때까지 대기
    options_window.wait_window()

    return contact_number
