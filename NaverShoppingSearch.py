from tkinter import *  # GUI를 위한 tkinter 모듈
import tkinter.messagebox 
from selenium import webdriver
import time
import win32com.client


tempHref = []
mulHref = []
Href = []
windowNumber = -1
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
wb = excel.Workbooks.Add()
ws = wb.Worksheets("Sheet1")
excelRow = 1
excelCol = 1
exitFlag = False
color = ""

def confirmColorEntryFlag():  # CheckBox에 따라 색깔 입력 칸 normal or disable  
    if check.get() == 1:
        colorEntry.config(state="normal")
    else:
        colorEntry.config(state="disable")


    
    

def searchStart():  # Entry에 입력한 값들로 '네이버쇼핑' 검색 시작 
    if brandEntry.get() == "" or nameEntry.get() == "" or sizeEntry.get() =="":
        tkinter.messagebox.showwarning("NaverShoppingSearch","모든 정보를 다 기입해 주세요") 
        return
    if check.get() == 1 and colorEntry.get() == "":
        tkinter.messagebox.showwarning("NaverShoppingSearch","모든 정보를 다 기입해 주세요") 
        return

    url = "https://search.shopping.naver.com/search/all.nhn?query="+brandEntry.get() + "+" + nameEntry.get()
    driver = webdriver.Chrome()
    driver.get(url)

    global tempHref     
    global mulHref
    global Href
    global exitFlag
    global excelRow
    global excelCol
    global color

    info = driver.find_elements_by_class_name("info")

    for i in info:
        a = i.find_element_by_tag_name("a")
        tempHref.append(a.get_attribute("href"))
    
    for i in range(len(tempHref)):  # url을 확인하여, 단수/복수 결과 저장 
        if 'adcrNoti.nhn?' in tempHref[i]:  # 단수
            Href.append(tempHref[i])
    
        elif 'adcr.nhn?' in tempHref[i]:    # 복수 
            mulHref.append(tempHref[i])

    for i in mulHref:  # 복수 결과를 하나하나 들어가보며, 각각의 url을 따와 Href에 저
        driver.get(i)
        mall = driver.find_elements_by_class_name("mall")
        for j in mall:
            a = j.find_element_by_tag_name("a")
            Href.append(a.get_attribute("href"))
       

    

    for i in Href:
       
        driver.get(i) # 사이트 하나 open
        while True: # 로딩 page 대기  
            if "shopping.naver.com" in driver.current_url:
                pass
            else:   # 로딩 page 끝나면 탈출
                break
        
        print(driver.current_url)
        if "lotteimall" in driver.current_url: # 1. 롯데 홈쇼핑
            print("----------[롯데 홈쇼핑] 검색 중-----------")
            
            for i in driver.window_handles:    # 팝업 창 예외 처리 
                driver.switch_to_window(i)
                if 'www.lotteimall.com/goods/viewGoodsDetail.lotte' in driver.current_url:  
                    windowNumber = i
                elif 'coop/affilGate.lotte' in driver.current_url:                   
                    while True:
                        if 'www.lotteimall.com/goods/viewGoodsDetail.lotte' in driver.current_url:
                            break;
                        else:
                            pass
                    windowNumber = i
                else:
                    driver.close()
                    pass               

            driver.switch_to_window(windowNumber)
            
            option = driver.find_elements_by_class_name('inp_option')
            option[0].find_element_by_tag_name('a').click() # 색상 or 사이즈 
            
            wrapScroll = driver.find_elements_by_class_name('wrap_scroll_option')
            p = wrapScroll[0].find_elements_by_tag_name('p')
                        
            if "색상" in option[0].find_element_by_tag_name('a').text: # 색상 - 사이즈
               # if colorEntry.get() == "": # 사용자가 색상 안 입력했을 때 예외 처리
                print("추가 옵션")
                for i in p:
                    print(i.text)

                color = input("위 옵션 중 하나를 입력해 주세요: ")
                #colorEntry.config(state="normal")
                #colorEntry.insert(0, color)
                                                    
                for i in p:                 
                    #if colorEntry.get() == i.text:
                    if color == i.text:
                        i.click()

                        option[1].find_element_by_tag_name('a').click()
                        wrapScroll = driver.find_elements_by_class_name('wrap_scroll_option')
                        p2 = wrapScroll[1].find_elements_by_tag_name('p')

                            
                        for j in p2:
                            #print(j.text)
                            if j.text == sizeEntry.get()  or (sizeEntry.get() in j.text and "남음" in j.text):
                                    
                                print(sizeEntry.get(),"재고 있음")
                                ws.Cells(excelRow, excelCol).Value = driver.current_url
                                excelRow = excelRow +1
                                exitFlag = True
                                break
                        if exitFlag == True:
                            exitFlag = False
                            break
                        else:
                            print(sizeEntry.get(),"재고 없음")
                            break                         
            else: # 오직 색상
               for i in p:                   
                   if i.text == sizeEntry.get() or (sizeEntry.get() in i.text and "남음" in i.text):
                       print(sizeEntry.get(),"재고 있음")
                       #print(driver.current_url)
                       ws.Cells(excelRow, excelCol).Value = driver.current_url
                       excelRow = excelRow +1
                       exitFlag = True
                       break
               if exitFlag == True:
                        exitFlag = False
                        
               else:     
                   print(sizeEntry.get(), "재고 없음")      

        if "http://www.ssg.com" in driver.current_url: # ssg 
           print("----------SSG 검색 중-----------")            
           for i in driver.window_handles:    # 팝업 창 예외 처리 
                driver.switch_to_window(i)
                print(i)
                if 'http://www.ssg.com/item/itemView.ssg' in driver.current_url:  
                    windowNumber = i

                else:
                    driver.close()
                    pass            

           driver.switch_to_window(windowNumber)
           group = driver.find_elements_by_class_name('cdtl_opt_group')
           dt = group[0].find_elements_by_tag_name('dt')

           if len(group) == 1:  # 사이즈 
                 group[0].find_element_by_class_name('cdtl_opt_select').click()
                 scroll = group[0].find_element_by_class_name('cdtl_scroll')
                 txt=scroll.find_elements_by_class_name('txt')
                 for j in txt:

                    if sizeEntry.get() == j.text or (sizeEntry.get() in j.text and "남음" in j.text):
                        print(sizeEntry.get(),"재고 있음")
                        ws.Cells(excelRow, excelCol).Value = driver.current_url
                        excelRow = excelRow +1
                        exitFlag = True
                        break
                 if exitFlag == True:
                     exitFlag = False
                 else:
                     print(sizeEntry.get(), "재고 없음")
                
           else: # 색상 & 사이즈(SIZE, 선택) or 사이즈(SIZE, 선택) & 색상
                
                    if dt[0].text == '색상':
                        group[0].find_element_by_class_name('cdtl_opt_select').click()
                        scroll = group[0].find_element_by_class_name('cdtl_scroll')
                        
                        txt = scroll.find_elements_by_class_name('txt')
                        #if colorEntry.get() =="":
                        print("옵션")
                        for i in txt:
                            print(i.text)

                        color = input("위 색깔 중 하나를 입력해 주세요: ")
                        #colorEntry.config(state="normal")
                        #colorEntry.insert(0, color)

                        #else:
                        for j in txt: 
                                #if colorEntry.get() == j.text:
                            if color == j.text:
                                j.click()
                                break

                        group = driver.find_elements_by_class_name('cdtl_opt_group')
                        group[1].find_element_by_class_name('cdtl_opt_select').click()
                        scroll = group[1].find_element_by_class_name('cdtl_scroll')
                        txt2 = scroll.find_elements_by_class_name('txt')
                        for k in txt2:
                            if sizeEntry.get() == k.text or (sizeEntry.get() in k.text and "남음" in k.text):
                                print(sizeEntry.get(),"재고 있음")
                                ws.Cells(excelRow, excelCol).Value = driver.current_url
                                excelRow = excelRow +1
                                exitFlag = True 
                                break


                                    
                    if exitFlag == True:
                         exitFlag = False
                         
                    else:
                        print(sizeEntry.get(), "재고 없음")


        if "http://www.ssg.com" in driver.current_url: # ssg 
           print("----------SSG 검색 중-----------")            
           for i in driver.window_handles:    # 팝업 창 예외 처리 
                driver.switch_to_window(i)
                print(i)
                if 'http://www.ssg.com/item/itemView.ssg' in driver.current_url:  
                    windowNumber = i

                else:
                    driver.close()
                    pass            

           driver.switch_to_window(windowNumber)
           group = driver.find_elements_by_class_name('cdtl_opt_group')
           dt = group[0].find_elements_by_tag_name('dt')
        

    #colorEntry.config(state='disable')
    #colorEntry.delete(0,END)
