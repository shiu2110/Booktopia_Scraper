
import scrapy
import json
import csv

class BooktobiaSpider(scrapy.Spider):
    name = "booktobia"

    custom_settings = {
		'FEEDS': { 'data.csv': { 'format': 'csv',}}
		}

    def start_requests(self):

        booklist = []
        with open('input_list.csv','r',newline='') as file:
            reader = csv.DictReader(file)
            for r in reader:
                booklist.append(r['ISBN13'])
        for product_id in booklist:
            urls = f"https://www.booktopia.com.au/abc/book/{product_id}.html"

            headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            }
            meta = {
                "number":product_id
            }
            yield scrapy.Request(url=urls, callback=self.parse,headers=headers,method="GET",meta=meta)

    def parse(self, response):
        if response.status == 200:
            data = response.xpath("//script[@id='__NEXT_DATA__']/text()").getall()[0]
            data = json.loads(data)
            product_id = response.meta['number']
            try:
                title = data['props']['pageProps']['product']['displayName']
            except:
                title='None' 
            try:
                author_name = data['props']['pageProps']['product']['contributors'][0]['name']
            except:
                author_name='None'
            try:
                Original_price = data['props']['pageProps']['product']['retailPrice']
            except:
                Original_price='None'
            try:
                Discounted_price = data['props']['pageProps']['product']['salePrice']
            except:
                Discounted_price = 'None'
            try:
                product_url = "https://www.booktopia.com.au/"+data['props']['pageProps']['product']['productUrl']
            except:
                product_url='None'
            try:
                published_date = data['props']['pageProps']['product']['publicationDate']
            except:
                published_date = 'None'
            try:
                isbn10 = data['props']['pageProps']['product']['isbn10']
            except:
                isbn10='None'
            try:
                publisher = data['props']['pageProps']['product']['publisher']
            except:
                publisher = 'None'
            try:
                number_of_pages = data['props']['pageProps']['product']['numberOfPages']
            except:
                number_of_pages = '-' 
            try:
                book_type = data['query']['type']
            except:
                book_type = 'None'
            
            item = {
                "Product Id":product_id,
                "Title":title,
                "Product Url":product_url,
                "Author Name":author_name,
                "Book Type":book_type,
                "Original Price":Original_price,
                "Discounted Price":Discounted_price,
                "ISBN10":isbn10,
                "Published Date":published_date,
                "Publisher":publisher,
                "Number of Pages":number_of_pages,
            }
            yield item
        else:
            print("Page Not Found!!!!!!!!")
     