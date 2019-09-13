import time
from selenium import webdriver


def scrapeCourses(link):
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

    driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH$0').click()
    driver.implicitly_wait(3)
    driver.find_element_by_id('SSR_CLSRCH_WRK2_SSR_ALPHANUM_B').click()
    driver.implicitly_wait(3)
    driver.find_element_by_id('SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$0').click()
    driver.implicitly_wait(3)
    driver.find_element_by_id('SSR_CLSRCH_WRK2_SSR_PB_SELECT_SUBJ$0').submit()
    # driver.refresh()
    # driver.find_element_by_id('SSR_CLSRCH_WRK_SSR_OPEN_ONLY$4').click()
    # driver.implicitly_wait(3)
    time.sleep(3)

    driver.quit()


if __name__ == "__main__":
    link = 'https://my.fresnostate.edu/psp/mfs/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?FolderPath=PORTAL_ROOT_OBJECT.FR_VIEW_SOC.FR_CLASS_SEARCH_GBL2&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder'

    scrapeCourses(link)
