from http.server import BaseHTTPRequestHandler
import requests
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):

        # Fetch the number of commits from the GitHub repository
        github_repo_url = "https://api.github.com/repos/wrownd/hacapi"
        response = requests.get(f"{github_repo_url}/commits")
        commits_count = len(response.json())


        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Get the current time as the loaded time
        loaded_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create the version number with the latest commit date
        version_number = f"1.0.{commits_count}"
        
        # Construct the response with HTML formatting and Calibri font
        response_text = f"""
<html>
<head>
<style>
body {{
    background-color: black;
    color: white;
    font-family: 'Calibri', sans-serif;
    font-weight: 400
}}
</style>
</head>
<body>
<h1 style="font-weight: 400">HACAPI<br><span style="font-size: 16; color: gray">by wrownd</span></h1>
<p style="color: gray;">Version {version_number}</p>
<p style="color: gray;">Loaded at: {loaded_time}</p>
</body>
</html>
"""
        self.wfile.write(response_text.encode(encoding="utf_8"))

        return