import scrapy

class SingaporeExpats(scrapy.Spider):
    name = 'singaporeexpats'

    start_urls = [
        'https://forum.singaporeexpats.com/viewforum.php?f=93',
    ]

    def parse(self, response):
        for topic_list in response.xpath('//*[@id="page-body"]/div[6]/div/ul[2]'):
            for topic in topic_list.xpath('li/dl'):
                yield {
                    'topic': topic.xpath('dt/div/a/text()').get(),
                    'number_of_replies': topic.xpath('dd[@class="posts"]/text()').get().strip(),
                    'number_of_views': topic.xpath('dd[@class="views"]/text()').get().strip(),
                }
                yield response.follow(topic.xpath('dt/div/a/@href').get(), \
                    self.parse)

        for post in response.xpath('//div[has-class("page-body")]/div[has-class("post has-profile")]/div'):
            content_list = post.xpath('div[@class="postbody"]/div/div[@class="content"]/descendant::text()[not(ancestor::blockquote)]').getall()
            content = " ".join(content_list)
            content = content.replace('\n', '')
            content = content.replace('\t', '')

            yield {
                'topic': post.xpath('//div[@class="page-body"]/h2[@class="topic-title"]/a/text()').get(),
                'author': post.xpath('dl[@class="postprofile"]/dt/a/text()').get(),
                'content': content,
            }

            post_next_page = response.xpath('//li[has-class("arrow next")]/a/@href').get()
            if post_next_page is not None:
                yield response.follow(post_next_page, self.parse)
                
        next_page = response.xpath('//li[has-class("arrow next")]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
