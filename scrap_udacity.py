"""
    UDACITY SCRAPPER
    Purpose: To extract courses from udacity.
    Created on - 02/09/2020
"""

import json
import requests
from bs4 import BeautifulSoup as bs

class UdacitySpider:
    """
        Udacity spider to get the data from https://www.udacity.com/
    """
    def __init__(self):
        self.url = "https://www.udacity.com/"

    def get_ai_courses(self):
        """
            Getting all AI courses from udacity.
            params: url
            return: list of json if data extracted else False.
        """
        url_for_ai = self.url + "courses/school-of-ai"
        response = requests.get(url_for_ai)
        # checking response code
        if response.status_code == 200:
            soup = bs(response.text, "html.parser")
            # finding out all ai programs
            all_ai_programs = soup.find_all(class_="catalog-cards__list__item")
            # test case whether available or not.
            if all_ai_programs:
                list_of_courses = list()
                for each in all_ai_programs:
                    list_of_courses.append(
                        json.dumps({
                            "course_name" : each.find(class_="card__title__nd-name").text,
                            "skills_covered" : each.find(class_="text-content__text").text
                        })
                    )
                return list_of_courses
        return False

# main code   
spider_obj = UdacitySpider()
result = spider_obj.get_ai_courses()
if result:
    print(result)