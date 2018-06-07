from tkinter import *
import tkinter.messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def initPage():
    global inputFrame, outputFrame, windowNumber, outputBtnIndex
    windowNumber = -1
    outputBtnIndex = 0
    #text =""
    inputFrame.grid_forget()
    outputFrame.grid_forget()
    window.title("[Naver Shopping Searcher]")
    titleLabel = Label(window, text="Naver Shopping Searcher", width=50, font="Helvetica 10 bold") 
    introLabel = Label(window, text="환영합니다! 메뉴를 선택해주세요!",height=6,width=50)

    introButton1 = Button(window, text="Read Me", command=introPage, width=30)
    introButton2 = Button(window, text="검색하기", command = searchPage, width=30)

    titleLabel.grid(row=0, column=0, columnspan=5)
    introLabel.grid(row=1,column=0, columnspan=5)
    introButton1.grid(row=30, column=0, columnspan=2)
    introButton2.grid(row=30, column=2, columnspan=2)
    

def introPage():
    global inputFrame,outputFrame
    inputFrame.grid_forget()
    outputFrame.grid_forget()
    window.title("[ReadMe Page]")
    titleLabel = Label(window, text="본 프로그램에 대하여", width=50, font="Helvetica 10 bold")
    introLabel = Label(window, text="본 프로그램은 '네이버 쇼핑'에서 상품의 재고 유무를\n알려주지 않는단점을 보완하기 위해 만들어졌습니다.\n사용자로부터 브랜드,제품명,사이즈를 입력 받아 상품의\n재고가 있는 쇼핑몰의 주소를 반환해주는 동작을 합니다.", width=50, height=6) 

    titleLabel.grid(row=0, column=0, columnspan=5)
    introLabel.grid(row=1, column=0, columnspan=5)

    introButton1 = Button(window, text="되돌아가기", command=initPage, width=30)
    introButton2 = Button(window, text="검색하기", command = searchPage, width=30)

    introButton1.grid(row=30, column=0, columnspan=2)
    introButton2.grid(row=30, column=2, columnspan=2)
    
def searchPage():
    global inputFrame
    window.title("[Search Page]")
    titleLabel = Label(window, text="Search Page", width=50, font="Helvetica 10 bold")
    introLabel = Label(window, text="상품 정보를 입력해주세요", width=50, height=6)

    titleLabel.grid(row=0, columnspan=5)
    introLabel.grid(row=1, columnspan=5)

    brandLabel = Label(inputFrame, text="브랜드 입력: ")
    brandEntry = Entry(inputFrame)

    nameLabel = Label(inputFrame, text="제품명 입력: ")
    nameEntry = Entry(inputFrame)

    sizeLabel = Label(inputFrame, text="사이즈 입력: ")
    sizeEntry = Entry(inputFrame)    

    brandLabel.grid(row=3, column=0, sticky=E)
    nameLabel.grid(row=4, column=0, sticky=E)
    sizeLabel.grid(row=5, column=0, sticky=E)

    brandEntry.grid(row=3, column=2)
    nameEntry.grid(row=4, column=2)
    sizeEntry.grid(row=5, column=2)

    inputFrame.grid(row=2, column=0, columnspan=4, pady= (0,20))

    introButton1 = Button(window, text="되돌아가기", command=initPage, width=30)
    introButton2 = Button(window, text="검색", command = lambda:searchStart(brandEntry.get(), nameEntry.get(), sizeEntry.get()), width=30)

    introButton1.grid(row=30, column=0, columnspan=2)
    introButton2.grid(row=30, column=2, columnspan=2)    

def outputPage():
    global inputFrame, outputFrame
    inputFrame.grid_forget()
    window.title("[Output Page]")
    titleLabel = Label(window, text="Output Page", width=50, font="Helvetica 10 bold")
    introLabel = Label(window, text="상품 검색 결과", width=50, height=6)

    titleLabel.grid(row=0, columnspan=5)
    introLabel.grid(row=1, columnspan=5)

    
    outputFrame.grid(row=3, column=0, columnspan=4, pady= (0,20))

    introButton1 = Button(window, text="초기화면으로", command=initPage, width=60)

    introButton1.grid(row=30, column=0, columnspan=4)
     

