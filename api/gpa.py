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

            transcriptPageContent = session.get("https://hac23.esp.k12.ar.us/HomeAccess/Content/Student/Transcript.aspx").text

            parser = BeautifulSoup(transcriptPageContent, "html.parser")

            weighted_gpa = parser.find(
                id="plnMain_rpTranscriptGroup_lblGPACum1").text
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response_json = json.dumps(weighted_gpa).encode(encoding="utf_8")
            self.wfile.write(response_json)

        except RequestException as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except ValueError as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        except Exception as e:
            self.send_error_response(f"An error occurred: {str(e)}")

        return