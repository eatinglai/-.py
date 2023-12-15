#高鐵爬蟲
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from captcha2upload import CaptchaUpload
import os
import time
import schedule
import random

##basic setup
s = 1
looptimes = random.randint(1,3)
waittimes = random.uniform(2,3)
asecond = random.uniform(0.3,1.2)
r = random.randint(0,2)
my_key = '2captch_key'
url = 'https://irs.thsrc.com.tw/IMINT/'
Path = '/Library/Developer/CommandLineTools/usr/bin/chromedriver'
filepath = '/Users/laieating/Downloads/captcha_image/'
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
service = webdriver.ChromeService(executable_path=Path)
driver = webdriver.Chrome(service=service, options=options)

def sol_popup():
    driver.get(url)
    time.sleep(asecond)
    try:
        popup = driver.find_element(By.ID, 'cookieAccpetBtn') 
        popup.click()
        time.sleep(asecond)
    except Exception as e:
        # 異常發生時的處理
        print(f"發生錯誤: {e}")
        print("cant close popup")
        time.sleep(2)

def thsr1():
    
    try:
        #來回票設定
        #tripopt = Select(driver.find_element(By.ID, 'BookingS1Form_tripCon_typesoftrip'))
        #tripopt.select_by_value('1')

        startstation = Select(driver.find_element(By.NAME, 'selectStartStation'))
        startstation.select_by_value('12')

        deliverystation = Select(driver.find_element(By.NAME, 'selectDestinationStation'))
        deliverystation.select_by_value('2')
        time.sleep(asecond)

    except Exception as e:
        # 異常發生時的處理
        print(f"發生錯誤: {e}")
        print("thsr1 error!")
        time.sleep(2)

def thsr2():
    try:
        findtime = driver.find_elements(By.CLASS_NAME, 'uk-input')
        clicktime = findtime[1]
        clicktime.click()
        findday = driver.find_elements(By.XPATH, '//span[@aria-label="十二月 2, 2023"]')
        for index, date in enumerate(findday):
            try:
                date.click()
            except Exception as e:
                # 異常發生時的處理
                print(f"發生錯誤: {e}")
                print("cant find clickable time")
                time.sleep(asecond)
                continue
            print(f"try clickdate for {index+1} time")
        findhour = Select(driver.find_element(By.XPATH, '//select[@name="toTimeTable"]'))
        findhour.select_by_visible_text("07:00")

    except Exception as e:
        # 異常發生時的處理
        print(f"發生錯誤: {e}")
        print("thsr2 error!")
        time.sleep(1)
        
def thsr3():
    try:
        #顯示隱藏：driver.execute_script("arguments[0].style.visibility = 'visible';", clicktime)
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'ticketPanel:rows:0:ticketAmount'))
        )
        findpeople = Select(dropdown_element)
        findpeople.select_by_visible_text('3')
        time.sleep(asecond)

    except Exception as e:
        # 異常發生時的處理
        print(f"發生錯誤: {e}")
        print("thsr3 error!")
        time.sleep(1)

def thsrimg():
    try:
        # 找到要下載的圖片元素
        captcha_img = driver.find_element(By.XPATH, '//img[@id="BookingS1Form_homeCaptcha_passCode"]')
        # 獲取圖片的URL
        captchaimg_path = filepath + 'screenshot.png'
        captcha_img.screenshot(captchaimg_path)
        captcha = CaptchaUpload(my_key)
        captcha_code = captcha.solve(captchaimg_path)
        send_code = driver.find_element(By.XPATH, '//input[@id="securityCode"]')
        send_code.send_keys(captcha_code)
        print(captcha_code)
        time.sleep(asecond)

    except Exception as e:
        # 異常發生時的處理
        print(f"發生錯誤: {e}")
        print("cant proccess captchaimg")
        time.sleep(1)

def submitting():
    submit_1 = driver.find_element(By.ID, 'SubmitButton')
    submit_1.click()
    time.sleep(waittimes)

