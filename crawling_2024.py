import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# chrome driver 불러오기
filepath = '/Users/sykim/Downloads'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

login_url = "http://www.khoa.go.kr/oceangrid/cmm/login.do"
url = 'http://www.khoa.go.kr/oceangrid/gis/category/reference/distribution.do#none'

driver.get(login_url)

# login 하기
USERNAME = 'siye1015'
PASSWORD = 'tldP8*273'

username_input = driver.find_element(By.NAME, 'user_id')
password_input = driver.find_element(By.NAME, 'user_passwd')
submit_button = driver.find_element(By.ID, 'btn_login')

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
submit_button.click()

time.sleep(3)

driver.get(url)
driver.maximize_window()

# 자료 유형 및 기간 선택하기
radio_btn = driver.find_element(By.ID, 'radioTermHour')
radio_btn.click()
check_btn = driver.find_element(By.ID, 'allcheck')
check_btn.click()

select_year = Select(driver.find_element(By.ID, 'searchPreYear1'))
select_month = Select(driver.find_element(By.ID, 'searchPreMonth1'))

# 다운로드 버튼이 '통계기간'에 있는 항목 존재
flag=False


for year in range(2000, 2024):  # 년도
    select_year.select_by_value(str(year))

    new_folderpath = str(year)
    os.mkdir(new_folderpath)

    for month in range(1, 13):  # 월
        select_month.select_by_value(str(month).zfill(2))
        search_btn = driver.find_element(By.XPATH, "//a[@onclick='javascript:fn_search(10);']")
        search_btn.click()

        new_filepath = str(year)+ "_" + str(month)
        os.mkdir(os.path.join(new_folderpath, new_filepath))
        time.sleep(5)

        paging = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div[1]/div[2]")
        num_pages  = len(paging.find_elements(By.XPATH, ".//span"))-4   # 페이지 수 확인

        next_pages = num_pages-1    # 페이지 수-1 만큼 넘기기


        for page in range(num_pages):   # 페이지 마다
            table = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div[1]/table/tbody")
            row_list = table.find_elements(By.XPATH, ".//tr")   # 모든 tr 태그 찾기
 
             # clickable 확인
            wait = WebDriverWait(driver, 100)
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[5]')))
            except:
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[4]')))
        
        
            for row in row_list:    # 행 마다
   
                row_value = row.find_elements(By.XPATH, ".//td")
     
                loc = row_value[1].text     # 관측소명
                type = row_value[2].text    # 관측유형
                period = row_value[3].text  # 통계기간

                try:
                    download_btn = row_value[4].find_element(By.XPATH, ".//a")
                except:
                    download_btn = row_value[3].find_element(By.XPATH, ".//a")      # 다운로드 버튼이 '통계기간'에 있을 때
                    flag == True

                download_btn.click()

                time.sleep(2)

                # loc, type, period 으로 다운로드 파일 이름 바꾸기
                filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)

                if flag:
                    new_filename = loc + '_' + type + '.csv'
                    flag=False
                else:    
                    new_filename = loc + '_' + type + '_' + period + '.csv'

                shutil.move(os.path.join(filepath, filename), os.path.join(new_folderpath, new_filepath, new_filename))
            
            if next_pages:
                paging = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div[1]/div[2]")
                pages = paging.find_elements(By.XPATH, ".//span")

                click_btn = pages[-2].find_element(By.XPATH, ".//a")    # 다음 페이지 버튼
                click_btn.click()

                next_pages -=1
                time.sleep(3)
            




                    





driver.close()

