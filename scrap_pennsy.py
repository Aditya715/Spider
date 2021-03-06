"""
    PENNSYLVANIA SCRAPPER
    Purpose: To extract relevant data from pennstlvania.
    Created on - 03/09/2020
"""
import re
import json
from pprint import pprint
import requests
from requests import Session, Request
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


class PennsylvanialScrapper:
    """
        ---- PENNSYLVANIA SPIDER -----
        Purpose: To extract data https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx.
    """

    def __init__(self, target_first_name, target_last_name, target_dob):
        self.url = "https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx"
        self.headers =  {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        self.target_first_name = target_first_name
        self.target_last_name = target_last_name
        # target dob should be in format MM/DD/YYYY
        self.target_dob = target_dob

    @staticmethod
    def find_captcha(soup):
        """
            Extract out captcha using the id or name
            params: beautifulsoup object
            return: captcha
        """
        scripts = soup.find_all('script')
        res = ''
        for script in scripts:
            s = script.string
            if s is None:
                continue
            indx = s.find("ctl00_ctl00_ctl00_ctl07_captchaAnswer")
            if indx != -1:
                x1 = s.find('=', indx)
                x2 = s.find(';', indx)
                res = s[x1 + 1:x2].strip().replace("'", "")
        return res

    @staticmethod
    def get_criminal_record(soup):
        """
            Extract the data once there is record found.
            params: beautifulsoup object
            return: json of record if found else boolean False.
        """
        list_of_records = list()
        data_table = soup.find("table", class_="gridView")
        # check whether records found or not.
        if data_table:
            all_trs = data_table.find_all("tr", class_="gridViewRow")
            if all_trs:
                for tr in all_trs:
                    all_tds = tr.find_all("td")
                    # check on datatable.
                    if all_tds:
                        json_out = {
                            "docket_number": all_tds[7].text.strip(),
                            "court_office" : all_tds[8].text.strip(),
                            "short_caption": all_tds[9].text.strip(),
                            "filling_date": all_tds[10].text.strip(),
                            "country": all_tds[11].text.strip(),
                            "case_status": all_tds[12].text.strip(),
                            "primary_participant": all_tds[13].text.strip(),
                            "OTN" : all_tds[15].text.strip(),
                            "complaint_number": all_tds[18].text.strip(),
                            "police_incident": all_tds[18].text.strip(),
                            "date_of_birth": all_tds[19].text.strip()
                        }
                        list_of_records.append(json_out)    
        return list_of_records

    @staticmethod
    def manual_testing(soup):
        """
            This is manual testing by creating a html file for the response.
            params: soup object
            return: None
        """

        manual_testing_file = "output.html"
        fopen = open(manual_testing_file, "w")
        fopen.write(str(soup))
        fopen.close()

    def post_request(self, session, payload_data, cookies):        
        """
            Hit a post request with the given payload.
            params: session object, payload, cookies
            return: response or error along with a status flag.
        """
        try:
            response = session.post(
                self.url, 
                headers=self.headers, 
                data=payload_data,
                verify=False,
                cookies=cookies
            )
            return response, True

        except ConnectionError:
            return {"Error": "Lost connction with the url."}, False
        
        if response.status_code != 200:
            return {
                    "Error Code": response.status_code,
                    "Error Message": "Unable to redirect to the page, check manually whether the page is down if not contact developer with error code."
                }, False
    
    @staticmethod
    def get_cookies(response):
        """This function takes response as params and returns cookies of that response."""
        return response.cookies

    def first_payload_creation(self,soup):
        """
            returns the payload data for the first post request from the soup params.
            params: self, beautifulsoup object
            return: a dictionary of payload
        """
        return {
            "__EVENTTARGET": "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS" : "",
            "__SCROLLPOSITIONX": soup.find("input", attrs={'name': '__SCROLLPOSITIONX'}).get("value"),
            "__SCROLLPOSITIONY": soup.find("input", attrs={'name': '__SCROLLPOSITIONY'}).get("value"),
            "__VIEWSTATE": soup.find("input", attrs={'name': '__VIEWSTATE'}).get("value"),
            "__VIEWSTATEGENERATOR": soup.find("input", attrs={'name': '__VIEWSTATEGENERATOR'}).get("value"),
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsDocketNumber$ddlCounty": '',
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": self.find_captcha(soup)
        }

    def second_payload_creation(self, soup):
        """
            returns the payload data for the second post request from the soup params.
            params: self, beautifulsoup object
            return: a dictionary of payload
        """
        return  {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS" : "",
            "__SCROLLPOSITIONX": soup.find("input", attrs={'name': '__SCROLLPOSITIONX'}).get("value"),
            "__SCROLLPOSITIONY": soup.find("input", attrs={'name': '__SCROLLPOSITIONY'}).get("value"),
            "__VIEWSTATE": soup.find("input", attrs={'name': '__VIEWSTATE'}).get("value"),
            "__VIEWSTATEGENERATOR": soup.find("input", attrs={'name': '__VIEWSTATEGENERATOR'}).get("value"),
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtLastName" : self.target_last_name,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtFirstName": self.target_first_name,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBox": self.target_dob,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBoxMaskExtender_ClientState": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCounty": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlDocketType": "CR",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCaseStatus": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBox": "__/__/____",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBoxMaskExtender_ClientState": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBox": "__/__/____",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBoxMaskExtender_ClientState": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$btnSearch" : "Search",
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": self.find_captcha(soup)
        }

    @staticmethod
    def create_soup(response):
        """
            params: response object
            return: BeautifulSoup object
        """
        return BeautifulSoup(response.content, "html.parser")

    def fetch_records(self):
        """
            Fetching records data for a particular body.
            params: self object
            return: list of records/ blank list/ error message
        """

        # creating session for request 
        with requests.session() as session:
            try:
                response = session.get(self.url, headers=self.headers, verify=False)
            except ConnectionError:
                return {"Error": "Check url or connectivity."}
            # response code check.
            if response.status_code != 200:
                return {
                    "Error Code": response.status_code, 
                    "Error Message": "Check the page manually and if it's there, contact developer with the error code."
                }

            # creating beautifulsoup object
            soup = self.create_soup(response)
            cookies = self.get_cookies(response)
            # payload creation here.
            data = self.first_payload_creation(soup)    
            # post method for request 1
            response, status = self.post_request(session, data, cookies)
            if not status:
                return response

            cookies = self.get_cookies(response)
            soup = self.create_soup(response)    
            # request 2 payload 
            data = self.second_payload_creation(soup)
            # post method for request 2
            response, status = self.post_request(session, data, cookies)
            if not status:
                return response
            
            soup = self.create_soup(response)
            # self.manual_testing(soup)     # for manual testing.

            # fetching criminal record.
            result = self.get_criminal_record(soup)
            return result


# main code here.
if __name__ == "__main__":
    # DOB format -- "MM/DD/YYYY"
    obj = PennsylvanialScrapper("steve", "smith", "04/23/2001")
    result = obj.fetch_records()
    if result:
        pprint(result)
    else:
        print("No records found.")