import scrapy
import re


class FilmsruSpider(scrapy.Spider):
    name = "filmsru"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

    def list_cleaning(self, data):
        symbols = ['\d', '\n', '[d]', '[1]', '[2]', '\xa0', ' ', ',', '/', '[3]', '[',']', '[4]', '[5]',
                   '[7]', '[6]', '[...]', '[…]', '[jp]', '[en]', 'рус.', 'англ.', ')', '(', ' / ', ' ,',
                   '[9]', '[10]', '*', ', ', '«', '»', '*', '(англ)', '(рус)', '(фр)', '[da]','(яп)','(it)','(итал)',
                   '[ko]','[zh]','[uk]', '[16]', '[—]', '[8]', '(англ)', '(фр.)', '[17]']

        return ';'.join(text.strip() for text in data if not text.strip() in symbols and text.strip() != '').replace(',','').replace('.','')

    def parse(self, response):
        for link in response.css('div.mw-category a::attr(href)'):
            yield response.follow(link, callback=self.parse_page)

        next_page = response.xpath("//*[contains(text(), 'Следующая страница')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):

        name = response.css('table.infobox th.infobox-above *::text').get()
        genre = response.css('table.infobox[data-name="Фильм"] td.plainlist *[data-wikidata-property-id="P136"] *::text').getall()
        director = response.css('table.infobox td.plainlist span[data-wikidata-property-id="P57"] *::text').getall()
        country = response.css('table.infobox td.plainlist *[data-wikidata-property-id="P495"] span::text').getall()
        if country is None:
            country = response.css('table.infobox td.plainlist *[data-wikidata-property-id="P495"] a::text').getall()

        genre = self.list_cleaning(genre)
        director = self.list_cleaning(director)
        country = self.list_cleaning(country)

        years = response.css('table.infobox tr:contains("Год")  *::text').getall()
        for yr in years:
            if len(yr) == 4:
                year = yr
                break

        imdb_url = response.css('table.infobox').css('td.plainlist').css('span[data-wikidata-property-id="P345"] a::attr(href)').get()

        yield {
            'name': name,
            'genre': genre,
            'director': director,
            'country': country,
            'year': year,
            'imdb_url': imdb_url
        }