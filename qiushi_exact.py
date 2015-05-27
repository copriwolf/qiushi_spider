#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
' qiushi spider '
__author__ = 'Copriwolf'

reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import re


class QSBK:

    def __init__(self):
        self.page = 1
        self.useragent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.useragent}
        self.stories = []
        self.pagestory = []
        self.Enable = True

    def LoadPage(self, page):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(self.page)
            Request = urllib2.Request(url, headers=self.headers)
            Responese = urllib2.urlopen(Request)
            PageOutput = Responese.read().decode('utf-8')
            return PageOutput

        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print '连接到糗事百科失败，失败原因:', e.reason
                return None

    def GetPageItem(self, page):
        Content = self.LoadPage(self.page)
        if not Content:
            print '页面加载失败'
            return None
        Petterm = re.compile(
            '<div.*?author.*?<a.*?/a>.*?<a.*?>(.*?)</a>.*?content">' + '(.*?)</div>(.*?)<div class="stats">.*?"number">(.*?)</i>', re.S)
        items = re.findall(Petterm, Content)

        for item in items:
            haveImg = re.search("img", item[2])
            if not haveImg:
                self.pagestory.append([item[0].strip(), item[1].strip(), item[3].strip()])
               

    def LoadEachItem(self):
    	print "+------------------------------+"
        print u"第%s页\t作者:%s\n%s\n点赞数:%s" % (self.page, self.pagestory[0][0], self.pagestory[0][1], self.pagestory[0][2])
        print "+------------------------------+"
        del self.pagestory[0]


    def Loading2Start(self):
        self.LoadPage(self.page)
        self.GetPageItem(self.page)
        while self.Enable == True:
        	if not self.pagestory:
        	    self.page += 1
        	    self.GetPageItem(self.page)
        	    self.LoadEachItem()
        	else:
        		self.LoadEachItem()

        	input = raw_input('输入任意键阅读下一条，退出请输入\"Q\":')
        	if input == "Q":
        	    self.Enable = False
        	    return 

spider = QSBK()
spider.Loading2Start()


        	
