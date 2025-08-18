import scrapy


class ArticlespiderSpider(scrapy.Spider):
    name = "articlespider"
    allowed_domains = ["pmc.ncbi.nlm.nih.gov"]
    start_urls = [
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC5822762/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11592192/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11926446/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC7744436/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10845090/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10853571/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11761573/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC7680410/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10001627/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11025255/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC12114474/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11919126/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11319290/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10767128/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC3496809/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC8786271/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10613447/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC6039504/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC3658571/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC5110375/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC8379542/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC4395304/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10483472/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC8748758/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11455897/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC8321773/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10106448/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC12055031/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11969452/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10051989/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10178355/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10756079/",
    ]

    def parse(self, response):
        bodies = response.css("article section p")
        for body in bodies:
            yield {"body": body.get()}
