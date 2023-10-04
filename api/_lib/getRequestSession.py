import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse, parse_qs

# Load school data from schools.json
current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, "schools.json")

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
else:
    print("File 'schools.json' not found.")
    data = {}

def get_school_info(domain, school_id):
    try:
        url = f"https://{domain}"
        school_name = data[domain].get(str(school_id))
        return url, school_name
    except KeyError:
        return None, None

def getRequestSession(username, password, url, school_id):
  login_url, school_name = get_school_info(url, school_id)

  if login_url is None:
        print("School not found for the provided URL and school ID.")
        return None, "Must have domain"
  
  if url not in data:
    return "Domain is not yet added to MyGrade. Please contact support to get your school added."

  print("School Name:", school_name)


  login_url = f"https://{url}/HomeAccess/Account/LogOn"
  print(login_url)

  # Create a session to persist cookies
  session = requests.Session()

  # Perform an initial GET request to obtain cookies
  login_page = session.get(login_url)
  login_page.raise_for_status()

  print("Status Code:", login_page.status_code)

  # Parse the response HTML
  loginScreenResponseText = login_page.text
  parser = BeautifulSoup(loginScreenResponseText, 'html.parser')

  # Find the __RequestVerificationToken input element
  requestVerificationTokenElement = parser.find(
      'input', {'name': '__RequestVerificationToken'})

  if requestVerificationTokenElement is not None:
    # Get the value attribute of the input element
    requestVerificationToken = requestVerificationTokenElement['value']
  else:
    raise ValueError("RequestVerificationToken not found")

  # Now, you have the RequestVerificationToken value in the requestVerificationToken variable
  print("RequestVerificationToken:", requestVerificationToken)

  # Prepare the login data using the obtained token
  login_data = {
    "Database": school_id,
    "LogOnDetails.UserName": username,
    "LogOnDetails.Password": password,
    "__RequestVerificationToken": requestVerificationToken,
    "VerificationOption": "UsernamePassword"
    }

  # Define request headers
  requestHeaders = {
      'User-Agent':
      'Your User Agent',
      'X-Requested-With':
      'XMLHttpRequest',
      'Host':
      'hac23.esp.k12.ar.us',
      'Origin':
      'https://hac23.esp.k12.ar.us',
      'Referer':
      "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f"
  }

  # Perform the login by sending a POST request with the login data and headers
  login_response = session.post(login_url,
                                data=login_data,
                                headers=requestHeaders)
  login_response.raise_for_status()

  return session, school_name
