#!/usr/bin/env python
# -*- coding: utf-8 -*-



GAE_DJANGO = False

if GAE_DJANGO :
    import logging
    from django.core.cache import cache
    from django.http import HttpResponseRedirect
    from django.http import HttpResponse
    from django.views.generic.simple import direct_to_template

    from google.appengine.ext import db


class BestSellerList():
    def __init__(self):
        self.data = None    # python list type
        self.dataUtf8 = None # python list which has Utf-8 string

    '''
        @rtype list
        @return self.data which has the list of bestsellers' information
                in forms of the python list format.
    '''
    def get(self):
        return self.data


    '''
        @rtype list
        @return self.dataUtf8 which has the list of bestsellers' information,
                which has the utf-8 encoded string,
                in forms of the python list format.
    '''
    def getUtf8(self):
        return self.dataUtf8



    '''
        @rtype json
        @return self.data which has the list of bestsellers' information
                in forms of the json format
    '''
    def getJson(self):
        import json
        jsonData = json.dumps(self.data, # do _parse()
                             separators=(',', ': ')
                    )

        return jsonData



    def set(self, data, dataUtf8):
        self.data = data
        self.dataUtf8 = dataUtf8



class BookChart():
    pass

class BookChartYes24(BookChart):



    def __init__(self):


        self.bsl = BestSellerList()

        ################################
        # session
        self.headers = {
           "cache-control":"no-cache",
           "Connection": "keep-alive",
           "accept-encoding":"gzip, deflate",
           "Accept" : "application/json, text/javascript, */*",
           "X-Requested-With": "XMLHttpRequest",
           "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.7 \
    (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7",
           "Content-type": "application/x-www-form-urlencoded",
           # "Referer" : referer,
           # "Cookie": self.cookie,
       }





    '''

        3 types of bestseller list could be possible.
            1. monthly : week and day are None.
            2. weekly : only day is None.
            3. daily : day is set.

        @type  date: datetime.date
        @param date: the date in which the bestsellers are listed.


        @type week : number
        @param week : nth week of the specific month. week must be more than 0

        @type day : number
        @param day : nth day of the specific month. day must be more than 0


        @rtype:  json
        @return: information of books
            for example :
            {
                {
                    'rank' : 1,
                    'bookcoverUrl' : "http://googl.e",
                    'title' : "blah",
                    'summary' : "blahblahblahblah"
                },
                {
                    ...
                }

            }


    '''
    def getBestSellerChart(self, year, month, week = None, day = None):

        content = self._connect(year, month, week, day)

        # to test
        # with open('./yes24BestSellerListExample_Weekly.htm','r') as fd:
        #     content = ''
        #     for line in fd:
        #         content += line



        # parse and convert into json format


        self._parse(content)
        return self.bsl


        '''
            TODO




        '''


    def _connect(self, year, month, week, day):

        if GAE_DJANGO :
            from google.appengine.api import urlfetch
        else :
            import httplib2




        # debug
        year = str(year)
        month = '6'
        week = str(2) # 2nd week of the month


        periodKey = 'month'
        postfix = ''
        if week is not None:
            periodKey = 'week'
            postfix = "&week=" + str(week)

        if day is not None:
            periodKey = 'day'
            postfix = "&day=" + str(day)


        ################################
        # url
        period = { 'day': '07', 'week': '08', 'month': '09'}

        url = "http://www.yes24.com/24/category/bestseller\
?CategoryNumber=001\
&sumgb=" + period[periodKey] + "\
&year=" + str(year) + "\
&month=" + str(month) + postfix


        if GAE_DJANGO :
            result = urlfetch.fetch(url,
                            method=urlfetch.GET,
                            headers=self.headers,
                            deadline=60
                        )
            if result.status_code != 200:
                print "status code = ", result.status_code
                raise

            dataRetrieved = result.content

            # uncompress gzip data
            key = 'content-encoding'
            if result.headers.has_key(key) is True:
                if result.headers[key] == 'gzip' :
                    import StringIO
                    import gzip

                    gzip_stream = StringIO.StringIO(dataRetrieved)
                    gzip_file = gzip.GzipFile(fileobj=gzip_stream)
                    dataRetrieved = gzip_file.read()

            return dataRetrieved


        else :

            response, content = httplib2.Http().request(url,
                                       "GET",
                                       headers=self.headers,
                            )

            if response['status'] != '200' :
                '''
                TODO
                    raise error depends on status
                '''
                raise

            return content



    '''
        Pare and Set self.BestSellerList
        parse the received data to retrieve the book information

        @type data : python string
        @param data : html-format data



    '''
    def _parse(self, data):

        import re

        from lxml import html


        # DOM making



        ################################
        # Yes24 specific formats

        bestsellerTable = root.get_element_by_id('category_layout')

        ################################
        # A book has two <tr>s
        # <tr> book information </tr>
        # <tr> book description </tr>
        bslist = []
        bslistUtf8 = []
        max = len(bestsellerTable)

        for i in range(0, max, 2):
            bookInfo = bestsellerTable[i]
            bookDesc = bestsellerTable[i+1]

            item = {}
            itemUtf8 = {}

            itemUtf8['rank'] = item['rank'] = int(bookInfo.find_class("num")[0].text[:-1])
            itemUtf8['bookcoverUrl'] = item['bookcoverUrl'] = bookInfo.find_class("image")[0].find(".//img").get('src')
            item['title'] = bookInfo.find(".//p").text_content()    # get 1st <p> tag
            item['summary'] = bookDesc.find_class('read')[0].text

            itemUtf8['rank'] = item['rank']
            itemUtf8['bookcoverUrl'] = bookInfo.find_class("image")[0].find(".//img").get('src')
            itemUtf8['title'] = item['title'].encode('utf-8')
            itemUtf8['summary'] = item['summary'].encode('utf-8')

            bslist.append(item)
            bslistUtf8.append(itemUtf8)


        self.bsl.set(bslist, bslistUtf8)


def week_of_month(date):
    month = date.month
    week = 0
    while date.month == month:
        week += 1
        date -= timedelta(days=7)

    return week

#------------------------------------------------------------------------------------
if __name__ == "__main__":

    from datetime import datetime
    from datetime import timedelta

    offset = 7

    bsPeriod = datetime.now() - timedelta(days=offset)
    week = week_of_month(bsPeriod)
    

    yes24 = BookChartYes24()
    result = yes24.getBestSellerChart(bsPeriod.year, bsPeriod.month, week=week).get()
    print result










