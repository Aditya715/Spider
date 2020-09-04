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
from bs4 import BeautifulSoup as bs


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
        data_table = soup.find("table", class_="gridView")
        # check whether records found or not.
        if data_table:
            tr = data_table.find("tr", class_="gridViewRow")
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

                return json.dumps(json_out)
        return False

    def get_form_data(self):
        """
            ------------------------
        """

        # creating session for request 
        with requests.session() as session:
            res = session.get(self.url, headers=self.headers)
            soup = bs(res.content, "html.parser")
            cookies = res.cookies

            # this regex is having some issue. Need to get resolved.
            # pattern = re.compile(
            #     r"document\.getElementById\( \'ctl00_ctl00_ctl00_ctl07_captchaAnswer\' \)\.value = (.*?);$", re.MULTILINE | re.DOTALL
            # )
            # script = soup.find("script", text=pattern)
            # print(pattern.search(script.text).group(1))

            captcha_answer = self.find_captcha(soup)

            # request 1 payload data
            data = {
                "__EVENTTARGET": "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS" : "",
                "__SCROLLPOSITIONX": soup.find("input", attrs={'name': '__SCROLLPOSITIONX'}).get("value"),
                "__SCROLLPOSITIONY": soup.find("input", attrs={'name': '__SCROLLPOSITIONY'}).get("value"),
                "__VIEWSTATE": soup.find("input", attrs={'name': '__VIEWSTATE'}).get("value"),
                "__VIEWSTATEGENERATOR": soup.find("input", attrs={'name': '__VIEWSTATEGENERATOR'}).get("value"),
                "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
                "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsDocketNumber$ddlCounty": '',
                "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer
            }

            # post method for request 1
            res = session.post(
                self.url, 
                headers=self.headers, 
                data=data,
                # cookies=cookies
            )

            cookies = res.cookies
            soup = bs(res.content, "html.parser")
            captcha = self.find_captcha(soup)

            # request 2 payload 
            payload = {
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
                "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer
            }

            # post method for request 2
            res = session.post(
                self.url, 
                headers=self.headers, 
                data=payload,
                cookies=cookies,
                # verify=True
            )
                
            soup = bs(res.text, "html.parser")
            # test by creating an HTML file.
            # print("writing file")
            # fopen = open("output.html", "w")
            # fopen.write(str(soup))
            # fopen.close()
            result = self.get_criminal_record(soup)
            return result

# main code here.
obj = PennsylvanialScrapper("william", "rios", "07/31/1975")
result = obj.get_form_data()
if result:
    print(result)
else:
    print("No records found.")