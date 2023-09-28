import json
from urllib import parse
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from api._lib.getRequestSession import getRequestSession

def handler(event, context):
    # Extract the parameters from the event
    query_string = event.get('queryStringParameters', '')
    username = query_string.get("username", "")
    password = query_string.get("password", "")
    school_id = query_string.get("sd", "380")

    # Check if any of the required parameters is missing
    if not username or not password:
        response_data = {"error": "Missing username or password"}
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(response_data),
        }

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
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(response_data),
        }

    except RequestException as e:
        # Handle requests-related exceptions
        error_response = {
            "error": "Internal Server Error",
            "message": str(e),  # Include the exception message for debugging
        }
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(error_response),
        }

    except Exception as e:
        # Handle other exceptions
        error_response = {
            "error": "Internal Server Error",
            "message": str(e),  # Include the exception message for debugging
        }
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(error_response),
        }
