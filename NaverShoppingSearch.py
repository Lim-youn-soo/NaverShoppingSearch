from tkinter import *  # GUI를 위한 tkinter 모듈

def confirmColorEntryFlag():  # CheckBox에 따라 색깔 입력 칸 normal or disable  
    if check.get() == 1:
        colorEntry.config(state="normal")
    else:
        colorEntry.config(state="disable")

window = Tk() # 윈도우 생성
window.title("Naver Shopping Searcher")

brandLabel = Label(window, text="브랜드 입력: ")
brandEntry = Entry(window)

nameLabel = Label(window, text="제품명 입력: ")
nameEntry = Entry(window)

sizeLabel = Label(window, text="사이즈 입력: ")
sizeEntry = Entry(window)

check = IntVar()
colorEntryFlag = Checkbutton(window, text="색깔 입력", variable = check,command=confirmColorEntryFlag) 
colorEntry = Entry(window)
colorEntry.config(state="disable")

button1 = Button(window, text="검색") 

brandLabel.grid(row=0, column=0, sticky =E)
nameLabel.grid(row=1, column=0, sticky =E)
sizeLabel.grid(row=2, column=0, sticky =E)
colorEntryFlag.grid(row=3, column=0, sticky =E)

brandEntry.grid(row=0, column=1)
nameEntry.grid(row=1, column=1)
sizeEntry.grid(row=2, column=1)
colorEntry.grid(row=3, column=1)

button1.grid(row=4, column = 0, columnspan=2)
