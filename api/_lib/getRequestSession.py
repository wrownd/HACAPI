import requests
from bs4 import BeautifulSoup
import lxml
import json

def getRequestSession(username, password, school_id):
    requestSession = requests.session()

    # Load the school data from the JSON file
    with open('_lib/schools.json', 'r') as schools_file:
        schools_data = json.load(schools_file)

    # Get the school name based on the school_id
    school_name = schools_data.get(school_id)

    if school_name is None:
        raise ValueError("Invalid school ID")

    loginScreenResponse = requestSession.get("https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f").text

    parser = BeautifulSoup(loginScreenResponse, "lxml")

    requestVerificationToken = parser.find('input', attrs={'name': '__RequestVerificationToken'})["value"]

    requestHeaders = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'hac23.esp.k12.ar.us',
        'Origin': 'hac23.esp.k12.ar.us',
        'Referer': "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f",
        '__RequestVerificationToken': requestVerificationToken
    }

    requestPayload = {
        "__RequestVerificationToken" : requestVerificationToken,
        "SCKTY00328510CustomEnabled" : "False",
        "SCKTY00436568CustomEnabled" : "False",
        "Database" : school_id,
        "VerificationOption" : "UsernamePassword",
        "LogOnDetails.UserName": username,
        "tempUN" : "",
        "tempPW" : "",
        "LogOnDetails.Password" : password
    }

    pageDOM = requestSession.post(
        "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f",
        data=requestPayload,
        headers=requestHeaders
    )

    return requestSession, school_name
