# coding:utf-8
"""
author:C-YC
target:爬取09-18年所有电影的简介和猫眼评分
finish date: 2019.01.20
"""
import sys
import time
import os
import json
import urllib
from selenium import webdriver
reload(sys)
sys.setdefaultencoding("utf-8")
driver = webdriver.PhantomJS(executable_path='./phantomjs')


def getContent(year, id, name):
    search_url = 'https://maoyan.com/query?kw=' + urllib.quote(name)
    print search_url
    driver.get(search_url)
    time.sleep(1)
    try:
        movie_url = driver.find_element_by_xpath("//dl[@class='movie-list']/dd//a").get_attribute('href')
        print "电影链接：:",movie_url
        driver.get(movie_url)
        time.sleep(1)
        try:
            movie_info = driver.find_element_by_xpath("//div[@class='mod-content']").text
            print "电影简介：", movie_info
            try:
                s = str(driver.find_element_by_xpath("//div[@class='star-wrapper']/div").get_attribute('style')
                        .replace('width:', '').replace('%;', ''))
                print s
                movie_score = float(s)/10.0
                print "评分：", movie_score
            except Exception,e:
                print e
                movie_score = 0.0
                print "评分：", movie_score
        except Exception, e:
            print e
            movie_info = '无'
            print "电影简介：", movie_info
        finally:
            data = {
                "movie_id": id,
                "movie_name": name,
                "introduction": movie_info,
                "cat_score": movie_score
            }
            with open("../movies_maoyan/"+year+"/"+id+".json","w+")as f1:
                json.dump(data, f1, ensure_ascii=False)
    except:
        return


def main():
    with open('../data/hasCrwaled.log', 'r')as f1:
        lines = f1.readlines()[-1].replace("\n", "")
    year = lines.split(',')[0]
    line = lines.split(',')[1]
    print "当前年份和行数： ",year,line
    with open('../data/China_boxOffice/movie_'+year+'.csv', 'r')as f2:
        all = f2.readlines()
        print "全部行数：",len(all)-1
    if line != str(len(all)-1):
        print "当前年份：",year
        for l in range(int(line), len(all)):
            movie_year = year
            movie_id = all[l].split(',')[0]
            movie_name = all[l].split(',')[1]
            print "电影名字：", movie_name
            getContent(movie_year, movie_id, movie_name)
            with open("../data/hasCrwaled.log", "a+")as f3:
                f3.write(movie_year+","+str(l)+"\n")
    else:
        year = str(int(year)+1)
        print "当前年份：",year
        with open('../data/China_boxOffice/movie_' + str(year) + '.csv', 'r')as f4:
            all1 = f4.readlines()
            print "全部行数：", len(all1)
        for l in range(len(all1)):
            movie_year = year
            movie_id = all[l].split(',')[0]
            movie_name = all[l].split(',')[1]
            print "电影名字：", movie_name
            getContent(movie_year, movie_id, movie_name)
            with open("../data/hasCrwaled.log", "a+")as f5:
                f5.write(movie_year + "," + str(l) + "\n")


if __name__ == '__main__':
    main()
