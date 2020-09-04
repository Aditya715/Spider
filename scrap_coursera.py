"""
    COURSERA SCRAPPER 
    Purpose: To extract courses from coursera.
    Created on - 02/09/2020
"""
import json
import requests
from bs4 import BeautifulSoup as bs

class CourseraScraper:
    """
        Coursera Scrap 
    """
    def __init__(self):
        self.url = "https://www.coursera.org/browse/data-science/"
        self.list_of_courses = list()
    
    def get_data_analysis_courses(self, this_url):
        """
            Scrapper top level worker.
        """
        page_count = 1
        while True:
            # page 1 behaves unique so for page 1
            if page_count == 1:
                response = requests.get(this_url)
                if response.status_code == 200:
                    soup = bs(response.text, "html.parser")
                    all_courses = soup.find_all(class_="_1meetf18")
                    for each_course in all_courses:
                        tmp = {
                            "course_name": each_course.text
                        }
                        if tmp not in self.list_of_courses:
                            self.list_of_courses.append(tmp)
            # for rest of the pages
            else:
                """
                    Everything is coming up by json so leaving for now.
                    I'll figure it out soon.
                """
                break
            page_count += 1 
        # return

    def get_ai_courses(self):
        """
            Getting all artificial intelligence courses.
        """
        # coursera has three types of projects in AI till 02/09/2020
        courses_type = (
            "data-analysis",
            "machine-learning",
            "probability-and-statistics"
        )

        # iterating to get data from all course type
        for each_course in courses_type:
            # making of urls for different course types
            new_url = self.url + each_course
            self.get_data_analysis_courses(new_url)

# Main code
obj = CourseraScraper()
obj.get_ai_courses()
if obj.list_of_courses:
    print(obj.list_of_courses)