def searchStart(brand, name, size):
    if brand == "" or name == "" or size == "":
        tkinter.messagebox.showwarning("NaverShoppingSearch","모든 정보를 다 기입해 주세요")
        searchPage()

    if int(size) < 225 or int(size) > 285:
        tkinter.messagebox.showwarning("NaverShoppingSearch","225에서 285사이의 사이즈를 기입해 주세요")

    if int(size)%5 != 0:
        tkinter.messagebox.showwarning("NaverShoppingSearch","5단위의 사이즈를 기입해주세요")
        
    else:
        global inputFrame, outputFrame, tempHref, mulHref, Href, windowNumber, outputBtnIndex
        inputFrame.grid_forget()
        window.title("[Searching..]")
        titleLabel = Label(window, text="Searching..", width=50, font="Helvetica 10 bold")
        introLabel = Label(window, text="", width=50, height=6)

        titleLabel.grid(row=0, columnspan=5)
        introLabel.grid(row=1, columnspan=5)

        introButton1 = Button(window, text="취소", command=outputPage, width=60)
        introButton1.grid(row=30, column=0, columnspan=4)

        try:
            url = "https://search.shopping.naver.com/search/all.nhn?query="+brand + "+" + name
            driver = webdriver.Chrome()
            driver.get(url)

            driver.find_element_by_class_name("_productSet_department").click()

            while True:
                if "department&viewType" in driver.current_url:
                    break
                else:
                    pass


            #print(driver.current_url)
            info = driver.find_elements_by_class_name("info")

            ### 결과 URL Href에 모두 저장 ###
            for i in info:
                a=i.find_element_by_tag_name("a")
                #print(a.get_attribute("href"))
                if 'adcrNoti.nhn?' in a.get_attribute("href"):
                    Href.append(a.get_attribute("href"))
                elif "adcr.nhn?" in a.get_attribute("href"):
                    mulHref.append(a.get_attribute("href"))
                #tempHref.append(a.get_attribute("href"))

            
            for i in mulHref:
                driver.get(i)
                mall = driver.find_elements_by_class_name("mall")
                for j in mall:
                    a = j.find_element_by_tag_name("a")
                    print(a.get_attribute("href"))
                    Href.append(a.get_attribute("href"))
            
            ##################################

            ### Href에 저장된 URL들 탐색 시작 ###
            for i in Href:
                driver.get(i)
                while True:
                    if "shopping.naver.com" in driver.current_url:
                        pass
                    else:
                        break
                print(driver.current_url)
                if "lotteimall" in driver.current_url:
                    introLabel = Label(window, text="롯데아이몰 검색중...", width=50, height=6)
                    introLabel.grid(row=1, columnspan=5)


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
                    try:
                        option = driver.find_element_by_class_name("inp_option")
                        option.find_element_by_tag_name("a").click()
                        wrapscroll = driver.find_element_by_class_name("wrap_scroll_option")
                        p=wrapscroll.find_elements_by_tag_name("p")

                        for i in p:
                            if i.text == size or (size in i.text and "남음" in i.text) or (size in i.text and "품절" not in i.text):
                                print(size, "재고 있음 [롯데아이몰]")
                                url = driver.current_url
                                btn = Button(outputFrame, text="롯데아이몰",  command=lambda url=url:openSite(url), width=60)
                                btn.grid(row = outputBtnIndex, column=0)
                                outputBtnIndex = outputBtnIndex +1 
                                break
                    
                    except:
                        print("폼이 다른 롯데아이몰")
                        pass 
            
                elif "hyundaihmall" in driver.current_url:
                    introLabel = Label(window, text="현대아이몰 검색중...", width=50, height=6)
                    introLabel.grid(row=1, columnspan=5)

                    try:
                        for i in driver.window_handles:    # 팝업 창 예외 처리 
                            driver.switch_to_window(i)
                            if 'www.hyundaihmall.com/front/pda/itemPtc' in driver.current_url:  
                                windowNumber = i
                            else:
                                driver.close()      
                        driver.switch_to_window(windowNumber)

                        driver.find_element_by_class_name("defaultVal").click()

                        ilist = driver.find_element_by_class_name("iListCont")
                        li = ilist.find_elements_by_class_name("item")

                        for i in li:
                            titlebold = i.find_element_by_class_name("title")
                            if size in titlebold.text:
                                try:
                                    num = i.find_element_by_class_name("num")
                                    if "품절" not in num.text and "남은수량 0" not in num.text:
                                       url = driver.current_url
                                       btn = Button(outputFrame, text="현대아이몰", command=lambda url=url:openSite(url), width=60)
                                       btn.grid(row=outputBtnIndex, column=0)
                                       outputBtnIndex = outputBtnIndex+1
                                       print(size, "재고 있음 [현대아이몰]")
                                       break
                                        
                                except:
                                    if "품절" not in titlebold.text:
                                       url = driver.current_url
                                       btn = Button(outputFrame, text="현대아이몰", command=lambda url=url:openSite(url), width=60)
                                       btn.grid(row=outputBtnIndex, column=0)
                                       outputBtnIndex = outputBtnIndex+1
                                       print(size, "재고 있음 [현대아이몰]")
                                       break                                   
                                        
                    except:
                        print("폼이 다른 현대아미몰")
                        pass
                    
                elif "department.ssg" in driver.current_url:
                    introLabel = Label(window, text="신세계몰 검색중...", width=50,height=6)
                    introLabel.grid(row=1, columnspan=5)

                    try:
                        for i in driver.window_handles:
                            driver.switch_to_window(i)
                            if "department.ssg.com/item/itemView.ssg" in driver.current_url:
                                windowNumber=i
                            else:
                                driver.close()
                        driver.switch_to_window(windowNumber)

                        cdtl = driver.find_element_by_class_name("cdtl_opt_select")
                        cdtl.click()

                        cdtlscroll = driver.find_element_by_class_name("cdtl_scroll")
                        li = cdtlscroll.find_elements_by_tag_name("li")

                        for i in li:
                            txt = i.find_element_by_class_name("txt")
                            if (size in txt.text) and ("품절" not in txt.text):
                                url = driver.current_url
                                btn = Button(outputFrame, text="신세계몰", command = lambda url=url: openSite(url), width=60)
                                btn.grid(row=outputBtnIndex, column=0)
                                outputBtnIndex = outputBtnIndex +1
                                print(size, "재고 있음 [신세계몰]")
                                break
                        
                    except:
                        print("폼이 다른 신세계몰")
                        pass
                    
                    
                elif "www.ssg" in driver.current_url:
                    introLabel = Label(window,text="SSG 검색중...", width=50, height=6)
                    introLabel.grid(row=1, columnspan=5)

                    try:
                        for i in driver.window_handles:
                            driver.switch_to_window(i)
                            if "ssg.com/item/itemView.ssg" in driver.current_url:
                                windowNumber=i
                            else:
                                driver.close()

                        driver.switch_to_window(windowNumber)

                        cdtl = driver.find_element_by_class_name("cdtl_opt_select")
                        cdtl.click()

                        cdtl_scroll = driver.find_element_by_class_name("cdtl_scroll")
                        li = cdtl_scroll.find_elements_by_tag_name("li")

                        for i in li:
                            txt = i.find_element_by_class_name("txt")
                            if (size in txt.text) and ("품절" not in txt.text):
                                url = driver.current_url
                                btn = Button(outputFrame, text="SSG", command =lambda url=url: openSite(url), width=60)
                                btn.grid(row=outputBtnIndex, column=0)
                                outputBtnIndex = outputBtnIndex+1
                                print(size, "재고 있음 [SSG]")
                                break
                                                
                    except:
                        print("폼이 다른 SSG")
                        pass
                    

            
                 
                elif "www.akmall" in driver.current_url:
                    introLabel = Label(window, text="AK몰 검색중...", width=50, height=6)
                    introLabel.grid(row=1, columnspan=5)
                    
                    try:
                        for i in driver.window_handles:    # 팝업 창 예외 처리 
                            driver.switch_to_window(i)
                            if 'www.akmall.com/goods/GoodsDetail' in driver.current_url:  
                                windowNumber = i
                            elif 'www.akmall.com/assc/associate.do' in driver.current_url:                   
                                while True:
                                    if 'www.akmall.com/goods/GoodsDetail' in driver.current_url:
                                        break;
                                    else:
                                        pass
                                windowNumber = i
                            else:
                                driver.close()
                            pass  
                        driver.switch_to_window(windowNumber)

                        selectMulti = driver.find_element_by_name("selectMulti")
                        selectMulti.click()
                        options = selectMulti.find_elements_by_tag_name("option")
                        print(len(options),"헤엑")
                        for i in options:
                            if (size in i.text and "품절" not in i.text) or size == i.text:
                                print(i.text)
                                url = driver.current_url
                                btn = Button(outputFrame, text="AK몰", command=lambda url=url:openSite(url), width=60)
                                btn.grid(row=outputBtnIndex, column=0)
                                outputBtnIndex = outputBtnIndex+1
                                print(size, "재고 있음 [AK몰]")
                                break
                        
                        
                    except:
                        print("폼이 다른 AK몰")
                        pass
        
                    
             
            print("검색 종료")
            for i in driver.window_handles:
                driver.switch_to_window(i)
                driver.close()
            outputPage()

        except:
            print("검색 종료")
                     
            for i in driver.window_handles:
                driver.switch_to_window(i)
                driver.close()
           
            outputPage()
            
        

def returnURL():
    return driver.current_url

def openSite(url):
    driver = webdriver.Chrome()
    driver.get(url)


window = Tk()
inputFrame = Frame(window)
outputFrame = Frame(window)
tempHref =[]
mulHref =[]
Href =[]
outputBtnIndex = 0
windowNumber = -1


initPage()


window.mainloop()
