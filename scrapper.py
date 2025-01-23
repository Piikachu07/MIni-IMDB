# -*- coding: utf-8 -*-
"""
Created on Fri Dec  20 14:44:34 2024

@author: User
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import numpy as np
import time
from parsel import Selector

def scrape_movie_reviews(url):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    # Create a Service object with the Chromedriver path
    chromedriver_path = "/Users/jangidpankaj/Desktop/Desk/Chrome/chromedriver-mac-arm64"
    service = Service(chromedriver_path)

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = url + 'reviews?ref_=tt_urv'
    driver.get(url)

    more_review_pages = 20  # Set the number of pages you want to load
    for _ in tqdm(range(more_review_pages)):
        try:
            css_selector = 'load-more-trigger'
            driver.find_element(By.ID, css_selector).click()
            time.sleep(2)  # Add a small delay to allow the reviews to load
        except:
            break

    # Extract reviews, ratings, and subjects from the loaded pages
    reviews = driver.find_elements(By.CSS_SELECTOR, '.review-container')
    rating_list = []
    review_date_list = []
    review_title_list = []
    author_list = []
    review_list = []

    for review in tqdm(reviews):
        try:
            sel2 = Selector(text=review.get_attribute('innerHTML'))

            try:
                rating = sel2.css('.rating-other-user-rating span::text').extract_first()
            except:
                rating = np.NaN
            rating_list.append(rating)

            try:
                review_date = sel2.css('.review-date::text').extract_first().strip()
            except:
                review_date = ''
            review_date_list.append(review_date)

            try:
                author = sel2.css('.display-name-link a::text').extract_first().strip()
            except:
                author = ''
            author_list.append(author)

            try:
                review_title = sel2.css('a.title::text').extract_first().strip()
            except:
                review_title = ''
            review_title_list.append(review_title)

            try:
                review = sel2.css('.text.show-more__control::text').extract_first().strip()
            except:
                review = ''
            review_list.append(review)
        except Exception :
            return None

    driver.quit()  # Close the browser after scraping

    # Create a dataframe from the scraped data
    review_df = pd.DataFrame({
        'Review_Date': review_date_list,
        'Author': author_list,
        'Rating': rating_list,
        'Review_Title': review_title_list,
        'Review': review_list
    })

    return review_df