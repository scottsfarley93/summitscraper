import scrapy


def cleanList(lst):
    i = 0
    while i < len(lst):
        try:
            lst[i] = "".join(lst[i].split())
        except:
            pass
        i += 1
    return lst


def generateStartURLs(base, max):
    i = 1
    urls = []
    while i <= max:
        url = base + "/p" + str(i)
        urls.append(url)
        i += 1
    return urls

class SPSpider(scrapy.Spider):
    name = "sp.trailheads"

    def start_requests(self):
        urls =generateStartURLs('http://www.summitpost.org/trailhead', 5)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows  = response.xpath("//table[@class='srch_results']/tr")
        idx = 0
        for row in rows:
            if idx == 0:
                idx += 1
            else:
                linkText = row.css(".srch_results_rht a").select(".//text()").extract()
                elementTitle = linkText[0]
                author = linkText[1]
                del linkText[:2]
                parents = linkText
                linkURL = row.css(".srch_results_rht a").select("./@href").extract()
                elementURL = linkURL[0]
                authorURL = linkURL[1]
                del linkURL[:2]
                parentURLs = linkURL
                attributes = row.css(".srch_results_rht::text").extract()
                attributes = cleanList(attributes)
                del attributes[:3]
                element = {
                    'title': elementTitle,
                    'author' : author,
                    'parents' : parents,
                    'URL' : elementURL,
                    'authorURL' : authorURL,
                    'parentURLs' : parentURLs,
                    'attributes' : attributes
                }
                yield element