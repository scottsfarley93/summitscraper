import scrapy
import json



def cleanList(lst):
    i = 0
    while i < len(lst):
        try:
            lst[i] = "".join(lst[i].split())
        except:
            pass
        i += 1
    return lst


def getLinksFromFile(f):
    data = json.load(open(f, 'r'))
    base = "http://summitpost.org"
    links = []
    i = 0
    while i < len(data):
        datum = data[i]
        link = datum['URL']
        href = base + link
        links.append(href)
        i += 1
    return links

keys_to_save = ['Page Type', 'Location', 'Lat/Lon', 'Object Title', 'Page By', 'Created/Edited', 'Object ID', 'Activities',
'Number of Pitches', 'Season', 'Route Type', 'Rock Difficulty', 'Difficulty', 'Grade']

class SPSpider(scrapy.Spider):
    name = "sp.getcanyonpages"

    def start_requests(self):
        urls = getLinksFromFile("./../../../data/spcanyon.json")
        urls = urls
        print urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        box = response.css("#main_data_box")
        title = box.css("td header h1::text").extract()
        key = box.css("td p  ::text").extract()
        data_box = box.css("td p").extract()
        i = 0
        data = {}
        while i < len(data_box):
            el = data_box[i]
            pair = "".join(el.split())
            pair = pair.replace("<p><strong>", "")
            pair = pair.replace(":", "")
            pair = pair.replace("</p>", "")
            pair = pair.split("</strong>")
            key = pair[0]
            value = pair[1]
            if key in keys_to_save:
                data[key] = value
            i += 1
        text_keys = response.css(".toc_list1 a ::text").extract()
        text_els = response.css("article ::text").extract()
        current_key = ""
        current_text = ""
        j = 0
        while j < len(text_els):
            text_el = text_els[j]
            if text_el in text_keys:
                if current_key != "":
                    data[current_key] = current_text
                    current_text = ""
                current_key = text_el
            else:## don't append header 
                current_text += text_el
            j += 1
        yield data
        