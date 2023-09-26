from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
import lxml
from urllib import parse

from api._lib.getRequestSession import getRequestSession

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_string = parse.urlsplit(self.path).query
        query_dict = dict(parse.parse_qsl(query_string))

        # Extract the parameters from the URL
        username = query_dict.get("username", "")
        password = query_dict.get("password", "")
        school_id = query_dict.get("sd", "380")  # Default to 380 if not provided

        # Check if any of the required parameters is missing
        if not username or not password:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing username or password"}).encode(encoding="utf_8"))
            return

        # Use the getRequestSession function with the provided parameters
        session, school_name = getRequestSession(username, password, school_id)

        registrationPageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Registration.aspx").text

        parser = BeautifulSoup(registrationPageContent, "lxml")

        studentName = parser.find(id="plnMain_lblRegStudentName").text
        studentBirthdate = parser.find(id="plnMain_lblBirthDate").text
        studentCounselor = parser.find(id="plnMain_lblCounselor").text
        studentCampus = parser.find(id="plnMain_lblBuildingName").text
        studentGrade = parser.find(id="plnMain_lblGrade").text
        totalCredits = 0

        # Try to get the student id from the registration page
        # If this fails, try to get the student id from the student schedule page
        try:
            studentId = parser.find(id="plnMain_lblRegStudentID").text
        except:
            schedulePageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Classes.aspx")
            parser = BeautifulSoup(schedulePageContent, "lxml")
            studentId = parser.find(id="plnMain_lblRegStudentID").text

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = {
            "id": studentId,
            "name": studentName,
            "birthdate": studentBirthdate,
            "campus": studentCampus,
            "grade": studentGrade,
            "counselor": studentCounselor,
            "totalCredits": str(totalCredits),
            "school_name": school_name
        }
        self.wfile.write(json.dumps(response_data).encode(encoding="utf_8"))

        return
