import scrapy
import re

class SummitPoster(scrapy.Spider):
    name = 'summitposter'
    base = 'http://www.summitpost.org/mountain/rock/p'
    start_urls = ['http://www.summitpost.org/mountain/rock/']
    for i in range(2, 275): ## get all of the pages
        url = base + str(i)
        start_urls.append(url)

    def parse(self, response):
        for href in response.xpath("//a[(contains(@style,'font-weight: bold'))]//@href").extract(): #get only bold links
            full_url = response.urljoin(href)
            if "summitpost" in full_url:
                yield scrapy.Request(full_url, callback=self.parseRock) ## follow links from index pages

    def parseRock(self, response):
        print "PARSING ROCK: ", response
        try:
            keys = response.css('.data_box p').extract()
            props = {}
            for key in keys:
                key = stripTag(key)
                key = splitTag(key, ":")
                props[key[0]] = key[1]
            ## get images
            props['images'] = []
            images = response.xpath("//img//@src").extract()
            for image in images:
                if "images" in image:
                    image_url = response.urljoin(image)
                    props['images'].append(image_url)
            if props != {}:
                props['url'] = response.url
                pages = response.xpath("//a//text()").extract()
                pages = pages[10:]
                links = response.xpath('//a//@href').extract()
                links = links[10:]
                try:
                    topIdx =pages.index("Routes")
                except:
                    topIdx = 0
                try:
                    bottomIdx = pages.index("Trip Reports")
                except:
                    try:
                        bottomIdx = pages.index("Geography")
                    except:
                        bottomIdx = len(pages)
                toFollow = links[topIdx:bottomIdx]
                for link in toFollow:
                    full_url = response.urljoin(link)
                    if "summitpost" in full_url:
                        print "Following: ", full_url
                        yield scrapy.Request(full_url, callback=lambda l=full_url, parent=props: self.parseRoute(l, parent))
            else:
                pass
        except Exception as e:
            print "ERROR:" + str(e)

    def parseRoute(self, response, parent):
        try:
            keys = response.css('.data_box p').extract()
            props = {}
            for key in keys:
                key = stripTag(key)
                key = splitTag(key, ":")
                try:
                    props[key[0]] = key[1]
                except:
                    pass
            props['images'] = []
            images = response.xpath("//img//@src").extract()
            for image in images:
                if "images" in image:
                    image_url = response.urljoin(image)
                    props['images'].append(image_url)
            if props != {}:
                props['url'] = response.url
                yield {
                    'parent': parent,
                    'route': props,
                }
        except Exception as e:
            print "ERROR:" + str(e)

def stripTag(string):
    s = re.sub(r'<.+?>', '', string)
    key = "".join(s.split())
    return key

def splitTag(string, char):
    out = {}
    s = string.split(char)
    return s