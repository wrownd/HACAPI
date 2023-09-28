from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
from urllib import parse
from requests.exceptions import RequestException  # Make sure to import RequestException
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

        try:
            # Use the getRequestSession function with the provided parameters
            session, school_name = getRequestSession(username, password, school_id)

            registrationPageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Assignments.aspx").text

            parser = BeautifulSoup(registrationPageContent, "lxml")

            courses = []

            courseContainer = parser.find_all("div", "AssignmentClass")

            for container in courseContainer:
                newCourse = {
                    "name": "",
                    "grade": "",
                    "lastUpdated": "",
                    "assignments": []
                }
                parser = BeautifulSoup(
                    f"<html><body>{container}</body></html>", "lxml")
                headerContainer = parser.find_all(
                    "div", "sg-header sg-header-square")
                assignementsContainer = parser.find_all("div", "sg-content-grid")

                for hc in headerContainer:
                    parser = BeautifulSoup(
                        f"<html><body>{hc}</body></html>", "lxml")

                    newCourse["name"] = parser.find(
                        "a", "sg-header-heading").text.strip()

                    newCourse["lastUpdated"] = parser.find(
                        "span", "sg-header-sub-heading").text.strip().replace("(Last Updated: ", "").replace(")", "")

                    newCourse["grade"] = parser.find("span", "sg-header-heading sg-right").text.strip().replace("Student Grades ", "").replace("%", "")

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
            self.wfile.write(json.dumps({
                "currentClasses": courses,
            }).encode(encoding="utf_8"))

        except RequestException as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode(encoding="utf_8"))

        return
