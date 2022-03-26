import scrapy
import os
class NewsSpider(scrapy.Spider):
    name = 'news'
    post_limit = 1000
    start_urls = []
    numOfpost = 0
    cate = ''
    '''
    category = [
        the-thao, khoa-hoc, giao-duc, du-lich,
        kinh-doanh, phap-luat, suc-khoe, 
        doi-song, so-hoa, oto-xe-may
        .....
    ]
    '''
    def __init__(self, category):
        URL = 'https://vnexpress.net/'+ category
        self.start_urls = [URL]
        self.cate = category
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse_list_posts)

    def parse_list_posts(self, response):
        if self.numOfpost > self.post_limit:
            return
        next_page_url = self.get_next_page_url(response)
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback = self.parse_list_posts)
        else:
            return
        section = response.css("section div")
        for list_posts in section.css("article"):
            relative_url = list_posts.css("a::attr(href)").extract_first()
            url = response.urljoin(relative_url)
            yield scrapy.Request(url, callback=self.parse_posts)

    def get_next_page_url(self, response):
        next_page_url = response.css("div.pagination a.btn-page.next-page::attr(href)").extract_first()
        return next_page_url

    def parse_posts(self, category):
        self.numOfpost += 1
        if self.numOfpost > self.post_limit:
            return
        content = self.extract_posts(category)
        if not os.path.exists('data/' + self.cate):
            os.makedirs('data/' + self.cate)
        with open('data/' + self.cate + '/' + self.cate + str(self.numOfpost) + '.txt', 'w+', encoding='utf-8') as f:
            f.write(content)
        yield None

    def extract_posts(self, response):
        content = self.extract_content(response)
        return ''.join(content)
    
    def extract_content(self, response):
        des = response.css("section p.description::text").getall()
        content = response.css("section article p.Normal::text").getall()
        if not content:
            content = response.css("section p::text").getall()
        return ''.join(des)+''.join(content)
