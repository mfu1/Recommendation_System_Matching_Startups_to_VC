# !/usr/bin/env python
# -*- coding: utf-8 -*

from StartupsURL import *

def get_founder_funding(url_num):
    funding = {}
    founder = {}
    startup_urls = sorted(load_startups_url(url_num).items())
    driver1, wait1 = set_browser(1560, 1600, 10)
    driver2, wait2 = set_browser(1560, 36000, 60)

    # ==================initial files=====================
    # print startup_urls

    # with open('startups_funding' + str(url_num) + '.csv', 'w') as f0:   
    #     f0.write('Company Name, Round, Type, Date, Amount, News, Investors, Investor Location\n')

    # with open('startups_founder_networks' + str(url_num) + '.csv', 'w') as f1:   
    #     f1.write('Company Name, Founder, School, Former Companies, Linkedin\n')

    # with open('startups_founder_skills' + str(url_num) + '.csv', 'w') as f2:   
    #     f2.write('Company Name, Founder, Major, Former Position, Top Skills\n')

    # with open('startups_founder_influence' + str(url_num) + '.csv', 'w') as f3:   
    #     f3.write('Company Name, Founder, Tweets, Following, Followers, Retweets, Likes, Twittwer\n')

    # ===========to resume crawling data uncomment line 29 and comment line 30==================
    # for co_name, co_url in startup_urls[startup_urls.index(('Careport Health', 'https://angel.co/careport-health')):]:
    for co_name, co_url in startup_urls:
        co_name = co_name.strip()
        funding[co_name] = {}
        founder[co_name] = {}
        print co_name, co_url

        driver1.get(co_url)
        time.sleep(random.randint(20,30))  
        html = driver1.page_source
        # html = urllib.urlopen(co_url).read()
        # print html

        # fundings
        try:
            fundings = driver1.find_element_by_xpath('//ul[@class="startup_rounds with_rounds"]').find_elements_by_tag_name('li')
            for i in range(len(fundings)):
                funding[co_name][i] = {}
                try:
                    funding[co_name][i]['type'] = fundings[i].find_element_by_class_name('type').text.replace(',','+')
                    funding_type = funding[co_name][i]['type']
                except:
                    funding[co_name][i]['type'] = ''
                funding_type = funding[co_name][i]['type']
                print 'type: ' + funding_type

                try:
                    funding[co_name][i]['date'] = fundings[i].find_element_by_class_name('date_display').text.replace(',','')
                    funding_date = funding[co_name][i]['date']
                except:
                    funding[co_name][i]['date'] = ''
                    funding_date = ''
                print 'date: ' + funding_date

                try:
                    funding[co_name][i]['amount'] = fundings[i].find_element_by_class_name('raised').text.replace(',','')
                    funding_amount = funding[co_name][i]['amount']
                except:
                    funding[co_name][i]['amount'] = ''
                    funding_amount = ''
                print 'amount: ' + funding_amount

                try:
                    funding[co_name][i]['news'] = fundings[i].find_element_by_class_name('raised').find_element_by_tag_name('a').get_attribute('href')
                    funding_news = funding[co_name][i]['news']
                except:
                    funding[co_name][i]['news'] = ''
                    funding_news = ''
                print 'news: ' + funding_news

                try:
                    elems = fundings[i].find_elements_by_class_name('more_participants_link')
                    for elem in elems:
                        elem.click()
                    time.sleep(2)
                except:
                    print 'no elems'

                try:
                    funding[co_name][i]['investors'] = [j.text.replace(',','+') for j in fundings[i].find_elements_by_class_name('name')]                    
                    investors = '|'.join(funding[co_name][i]['investors'])
                except:
                    funding[co_name][i]['investors'] = ''
                    investors = ''
                print 'investors: ' + investors

                try:
                    funding[co_name][i]['investors_location'] = [j.find_elements_by_tag_name('a')[1].text.replace(',','+') for j in fundings[i].find_elements_by_class_name('tags')]
                    investors_location = '|'.join(funding[co_name][i]['investors_location'])
                except:
                    funding[co_name][i]['investors_location'] = ''
                    investors_location = ''
                print 'investors_location: ' + investors_location

                try:
                    with open('startups_funding' + str(url_num) + '.csv', 'a+') as f0:
                        i = str(i)
                        f0.write('{},{},{},{},{},{},{},{}\n'.format(co_name, i, funding_type, funding_date, funding_amount, funding_news, investors, investors_location))
                except:
                    print 'failed to write csv'
        except:
            print 'No Fundings'

        # founders
        soup = BeautifulSoup(html, 'html.parser') 
        try:
            founders = soup.find('ul', class_='larger roles')
            founders = founders.find_all('li')
            for fo in founders:
                if fo.find('img')['src'] != 'https://angel.co/images/shared/nopic.png':
                    founder_name = fo.find('div', class_='name').get_text().replace(',','+').strip()
                    founder[co_name][founder_name] = {}
                    print founder_name
                    if fo.find('a')['href']:
                        print fo.find('a')['href']
                        driver1.get(fo.find('a')['href'])
                        time.sleep(random.randint(31,42))
                        founder_page = driver1.page_source
                        # founder_page = urllib.urlopen(fo.find('a')['href']).read()
                        founder_soup = BeautifulSoup(founder_page, 'html.parser')
                            
                        try:
                            linkedin_url = founder_soup.find('a', class_='icon link_el fontello-linkedin')['href']
                            founder[co_name][founder_name]['linkedin'] = linkedin_url
                            print founder[co_name][founder_name]['linkedin']
                            driver1.get(linkedin_url)
                            time.sleep(10)
                            linkedin_page = driver1.page_source
                            # linkedin_page = urllib.unquote(urllib.urlopen(linkedin_url).read())
                            # print linkedin_page
                            linkedin_soup = BeautifulSoup(linkedin_page, 'html.parser')

                            if linkedin_soup.find('h1') != 'Profile Not Found':
                                try:
                                    founder[co_name][founder_name]['school'] = list(set([school.find('h4', class_='item-title').get_text().replace(',','+') for school in linkedin_soup.find('section', id='education').find_all('li', class_='school')]))
                                    school = '|'.join(founder[co_name][founder_name]['school'])
                                except:
                                    founder[co_name][founder_name]['school'] = ''
                                    school = ''
                                print 'school: ' + school

                                try:
                                    founder[co_name][founder_name]['former_companies'] = list(set([company.find('h5', class_='item-subtitle').get_text().replace(',','+') for company in linkedin_soup.find('section', id='experience').find_all('li', class_='position')[1:]]))
                                    former_companies = '|'.join(founder[co_name][founder_name]['former_companies'])
                                except:
                                    founder[co_name][founder_name]['former_companies'] = ''
                                    former_companies = ''
                                print 'former_companies: ' + former_companies

                                # founder[co_name][founder_name]['connections'] = linkedin_soup.find('h3', class_='indpv-top-card-section__connections pv-top-card-section__connections--with-separator Sans-15px-black-55% mb1 inline-block').get_text()

                                try:
                                    founder[co_name][founder_name]['major'] = [major.find('h5', class_='item-subtitle').find('span').get_text().replace(',','+') for major in linkedin_soup.find('section', id='education').find_all('li', class_='school')]
                                    major = '|'.join(founder[co_name][founder_name]['major'])
                                except:
                                    founder[co_name][founder_name]['major'] = ''
                                    major = ''
                                print 'major: ' + major

                                try:
                                    founder[co_name][founder_name]['former_position'] = linkedin_soup.find('section', id='experience').find_all('li', class_='position')[1].find('h4', class_='item-title').get_text().replace(',','+')
                                    former_position = founder[co_name][founder_name]['former_position']
                                except:
                                    founder[co_name][founder_name]['former_position'] = ''
                                    former_position = ''
                                print 'former_position: ' + former_position

                                try:
                                    founder[co_name][founder_name]['skills'] = [skill.get_text().replace(',','+') for skill in linkedin_soup.find('section', id='skills').find_all('span', class_='wrap')]
                                    skills = '|'.join(founder[co_name][founder_name]['skills'])
                                except:
                                    founder[co_name][founder_name]['skills'] = ''
                                    skills = ''
                                print 'skills: ' + skills
                                    
                                with open('startups_founder_networks' + str(url_num) + '.csv', 'a') as f1:
                                    f1.write('{},{},{},{},{}\n'.format(co_name, founder_name, school, former_companies, linkedin_url))
                                with open('startups_founder_skills' + str(url_num) + '.csv', 'a') as f2:
                                    f2.write('{},{},{},{},{}\n'.format(co_name, founder_name, major, former_position, skills))
                            
                            else:
                                print 'Linkedin Profile Not Found'

                        except:
                            print 'No Linkedin'

                        try:
                            twitter_url = founder_soup.find('a', class_='icon link_el fontello-twitter')['href']
                            if '#!' in twitter_url:
                                twitter_url = twitter_url.replace('#!/', '')
                            print twitter_url
                            founder[co_name][founder_name]['twitter'] = twitter_url
                            twitter_page = urllib.urlopen(twitter_url).read()
                            twitter_soup = BeautifulSoup(twitter_page, 'html.parser')

                            twitter_data = twitter_soup.find_all('span', class_='ProfileNav-value')[:3]
                            founder[co_name][founder_name]['tweets'] = twitter_data[0].get_text().replace(',', '')
                            print 'tweets:' + str(founder[co_name][founder_name]['tweets'])
                            founder[co_name][founder_name]['following'] = twitter_data[1].get_text().replace(',', '')
                            print 'following: ' + str(founder[co_name][founder_name]['following'])
                            founder[co_name][founder_name]['followers'] = twitter_data[2].get_text().replace(',', '')
                            print 'followers: ' + str(founder[co_name][founder_name]['followers'])

                            driver2.get(twitter_url)
                            js = "document.body.scrollTop=100000"
                            driver2.execute_script(js)
                            time.sleep(10)
                            driver2.implicitly_wait(30)  
                            # wait2.until(lambda dr: dr.find_elements_by_xpath('//div[@class="ProfileTweet-actionCountList u-hiddenVisually"]').is_displayed())
                            twitter_info = driver2.find_elements_by_xpath('//div[@class="ProfileTweet-actionCountList u-hiddenVisually"]')
                            founder[co_name][founder_name]['retweets'] = []
                            founder[co_name][founder_name]['likes'] = []
                            for twitters in twitter_info:
                                re_re_like = twitters.find_elements_by_class_name('ProfileTweet-actionCount')
                                founder[co_name][founder_name]['retweets'].append(str(re_re_like[1].get_attribute('data-tweet-stat-count')))
                                founder[co_name][founder_name]['likes'].append(str(re_re_like[2].get_attribute('data-tweet-stat-count')))
                            retweets = '|'.join(founder[co_name][founder_name]['retweets'])
                            print 'retweets: '+ retweets
                            likes = '|'.join(founder[co_name][founder_name]['likes'])
                            print 'likes:' + likes
                            with open('startups_founder_influence' + str(url_num) + '.csv', 'a') as f3:
                                f3.write('{},{},{},{},{},{},{},{}\n'.format(co_name, founder_name, founder[co_name][founder_name]['tweets'], founder[co_name][founder_name]['following'], founder[co_name][founder_name]['followers'], retweets, likes, twitter_url))
                        
                        except:
                            print 'No Twitter'
        except:
            print 'No Founders'

    return None





