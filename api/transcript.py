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

            schedulePageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Transcript.aspx").text

            parser = BeautifulSoup(schedulePageContent, "html.parser")

            transcriptGroup = parser.find_all("td", class_="sg-transcript-group")

            transcriptDetails = []

            for index, transcript in enumerate(transcriptGroup):
                print(f"Processing transcript at index {index}")
                # No need to wrap transcript in additional HTML body
                innerTables = transcript.find_all('table')

                # Ensure there are enough inner tables
                if len(innerTables) >= 3:
                    headerTable = innerTables[0]
                    coursesTable = innerTables[1]
                    totalCreditsTable = innerTables[2]

                    # Extract details from header table
                    yearsAttended = headerTable.find('span', id=f'plnMain_rpTranscriptGroup_lblYearValue_{index}').text.strip()
                    gradeLevel = headerTable.find('span', id=f'plnMain_rpTranscriptGroup_lblGradeValue_{index}').text.strip()
                    building = headerTable.find('span', id=f'plnMain_rpTranscriptGroup_lblBuildingValue_{index}').text.strip()

                    # Extract course details from courses table
                    courseRows = coursesTable.find_all('tr', class_='sg-asp-table-data-row')
                else:
                    print(f"Skipping transcript at index {index} due to insufficient inner tables.")
                    courseRows = []  # Initialize as an empty list when there are insufficient inner tables

                courseDetails = []

                for courseRow in courseRows:
                    courseInfo = courseRow.find_all('td')

                    courseCode = courseInfo[0].text.strip()
                    courseName = courseInfo[1].text.strip()
                    sem1Grade = courseInfo[2].text.strip()
                    sem2Grade = courseInfo[3].text.strip()
                    courseCredits = courseInfo[4].text.strip()

                    courseDetails.append({'courseCode': courseCode, 'courseName': courseName, 'sem1Grade': sem1Grade, 'sem2Grade': sem2Grade, 'courseCredits': courseCredits})

                # Extract total credits from totalCreditsTable
                totalCredits = totalCreditsTable.find('label', id=f'plnMain_rpTranscriptGroup_LblTCreditValue_{index}').text

                transcriptDetails.append({'yearsAttended': yearsAttended, 'gradeLevel': gradeLevel, 'building': building, 'totalCredits': totalCredits, 'courses': courseDetails})

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(transcriptDetails).encode(encoding="utf_8"))

        except RequestException as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except ValueError as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except Exception as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        return