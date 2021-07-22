from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget
import pandas as pd
import random

counter = random.randint(0,2)

def createBrowser():
    file_path = '/home/divyanshusharma/Documents/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized");
    options.add_argument("--disable-extensions");
    options.add_argument("disable-infobars");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    options.add_argument("--no-sandbox");
    browser = webdriver.Chrome(chrome_options=options, executable_path=file_path)
    return browser


def randomizeProfiles():
    global counter
    profiles = [("bigggerdawg", "bigestdawg"), ("smalldawgz5246", "smalldawgz"), ("archangel_bgg", "dropDEAD")]
    if counter >= len(profiles):
        counter = 0;
    counter += 1
    return profiles[counter - 1]


def login(browser):
    browser.get("http://www.instagram.com")
    username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    profile = randomizeProfiles()
    USERNAME = profile[0]
    PASSWORD = profile[1]

    username.clear()
    username.send_keys(USERNAME)  # Instagram username
    password.clear()
    password.send_keys(PASSWORD)  # Instagram password

    Login_button = WebDriverWait(browser, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    not_now = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    not_now = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    return browser


def openProfile(browser, username):
    browser.get("https://www.instagram.com/" + username)


def scrollDown(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)


def saveImage(image, username, counter):
    path = os.getcwd()
    path = os.path.join(path, "data", username)
    if not os.path.exists(path):
        os.mkdir(path)
    save_as = os.path.join(path, username + str(counter) + '.jpg')
    wget.download(image, save_as)


def downloadImages():
    data = pd.read_csv('June222021.csv')
    usernames = data['username'].unique()[35:]
    browser = createBrowser()
    browser = login(browser)

    counter = 0
    profileCount = 0
    for username in usernames:
        openProfile(browser, username)
        time.sleep(2)
        anchors = [i for i in browser.find_elements_by_tag_name('img') if i.get_attribute('sizes') != ""]
        first_image = anchors[0].find_element_by_xpath('../..')
        first_image.click()
        time.sleep(1)
        k = 2
        while counter < 120:
            print(username + " : " + str(counter))
            skip = False
            try:
                photo = browser.find_element_by_xpath(
                    '/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/div[1]/img')
            except:
                try:
                    photo = browser.find_element_by_xpath(
                        '/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[' + str(
                            k) + ']/div/div/div/div[1]/div[1]/img')
                except:
                    try:
                        photo = browser.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[' + str(
                                k) + ']/div/div/div/div[1]/img')
                    except:
                        try:
                            photo = browser.find_element_by_xpath(
                                '/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/img')
                        except:
                            skip = True
                            try:
                                nextPic = browser.find_element_by_css_selector('div.coreSpriteRightChevron')
                                time.sleep(2)
                                nextPic.click()
                            except:
                                k = 2
                                skip = True
                                browser.find_element_by_css_selector('a.coreSpriteRightPaginationArrow').click()
            if not skip:
                saveImage(photo.get_attribute('src'), username, counter)
                counter += 1
                try:
                    nextPic = browser.find_element_by_css_selector('div.coreSpriteRightChevron')
                    time.sleep(4)
                    nextPic.click()
                    k = 3
                except:
                    browser.find_element_by_css_selector('a.coreSpriteRightPaginationArrow').click()
                    k = 2
                    time.sleep(5)
        counter = 0
        profileCount += 1
        if profileCount > 3:
            time.sleep(10000)
            login()
            profileCount = 0


downloadImages()
