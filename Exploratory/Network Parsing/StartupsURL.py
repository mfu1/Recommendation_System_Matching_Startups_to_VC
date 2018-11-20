# !/usr/bin/env python
# -*- coding: utf-8 -*

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import urllib
from bs4 import BeautifulSoup

import json, time, re, sys, random
reload(sys)
sys.setdefaultencoding('utf8')

# set up browser
def set_browser(size1,size2,secs):
    headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'Connection': 'keep-alive'
            }
    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = random.choice(['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
                                                                                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                                                                                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
                                                                                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                                                                                  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                                                                                                  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'])
    driver = webdriver.PhantomJS()
    driver.set_window_size(size1,size2)
    wait = ui.WebDriverWait(driver, secs)
    return driver, wait

# get startup companies in certain industry
# setting diverse criteria to avoid searching limitation
def get_full_url(market):
    base_url = 'https://angel.co/companies?locations[]=1688-United+States&markets[]={}&'.format(market)
    params1, params2, params3 = {}, {}, {}
    full_url = []

    # 1) get by raised around 1929
    x = 100000
    raised_min1 = [1, 1*x+1, 5*x+1, 20*x+1, 100*x+1, 800*x+1]
    raised_max1 = [1*x, 5*x, 20*x, 100*x, 800*x, 1000000*x]
    for i in range(len(raised_min1)):
        params1['raised[min]'] = raised_min1[i]
        params1['raised[max]'] = raised_max1[i]
        data1 = urllib.urlencode(params1)
        full_url.append(base_url + data1)

    # # 2) when raised = 0, get by signal around 635
    # raised = 'raised[min]=0&raised[max]=0&'
    # signal_min2 = [8,7]
    # signal_max2 = [10,8]
    # for i in range(len(signal_min2)):
    #     params2['signal[min]'] = signal_min2[i]
    #     params2['signal[max]'] = signal_max2[i]
    #     data2 = urllib.urlencode(params2)
    #     full_url.append(base_url + raised + data2)

    # # 3) when raised = 0 & signal too many, get by signal & rounds around 1180
    # raised = 'raised[min]=0&raised[max]=0&'
    # stage = 'stage[]=Seed&stage[]=Series+A&stage[]=Series+B&stage[]=Series+C&stage[]=Acquired&'
    # signal_min3 = [5,4,0]
    # signal_max3 = [7,5,4]
    # for i in range(len(signal_min3)):
    #     params3['signal[min]'] = signal_min3[i]
    #     params3['signal[max]'] = signal_max3[i]
    #     data3 = urllib.urlencode(params3)
    #     full_url.append(base_url + raised + stage + data3)
        
    return full_url

# parse each webpage to get company information and url link
def get_startups_url(market, url_num):
    # 1) setup cache file
    cache_fname = 'cache_startups_url' + str(url_num) + '.txt'
    try:
        fobj = open(cache_fname, 'r')
        cache_startups_url = json.loads(fobj)
        fobj.close()
    except:
        cache_startups_url = {}

    # 2) setup output file
    with open('startups_info' + str(url_num) + '.csv', 'w') as f:   
        f.write('Company Name, URL, Pitch, Signal, Location, Markets, Website, Employees, Stage, Total Raised\n')

    # 3) open and load JS page
    driver, wait = set_browser(1560, 1600, 10)
    startup_urls = {}
    full_url = get_full_url(market)[url_num]
    driver.get(full_url)

    print ('Saving data from {}:'.format(full_url))
    page_num = 0
    anchor = '//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[22]'
    anchor_plus = '/div/div[21]'
    while True:
        try:
            wait.until(lambda dr: dr.find_element_by_xpath(anchor).is_displayed())
            elem = driver.find_element_by_xpath(anchor)
            elem.click()
            time.sleep(1)
            page_num += 1
            print ('Loading more {}'.format(page_num))
            anchor += anchor_plus
        except:
            break

    # 4) get info and save to csv
    with open('startups_info' + str(url_num) + '.csv', 'a+') as f:
        data = driver.find_elements_by_xpath('//div[@class="base startup"]')
        for i in range(len(data)):
            # print dir(data[0])
            name = data[i].find_element_by_class_name('name').find_element_by_tag_name('a').text.replace(',', ';')
            url = data[i].find_element_by_class_name('name').find_element_by_tag_name('a').get_attribute('href')
            pitch = data[i].find_element_by_class_name('pitch').text.replace(',', ';')
            signal = data[i].find_elements_by_tag_name('img')[1].get_attribute('alt')
            location = data[i].find_elements_by_class_name('tag')[0].text.replace(',', ';')
            markets = data[i].find_elements_by_class_name('tag')[1].text.replace(',', ';')
            try:
                website = data[i].find_element_by_class_name('website').find_element_by_tag_name('a').get_attribute('href')
            except:
                website = ''
            employees = data[i].find_elements_by_xpath('//*[@class="column company_size"]')[i+1].text
            stage = data[i].find_elements_by_xpath('//*[@class="column stage"]')[i+1].text
            raised = data[i].find_elements_by_xpath('//*[@class="column raised"]')[i].text.replace(',', '')               

            if name not in cache_startups_url:
                f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(name, url, pitch, signal, location, markets, website, employees, stage, raised))
                cache_startups_url[name] = url
            else:
                print ('Startup {} Exists'.format(name))

        with open(cache_fname, 'wb') as fobj:
            fobj = json.dumps(cache_startups_url)
        print ('Total companies in this page: {}'.format(len(data)))
    return cache_startups_url

# get back {company name: url, ...} dictionary for the url_num part
def load_startups_url(url_num):
    startup_urls = {}
    with open('startups_info' + str(url_num) + '.csv', 'r') as f:
        for line in f:
            if re.match(r'Company Name', line):
                continue
            line = line.split(',')
            startup_urls[line[0]] = line[1]
    return startup_urls 





