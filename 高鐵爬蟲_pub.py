from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from captcha2upload import CaptchaUpload
import os
import time
import random

# Basic setup
s = 1
looptimes = random.randint(1, 3)
waittimes = random.uniform(2, 3)
asecond = random.uniform(0.3, 1.2)
r = random.randint(0, 2)
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
        print(f"發生錯誤: {e}")
        print("Can't close popup")
        time.sleep(2)

def select_station(element_name, value):
    try:
        station_select = Select(driver.find_element(By.NAME, element_name))
        station_select.select_by_value(value)
        time.sleep(asecond)
    except Exception as e:
        print(f"發生錯誤: {e}")
        print("Station selection error!")
        time.sleep(2)

def select_date():
    try:
        findtime = driver.find_elements(By.CLASS_NAME, 'uk-input')
        clicktime = findtime[1]
        clicktime.click()
        findday = driver.find_elements(By.XPATH, '//span[@aria-label="十二月 2, 2023"]')
        for index, date in enumerate(findday):
            try:
                date.click()
            except Exception as e:
                print(f"發生錯誤: {e}")
                print("Can't find clickable time")
                time.sleep(asecond)
                continue
            print(f"Try clickdate for {index+1} time")
        findhour = Select(driver.find_element(By.XPATH, '//select[@name="toTimeTable"]'))
        findhour.select_by_visible_text("07:00")
    except Exception as e:
        print(f"發生錯誤: {e}")
        print("Date selection error!")
        time.sleep(1)

def select_passengers():
    try:
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'ticketPanel:rows:0:ticketAmount'))
        )
        findpeople = Select(dropdown_element)
        findpeople.select_by_visible_text('3')
        time.sleep(asecond)
    except Exception as e:
        print(f"發生錯誤: {e}")
        print("Passenger selection error!")
        time.sleep(1)

def process_captcha():
    try:
        captcha_img = driver.find_element(By.XPATH, '//img[@id="BookingS1Form_homeCaptcha_passCode"]')
        captchaimg_path = filepath + 'screenshot.png'
        captcha_img.screenshot(captchaimg_path)
        captcha = CaptchaUpload(my_key)
        captcha_code = captcha.solve(captchaimg_path)
        send_code = driver.find_element(By.XPATH, '//input[@id="securityCode"]')
        send_code.send_keys(captcha_code)
        print(captcha_code)
        time.sleep(asecond)
    except Exception as e:
        print(f"發生錯誤: {e}")
        print("Can't process captcha image")
        time.sleep(1)

def submitting():
    submit_1 = driver.find_element(By.ID, 'SubmitButton')
    submit_1.click()
    time.sleep(waittimes)

def select_train():
    try:
        checkpage = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="BookingS2Form_TrainQueryDataViewPanel"]')))
        driver.execute_script("window.scrollBy(0, 200);")
        trainfind = driver.find_elements(By.XPATH, '//input[@querydeparture="07:55"]')
        for index, trainclick in enumerate(trainfind):
            try:
                trainclick.click()
            except Exception as e:
                print(f"發生錯誤: {e}")
                print("Can't find clickable train")
                time.sleep(asecond)
                continue
            print(f"Try clicktrain for {index+1} time")
        driver.execute_script("window.scrollBy(0, 300);")
        submit2 = driver.find_element(By.XPATH, '//input[@name="SubmitButton"]')
        submit2.click()
        time.sleep(waittimes)
    except Exception as e:
        print(f"發生錯誤: {e}")
        print("Train selection error!")
        time.sleep(1)

def fill_personal_info():
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
        # submit3 = driver.find_element(By.XPATH, '//input[@id="isSubmit"]')
        # submit3.click()
    except Exception as e:
        print("Personal info submission error!")
        print(f"發生錯誤: {e}")
        time.sleep(1)
        print("Restarting the process...")

def check_for_errors():
    try:
        error_message = driver.find_element(By.XPATH, '//span[@class="feedbackPanelERROR"]')
        return True
    except:
        return False

def main_randomly():
    print(f'執行：{r}')
    sol_popup()
    while True:
        try:
            if r == 1:
                thsr1()
                process_captcha()
                select_date()
                select_passengers()
            elif r == 2:
                thsr1()
                select_date()
                process_captcha()
                select_passengers()
            else:
                process_captcha()
                thsr1()
                select_date()
                select_passengers()
            submitting()

            if check_for_errors():
                print("發現錯誤訊息，重新開始程式...")
                continue
            else:
                print("沒有錯誤訊息，繼續執行程式...")
                select_train()
                fill_personal_info()
                break
        except Exception as e:
            print(f"發生錯誤: {e}")
            print("重新啟動程式...")
            continue
    print('Done! End in...')
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

main_randomly()
