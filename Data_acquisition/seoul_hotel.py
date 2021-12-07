import platform
import sys
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

# 목표 : 여기어때의 사이트에서 원하는 항목을 검색하여
# 각 리뷰의 평점과 리뷰 text를 들고와서 csv로 저장하기

driver = webdriver.Chrome()
# 여기어때 url
driver.get('https://www.dailyhotel.com/stays?shortCutType=stayAll&regionStayType=new_all&dateCheckIn=2021-12-06&rai=300000016&rpi=300000016&stays=1&reg=0')
time.sleep(1)

# 스크롤 내리기
def doScrollDown(whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break
        
doScrollDown(2)

driver.implicitly_wait(5)


j=1
while True: 
    if j == 100:
        break
    else:
        # 호텔 클릭해서 호텔 링크로 이동
        hotel = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/ul/div[1]/div/li['+str(j)+']/div[2]/div[1]/div[2]/div[1]')
        driver.implicitly_wait(0.5)
        hotel.click()

        driver.implicitly_wait(2)
        # 리뷰 페이지로 이동
        review = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div[2]/div[2]/div[2]/div/a/span[2]')
        driver.implicitly_wait(1)
        review.click()

        review_list = []
        i = 1

        # 전체 리뷰 개수
        all_review_cnt = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[5]/div[7]/strong')
        all_review_cnt = all_review_cnt.text[3:-1]
        print(all_review_cnt)
    
        for i in range(1,int(all_review_cnt)+1):
            try:
                review_txt = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[5]/ul/li['+str(i)+']/div[3]/div')
                review_star = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[5]/ul/li['+str(i)+']/div[1]/span[2]')
                # 리뷰 별점 들고오기 

                review_list.append([review_star.text,review_txt.text])
                            
                print(i,"번째 리뷰")
                print(review_star.text,review_txt.text)
                i+=1
                    
                # # 마지막 review면 
                # if i ==  int(all_review_cnt):
                #     break 
            except:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(1.5)


time.sleep(1) 

# csv 파일로 저장 
df = pd.DataFrame(review_list, columns=['star','review'])
df.to_csv('seoul_hotel_review.csv', index=False, encoding='utf-8-sig')



