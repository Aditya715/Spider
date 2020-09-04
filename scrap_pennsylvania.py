"""
    PENNSYLVANIA SCRAPPER
    Purpose: To extract relevant data from pennstlvania.
    Created on - 03/09/2020
"""
import json
import requests
from bs4 import BeautifulSoup as bs


class PennsylvanialScrapper:
    """
        ---- PENNSYLVANIA SPIDER -----

    """

    def __init__(self, target_first_name, target_last_name, target_dob):
        self.url = "https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.target_first_name = target_first_name
        self.target_last_name = target_last_name
        # target dob should be in format MM/DD/YYYY
        self.target_dob = target_dob

    def get_form_data(self):
        """
            ------------------------
        """
        with requests.session() as session:
            res = session.get(self.url, headers=self.headers)
            soup = bs(res.content, "html5lib")
            payload = {
                "__VIEWSTATE": soup.find("input", attrs={'name': '__VIEWSTATE'})['value'],
                "__VIEWSTATEGENERATOR": soup.find("input", attrs={'name': '__VIEWSTATEGENERATOR'})['value'],
                "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
                "ctl00$ctl00$ctl00$ctl07$captchaAnswer": soup.find("input", attrs={
                    'name': 'ctl00$ctl00$ctl00$ctl07$captchaAnswer'
                    })['value'],
                "op": "submit"
            }

            res = session.post(self.url, headers=self.headers, data=payload)
            print(res.content)

        # # search by participant
        # form-data = {
        #     __EVENTTARGET : "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType"
        # }
        
        # # requesting for a url under session 
        # with requests.session() as session:
        #     session.post(
        #         url=self.url,
        #         headers=self.headers,
        #         data=data
        #     )

obj = PennsylvanialScrapper("williams", "rios", "07/31/1975")
obj.get_form_data()