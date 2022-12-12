import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Сбор всех ссылок на документацию PEP."""
        all_peps_links = response.xpath(
            '//section[@id="numerical-index"]'
        ).css('a[class="pep reference internal"]::attr(href)')
        for pep_link in all_peps_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсинг страницы PEP и формирвоание Items."""
        pars_data = ''.join(
            response.xpath('//h1[@class="page-title"]/text()').get()
        ).split(' – ', maxsplit=1)
        data = {
            'number': pars_data[0],
            'name': pars_data[1],
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
