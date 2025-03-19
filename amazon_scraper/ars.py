from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def scrape_reviews(url, output_file='reviews.txt'):
    # Set up Selenium Chrome WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options)


    # Open the Amazon product page
    driver.get(url)

    # Get the product name
    product_name = driver.find_element(By.CSS_SELECTOR, 'span[data-asin="B0CHWRXH8B"]').text
    print(f"Product: {product_name}")

    # Scroll down to load more reviews
    scroll_down(driver)

    # Extract review elements
    reviews_data = []

    reviews = driver.find_elements(By.CSS_SELECTOR, 'div[data-asin]')

    for review in reviews:
        # Extract review details
        star_rating = review.find_element(By.CSS_SELECTOR, 'i[data-asin="B0CHWRXH8B"]').text
        reviewer_profile_url = review.find_element(By.CSS_SELECTOR, 'a[data-asin="B0CHWRXH8B"]')['href']

        # Calculate the average rating for the reviewer
        average_rating = analyze_reviewer_profile(driver, reviewer_profile_url)

        # Append review details to the list
        reviews_data.append({
            'Star Rating': star_rating,
            'Reviewer Profile URL': reviewer_profile_url,
            'Average Rating for Reviewer': average_rating
        })

        # Wait for a random time before making the next request
        wait_time = random.uniform(2, 6)  # Random wait time between 2 and 6 seconds
        time.sleep(wait_time)

    # Write the reviews data to a text file
    with open(output_file, 'w') as file:
        for review_data in reviews_data:
            file.write(str(review_data) + '\n')

    print(f"Reviews data written to {output_file}")

def scroll_down(driver):
    # Scroll down to load more reviews
    while True:
        try:
            # Locate the "See all reviews" button and click it
            see_all_reviews = driver.find_element(By.CSS_SELECTOR, 'a[data-asin="B0CHWRXH8B"]')
            ActionChains(driver).move_to_element(see_all_reviews).click(see_all_reviews).perform()
            time.sleep(2)  # Wait for reviews to load
        except Exception as e:
            break

def analyze_reviewer_profile(driver, profile_url):
    # Open the reviewer's profile page
    driver.get(profile_url)

    # Extract and calculate the average rating for the reviewer
    reviewer_reviews = driver.find_elements(By.CSS_SELECTOR, 'span[data-asin="B0CHWRXH8B"]')
    total_rating = 0
    total_reviews = 0

    for reviewer_review in reviewer_reviews:
        # Extract the star rating for each review
        try:
            rating = reviewer_review.find_element(By.CSS_SELECTOR, 'i[data-asin="B0CHWRXH8B"]').text
            total_rating += int(rating)
            total_reviews += 1
        except Exception as e:
            # Handle cases where the star rating is not available or not valid
            print(f"Error extracting star rating: {e}")

    # Calculate the average rating
    average_rating = total_rating / total_reviews if total_reviews > 0 else 0
    return average_rating

if __name__ == "__main__":
    scrape_reviews("https://www.amazon.com/Apple-Generation-Cancelling-Transparency-Personalized/product-reviews/B0CHWRXH8B/ref=cm_cr_arp_d_show_all?ie=UTF8&reviewerType=all_reviews&pageNumber=1", 'reviews.txt')
