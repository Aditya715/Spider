"""
    Automation Testing for PennsylvanialScrapper
        -> Functional Testing so far.
    Created on - 07/09/2020
    Last edit - 07/09/2020
"""

import json
import pytest
from .scrap_pennsy import PennsylvanialScrapper


def test_scrapper_pennsy():
    """
        Tester function to check the functionality of PennsylvanialScrapper.
        Test includes -> i) Records found \nii) No records found.
    """
    
    # json file which has all the test cases.
    input_json = "test_case_pennsylvania.json"
    
    with open(input_json) as file:
        json_read = json.load(file)

        # iterating over all the test cases.
        for each_test in json_read:
            input_values = each_test['input']
            expected_output = each_test['output']
            scrapper_object = PennsylvanialScrapper(
                            input_values['first_name'], 
                            input_values['last_name'],
                            input_values['date_of_birth']
                        )
            exact_output = scrapper_object.get_form_data()
            # exact output is json format.
            assert exact_output == json.dumps(expected_output)