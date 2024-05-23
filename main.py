from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
#запустим паука с именем циан
process.crawl('cian')
process.start()
