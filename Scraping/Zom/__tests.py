#!/usr/bin/env python
"""
Author: Kaali
Date: 16 january, 2015
Description: This python has been written to test the proper working of the main_scrape.py file
            to detect any changes in the dom of the website being scraped

"""
import sys
from main_scrape import scrape_links, eatery_specific, EateriesList
import pymongo
import BeautifulSoup
import requests
import goose
import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from reviews_scrape import Reviews
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colored_print import bcolors
import random
import re


class TestMainScrape:
        
        def __init__(self, page_url, eatery_url, number_of_restaurants, skip):
                """
                        Args:
                                page_url: The url of the page like https://www.zomato.com/ncr/restaurants?page=1
                                Which will have several eateries present in it.
                                The EateriesList deals with checking the number of the pages present for the 
                                eateries present on this page.
                                Also deals wih scraping details of the eateries present on this page without
                                going to the each page of each particular eatery

                                The scraping of the each restaurant is being dealt with eatery_specific instance
                                ehich takes up the url of the eatery and then scrapes more deatils of the 
                                eatery present on its individual page and also scrape the reviews present on that page

                        eatery_url:
                                This being given in args, beacuse if you want to check the proper scraping of each eatery
                                EateriesList has an option to select whether the url given to it belongs to individual eatery
                                or belongs to area page


                """
                connection = pymongo.Connection()
                db = connection.intermediate
                self.collection = db.review
                self.number_of_restaurants = number_of_restaurants
                self.skip = skip
                self.eatery_url = eatery_url
                self.page_url = page_url

                self.page_instance = EateriesList(self.page_url, int(number_of_restaurants), int(skip), False) 
                self.eatery_instance = EateriesList(self.eatery_url, 0, 0, True) 
            


        def test_page_numbers(self):
                pages_link = self.page_instance.pagination_links()
                return pages_link 


        def test_skip_and_restaurants(self):
                """
                This checks whether the skip and number of restaurants arguments are working properly
                skip means that this many number of restaurants has to be skipped and the page number to be scraped 
                is to be chosen accordingly
                """
                pages_to_be_scraped = list()
                self.start_page_number = self.skip/30 #Keeping in mind that zomato does have 30 restaurants per page
                self.end_page_number = self.number_of_restaurants/30    
                for page in PAGES[self.start_page_number: self.start_page_number + self.end_page_number]:
                        pages_to_be_scraped.append(page)

                return pages_to_be_scraped


        def test_number_of_eateries(self):
                goose_instance = goose.Goose()
                data = goose_instance.extract(PAGES_TO_BE_SCRAPED[0])
                 
                page_soup = soup = BeautifulSoup.BeautifulSoup(data.raw_html)
                eatries_list = soup.findAll("li", {"class": "resZS mb5 pb5 bb even  status1"}) 
                return eatries_list


        def test_eatery_soup(self):
                eatery_soup = EATERIES_SOUP_LIST[0]
                global EATERIES_SUB_AREA, EATERY_ID, EATERY_URL, EATERY_NAME, EATERY_ADDRESS, EATERY_CUISINE,\
                        EATERY_COST, EATERY_RATING, EATERY_TITLE, EATERY_TRENDING, EATERY_POPULAR_REVIEWS
    

                try:
                        EATERIES_SUB_AREA = self.page_url.split("/")[-2]
                        print "{0} <<---->> {1}\n".format("EATERIES_SUB_AREA", EATERIES_SUB_AREA)
                except Exception as e:
                        print "{0} failed with exception {1}".format("EATERIES_SUB_AREA", e)
                        pass 

                try:
                        EATERY_ID = eatery_soup.get("data-res_id")
                        print "{0}  <<---->> {1}\n".format("EATERY_ID", EATERY_ID)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_ID", e)
                        pass 
                
                try:
                        EATERY_URL = eatery_soup.find("a").get("href")
                        print "{0}  <<---->> {1}\n".format("EATERY_URL", EATERY_URL)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_URL", e)
                        pass 
                
                try:
                        EATERY_NAME = eatery_soup.find("a").text                                                  
                        print "{0}  <<---->> {1}\n".format("EATERY_NAME", EATERY_NAME)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_NAME", e)
                        pass 
                
                try:
                        EATERY_ADDRESS = eatery_soup.find("span", {"class": "search-result-address"})["title"] 
                        print "{0}  <<---->> {1}\n".format("EATERY_ADDRESS", EATERY_ADDRESS)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_ADDRESS", e)
                        pass 
                
                try:
                        EATERY_CUISINE = eatery_soup.find("div", {"class": "res-snippet-small-cuisine truncate search-page-text"}).text 
                        print "{0}  <<---->> {1}\n".format("EATERY_CUISINE", EATERY_CUISINE)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_CUISINE", e)
                        pass 
                
                try:
                        EATERY_COST = eatery_soup.find("div", {"class": "search-page-text"}).text
                        print "{0}  <<---->> {1}\n".format("EATERY_COST", EATERY_COST)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_COST", e)
                        pass 
                
                try:
                        soup = eatery_soup.find("div", {"class": "right"})
                        EATERY_RATING = {"rating": soup.findNext().text.replace(" ", "").replace("\n", ""), "votes": soup.find("div",  {"class": "rating-rank right"}).findNext().text } 
                        print "{0}  <<---->> {1}\n".format("EATERY_RATING", EATERY_RATING)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_RATING", e)
                        pass 
                
                try:
                        EATERY_TITLE = eatery_soup.findNext().get("title") 
                        print "{0}  <<---->> {1}\n".format("EATERY_TITLE", EATERY_TITLE)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_TITLE", e)
                        pass 

                try:
                        collection =  eatery_soup.find("div", {"class": "srp-collections"}).findAll("a")
                        EATERY_TRENDING = [element.text for element in collection] 
                        print "{0}  <<---->> {1}\n".format("EATERY_TRENDING", EATERY_TRENDING)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_TRENDING", e)
                        pass 

                try:
                        EATERY_POPULAR_REVIEWS = eatery_soup.find("a", {"data-result-type": "ResCard_Reviews"}).text 
                        print "{0}  <<---->> {1}\n".format("EATERY_POPULAR_REVIEWS", EATERY_POPULAR_REVIEWS)
                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_POPULAR_REVIEWS", e)
                        pass


        def test_more_eateries_details(self):
                driver = webdriver.Firefox()
                """
                chromedriver = "{path}/chromedriver".format(path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                os.environ["webdriver.chrome.driver"] = chromedriver
                driver = webdriver.Chrome(chromedriver)
                """

                driver.get(self.eatery_url)


                try:
                        driver.find_element_by_css_selector("a.everyone.empty").click()

                except NoSuchElementException:
                        pass

                time.sleep(10)
                try:
                        while True:
                                time.sleep(random.choice([4, 3]))
                                driver.find_element_by_class_name("load-more").click()
                except NoSuchElementException as e:
                        print "{color} Catching Exception -<{error}>- with messege -<No More Loadmore tag present>-".format(color=bcolors.OKGREEN, error=e)
                        pass

                except Exception as e:
                        print e
                        raise StandardError("Coould not make the request")



                read_more_links = driver.find_elements_by_xpath("//div[@class='rev-text-expand']")
                for link in read_more_links:
                        time.sleep(random.choice([2, 3]))
                        link.click()

                html = driver.page_source
                driver.close()
                eatery_soup = BeautifulSoup.BeautifulSoup(html)



                try:
                        EATERY_ID = eatery_soup.find("div", {"itemprop": "ratingValue"}).get("data-res-id") 
                        print "{0}  <<---->> {1}\n".format("EATERY_ID", EATERY_ID)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_ID", e)
                        pass 
                
                
                try:
                        EATERY_NAME = eatery_soup.find("h1", {"class": "res-name left"}).find("a").text                                                 
                        print "{0}  <<---->> {1}\n".format("EATERY_NAME", EATERY_NAME)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_NAME", e)
                        pass 
                
                try:
                        EATERY_ADDRESS = eatery_soup.find("h2", {"class": "res-main-address-text"}).text 
                        print "{0}  <<---->> {1}\n".format("EATERY_ADDRESS", EATERY_ADDRESS)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_ADDRESS", e)
                        pass 
                
                try:
                        EATERY_CUISINE = eatery_soup.find("div", {"class": "pb2 res-info-cuisines clearfix"}).text  
                        print "{0}  <<---->> {1}\n".format("EATERY_CUISINE", EATERY_CUISINE)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_CUISINE", e)
                        pass 
                
                try:
                        EATERY_COST = eatery_soup.find("span", {"itemprop": "priceRange"}).text 
                        print "RETRY OF {0}  <<---->> {1}\n".format("EATERY_COST", EATERY_COST)

                except Exception as e:
                        print "{0} failed with exception {1}\n".format("EATERY_COST", e)
                        pass 
                
                try:
                        EATERY_RATING =  {"rating": eatery_soup.find("div", {"itemprop": "ratingValue"}).text.split("/")[0], 
                                        "votes": eatery_soup.find("span", {"itemprop": "ratingCount"}).text}         
                        
                        print "{0}  <<---->> {1}\n".format("EATERY_RATING", EATERY_RATING)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_RATING", e)
                        pass 
                

                try:
                        collection =  eatery_soup.find("div", {"class": "collections_res_container"}).findAll("a") 
                        EATERY_TRENDING = [element.text for element in collection] 
                        print "{0}  <<---->> {1}\n".format("EATERY_TRENDING", EATERY_TRENDING)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_TRENDING", e)
                        pass 

		
		try:
                        variable = eatery_soup.find("div", {"class": "pb5 res-info-cuisines clearfix"}).text
			EATERY_ESTABLISHMENT_TYPE = variable
                        print "{0}  <<---->> {1}\n".format("EATERY_ESTABLISHMENT_TYPE", EATERY_ESTABLISHMENT_TYPE)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_ESTABLISHMENT_TYPE", e)
                        pass 
	
		
                try:
                        variable = eatery_soup.find("div", {"class": "res-info-known-for-text mr5"}).text
			EATERY_KNOWN_FOR = variable
                        print "{0}  <<---->> {1}\n".format("EATERY_KNOWN_FOR", EATERY_TRENDING)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_KNOWN_FOR", e)
                        pass 
            

		try:
			variable = eatery_soup.find("div", {"class": "res-main-stats-num"})
			EATERY_WISHLIST = variable.text
                        print "{0}  <<---->> {1}\n".format("EATERY_WISHLIST", EATERY_WISHLIST)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_WISHLIST", e)
                        pass 



		try:
			EATERY_HIGHLISHTS = [dom.text.replace("\n", "") for dom in eatery_soup.findAll("div", {"class": "res-info-feature"})]
                        print "{0}  <<---->> {1}\n".format("EATERY_HIGHLISHTS", EATERY_HIGHLISHTS)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_HIGHLISHTS", e)
                        pass 
		
                
		
                
                try:
                        #error Occurred
                        EATERY_OPENING_HOURS = eatery_soup.find("div", {"class": "clearfix"}).find("span", {"class": "left"}).text
                        print "{0}  <<---->> {1}\n".format("EATERY_OPENING_HOURS", EATERY_OPENING_HOURS)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_OPENING_HOURS", e)
                        pass 

		
                
		try:
                        stations = eatery_soup.findAll("a", {"class": "res-metro-item clearfix left tooltip_formatted-e"})
			EATERY_F_M_STATION = {"distance": stations[0].find("div", {"class": "left res-metro-distance"}).text, "name": stations[0].find("div", {"class": "left res-metro-name"}).text}
                        print "{0}  <<---->> {1}\n".format("EATERY_F_M_STATION", EATERY_F_M_STATION)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_F_M_STATION", e)
                        pass 

		try:
			EATERY_S_M_STATION = {"distance": stations[1].find("div", {"class": "left res-metro-distance"}).text, 
					"name": stations[1].find("div", {"class": "left res-metro-name"}).text}
                        print "{0}  <<---->> {1}\n".format("EATERY_S_M_STATION", EATERY_S_M_STATION)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_S_M_STATION", e)
                        pass 

		try:
                        #Error Occurred
                        EATERY_PHOTOS = eatery_soup.find("div", {"id": "ph_count"}).text
                        print "{0}  <<---->> {1}\n".format("EATERY_PHOTOS", EATERY_PHOTOS)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_PHOTOS", e)
                        pass 

		try:
			EATERY_SHOULD_ORDER= eatery_soup.find("div", {"class": "res-info-dishes-text"}).text
                        print "{0}  <<---->> {1}\n".format("EATERY_SHOULD_ORDER", EATERY_SHOULD_ORDER)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_SHOULD_ORDER", e)
                        pass 

		try:
			EATERY_BUFFET_PRICE = eatery_soup.find("span", {"class": "res-buffet-price rbp3"}).text
                        print "{0}  <<---->> {1}\n".format("EATERY_BUFFET_PRICE", EATERY_BUFFET_PRICE)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_BUFFET_PRICE", e)
                        pass 
		

		try:
			EATERY_BUFFET_DETAILS = eatery_soup.find("span", {"class": "res-buffet-details"}).text
                        print "{0}  <<---->> {1}\n".format("EATERY_BUFFET_DETAILS", EATERY_BUFFET_DETAILS)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_BUFFET_DETAILS", e)
                        pass 


		try:
			coord = re.findall("\d+.\d+,\d+.\d+", eatery_soup.find("div", {"id": "res-map-canvas"}).find("img").get("data-original"))
			EATERY_COORDINATES = coord[-1]

                        print "{0}  <<---->> {1}\n".format("EATERY_COORDINATES", EATERY_COORDINATES)
                except Exception as e:
                        print "RETRY OF {0} failed with exception {1}\n".format("EATERY_COORDINATES", e)
                        pass 


                area_or_city = EATERY_URL.split("/")[-2]

                try:
			global REVIEWS_LIST
                        REVIEWS_LIST = eatery_soup.findAll("div" ,{"class": "res-review clearfix js-activity-root mbot   item-to-hide-parent stupendousact"})                                                                                                                                                            
                except Exception as e:
                        print "Reviews cannot be scraped"
                        return

			
	    
                        
                for review in REVIEWS_LIST:
                        print "{0} <====> {1}".format("USER_ID",  self.user_id(review))
                        print "{0} <====> {1}".format("USER_URL",  self.user_url(review))
                        print "{0} <====> {1}".format("USER_REVIEWS",  self.user_reviews(review))
                        print "{0} <====> {1}".format("USER_FOLLOWERS",  self.user_followers(review))
                        print "{0} <====> {1}".format("USER_NAME",  self.user_name(review))
                        print "{0} <====> {1}".format("REVIEW_URL",  self.review_url(review))
                        print "{0} <====> {1}".format("REVIEW_TIME",  self.review_time(review))
                        print "{0} <====> {1}".format("REVIEW_SUMMARY",  self.review_summary(review))
                        print "{0} <====> {1}".format("REVIEW_TEXT",  self.review_text(review))
                        print "{0} <====> {1}".format("REVIEW_LIKES",  self.review_likes(review))
                        print "{0} <====> {1}".format("REVIEW_ID",  self.review_id(review))
                        print "{0} <====> {1}".format("EATERY_ID",  self.eatery_id(eatery_soup))
                        print "{0} <====> {1}".format("TIME",  int(time.time()))
                        print "{0} <====> {1}".format("EPOCH_TIME",  self.converted_to_epoch(review))
                        print "{0} <====> {1}".format("AREA_OR_CITY",  area_or_city)
                        print "{0} <====> {1}".format("MANAGEMENT_RESPONSE",  self.review_management_response(review))
                        print "{0} <====> {1}".format("REVIEW_YEAR",  self.review_year(review))
                        print "{0} <====> {1}".format("REVIEW_MONTH",  self.review_month(review))
                        print "{0} <====> {1}".format("REVIEW_DAY",  self.review_day(review))
                        print "\n\n\n"




		
        def exception_handling(func):
                def deco(self, review):
                        try:
                                return func(self, review)

                        except ValueError as e:
                                print "{color} ERROR <{error}> in function <{function}>".format(color=bcolors.FAIL, error=e, function=func.__name__)
                                return None

                        except Exception as e:
                                print "{color} ERROR <{error}> in function <{function}>".format(color=bcolors.FAIL, error=e, function=func.__name__)
                                return None
                return deco



	@exception_handling
	def converted_to_epoch(self, review):
		time_stamp = review.find("a", {"class": "res-review-date"}).time.get("datetime")
		return time.mktime(time.strptime(time_stamp, "%Y-%m-%d %H:%M:%S"))


	@exception_handling
	def review_year(self, review):
		epoch = self.converted_to_epoch(review)
		return time.strftime("%Y", time.localtime(int(epoch)))

	@exception_handling
	def review_month(self, review):
		epoch = self.converted_to_epoch(review)
		return time.strftime("%m", time.localtime(int(epoch)))
	
		
	@exception_handling
	def review_day(self, review):
		epoch = self.converted_to_epoch(review)
		return time.strftime("%d", time.localtime(int(epoch)))
	
		
	@exception_handling
	def eatery_id(self, eatery_soup):
		return eatery_soup.find("div", {"class": "res-review-body clearfix"})["data-res_id"]


	@exception_handling
	def review_id(self, review):
		return review["data-review_id"]

	@exception_handling
	def user_name(self, review):
                return review.find("div" , {"class": "snippet__name"}).find("a").text

	@exception_handling
	def user_id(self, review):
                return review.find("a" , {"class": "snippet__link"})["data-entity_id"]

	@exception_handling
	def user_url(self, review):
                return review.find("div" , {"class": "snippet__head"}).find("a")["href"]

	@exception_handling
	def user_reviews(self, review):
                return review.findAll("span" , {"class": "snippet__reviews"})[0].text

	@exception_handling
	def user_followers(self, review):
                return review.find("span" , {"class": "snippet__followers"}).text

	@exception_handling
	def review_url(self, review):
		return review.find("a", {"class": "res-review-date"}).get("href")

	@exception_handling
	def review_time(self, review):
		return review.find("a", {"class": "res-review-date"}).time.get("datetime")

	@exception_handling
	def review_summary(self, review):
		return review.find("div", {"class": "rev-text"}).findChild().findChild().get("title")
		     
	@exception_handling
	def review_text(self, review):
		try:
		        review_dom = review.find("div", {"class": "rev-text hidden"})
			review_dom.find("div", {"class": "left"}).extract()#This removes the unimportqant divs from the review text div
			return review_dom.text
		except Exception:
			review_dom = review.find("div", {"class": "rev-text"})
			review_dom.find("div", {"class": "left"}).extract()#This removes the unimportqant divs from the review text div
			return review_dom.text


	@exception_handling
	def review_management_response(self, review):
		return review.find("div", {"class": "review-reply-text "}).text



	@exception_handling
	def review_likes(self, review):
		return review.find("a", {"class": "left thank-btn js-btn-thank "}).get("data-likes")




if __name__ == "__main__":
    
        t_est = TestMainScrape("https://www.zomato.com/ncr/restaurants", "https://www.zomato.com/ncr/majeeds-dwarka-new-delhi",
                    30, 120, )

        
        page_number = raw_input("Enter Page Numbers: ")
        PAGES = t_est.test_page_numbers()
        print "The length of the pages is now %s"%(len(PAGES))
        if int(page_number) == len(PAGES):
                print "The test for page humbers has been passed"
        else:
                sys.exit()


        PAGES_TO_BE_SCRAPED = t_est.test_skip_and_restaurants()
        print PAGES_TO_BE_SCRAPED
        pages_to_be_scraped = raw_input("DO you Think pages to be scraped are correct press 'y' to continue or else 'n' ")
        if pages_to_be_scraped == "n":
                sys.exit()

        EATERIES_SOUP_LIST = t_est.test_number_of_eateries()
        print len(EATERIES_SOUP_LIST)
        t_est.test_eatery_soup()


        if raw_input("If you think eateries data is being scraped correctly press 'y' to continue or else 'n' ") == "n":
                sys.exit()


        t_est.test_more_eateries_details()







