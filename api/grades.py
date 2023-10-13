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

            registrationPageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Assignments.aspx").text

            parser = BeautifulSoup(registrationPageContent, "lxml")

            courses = []

            courseContainer = parser.find_all("div", "AssignmentClass")

            for container in courseContainer:
                newCourse = {
                    "name": "",
                    "grade": "",
                    "assignments": []
                }
                parser = BeautifulSoup(
                    f"<html><body>{container}</body></html>", "lxml")
                headerContainer = parser.find_all(
                    "div", "sg-header sg-header-square")
                assignementsContainer = parser.find_all("div", "sg-content-grid")

                for hc in headerContainer:
                    parser = BeautifulSoup(f"<html><body>{hc}</body></html>", "lxml")
                
                    name = parser.find("a", "sg-header-heading").text
                    newCourse["name"] = name
                    grade_span = parser.find("span", "sg-header-heading sg-right").text.strip()
                    if "9 Weeks Grade " in grade_span:
                        grade_value = grade_span.replace("9 Weeks Grade ", "").strip()
                    else:
                        grade_value = grade_span
                
                    grade_value = grade_value.replace('%', '')
                
                    newCourse["grade"] = grade_value

                for ac in assignementsContainer:
                    parser = BeautifulSoup(
                        f"<html><body>{ac}</body></html>", "lxml")
                    rows = parser.find_all("tr", "sg-asp-table-data-row")
                    for assignmentContainer in rows:
                        try:
                            parser = BeautifulSoup(
                                f"<html><body>{assignmentContainer}</body></html>", "lxml")
                            tds = parser.find_all("td")
                            assignmentName = parser.find("a").text.strip()
                            assignmentDateDue = tds[0].text.strip()
                            assignmentDateAssigned = tds[1].text.strip()
                            assignmentCategory = tds[3].text.strip()
                            assignmentScore = tds[4].text.strip()
                            assignmentTotalPoints = tds[5].text.strip()

                            newCourse["assignments"].append(
                                {
                                    "name": assignmentName,
                                    "category": assignmentCategory,
                                    "dateAssigned": assignmentDateAssigned,
                                    "dateDue": assignmentDateDue,
                                    "score": assignmentScore,
                                    "totalPoints": assignmentTotalPoints
                                }
                            )
                        except:
                            pass

                courses.append(newCourse)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(courses).encode(encoding="utf_8"))

        except RequestException as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode(encoding="utf_8"))

        return
