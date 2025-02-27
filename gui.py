import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter import messagebox, Toplevel, Menu

import speech_recognition as sr
from datetime import datetime
import func
import numpad
import save_file

data_lst = []
saved_path = ""

def make_gui(r):
    global data_lst

    # 메인 윈도우 생성
    root = tk.Tk()
    root.title("Speach To Text (v1)")
    root.state('zoomed')  # 창을 전체 화면으로 설정

    # 모니터 해상도 가져오기
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 버튼 크기 비율 계산
    button_width = int(screen_width * 0.2)  # 화면 너비의 20%
    button_height = int(screen_height * 0.05)  # 화면 높이의 5%

    # 버튼 생성 및 배치
    buttons = []
    button_texts = ["보내는 분 성함", "보내는 분 연락처", "보내는 분 주소", "받는 분 성함", "받는 분 연락처", "받는 분 주소", "물건 종류 및 수량"]
    data_lst = ["" for i in range(len(button_texts))] # 음성인식된 데이터 저장

    for i, text in enumerate(button_texts):
        button = tk.Button(
            root,
            text=text,
            font=("맑은고딕", 30),
            width=button_width // 10,  # Tkinter에서 width는 문자 단위
            height=button_height // 20,  # Tkinter에서 height는 행 단위
            command=lambda num=i: button_action(num),
            relief="solid",  # 테두리 스타일 (solid: 실선)
            highlightbackground="black",  # 테두리 색상
            highlightthickness=2          # 테두리 두께
        )
        button.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")  # 그리드 배치
        buttons.append(button)

    # 라디오 버튼 변수 생성
    radio_var = tk.StringVar(value="착불")  # 기본 선택값 설정

    # 라디오 버튼 생성 및 배치 (1행 2열)
    radio1 = tk.Radiobutton(
        root,
        text="착불",
        font=("맑은고딕", 30),
        variable=radio_var,
        value="착불",
        width=button_width // 20,  # Tkinter에서 width는 문자 단위
        height=button_height // 20,  # Tkinter에서 height는 행 단위
        relief="solid",  # 테두리 스타일 (solid: 실선)
        highlightbackground="black",  # 테두리 색상
       highlightthickness=2 # 테두리 두께
    )
    radio1.grid(row=len(button_texts), column=0, pady=10, padx=10, sticky="w")  # 첫 번째 라디오 버튼

    radio2 = tk.Radiobutton(
        root,
        text="현불",
        font=("맑은고딕", 30),
        variable=radio_var,
        value="현불",
        width=button_width // 20,  # Tkinter에서 width는 문자 단위
        height=button_height // 20,  # Tkinter에서 height는 행 단위
        relief="solid",  # 테두리 스타일 (solid: 실선)
        highlightbackground="black",  # 테두리 색상
        highlightthickness=2          # 테두리 두께
    )
    radio2.grid(row=len(button_texts), column=0, pady=10, padx=10,sticky="e")  # 두 번째 라디오 버튼

    def get_saved_path():
        global saved_path
        saved_path = save_file.open_login_gui(root)
        print(f"[디버깅] saved_path: {saved_path}")

    # 선택된 옵션 출력 함수
    def show_selected_option():
        global data_lst
        ans = askyesno(title="제출 확인", message="제출하시겠습니까?")

        if ans:
            print(f"\n====최종 데이터 출력===")

            for i in range(len(button_texts)):
                print(f"[디버깅] {button_texts[i]}: {data_lst[i]}")

            print(f"[디버깅] 결제 방식: {radio_var.get()}")

            # saved_path = save_file.show_path_gui(root)
            # print(f"[디버깅] saved_path: {saved_path}")
            
            output_by_txt()
            all_clear()
            func.filtering_noise(r)

            messagebox.showinfo("Success", "성공적으로 제출되었습니다!")

        else:
            print(f"[디버깅] 제출 취소")

    # 확인 버튼 생성 및 배치
    confirm_button = tk.Button(
            root,
            text="완료",
            font=("맑은고딕", 30),
            foreground="red",
            width=button_width // 10,  # Tkinter에서 width는 문자 단위
            height=button_height // 20,  # Tkinter에서 height는 행 단위
            command=show_selected_option,
            relief="solid",  # 테두리 스타일 (solid: 실선)
            highlightbackground="black",  # 테두리 색상
            highlightthickness=2          # 테두리 두께
        )
    confirm_button.grid(row=len(button_texts) + 1, column=0, padx=10, pady=10, sticky="nsew")


    # 그리드 행/열 확장 가능하도록 설정
    for i in range(len(button_texts)):
        root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(0, weight=1)

    def show_notification(root, message):
        # Toplevel 창 생성
        notification_window = tk.Toplevel(root)
        notification_window.title("알림")

        # 메인 창의 크기와 위치 가져오기
        root.update_idletasks()  # 창 크기 계산을 위해 필요
        root_width = root.winfo_width()
        root_height = root.winfo_height()
        root_x = root.winfo_x()  # 메인 창의 X 좌표
        root_y = root.winfo_y()  # 메인 창의 Y 좌표

        # 알림 창 크기 (메인 창의 1/2)
        notification_width = root_width // 2
        notification_height = root_height // 2

        # 알림 창 위치 계산 (메인 창 정중앙)
        pos_x = root_x + (root_width - notification_width) // 2
        pos_y = root_y + (root_height - notification_height) // 2

        # 알림 창 크기 및 위치 설정
        notification_window.geometry(
            f"{notification_width}x{notification_height}+{pos_x}+{pos_y}"
        )

        # 알림 메시지 표시 (레이블)
        label = tk.Label(
            notification_window,
            text=message,
            font=("맑은고딕", 35),
            wraplength=notification_width - 20  # 메시지 자동 줄바꿈
        )
        label.pack(expand=True, padx=10, pady=10)

        # 알림 창이 메인 창 위에 고정되도록 설정
        notification_window.transient(root)
        notification_window.grab_set()

        return notification_window  
    
    # 버튼 클릭 시 실행될 함수
    def button_action(button_number):
        global data_lst

        print(f"\n[디버깅] 버튼 {button_number}이 눌렸습니다.")
        print(f"[디버깅] type: {type(buttons[button_number])}")

        if button_number == 1 or button_number == 4:
            a = numpad.open_contact_options(root, data_lst[button_number])
            print(f"[디버깅] 넘어온 contact_number: {a}")

            if a == 'voice_start': # 음성인식 시작
                # 알림 창 표시
                try:
                    notification_window = show_notification(root, f"[{button_texts[button_number]}] \n 음성 인식 중...")
                    root.update()

                    audio = func.capture_audio(r)
                    txt = func.minning_word(r, audio)

                    # 버튼 텍스트 변경
                    buttons[button_number].config(text=f'{button_texts[button_number]}: {txt}')
                    
                    # 음성인식 데이터 저장
                    data_lst[button_number] = txt

                finally:
                    # 알림 창 닫기
                    notification_window.destroy()

            else:
                # 버튼 텍스트 변경
                buttons[button_number].config(text=f'{button_texts[button_number]}: {a}')
                
                # 음성인식 데이터 저장
                data_lst[button_number] = a

        else:
            # 알림 창 표시
            try:
                notification_window = show_notification(root, f"[{button_texts[button_number]}] \n 음성 인식 중...")
                root.update()

                audio = func.capture_audio(r)
                txt = func.minning_word(r, audio)

                # 버튼 텍스트 변경
                buttons[button_number].config(text=f'{button_texts[button_number]}: {txt}')
                
                # 음성인식 데이터 저장
                data_lst[button_number] = txt

            finally:
                # 알림 창 닫기
                notification_window.destroy()
        
    # 창 크기 변경 시 버튼 크기 동적 조정
    def resize_buttons(event):
        new_width = event.width // 5  # 창 너비의 20%
        new_height = event.height // 20  # 창 높이의 5%
        for button in buttons:
            button.config(width=new_width // 10, height=new_height // 20)

    def all_clear():
        global data_lst
        data_lst = ["" for _ in range(len(button_texts))]

        for i in range(len(button_texts)):
            buttons[i].config(text=f"{button_texts[i]}")

    def output_by_txt():
        global saved_path

        with open("saved_root.txt", "r", encoding="utf-8") as f:
            saved_path = f.readline()

        print(f"[디버깅] output_bt_txt: 저장된 saved_path: {saved_path}")

        now = datetime.now()
        file_name = now.strftime("%Y-%m-%d_%H;%M;%S") # 파일 이름
        date = now.strftime("%Y-%m-%d %H시%M분%S초") # 메모장에 적을 일자

        try:
            if saved_path == "":
                save_root = file_name + ".txt"
            else:
                save_root = saved_path + '/' + file_name + ".txt"

            with open (save_root, "w", encoding="utf-8") as file:
                file.write(f"[일자]: {date}\n")

                for i in range(len(button_texts)):
                    if i == 3 or i == 6:
                        file.write("\n")

                    file.write(f"[{button_texts[i]}]: {data_lst[i]}\n")
                file.write(f"[결제 방식]: {radio_var.get()}\n")
            print(f"[디버깅] 데이터가 '{file_name}' 파일에 저장되었습니다.")

        except Exception as e:
            print(f"[ERROR: output_by_txt] 파일 저장 중 에러 발생: {e}")

    # Menu 생성
    menutree = Menu(root)
    root.config(menu=menutree)
    menutree.add_command(label="파일 저장경로 설정", command=get_saved_path)

    root.bind("<Configure>", resize_buttons)  # 창 크기 변경 이벤트 바인딩

    # 메인 루프 실행
    root.mainloop()