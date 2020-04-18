# LinkedBot.py
import argparse
import os
import random
import time
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver


def getPeopleLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/in' in url:
                links.append(url)
    return links


def getJobLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)
    return links


def getID(url):
    pUrl = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(pUrl.query)['id'][0]


def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    while True:
        # sleep to make sure everything loads, add random to make us look human.
        time.sleep(random.uniform(3.5, 6.9))
        page = BeautifulSoup(browser.page_source,features="html.parser")
        people = getPeopleLinks(page)
        if people:
            for person in people:
                ID = getID(person)
                if ID not in visited:
                    pList.append(person)
                    visited[ID] = 1
        if pList:  # if there is people to look at look at them
            person = pList.pop()
            browser.get(person)
            count += 1
        else:  # otherwise find people via the job pages
            jobs = getJobLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'https://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com' + job
                browser.get(job)
            else:
                print
                "I'm Lost Exiting"
                break

        # Output (Make option for this)
        print
        "[+] " + browser.title + " Visited! \n(" \
        + str(count) + "/" + str(len(pList)) + ") Visited/Queue)"


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="linkedin email")
    parser.add_argument("password", help="linkedin password")
    args = parser.parse_args()

    browser = webdriver.Chrome()

    browser.get("https://linkedin.com/uas/login")

    emailElement = browser.find_element_by_id("username")
    emailElement.send_keys(args.email)
    passElement = browser.find_element_by_id("password")
    passElement.send_keys(args.password)
    passElement.submit()

    #os.system('clear')
    print("[+] Success! Logged In, Bot Starting!")
    ViewBot(browser)
    browser.close()


if __name__ == '__main__':
    Main()