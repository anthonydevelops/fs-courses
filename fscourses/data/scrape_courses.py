# scrape_courses.py
# Focuses on scraping the desired contents of each class and
# section associated through fresno states class search web application

import time
import re
import string
import json
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


class WebDriver:
    def __init__(self, link):
        self.link = link
        self.generateBrowser()
        self.execute()

    def generateBrowser(self):
        # Start Selenium session on Google Chrome & fetch webpage
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            "/home/anthony/Desktop/drivers/chromedriver", chrome_options=options)
        self.driver.get(self.link)
        self.driver.implicitly_wait(5)
        # Change to iframe
        frame = self.driver.find_element_by_css_selector(
            'div#ptifrmtarget iframe')
        self.driver.switch_to.frame(frame)
        self.driver.implicitly_wait(5)

    def execute(self):
        data = []
        subjectLetters = list(string.ascii_uppercase)
        # Set career type as undergraduate
        careerType = self.driver.find_element_by_id(
            'SSR_CLSRCH_WRK_ACAD_CAREER$3')
        careerType.click()
        self.driver.implicitly_wait(5)
        careerOptions = careerType.find_elements_by_css_selector('option')
        for option in careerOptions:
            if option.get_attribute('value') == 'UGRD':
                option.click()
                self.driver.implicitly_wait(5)
        # Click 'Show Open Classes Only' to toggle off
        allClasses = self.driver.find_element_by_id(
            'SSR_CLSRCH_WRK_SSR_OPEN_ONLY$chk$4')
        if allClasses.get_attribute('value') == "Y":
            self.driver.find_element_by_id(
                'SSR_CLSRCH_WRK_SSR_OPEN_ONLY$4').click()
            self.driver.implicitly_wait(5)
        # Click 'select subject'
        self.driver.find_element_by_id(
            'CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH$0').click()
        self.driver.implicitly_wait(5)
        # For each letter, sort and scrape subject data
        for letter in subjectLetters:
            # Click letter for sorting
            self.driver.find_element_by_id(
                'SSR_CLSRCH_WRK2_SSR_ALPHANUM_' + letter).click()
            self.driver.implicitly_wait(5)
            # Get list of all subjects
            totalSubjects = self.driver.find_elements_by_css_selector(
                'table tbody tr td div span.PSHYPERLINK')
            self.driver.implicitly_wait(5)
            sections = self.scrapeCourses(letter, totalSubjects)
            data.append(sections)

        # End script process
        self.stopBrowser()

        # Write sample classes to JSON file
        with open('./fscourses/data/data.json', 'w') as outfile:
            for i in data:
                json.dump([ob.__dict__ for ob in i], outfile)

    def scrapeCourses(self, letter, totalSubjects):
        sections = []
        for i in range(len(totalSubjects)-1):
            # Find the next subject to scrape
            if self.driver.find_elements_by_id('SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)):
                # Click link to subject
                self.driver.find_element_by_id(
                    'SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)).click()
                self.driver.implicitly_wait(5)
                # Submit subject chosen
                self.driver.find_element_by_id(
                    'SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)).submit()
                self.driver.implicitly_wait(5)
            else:
                self.driver.implicitly_wait(5)
                # Click link to subject
                self.driver.find_element_by_id(
                    'SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)).click()
                self.driver.implicitly_wait(5)
                # Submit subject chosen
                self.driver.find_element_by_id(
                    'SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$' + str(i)).submit()
                self.driver.implicitly_wait(5)

            # Submit form search
            self.driver.find_element_by_id(
                'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
            self.driver.implicitly_wait(5)

            # Check if error msg returned
            if self.driver.find_elements_by_css_selector('span.PSPAGE#DERIVED_CLSMSG_ERROR_TEXT'):
                time.sleep(2)
                if len(self.driver.find_elements_by_css_selector('td.PAGROUPBOXLABELLEVEL1 div')) < 1:
                    print("error error")
                    self.newSearch(letter)
                    continue

            # Check pop-up notification
            if self.driver.find_elements_by_id('#ICSave'):
                self.driver.find_element_by_id('#ICSave').click()
                self.driver.implicitly_wait(5)

            # Parse course content & titles
            id = 0
            courseTitles = self.driver.find_elements_by_css_selector(
                'td.PAGROUPBOXLABELLEVEL1 div')

            # For each title, assign the sections that correlate
            for index, title in enumerate(courseTitles):
                course = self.driver.find_element_by_id(
                    'ACE_SSR_CLSRSLT_WRK_GROUPBOX2$' + str(index))
                numOfSections = course.find_elements_by_css_selector(
                    'table.PSLEVEL1GRIDNBONBO')
                # Get each section content and store in a list
                for num in range(len(numOfSections)):
                    self.driver.implicitly_wait(5)
                    sectionNumber = self.driver.find_element_by_id(
                        'MTG_CLASS_NBR$' + str(id)).text
                    sectionName = self.driver.find_element_by_id(
                        'MTG_CLASSNAME$' + str(id)).text
                    sectionTime = self.driver.find_element_by_id(
                        'MTG_DAYTIME$' + str(id)).text
                    sectionRoom = self.driver.find_element_by_id(
                        'MTG_ROOM$' + str(id)).text
                    sectionInstr = self.driver.find_element_by_id(
                        'MTG_INSTR$' + str(id)).text
                    sectionDates = self.driver.find_element_by_id(
                        'MTG_TOPIC$' + str(id)).text
                    # Parse img for alt attribute
                    sectionDivStatus = self.driver.find_element_by_id(
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
            self.modifySearch(letter)

        return sections

    def stopBrowser(self):
        self.driver.quit()

    def modifySearch(self, letter):
        # Click 'modify search'
        self.driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_MODIFY').click()
        self.driver.implicitly_wait(5)
        self.newSearch(letter)

    def newSearch(self, letter):
        # Click 'select subject'
        self.driver.find_element_by_id(
            'CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH$0').click()
        self.driver.implicitly_wait(5)
        # Click letter for sorting
        self.driver.find_element_by_id(
            'SSR_CLSRCH_WRK2_SSR_ALPHANUM_' + letter).click()
        self.driver.implicitly_wait(5)
