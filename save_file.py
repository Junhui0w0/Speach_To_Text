import tkinter as tk
from tkinter import Toplevel
from tkinter import filedialog
from tkinter import messagebox

saved_path = ""

def open_login_gui(root):
    pw_window = Toplevel(root)
    pw_window.title("관리자 인증")
    pw_window.resizable(False,False)

    # root 창의 크기와 위치 가져오기
    root.update_idletasks()  # 현재 창 크기를 정확히 계산하기 위해 필요
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    all_width =int(root_width * 0.2)
    all_height = int(root_height *0.05)

    pw_window_width= 800
    pw_window_height= 400

    # 정중앙 위치 계산
    pos_x = root_x + (root_width // 2) - (pw_window_width // 2)
    pos_y = root_y + (root_height // 2) - (pw_window_height // 2)

    # 창 위치 및 크기 설정
    pw_window.geometry(f"{pw_window_width}x{pw_window_height}+{pos_x}+{pos_y}")

    pw_lbl = tk.Label(
        pw_window,
        text="비밀번호 입력",
        font=("맑은고딕", 30),
        foreground="black",
        width=all_width // 10,
        height=all_height // 20
    )
    pw_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # 그리드 배치

    #비밀번호 입력칸 추가
    pw_entry = tk.Entry(
        pw_window,
        font=("맑은고딕", 30),
        foreground="black",
        width=all_width//10
    )
    pw_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # 그리드 배치
    pw_entry.config(show='*')

    # 버튼 추가
    pw_btn = tk.Button(
        pw_window,
        text="로그인",
        font=("맑은고딕", 30),
        command=lambda: check_pw(pw_entry.get(), root, pw_window),
        width=all_width//10,
        height=all_height//20,
        relief="solid",  # 테두리 스타일 (solid: 실선)
        highlightbackground="black",  # 테두리 색상
        highlightthickness=2          # 테두리 두께
    )
    pw_btn.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")  # 그리드 배치

    # 창이 닫힐 때까지 대기
    pw_window.wait_window()

    return saved_path

def check_pw(pw, root, pw_win):
    if pw == '4197':
        show_path_gui(root, pw_win)
        
        print("[디버깅] pw 일치")

    else:
        print("[디버깅] pw 불일치")



def open_set_directory(path_lbl, window):
    global saved_path
    saved_path = filedialog.askdirectory(parent=window)

    if len(saved_path) < 1:
        messagebox.showinfo("알림", "저장경로가 설정되지 않았습니다.")
        return 'Not Setted'
    
    else:
        # 저장 경로가 설정되었다면 ?
        print(f"\n[디버깅] window 타입: {type(window)}")
        path_lbl.config(text=f"설정된 경로: {saved_path}")
        return saved_path
    
def sending_save_path(window, pw_win):
    window.destroy()
    pw_win.destroy()

def show_path_gui(root, pw_win):
    # 팝업 창 생성
    save_path_window = Toplevel(root)
    save_path_window.title("파일 저장 경로 설정")
    save_path_window.resizable(False, False)

    # root 창의 크기와 위치 가져오기
    root.update_idletasks()  # 현재 창 크기를 정확히 계산하기 위해 필요
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    all_width =int(root_width * 0.2)
    all_height = int(root_height *0.05)

    # options_window 크기 설정
    window_width = 800
    window_height = 500

    # 정중앙 위치 계산
    pos_x = root_x + (root_width // 2) - (window_width // 2)
    pos_y = root_y + (root_height // 2) - (window_height // 2)

    # 창 위치 및 크기 설정
    save_path_window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    # 버튼 추가
    set_path_btn = tk.Button(
        save_path_window,
        text="저장경로 설정",
        font=("맑은고딕", 15),
        command=lambda: open_set_directory(show_path_lbl, save_path_window),
        width=all_width//10,
        height=all_height//20
    )
    set_path_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # 그리드 배치

    show_path_lbl = tk.Label(
        save_path_window,
        text="설정된 경로: ???",
        font=("맑은고딕", 15),
        foreground="blue",
        width=all_width//6,
        height=all_height//20,
        justify="left"
    )
    show_path_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # 그리드 배치

    confirm_btn = tk.Button(
        save_path_window,
        text="완료",
        font=("맑은고딕", 15),
        foreground="red",
        width=all_width//10,
        height=all_height//20,
        justify="left",
        command=lambda: sending_save_path(save_path_window, pw_win)
    )
    confirm_btn.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

    # 창이 닫힐 때까지 대기
    save_path_window.wait_window()

    return saved_path