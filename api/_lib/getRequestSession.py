import requests
from bs4 import BeautifulSoup
import lxml
import json
import os

def getRequestSession(username, password, school_id):
    try:
        requestSession = requests.session()

        # Set the current working directory to the directory of this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_dir)

        # Now you can open 'schools.json'
        with open('schools.json', 'r') as schools_file:
            schools_data = json.load(schools_file)  # Load schools_data from the JSON file

        # Get the school name based on the school_id
        school_name = schools_data.get(school_id)

        if school_name is None:
            raise ValueError("Invalid school ID")

        # Make the HTTP GET request
        loginScreenResponse = requestSession.get("https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f")

        # Check the HTTP status code
        loginScreenResponse.raise_for_status()

        # Access the response text after verifying the status code
        loginScreenResponseText = loginScreenResponse.text
        parser = BeautifulSoup(loginScreenResponseText, "lxml")

        requestVerificationToken = parser.find('input', attrs={'name': '__RequestVerificationToken_L0hvbWVBY2Nlc3M1'})["value"]

        requestHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'hac23.esp.k12.ar.us',
            'Origin': 'hac23.esp.k12.ar.us',
            'Referer': "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f",
            '__RequestVerificationToken': requestVerificationToken
        }

        requestPayload = {
            "__RequestVerificationToken": requestVerificationToken,
            "SCKTY00328510CustomEnabled": "False",
            "SCKTY00436568CustomEnabled": "False",
            "Database": school_id,
            "VerificationOption": "UsernamePassword",
            "LogOnDetails.UserName": username,
            "tempUN": "",
            "tempPW": "",
            "LogOnDetails.Password": password
        }

        pageDOM = requestSession.post(
            "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f",
            data=requestPayload,
            headers=requestHeaders
        )

        return requestSession, school_name
    except Exception as e:
        # Handle exceptions here, e.g., log the error, return an error response, etc.
        print(f"An error occurred: {e}")
        return None, None  # Modify the return value as needed
