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

        username = query_dict.get("username", "")
        password = query_dict.get("password", "")
        school_id = query_dict.get("sd", "1")
        url = query_dict.get("url", "")

        if not username or not password:
            self.send_error_response("Missing username or password")
            return

        if not url:
            self.send_error_response("Missing school domain")
            return

        try:
            session, school_name = getRequestSession(username, password, url, school_id)

            reportCardPageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/ReportCards.aspx").text

            parser = BeautifulSoup(reportCardPageContent, "html.parser")

            reportCardTable = parser.find("table", {"id": "plnMain_dgReportCard"})
            if not reportCardTable:
                self.send_error_response("Report card table not found")
                return

            reportCardRows = reportCardTable.find_all("tr", class_="sg-asp-table-data-row")

            reportCardData = []

            for row in reportCardRows:
                columns = row.find_all("td")

                course_code = columns[0].text.strip()
                course_name = columns[1].text.strip()
                teacher = columns[3].text.strip()
                room = columns[4].text.strip()
                attendance_credit = columns[5].text.strip()
                earned_credit = columns[6].text.strip()
                period1 = columns[7].text.strip()
                period2 = columns[8].text.strip()
                exam1 = columns[9].text.strip()
                semester1 = columns[10].text.strip()
                period3 = columns[11].text.strip()
                period4 = columns[12].text.strip()
                exam2 = columns[13].text.strip()
                semester2 = columns[14].text.strip()

                reportCardData.append({
                    "course_code": course_code,
                    "course_name": course_name,
                    "teacher": teacher,
                    "room": room,
                    "attendance_credit": attendance_credit,
                    "earned_credit": earned_credit,
                    "period1": period1,
                    "period2": period2,
                    "exam1": exam1,
                    "semester1": semester1,
                    "period3": period3,
                    "period4": period4,
                    "exam2": exam2,
                    "semester2": semester2
                })

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(reportCardData).encode(encoding="utf_8"))

        except RequestException as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except ValueError as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except Exception as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        return