'''
            


       if "http://www.11st.co.kr" in driver.current_url: #
           print("--------------------11번가 검색 중---------------------")

            for i in driver.window_handles:    # 팝업 창 예외 처리 
                driver.switch_to_window(i)
                if 'http://www.11st.co.kr/product/SellerProductDetail' in driver.current_url:  
                    windowNumber = i
                elif 'http://www.11st.co.kr/connect/Gateway' in driver.current_url:                   
                    while True:
                        if 'www.lotteimall.com/goods/viewGoodsDetail.lotte' in driver.current_url:
                            break;
                        else:
                            pass
                    windowNumber = i
                else:
                    driver.close()
                    pass            

            driver.switch_to_window(windowNumber)
'''
                 
 
    

            
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

button1 = Button(window, text="검색", command = searchStart) 

brandLabel.grid(row=0, column=0, sticky =E)
nameLabel.grid(row=1, column=0, sticky =E)
sizeLabel.grid(row=2, column=0, sticky =E)
colorEntryFlag.grid(row=3, column=0, sticky =E)

brandEntry.grid(row=0, column=1)
nameEntry.grid(row=1, column=1)
sizeEntry.grid(row=2, column=1)
colorEntry.grid(row=3, column=1)

button1.grid(row=4, column = 0, columnspan=2)
