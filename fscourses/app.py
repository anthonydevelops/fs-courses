from fscourses.data import scrape_courses


def run():
    scrape_courses.scrapeCourses(
        'https://my.fresnostate.edu/psp/mfs/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL')
