# -*- coding: utf-8 -*-
import scrapy
from habr.items import HabrItemComment


class HabrSpiderSpider(scrapy.Spider):
    name = 'habr_spider'
    allowed_domains = ['habrahabr.ru']

    def start_requests(self):
        urls = ['https://habrahabr.ru/all/top100/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_posts)

    def get_posts(self, response):
        posts = response.xpath("//article")
        for post in posts:
            comments_num = post.xpath(
                'footer/ul/li[contains(@class, "comments")]/a/span[2]/text()').extract_first()
            if comments_num != 'Комментировать':
                url = post.xpath(
                    'h2/a[@class="post__title_link"]/@href').extract_first()
                yield scrapy.Request(url=url, callback=self.parse)

        # posts = response.xpath(
        #    '//a[@class="post__title_link"]/@href').extract()

        #posts = ['https://habrahabr.ru/company/mailru/blog/351836/']
        next_page = response.xpath(
            '//*[@id="next_page"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.get_posts)

    def parse(self, response):
        comments = response.xpath('//div[@class="comment"]/div[contains(@class, "comment__head")]')
        #url = response.url.split('/')[-2]
        for comment in comments:
            comm = HabrItemComment()
            comm['name'] = comment.xpath(
                'a/span[contains(@class, "user-info__nickname_comment")]/text()').extract_first()
            comm['likes'] = comment.xpath(
                'div[1]/span/text()').extract_first()
            comment_id = comment.xpath(
                'ul/li[1]/a/@href').extract_first()
            comm['post_url'] = response.urljoin(comment_id)
            yield comm


#'//*[@id="comment_10725316"]/div[1]/div/span'
#'//*[@id="comment_10725278"]/div[1]/a/span'
#'//*[@id="comment_10725278"]/div[1]/ul/li[1]/a'
#'//*[@id="comment_10726174"]/div[1]/a/span[2]'
#'//*[@id="infopanel_post_352122"]/li[4]/a/span[2]'
