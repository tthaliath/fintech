import scrapy
import json
import sys
from cointrader.items import *
import requests
import json
import logging
import time
reload(sys)
sys.setdefaultencoding('utf8')
class QuotesSpider(scrapy.Spider):
    name = "coinmaster"
    #epoch_time_hr_ago = int(time.time()) - 3600
    def start_requests(self):
        urls = [
            'https://www.cryptocompare.com/api/data/coinlist/',
        ]
        for urlmain in urls:
	    r = requests.get(urlmain).text.encode('utf-8')
	    jsonresponse = json.loads(r)
            symbols = jsonresponse['Data'].keys()
            for ticker in symbols:
		url =  "https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+ticker+"&tsyms=USD"
            	yield scrapy.Request(url=url, callback=self.parse,meta={'ticker': ticker,'ord' : jsonresponse['Data'][ticker]['SortOrder'],'name' : jsonresponse['Data'][ticker]['CoinName']})

    def parse(self, response):
	jsonresponse = json.loads(response.body_as_unicode())
 	item = CointraderItem() 
        item['ticker'] = response.meta['ticker']
	ticker = item['ticker']
        item['name'] = response.meta['name']	
        item['ord'] = response.meta['ord'] 
	if 'RAW' in jsonresponse:
		if int(item['ord']) <= 100:
			#print "ticker :" + ticker + "ord :" + item['ord']
			self.logger.info('Parse function called on %s', item['ord'])
               		item['lastprice'] = jsonresponse['RAW'][ticker]['USD']['PRICE']
               		item['dayhigh'] = jsonresponse['RAW'][ticker]['USD']['HIGH24HOUR']
                	item['daylow'] = jsonresponse['RAW'][ticker]['USD']['LOW24HOUR']
			item['epochtime'] = jsonresponse['RAW'][ticker]['USD']['LASTUPDATE']
			self.logger.info('Parse function called on %s', item)
       		        return item
