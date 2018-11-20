# !/usr/bin/env python
# -*- coding: utf-8 -*

from StartupsURL import *
from FoundersnFundings import *


if __name__ == '__main__':

    market = 'Health+Care'
    url_num = int(raw_input("Enter url num: ")) # enter num 1-6

    # print get_full_url(market) # get filtering urls
    get_startups_url(market, url_num)  # save startups info & urls
    get_founder_funding(url_num)  # output founders and fundings info




