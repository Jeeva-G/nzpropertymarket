import scrapy
from auctionresults.items import AuctionresultsItem
import requests
from bs4 import BeautifulSoup

class AuctionListingsSpider(scrapy.Spider):
    name = "nzresauctionresults"
    allowed_domains = ["interest.co.nz"]
    #Base url for nz residential auction results. Change if necessary
    base_url = "https://www.interest.co.nz/property/residential-auction-results?"
    start_urls = ["https://www.interest.co.nz/property/residential-auction-results?"]
    #Initially grab all of the urls up to where search results appear
    soup = BeautifulSoup(requests.get(base_url).text, "lxml")
    search_results_text = str(soup.find(id="padb-query-message").get_text())
    total_results = int(''.join(filter(str.isdigit, search_results_text)))
    #In this case, it's 35193 search results from what we found in UI
    num_pages = (total_results/25) + 1
    #num_pages = 1
    for i in range(num_pages):
        start_urls.append(base_url + "&page=" + str(i))


    def parse(self, response):

        items = []

        #find all property listings
        listings_auctioned = response.xpath('//div[@class="padb-property-card"]')
        #loop through the property listings
        for i in range(0, len(listings_auctioned)-1):
            item = AuctionresultsItem()
            #Grab Auction listing details
            item["property_id"] = " ".join(str(x) for x in listings_auctioned[i].css(".padb-listing-id::text").getall()).split()
            item["property_address"] = listings_auctioned[i].css(".address::text").extract_first(default=None)
            item["property_region_district"] = listings_auctioned[i].css(".region-district::text").extract_first(default=None)
            item["property_beds"] = listings_auctioned[i].css(".padb-beds::text").extract_first(default=None)
            item["property_baths"] = listings_auctioned[i].css(".padb-baths::text").extract_first(default=None)
            item["property_carparks"] = listings_auctioned[i].css(".padb-parking::text").extract_first(default=None)
            item["property_area"] = listings_auctioned[i].css(".padb-area::text").extract_first(default=None)
            item["property_value"] = " ".join(str(x) for x in listings_auctioned[i].css(".padb-property-value::text").getall()).split()
            item["property_auctiondetails"] = " ".join(str(x) for x in listings_auctioned[i].css(".padb-auction-details::text").getall()).split()
            item["property_ratingvalue"] = " ".join(str(x) for x in listings_auctioned[i].css(".padb-property-rating-value::text").getall()).split()
            #item["property_agentdetails"] = listings_auctioned[i].css(".padb-agents a::attr(href)").extract_first(default=None)
            item["property_agentdetails"] = listings_auctioned[i].css(".padb-agency-logo img::attr(src)").extract_first(default=None)
            item["property_auction_status"] = listings_auctioned[i].css('div[class^="padb-ribbon"]').xpath("span/text()").extract_first(default=None)

            items.append(item)

        return items
