#import time
#import os
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
#import json


def checkIfContainsLink(element):
    if element.get_attribute("href") != None:
        return True
    else:
        return False


def getLinksJson(keyword):
    list = []
    driver = webdriver.Chrome("./chromedriver")
    driver.set_window_size(1920, 1080)
    driver.get("https://nida.nih.gov/search?sort=unified_date:desc")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, " //*[@id='root']/div/div[2]/div[2]/section[3]/div   ")))
    y = 1000
    for timer in range(0, 3):
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 1000
        time.sleep(1)
    barrecherche = driver.find_element(By.XPATH, "//*[@id='search_keyword']")
    barrecherche.send_keys(keyword)
    time.sleep(3)
    searchbtn = driver.find_element(
        By.XPATH, "  //*[@id='root']/div/div[2]/div[2]/section[1]/div/form/div/button[1] ")
    searchbtn.click()
    time.sleep(3)
    sectionElement = driver.find_element(
        By.XPATH, "//*[@id='root']/div/div[2]/div[2]/section[3] ")
    childElements = sectionElement.find_elements(By.TAG_NAME, "a")
    time.sleep(3)
    filterdList = filter(checkIfContainsLink, childElements)
    for e in filterdList:
        list.append(e.get_attribute("href"))
    jsonList = json.dumps(list)
    driver.close()
    return jsonList

 # ---------------------------


def ArticleScrper(link):

    driver = webdriver.Chrome("./chromedriver")
    driver.set_window_size(1920, 1080)
    driver.get(link)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, " //*[@id='block-nidapagetitle']/h1/span")))
    element = driver.find_element(
        By.XPATH, " //*[@id='block-nidapagetitle']/h1/span")
    title = element.text
    bodyWrapper = driver.find_element(
        By.XPATH, " /html/body/div[1]/div/div[4]/div/main/div[2]")
    new_paragraphs=[]
    paragraphs = bodyWrapper.find_elements(By.TAG_NAME, "p")
    for i in paragraphs:
        new_paragraphs.append(i.text)
    dict = {"title": title, "body": new_paragraphs}
    return json.dumps(dict, default=lambda o: '<not serializable>')


def WebScraper(keywords):
    ArticlesJson = []
    for keyword in keywords:
        links = getLinksJson(keyword)
        for link in links:
            articleJson = ArticleScrper(link)
            ArticlesJson = ArticlesJson.append(articleJson)
    return json.loads(ArticlesJson)

#links = getLinksJson('drugs')
#print(links)
#links = json.loads(links)
#for i in range(10):
#    print(ArticleScrper(links[i]))