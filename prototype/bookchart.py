#!/usr/bin/env python
# -*- coding: utf-8 -*-



class BookChart():
    pass

class BookChartYes24(BookChart):



    def __init__(self):

        ################################
        # session
        import httplib2

        self.http = httplib2.Http()
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
        import json
        jsonData = json.dumps(self._parse(content), # do _parse()
                             separators=(',', ': ')
                    )

        return jsonData

        '''
            TODO




        '''


    def _connect(self, year, month, week, day):
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


        response, content = self.http.request(url,
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
        parse the received data to retrieve the book information

        @rtype:  list
        @return: list of information dictionary of books
    '''
    def _parse(self, data):

        import re

        from lxml import html
        # DOM making
        root = html.fromstring(data)


        ################################
        # Yes24 specific formats

        bestsellerTable = root.get_element_by_id('category_layout')

        bookCovers = bestsellerTable.find_class('image')
        bookInfos = [image.getparent() for image in bookCovers]


        ################################
        # A book has two <tr>s
        # <tr> book information </tr>
        # <tr> book description </tr>
        bslist = []
        max = len(bestsellerTable)
        for i in range(0, max, 2):
            bookInfo = bestsellerTable[i]
            bookDesc = bestsellerTable[i+1]

            item = {}
            item['rank'] = int(bookInfo.find_class("num")[0].text[:-1])
            item['bookcoverUrl'] = bookInfo.find_class("image")[0].find(".//img").get('src')
            item['title'] = bookInfo.find(".//p").text_content()    # get 1st <p> tag
            item['summary'] = bookDesc.find_class('read')[0].text

            bslist.append(item)


        return bslist











#------------------------------------------------------------------------------------
if __name__ == "__main__":

    yes24 = BookChartYes24()
    result = yes24.getBestSellerChart(2012, 6, week=2)
    print result










