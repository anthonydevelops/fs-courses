from selenium import webdriver
from fscourses.data import scrape_courses


link = 'https://my.fresnostate.edu/psp/mfs/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL'


def run():
    scrape_courses.execute(link)
