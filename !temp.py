import tkinter as tk
from tkinter import Toplevel, messagebox

# 연락처 데이터 저장 변수
contact_number = ""  # 현재 연락처 데이터

# 음성인식 함수 (예제용)
def start_voice_recognition():
    global contact_number
    if contact_number:
        # 이미 데이터가 있는 경우 경고 메시지 표시
        overwrite = messagebox.askyesno("경고", "이미 연락처 데이터가 있습니다. 다시 음성인식을 진행하시겠습니까?")
        if not overwrite:
            return  # 사용자가 취소를 선택한 경우 함수 종료

    # 음성인식 로직 (예제)
    contact_number = "010-1234-5678"  # 예제 데이터
    print(f"[디버깅] 음성인식 완료: {contact_number}")
    messagebox.showinfo("음성인식 완료", f"연락처가 음성인식을 통해 입력되었습니다: {contact_number}")

# 넘패드 팝업 창 생성 함수
def open_numpad(root):
    def add_digit(digit):
        """숫자 버튼 클릭 시 Entry에 추가"""
        current = phone_var.get()
        phone_var.set(current + digit)

    def clear_entry():
        """Entry 초기화"""
        phone_var.set("")

    def delete_last():
        """Entry에서 마지막 문자 삭제"""
        current = phone_var.get()
        phone_var.set(current[:-1])

    def confirm_input():
        """입력값 확인 및 저장"""
        global contact_number
        contact_number = phone_var.get()
        print(f"[디버깅] 입력된 연락처: {contact_number}")
        numpad.destroy()  # 넘패드 창 닫기

    def format_phone_number(*args):
        """휴대폰 번호를 자동으로 하이픈(-) 형식으로 변환"""
        input_value = phone_var.get().replace("-", "")  # 기존 하이픈 제거
        formatted_value = ""

        # 번호 길이에 따라 하이픈 추가 (예외 처리 포함)
        if input_value.startswith("010") and len(input_value) > 3:
            if len(input_value) <= 7:
                formatted_value = f"{input_value[:3]}-{input_value[3:]}"
            else:
                formatted_value = f"{input_value[:3]}-{input_value[3:7]}-{input_value[7:]}"
        elif input_value.startswith("01") and len(input_value) > 2:
            if len(input_value) <= 6:
                formatted_value = f"{input_value[:2]}-{input_value[2:]}"
            else:
                formatted_value = f"{input_value[:2]}-{input_value[2:6]}-{input_value[6:]}"
        else:
            formatted_value = input_value  # 예외적인 경우 그대로 유지

        # 변환된 값 설정
        phone_var.set(formatted_value)

    # 팝업 창 생성
    numpad = Toplevel(root)
    numpad.title("넘패드")
    numpad.geometry("400x400")
    numpad.resizable(False, False)

    # Entry 위젯 (입력값 표시)
    phone_var = tk.StringVar(value=contact_number)  # 초기값은 현재 연락처 데이터
    phone_var.trace_add("write", format_phone_number)  # 값 변경 시 format_phone_number 호출

    entry = tk.Entry(numpad, textvariable=phone_var, font=("맑은고딕", 20), justify="center")
    entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # 숫자 버튼 생성
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

    # 제어 버튼 (지우기, 삭제, 확인)
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

# 연락처 옵션 GUI 생성 함수
def open_contact_options(root):
    options_window = Toplevel(root)
    options_window.title("연락처 옵션")
    options_window.geometry("300x200")
    options_window.resizable(False, False)

    tk.Button(
        options_window,
        text="음성인식",
        font=("맑은고딕", 15),
        command=start_voice_recognition,
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        options_window,
        text="키패드",
        font=("맑은고딕", 15),
        command=lambda: open_numpad(root),
        width=20,
        height=2
    ).pack(pady=10)

# # 메인 윈도우 생성
# root = tk.Tk()
# root.title("연락처 입력 옵션")
# root.geometry("400x300")

# # "연락처" 버튼 생성
# contact_button = tk.Button(
#     root,
#     text="연락처",
#     font=("맑은고딕", 20),
#     command=open_contact_options,
#     width=10,
#     height=2
# )
# contact_button.pack(pady=50)

# # 메인 루프 실행
# root.mainloop()
