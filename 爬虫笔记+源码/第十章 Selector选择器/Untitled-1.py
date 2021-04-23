from scrapy import Selector


content = "<html><head><title>my html</title><body><h3>Hello World</h3></body></head></html>"
selector = Selector(text=content)
print(selector.xpath('/html/head/title/text()'))
# [<Selector xpath='/html/head/title/text()' data='my html'>]
print(selector.xpath('/html/head/title/text()').extract())
# ['my html']
print(selector.xpath('/html/head/title/text()').extract_first())
# my html
print(selector.css('h3::text').extract_first())