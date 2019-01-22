# coding:utf-8
"""
author:C-YC
target:爬取09-18年所有电影的豆瓣评分和星星百分比，以及好中差评比例
finish date: 2019.01.22
"""
import sys
import time
import os
import json
import urllib
from selenium import webdriver
reload(sys)
sys.setdefaultencoding("utf-8")
driver = webdriver.Firefox(executable_path='./geckodriver')


def getDouban(id,year,name):
    # 获取豆瓣评分
    score = ''
    star = ''
    comment = ''
    url = 'https://movie.douban.com/subject_search?search_text='+urllib.quote(name)  # 使用urllib改变中文编码
    print "搜索链接：",url
    driver.get(url)
    time.sleep(2)
    texts = driver.find_elements_by_xpath("//a[@class='title-text']")  # 搜索电影名字获得结果
    print "texts的长度：",len(texts)
    if len(texts) == 0:
        return
    else:
        for t in range(len(texts)):
            title = texts[t].text
            print title
            time.sleep(0.5)
            if name in title:  # 判断是否是所要查找的电影
                if year in title or str(int(year)-1) in title or str(int(year)+1) in title:
                    movie_url = texts[t].get_attribute('href')
                    print "电影链接：",movie_url
                    driver.get(movie_url)
                    time.sleep(1)
                    try:
                        score = driver.find_element_by_xpath("//div[@id='interest_sectl']//strong[@class='ll rating_num']").text
                        if len(score) == 0:
                            score = '0.0'
                            star = '5星`0.0%##4星`0.0%##3星`0.0%##2星`0.0%##1星`0.0%##'
                            print "豆瓣评分：", score
                            print "星星比例：",star
                        score_content = driver.find_elements_by_xpath("//div[@class='ratings-on-weight']/div[@class='item']")
                        for item in score_content:
                            star_num = item.find_element_by_xpath('span').text
                            star_per = item.find_element_by_xpath("span[@class='rating_per']").text
                            star = star + (star_num+"`"+star_per) + "##"
                            print star_num,star_per
                        print star
                        comment_url = movie_url+'comments?status=P'
                        driver.get(comment_url)
                        time.sleep(1)
                        try:
                            comments = driver.find_elements_by_xpath("//div[@class='comment-filter']/label")
                            for i in range(1,4):
                                comment_style = comments[i].find_element_by_xpath("span[@class='filter-name']").text
                                comment_per = comments[i].find_element_by_xpath("span[@class='comment-percent']").text
                                comment = comment + (comment_style+"`"+comment_per)+"##"
                                print comment_style, comment_per
                            print comment
                        except:
                            comment = '好评`0%##一般`0%##差评`0%##'
                            print comment
                    except:
                        score = '0.0'
                        star = '5星`0.0%##4星`0.0%##3星`0.0%##2星`0.0%##1星`0.0%##'
                        comment = '好评`0%##一般`0%##差评`0%##'
                        print "豆瓣评分：", score
                        print "星星比例：", star
                        print comment
                    finally:
                        data = {
                            "douban_score": score,
                            "start_5": star.split('##')[0].split('`')[1],
                            "start_4": star.split('##')[1].split('`')[1],
                            "start_3": star.split('##')[2].split('`')[1],
                            "start_2": star.split('##')[3].split('`')[1],
                            "start_1": star.split('##')[4].split('`')[1],
                            "h": comment.split("##")[0].split('`')[1],
                            "m": comment.split("##")[1].split('`')[1],
                            "l": comment.split("##")[2].split('`')[1]
                        }
                        with open('../movies_douban/'+year+'/'+id+'.json','w+')as f:  # json存储数据
                            json.dump(data, f, ensure_ascii=False)
                    break
            else:
                pass


def main():
    with open('../data/hasCrwaled2.log', 'r')as f3:
        row = f3.readlines()[-1].replace('\n','')
    cYear = row.split(',')[0]
    cPage = row.split(',')[1]
    total = row.split(',')[2]
    print cYear,cPage,total
    if cPage == total:
        year = int(cYear) + 1
    else:
        year = int(cYear)
    for year in range(year, 2019):
        with open('../data/hasCrwaled2.log', 'r')as f3:
            row = f3.readlines()[-1].replace('\n', '')
        ccYear = row.split(',')[0]
        if year == int(ccYear) + 1:
            with open('../data/China_boxOffice/movie_'+str(year)+'.csv','r')as f1:
                lines = f1.readlines()
                for l in range(len(lines)):
                    movie_id = lines[l].split(',')[0]
                    movie_name = lines[l].split(',')[1]
                    movie_year = str(year)
                    print "电影名字：",movie_name
                    getDouban(movie_id,movie_year,movie_name)
                    with open('../data/hasCrwaled2.log','a+')as f2:
                        f2.write(movie_year+","+str(l)+","+str(len(lines)-1)+"\n")
        else:
            print "当前年份：", year
            with open('../data/China_boxOffice/movie_' + str(year) + '.csv', 'r')as f4:
                lines = f4.readlines()
                for i in range(int(cPage), len(lines)):
                    page = i
                    movie_id = lines[i].split(',')[0]
                    movie_name = lines[i].split(',')[1]
                    movie_year = str(year)
                    print "电影名字：", movie_name
                    getDouban(movie_id, movie_year,movie_name)
                    with open('../data/hasCrwaled2.log', 'a+')as f5:
                        f5.write(movie_year + "," + str(page) + "," + str(len(lines) - 1) + "\n")


def login_Douban():
    driver.get('https://www.douban.com/accounts/login?source=main')
    time.sleep(1)
    driver.find_element_by_xpath("//input[@id='email']").send_keys('1425575659@qq.com')
    time.sleep(0.5)
    driver.find_element_by_xpath("//input[@id='password']").send_keys('zxcvbnm,233')
    time.sleep(10)
    driver.find_element_by_xpath("//input[@class='btn-submit']").click()


if __name__ == '__main__':
    login_Douban()
    main()