# scrape_courses.py
# Focuses on scraping the desired contents of each class and
# section associated through fresno states class search web application

import time
import re
import string
from selenium import webdriver


# Section stores all section related info
class Section:
    def __init__(self, title, number, name, time, room, instr, dates, status):
        self.title = title
        self.number = number
        self.name = name
        self.time = time
        self.room = room
        self.instr = instr
        self.dates = dates
        self.status = status

    def __str__(self):
        return "Title: %s, cNumber: %s, cName: %s, cTime: %s" % (self.title, self.number, self.name, self.time)


def execute(link):
    # Start Selenium session on Google Chrome & fetch webpage
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        "/home/anthony/Desktop/drivers/chromedriver", chrome_options=options)
    driver.get(link)
    driver.implicitly_wait(3)

    # Change to iframe
    frame = driver.find_element_by_css_selector('div#ptifrmtarget iframe')
    driver.switch_to.frame(frame)
    driver.implicitly_wait(3)

    # Modify form elements for parsing
    modForm(driver)


def stopExecution(driver):
    driver.quit()


def modForm(driver):
    subjectLetters = list(string.ascii_uppercase)
    for subject in subjectLetters:
        # Click 'choose subject'
        driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH$0').click()
        driver.implicitly_wait(3)
        # Click letter for sorting
        driver.find_element_by_id(
            'SSR_CLSRCH_WRK2_SSR_ALPHANUM_' + subject).click()
        driver.implicitly_wait(3)
        totalSubjects = driver.find_elements_by_css_selector(
            'table tbody tr td div span.PSHYPERLINK')
        scrapeCourses(driver, subject, totalSubjects)
    # End script process
    stopExecution(driver)


def reModForm(driver, subject):
    # Click 'choose subject'
    driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH$0').click()
    driver.implicitly_wait(3)
    # Click letter for sorting
    driver.find_element_by_id(
        'SSR_CLSRCH_WRK2_SSR_ALPHANUM_' + subject).click()
    driver.implicitly_wait(3)


def scrapeCourses(driver, subject, totalSubjects):
    sections = []
    for i in range(len(totalSubjects)):
        # Click first link
        driver.find_element_by_id(
            'SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)).click()
        driver.implicitly_wait(3)
        # Submit subject chosen
        driver.find_element_by_id(
            'SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)).submit()
        driver.implicitly_wait(3)
        # Click career type
        careerType = driver.find_element_by_id('SSR_CLSRCH_WRK_ACAD_CAREER$3')
        careerType.click()
        driver.implicitly_wait(3)
        careerOptions = careerType.find_elements_by_css_selector('option')
        for option in careerOptions:
            if option.get_attribute('value') == 'UGRD':
                option.click()
                driver.implicitly_wait(3)
        # Click 'Show Open Classes Only' to toggle off & submit form
        driver.find_element_by_id('SSR_CLSRCH_WRK_SSR_OPEN_ONLY$4').click()
        driver.implicitly_wait(3)
        driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
        driver.implicitly_wait(3)

        if driver.find_elements_by_id('DERIVED_CLSMSG_ERROR_TEXT'):
            reModForm(driver, subject)
            continue

        # Check pop-up notification
        if driver.find_elements_by_id('#ICSave'):
            driver.find_element_by_id('#ICSave').click()
            driver.implicitly_wait(3)

        # Parse course content & titles
        id = 0
        courseTitles = driver.find_elements_by_css_selector(
            'td.PAGROUPBOXLABELLEVEL1 div')

        # For each title, assign the sections that correlate
        for index, title in enumerate(courseTitles):
            course = driver.find_element_by_id(
                'ACE_SSR_CLSRSLT_WRK_GROUPBOX2$' + str(index))
            numOfSections = course.find_elements_by_css_selector(
                'table.PSLEVEL1GRIDNBONBO')
            # Get each section content and store in a list
            for num in range(len(numOfSections)):
                driver.implicitly_wait(3)
                sectionNumber = driver.find_element_by_id(
                    'MTG_CLASS_NBR$' + str(id)).text
                sectionName = driver.find_element_by_id(
                    'MTG_CLASSNAME$' + str(id)).text
                sectionTime = driver.find_element_by_id(
                    'MTG_DAYTIME$' + str(id)).text
                sectionRoom = driver.find_element_by_id(
                    'MTG_ROOM$' + str(id)).text
                sectionInstr = driver.find_element_by_id(
                    'MTG_INSTR$' + str(id)).text
                sectionDates = driver.find_element_by_id(
                    'MTG_TOPIC$' + str(id)).text
                # Parse img for alt attribute
                sectionDivStatus = driver.find_element_by_id(
                    'win0divDERIVED_CLSRCH_SSR_STATUS_LONG$' + str(id))
                sectionImgStatus = sectionDivStatus.find_element_by_css_selector(
                    'img')
                sectionStatus = sectionImgStatus.get_attribute('alt')
                # Assign section & store in list
                section = Section(title.text, sectionNumber, sectionName, sectionTime,
                                  sectionRoom, sectionInstr, sectionDates, sectionStatus)
                sections.append(section)
                id += 1
        # Restart search
        driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH').click()
        driver.implicitly_wait(3)
        reModForm(driver, subject)

    # # Check section contents
    for section in sections:
        print(section)
