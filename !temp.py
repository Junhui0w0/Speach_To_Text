
def make_gui(r):
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

    
    # 선택된 옵션 출력 함수
    def show_selected_option():
        ans = askyesno(title="제출 확인", message="제출하시겠습니까?")

        if ans:
            print(f"\n====최종 데이터 출력===")

            for i in range(len(button_texts)):
                print(f"[디버깅] {button_texts[i]}: {data_lst[i]}")

            print(f"[디버깅] 선택된 옵션: {radio_var.get()}")

            all_clear()

        else:
            print(f"[디버깅] 제출 취소")

        print(f"[디버깅] data_lst: {data_lst}")


    def all_clear():
        global data_lst
        data_lst = ["" for _ in range(len(button_texts))]

        for i in range(len(button_texts)):
            buttons[i].config(text=f"{button_texts[i]}")

        func.filtering_noise(r)