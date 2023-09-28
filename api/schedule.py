from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
from urllib import parse
from requests.exceptions import RequestException

from api._lib.getRequestSession import getRequestSession

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_string = parse.urlsplit(self.path).query
        query_dict = dict(parse.parse_qsl(query_string))

        username = query_dict.get("username", "")
        password = query_dict.get("password", "")
        school_id = query_dict.get("sd", "380")  # Default to CSD if not provided

        if not username or not password:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing username or password"}).encode(encoding="utf_8"))
            return
            
        try:
            session, school_name = getRequestSession(username, password, school_id)

            schedulePageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Classes.aspx").text

            parser = BeautifulSoup(schedulePageContent, "lxml")

            schedule = []

            courses = parser.find_all("tr", "sg-asp-table-data-row")

            for row in courses:
                parser = BeautifulSoup(f"<html><body>{row}</body></html>", "lxml")
                tds = [x.text.strip() for x in parser.find_all("td")]

                if(len(tds) > 3):
                    schedule.append({
                        "building": tds[7],
                        "courseCode": tds[0],
                        "courseName": tds[1],
                        "days": tds[5],
                        "markingPeriods": tds[6],
                        "periods": tds[2],
                        "room": tds[4],
                        "status": tds[8],
                        "teacher": tds[3],
                    })

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "studentSchedule": schedule,
            }).encode(encoding="utf_8"))

            return
        except Exception as e:
            # Handle exceptions, if needed
            print(f"An error occurred: {e}")
