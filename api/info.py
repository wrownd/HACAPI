from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
from urllib import parse
from requests.exceptions import RequestException

from api._lib.getRequestSession import getRequestSession

class handler(BaseHTTPRequestHandler):

    def send_error_response(self, error_message):
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        error_response = {
            "error": "Bad Request",
            "message": error_message
        }
        self.wfile.write(json.dumps(error_response).encode(encoding="utf_8"))

    def do_GET(self):
        query_string = parse.urlsplit(self.path).query
        query_dict = dict(parse.parse_qsl(query_string))

        # Extract the parameters from the URL
        username = query_dict.get("username", "")
        password = query_dict.get("password", "")
        school_id = query_dict.get("sd", "380")  # Default to 380 if not provided
        url = query_dict.get("url", "")

        # Check if any of the required parameters is missing
        if not username or not password:
            self.send_error_response("Missing username or password")
            return

        if not url:
            self.send_error_response("Missing school domain")
            return


        try:
            # Use the getRequestSession function with the provided parameters
            session, school_name = getRequestSession(username, password, url, school_id)

            registrationPageContent = session.get(f"https://{url}/HomeAccess/Content/Student/Registration.aspx").text

            parser = BeautifulSoup(registrationPageContent, "lxml")
            studentLang = parser.find(id="plnMain_lblLanguage").text
            studentName = parser.find(id="plnMain_lblRegStudentName").text
            studentSSN = parser.find(id="plnMain_lblSSN").text
            studentBirthdate = parser.find(id="plnMain_lblBirthDate").text
            studentCounselor = parser.find(id="plnMain_lblCounselor").text
            studentCampus = parser.find(id="plnMain_lblBuildingName").text
            studentGrade = parser.find(id="plnMain_lblGrade").text
            totalCredits = 0

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response_data = {
                "lang": studentLang,
                "ssn": studentSSN,
                "name": studentName,
                "birthdate": studentBirthdate,
                "campus": studentCampus,
                "grade": studentGrade,
                "counselor": studentCounselor,
                "totalCredits": str(totalCredits),
                "school_name": school_name,
            }
            response_json = json.dumps(response_data).encode(encoding="utf_8")
            self.wfile.write(response_json)

        except RequestException as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except ValueError as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except Exception as e:
            self.send_error_response(f"An error occurred: {str(e)}")