def thsr4():
    try:
        checkpage = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@id="BookingS2Form_TrainQueryDataViewPanel"]')))
        driver.execute_script("window.scrollBy(0, 200);")
        trainfind = driver.find_elements(By.XPATH, '//input[@querydeparture="07:55"]')
        for index, trainclick in enumerate(trainfind):
            try:
                trainclick.click()
            except Exception as e:
                # 異常發生時的處理
                print(f"發生錯誤: {e}")
                print("cant find clickable train")
                time.sleep(asecond)
                continue
            print(f"try clicktrain for {index+1} time")
        driver.execute_script("window.scrollBy(0, 300);")
        submit2 = driver.find_element(By.XPATH, '//input[@name="SubmitButton"]')
        submit2.click()
        time.sleep(waittimes)
        
    except Exception as e:
        # 異常發生時的處理
        print(f"發生錯誤: {e}")
        print("thsr4 error!")
        time.sleep(1)

def thsr5():
    try:
        checkpage = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//section[@class="ticket-summary"]')))
        order_path = filepath + 'order_record.png'
        driver.save_screenshot(order_path)
        driver.execute_script("window.scrollBy(0, 300);")
        id = driver.find_element(By.XPATH, '//input[@id="idNumber"]')
        id.send_keys('E100000001')
        phone = driver.find_element(By.XPATH, '//input[@id="mobilePhone"]')
        phone.send_keys('0900000001')
        email = driver.find_element(By.XPATH, '//input[@id="email"]')
        email.send_keys('mymail@gmail.com')
        driver.execute_script("window.scrollBy(0, 300);")
        member_check = driver.find_element(By.XPATH, '//input[@id="memberSystemRadio1"]')
        member_check.click()
        member = driver.find_element(By.XPATH, '//input[@id="memberShipCheckBox"]')
        member.click()
        agreement = driver.find_element(By.XPATH, '//input[@name="agree"]')
        agreement.click()
        time.sleep(waittimes)

        #submit3 = driver.find_element(By.XPATH, '//input[@id="isSubmit"]')
        #submit3.click()

    except Exception as e:
        # 異常發生時的處理
        print("thsr5 error!")
        print(f"發生錯誤: {e}")
        time.sleep(1)
        print("Restarting the process...")

