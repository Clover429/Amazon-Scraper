from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time


def review():
    #Initializes Variables
    count = 0
    j = "2"
    crit = 1
    totReviews = 0
    totStars = 0
    average = 0
    probNotBias = 0
    potBiasHigh = 0
    potBiasLow = 0
    star1 = "a-star-1"
    star2 = "a-star-2"
    star3 = "a-star-3" 
    star4 = "a-star-4"
    star5 = "a-star-5"

    #Initializes Driver and Opens Amazon Page
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    url = 'https://www.amazon.com/Apple-Generation-Cancelling-Transparency-Personalized/dp/B0CHWRXH8B/ref=sr_1_1_sspa?crid=2K0P32J239GTI&keywords=airpods&qid=1700011455&s=amazon-devices&sprefix=%2Camazon-devices%2C102&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
    driver.get(url)

    #Goes to the Reviews Section
    reviews_box = driver.find_element(By.ID, 'acrCustomerReviewLink')
    reviews_box.click()
    time.sleep(1)

    #Opens the Reviews
    search_more = driver.find_element(By.XPATH, '//a[@data-hook="see-all-reviews-link-foot"]')
    search_more.click()
    time.sleep(2)

    #Initalizes Variables
    count = 0
    i = 0

    #Opens Text File to Store Data
    with open ('reviews.txt', 'w') as file:
        while True:
            try:
                reviewList = []
                currReview = []
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='a-profile-name']")))
                #Stores all of the Name and Review Elements on the Current Page
                names = driver.find_elements(By.XPATH, "//span[@class='a-profile-name']")
                reviews = driver.find_elements(By.XPATH, "//i[@data-hook='review-star-rating']") 
                for r in reviews:
                    #Stores the Star Rating of Each Review
                    review = r.get_attribute("class")
                    if star1 in review:
                        reviewList.append("1")
                        currReview.append(1)
                    elif star2 in review:
                        reviewList.append("2")
                        currReview.append(2)
                    elif star3 in review:
                        reviewList.append("3")
                        currReview.append(3)
                    elif star4 in review:
                        reviewList.append("4")
                        currReview.append(4)
                    elif star5 in review:
                        reviewList.append("5")
                        currReview.append(5)
                #Cycles Through Each Reviewer, Going through their Profile and Checking All Their Reviews
                for n in range(len(names)):
                    totReviews = 0
                    totStars = 0
                    average = 0

                    if i == len(reviewList):
                        break

                    try:
                        count = count + 1
                        name = names[n].text
                        if len(name) > 0 and count > 2:
                            file.write("Name: " + name)
                            file.write(", Rating: " + reviewList[i])
                            names[n].click()
                            time.sleep(1)
                            
                            #Counts Total Star Rating of All Reviews and Averages it
                            profileReviewsFive = driver.find_elements(By.XPATH, "//i[@class='a-icon a-icon-star a-star-5 profile-at-review-stars']")
                            numFive = len(profileReviewsFive)
                            totReviews = totReviews+numFive
                            totStars = totStars + 5*numFive

                            profileReviewsFour = driver.find_elements(By.XPATH, "//i[@class='a-icon a-icon-star a-star-4 profile-at-review-stars']")
                            numFour = len(profileReviewsFour)
                            totReviews = totReviews+numFour
                            totStars = totStars + 4*numFour
                            time.sleep(1)

                            profileReviewsThree = driver.find_elements(By.XPATH, "//i[@class='a-icon a-icon-star a-star-3 profile-at-review-stars']")
                            numThree = len(profileReviewsThree)
                            totReviews = totReviews+numThree
                            totStars = totStars + 3*numThree

                            profileReviewsTwo = driver.find_elements(By.XPATH, "//i[@class='a-icon a-icon-star a-star-2 profile-at-review-stars']")
                            numTwo = len(profileReviewsTwo)
                            totReviews = totReviews+numTwo
                            totStars = totStars + 2*numTwo

                            profileReviewsOne = driver.find_elements(By.XPATH, "//i[@class='a-icon a-icon-star a-star-1 profile-at-review-stars']")
                            numOne = len(profileReviewsOne)
                            totReviews = totReviews+numOne
                            totStars = totStars + 1*numOne
                            time.sleep(1)

                            try:
                                numHearts = driver.find_element(By.XPATH, "//span[@class='impact-text']")
                                hearts = numHearts.text
                            except Exception:
                                hearts = "0"

                            if ',' in hearts:
                                numHearts = int(hearts.replace(',', ''))
                            else:
                                numHearts = int(hearts)
                            
                            if totReviews == 0:
                                average = currReview[i]
                                avgStr = str(average)
                            else: 
                                average = totStars / totReviews
                                average = round(average, 2)
                                avgStr = str(average)
                            time.sleep(1)
                            file.write(", Average Rating: " + avgStr + " out of 5 stars, ")
                            file.write("Heart Count: " + hearts + ", Summary: ")
                            #Summarizes Findings, Indicates Potential Bias
                            if average > 3 :
                                if totReviews > 8:
                                    if numHearts > 100:
                                        file.write("High Average, Many Reviews, High Hearts, Potentially Biased (High)\n")
                                        potBiasHigh += 1
                                    else:
                                        file.write("High Average, Many Reviews, Low Hearts, Probably Not Biased\n")
                                        probNotBias += 1
                                else :
                                    if numHearts > 100:
                                        file.write("High Average, Not Many Reviews, High Hearts, Potentially Biased (High)\n")
                                        potBiasHigh += 1
                                    else :
                                        file.write("High Average, Not Many Reviews, Low Hearts, Probably Not Biased\n")
                                        probNotBias += 1
                            else :
                                if totReviews > 8:
                                    if numHearts > 100:
                                        file.write("Low Average, Many Reviews, High Hearts, Probably Not Biased\n")
                                        probNotBias += 1
                                    else:
                                        file.write("Low Average, Many Reviews, Low Hearts, Potentially Biased (Low)\n")
                                        potBiasLow += 1
                                else:
                                    if numHearts > 100:
                                        file.write("Low Average, Not Many Reviews, High Hearts, Probably Not Biased\n")
                                        probNotBias += 1
                                    else:
                                        file.write("Low Average, Not Many Reviews, Low Hearts, Probably Not Biased\n")
                                        probNotBias += 1
                            i = i + 1
                            driver.back()
                            time.sleep(1)
                            names = driver.find_elements(By.XPATH, "//span[@class='a-profile-name']")
                            time.sleep(1)
                    except StaleElementReferenceException:
                        pass
                        
                
                #Goes To the Next Review Page
                count = 0
                i = 0
                next_page = driver.find_element(By.XPATH, f"//a[contains(@href, 'pageNumber={j}')]")
                next_page.click()
                jNum = int(j)
                jNum = jNum + 1
                j = str(jNum)
                time.sleep(3)
            except Exception:
                #If there are no more pages of Positive Reivews, it goes to the Critical Reviews
                if crit == 1:
                    critical_reviews = driver.find_element(By.XPATH, "//a[contains(@href, 'filterByStar=critical')]")
                    critical_reviews.click()
                    time.sleep(3)
                    crit += 1
                    j = "2"
                else:
                    #Loop Breaks Once All Reviews Have Been Covered
                    break
        
        #Prints Out Number of Reviewes With/Without Bias
        file.write("\n")
        file.write("In Total: Reviewers With Probably Not Much Bias: " + str(probNotBias) + "\n")
        file.write("Reviewers That Potentially Are Biased to Review High: " + str(potBiasHigh) + "\n")
        file.write("Reviewers That Potentially Are Biased to Review Low: " + str(potBiasLow) + "\n")

    driver.quit()


if __name__ == "__main__":
    review()
    