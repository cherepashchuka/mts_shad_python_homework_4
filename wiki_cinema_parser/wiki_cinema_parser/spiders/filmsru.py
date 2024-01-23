import scrapy


class FilmsruSpider(scrapy.Spider):
    name = "filmsru"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

    def parse(self, response):
        for link in response.css('div.mw-category a::attr(href)'):
            yield response.follow(link, callback=self.parse_page)

        next_page = response.xpath('//*[@id="mw-pages"]/a[1]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        name = response.css('table.infobox').css('th.infobox-above::text').get()
        genre = response.css('table.infobox').css('td.plainlist').css('span[data-wikidata-property-id="P136"] a::attr(title)').get()
        director = response.css('table.infobox').css('td.plainlist').css('span[data-wikidata-property-id="P57"] a::text').get()
        country = response.css('table.infobox').css('td.plainlist').css('span[data-wikidata-property-id="P495"] a::attr(title)').get()
        year = response.css('table.infobox').css('td.plainlist').css('span.dtstart::text').get()
        imdb_url = response.css('table.infobox').css('td.plainlist').css('span[data-wikidata-property-id="P345"] a::attr(href)').get()

        yield {
            'name': name,
            'genre': genre,
            'director': director,
            'country': country,
            'year': year,
            'imdb_url': imdb_url
        }