def test_basic_options():
    print("none")
    #options = webdriver.ChromeOptions()
    #options.add_argument("Accept-Encoding: gzip, deflate, br")
    #options.add_argument("Connection: keep-alive")
    #options.add_argument("Referer: https://irs.thsrc.com.tw/IMINT/")
    #options.add_argument("Sec-Fetch-Dest: document")
    #options.add_argument("Sec-Fetch-Mode: navigate")
    #options.add_argument("Cookie: JSESSIONID=FB731FA8686F753CFF9799837C80F86C; _ga=GA1.3.1064767780.1699074824; _ga_6M07CCJT7N=GS1.1.1699074824.1.1.1699075049.60.0.0; _gat_UA-9967381-26=1; _gid=GA1.3.1364035233.1699074824; bm_sv=D65B36A3B53F39378E1AAAE8F3796893~YAAQw4pFy/o5FpOLAQAAUKbAmBUXMjr+KDdgJd7v6XgPqQIm2fWkXDOrno7MMtuRtCWwWuSkgvPR0rU6T8tWoKuYskoFG/xL4EcFNMUUrSoLXAGb0o7Nck4idS/tw2bKU2Osa3l33SDo0rt54Sb/k+pBsYTT5aYMKsDBcpaJ+W9VPFTedI9dAOjSPXPnzLJX8ACWs4F1SRZbKdLEJZMd5xLL+D7I6BH1hONvf1FysnKwZJvErZ4D+fZ2/7ZEXYLy+YkC~1; JSESSIONID=FB731FA8686F753CFF9799837C80F86C; TS01a1ad28=01ea55a4f90e8b127e8dca0ea11ecf61afbd80af51b04b8f750de8b6b7f58ffba0c65683ab319877bfb362b2a823e8f8efdf400c34; ak_bmsc=1466BC3BD653C157202A8FC6B163BE2E~000000000000000000000000000000~YAAQw4pFywU4FpOLAQAAR1jAmBVQO8pT93+284wnjf2VFQCvqYP9gbz8wldwK/J22VFPdkKDwQdyO9FRbPC9joeE40HV6Z+craA/f/l8z3GSHmKM95IpBd1Vn3oP2T4q9zUUw5XWzk1LnwG23zZvT6kQIHM4K/wxI2IZwqB5cyexlZ/K2VimYEyiI3W5G1Qfu+/H4W8fKKUbRct3MFeBnjYODnvQe6WOIKg/w8kjiYJvQqzi4EXf+5nETYF4hyX3t7fryMenWe/rC0MN4gXr0PrpuWuQnmXOp+2xBAq1IlgvJkCS0hGbbecplR328XWc684sm4S6Twc87Rt5ptlsqd7BI/prPDxZRx0Dv+CUI16rrTt36B1e5ty7CD3JcVfLFUnM97tcBt6+YSK1YnPIIUb79m0pHYZWri2PznX7DQZWsyvw0TqB0rFoGqhuw1fbxNfjmHNXEQZQvyZlDW7zNMbse9zzsApQBJua9jsJs7FNmPow68KaJXVy998d0mQ7xa9oNMhwAmmtRt6+Q480LjtO1OFrVJ4wWtHRVqs=; bm_mi=33DA874B5E6C18E30E102D7F274AD06E~YAAQw4pFy9U3FpOLAQAAqVTAmBUrQbSOcRueTcBgyZGbGDHV9ysHZtWXCj5u3wbAHKJ6bpDCPyMrOZLCS24dK6AFDPEulx4mC4yed+x18CctsWy1U5Vizl6ak6CXME0/rqfyOKWJ8Jcjgrnkc8pTTIBZJYhBKdcAEyaKYZNvfd6cUyFnhB2YAK3mWr3hnxNsyHvGaG2QSPEM42Ly5WwzyhyKAkvtyU7ZcnJ7zWG2ghRggoGe+GqjDLlo8dswmz6AxOTFJFHZzkH/EulFTs9chFwvC4D2MLonhlyj/6y1q0DYv912feYct2bQXcdy4ZShRYwN2w11~1; IRS-SESSION=!aaaTAODiCfcFf6vqzadA/cVfsw5v9QiQxIFajyzMECY1IWZ9GSsSukDHE9CcDW/C; THSRC-IRS=!XZkLyhO0L2l3iknrPTQ8cjzg9I33e0Xx7yCibz+YmrhsbGxbKxQ+uvh18gEMHZlstn23SfsrBx8cSg==")
    #options.add_argument("Sec-Fetch-Site: same-origin")
    #driver = webdriver.Chrome(options=options)
    #driver.quit()

def check_for_errors():
    # 檢查是否有錯誤訊息，這裡假設錯誤訊息是根據某個元素是否存在來判斷
    try:
        error_message = driver.find_element(By.XPATH, '//span[@class="feedbackPanelERROR"]')
        return True
    except:
        return False

def main_randomly():
    print(f'執行：{r}' )
    sol_popup()
    #檢測錯誤重複執行
    while True:
        try:
            #步驟1~3隨機順序
            if r == 1:
                thsr1()
                thsrimg()
                thsr2()
                thsr3()
                        
            elif r ==2:
                thsr1()
                thsr2()
                thsrimg()
                thsr3()
                
            else:
                thsrimg()
                thsr1()
                thsr2()
                thsr3()
            submitting()

            # 檢查是否有錯誤訊息
            if check_for_errors():
                print("發現錯誤訊息，重新開始程式...")
                continue  # 重新開始迴圈
            else:
                print("沒有錯誤訊息，繼續執行程式...")
                thsr4()
                thsr5()
                break  # 跳出迴圈，程式完成
        except Exception as e:
            print(f"發生錯誤: {e}")
            print("重新啟動程式...")
            continue  # 重新開始迴圈
    print('Done! End in...')
    for i in range(5,0,-1):
        print(i)
        time.sleep(1)    

main_randomly()
