from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
from urllib import parse
from requests.exceptions import RequestException
from api._lib.getRequestSession import getRequestSession

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/info"):
            query = parse.parse_qs(parse.urlsplit(self.path).query)
            username = query.get("username", [""])[0]
            password = query.get("password", [""])[0]
            school_id = query.get("sd", ["380"])[0]

            if not username or not password:
                response_data = {"error": "Missing username or password"}
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                return

            try:
                # Call the getRequestSession function to obtain the session and school name
                session, school_name = getRequestSession(username, password, school_id)

                # Simulate the response for the registration page content
                registrationPageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Registration.aspx").text
                parser = BeautifulSoup(registrationPageContent, "lxml")

                studentName = parser.find(id="plnMain_lblRegStudentName").text
                studentBirthdate = parser.find(id="plnMain_lblBirthDate").text
                studentCounselor = parser.find(id="plnMain_lblCounselor").text
                studentCampus = parser.find(id="plnMain_lblBuildingName").text
                studentGrade = parser.find(id="plnMain_lblGrade").text
                totalCredits = 0

                response_data = {
                    "id": "studentId",
                    "name": studentName,
                    "birthdate": studentBirthdate,
                    "campus": studentCampus,
                    "grade": studentGrade,
                    "counselor": studentCounselor,
                    "totalCredits": str(totalCredits),
                    "school_name": school_name,
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

            except RequestException as e:
                # Handle requests-related exceptions
                error_response = {
                    "error": "Internal Server Error",
                    "message": str(e),  # Include the exception message for debugging
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode("utf-8"))

            except Exception as e:
                # Handle other exceptions
                error_response = {
                    "error": "Internal Server Error",
                    "message": str(e),  # Include the exception message for debugging
                }
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
