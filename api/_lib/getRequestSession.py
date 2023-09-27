import requests
from bs4 import BeautifulSoup
import json
import os

data = {
    "10": "Academics Plus Charter",
    "20": "Alma School District",
    "30": "Alpena School District",
    "40": "Ar School For The Blind School District",
    "50": "Arch Ford Education Service Cooperative",
    "60": "Arkadelphia School District",
    "70": "Arkansas Arts Academy",
    "80": "Arkansas Connections Academy",
    "90": "Arkansas Lighthouse Charter Schools",
    "100": "Arkansas Military & First Responders Academy",
    "110": "Arkansas River Education Service Cooperative",
    "120": "Arkansas School for the Deaf",
    "130": "Arkansas Virtual Academy",
    "140": "Armorel School District",
    "150": "Ashdown School District",
    "160": "Atkins School District",
    "170": "Augusta School District",
    "180": "Bald Knob School District",
    "190": "Barton-Lexa School District",
    "200": "Batesville School District",
    "210": "Bauxite School District",
    "220": "Bay School District",
    "230": "Bearden School District",
    "240": "Beebe School District",
    "250": "Benton School District",
    "260": "Bentonville School District",
    "270": "Bergman School District",
    "280": "Berryville School District",
    "290": "Bismarck School District",
    "300": "Blevins School District",
    "310": "Blytheville School District",
    "320": "Booneville School District",
    "330": "Bradford School District",
    "340": "Brinkley School District",
    "350": "Brookland School District",
    "360": "Bryant School District",
    "370": "Buffalo Island Central School District",
    "380": "Cabot School District",
    "390": "Caddo Hills School District",
    "400": "Calico Rock School District",
    "410": "Camden Fairview School District",
    "420": "Carlisle School District",
    "430": "Cave City School District",
    "440": "Cedar Ridge School District",
    "450": "Cedarville School District",
    "460": "Centerpoint School District",
    "470": "Charleston School District",
    "480": "Clarendon School District",
    "490": "Clarksville School District",
    "500": "Cleveland County School District",
    "510": "Clinton School District",
    "520": "Concord School District",
    "530": "Conway School District",
    "540": "Corning School District",
    "550": "Cossatot River School District",
    "560": "Cotter School District",
    "570": "County Line School District",
    "580": "Cross County School District",
    "590": "Crossett School District",
    "600": "Crowley's Ridge Education Service Cooperative",
    "610": "Cutter Morning Star School District",
    "620": "Danville School District",
    "630": "Dardanelle School District",
    "640": "Dawson Education Service Cooperative",
    "650": "Decatur School District",
    "660": "Deer-Mount Judea School District",
    "670": "DeQueen School District",
    "680": "Dequeen-Mena Education Service Cooperative",
    "690": "Dermott School District",
    "700": "Des Arc School District",
    "710": "Dewitt School District",
    "720": "Dierks School District",
    "730": "Division of Youth Services",
    "740": "Dover School District",
    "750": "Drew Central School District",
    "760": "Dumas School District",
    "770": "Earle School District",
    "780": "East End School District",
    "790": "East Poinsett County School District",
    "800": "El Dorado School District",
    "810": "Elkins School District",
    "820": "Emerson-Taylor-Bradley School District",
    "830": "England School District",
    "840": "eSTEM Public Charter School",
    "850": "Eureka Springs School District",
    "860": "Exalt Academy of Southwest Little Rock",
    "870": "Farmington School District",
    "880": "Fayetteville School District",
    "890": "Flippin School District",
    "900": "Fordyce School District",
    "910": "Foreman School District",
    "920": "Forrest City School District",
    "930": "Fort Smith School District",
    "940": "Fouke School District",
    "950": "Founders Classical Academies of Arkansas",
    "960": "Fountain Lake School District",
    "970": "Friendship Aspire Academies Arkansas",
    "980": "Future School of Fort Smith",
    "990": "Genoa Central School District",
    "1000": "Gentry School District",
    "1010": "Glen Rose School District",
    "1020": "Gosnell School District",
    "1030": "Graduate Arkansas",
    "1040": "Gravette School District",
    "1050": "Great Rivers Education Service Cooperative",
    "1060": "Green Forest School District",
    "1070": "Greenbrier School District",
    "1080": "Greene County Tech School District",
    "1090": "Greenland School District",
    "1100": "Greenwood School District",
    "1110": "Gurdon School District",
    "1120": "Guy Fenter Education Service Cooperative",
    "1130": "Guy-Perkins School District",
    "1140": "Haas Hall Academy",
    "1150": "Hackett School District",
    "1160": "Hamburg School District",
    "1170": "Hampton School District",
    "1180": "Harmony Grove (Ouachita County) School District",
    "1190": "Harmony Grove (Saline County) School District",
    "1200": "Harrisburg School District",
    "1210": "Harrison School District",
    "1220": "Hazen School District",
    "1230": "Heber Springs School District",
    "1240": "Hector School District",
    "1250": "Helena-West Helena School District",
    "1260": "Hermitage School District",
    "1270": "Highland School District",
    "1280": "Hillcrest School District",
    "1290": "Hope Academy of Northwest Arkansas",
    "1300": "Hope School District",
    "1310": "Horatio School District",
    "1320": "Hot Springs School District",
    "1330": "Hoxie School District",
    "1340": "Huntsville School District",
    "1350": "Imboden Area Charter School",
    "1360": "Izard County Consolidated School District",
    "1370": "Jackson County School District",
    "1380": "Jacksonville-North Pulaski School District",
    "1390": "Jasper School District",
    "1400": "Jessieville School District",
    "1410": "Jonesboro School District",
    "1420": "Junction City School District",
    "1430": "Kipp: Delta Public Schools",
    "1440": "Kirby School District",
    "1450": "Lafayette County School District",
    "1460": "Lake Hamilton School District",
    "1470": "Lakeside (Chicot County) School District",
    "1480": "Lakeside (Garland County) School District",
    "1490": "Lamar School District",
    "1500": "Lavaca School District",
    "1510": "Lawrence County School District",
    "1520": "Lead Hill School District",
    "1530": "Lee County School District",
    "1540": "Lincoln Consolidated School District",
    "1550": "LISA Academy",
    "1560": "Little Rock School District",
    "1570": "Lonoke School District",
    "1580": "Magazine School District",
    "1590": "Magnet Cove School District",
    "1600": "Magnolia School District",
    "1610": "Malvern School District",
    "1620": "Mammoth Spring School District",
    "1630": "Manila School District",
    "1640": "Mansfield School District",
    "1650": "Marion School District",
    "1660": "Marked Tree School District",
    "1670": "Marmaduke School District",
    "1680": "Marvell-Elaine School District",
    "1690": "Mayflower School District",
    "1700": "Maynard School District",
    "1710": "McCrory School District",
    "1720": "McGehee School District",
    "1730": "Melbourne School District",
    "1740": "Mena School District",
    "1750": "Midland School District",
    "1760": "Mineral Springs School District",
    "1770": "Monticello School District",
    "1780": "Mount Ida School District",
    "1790": "Mountain Home School District",
    "1800": "Mountain Pine School District",
    "1810": "Mountain View School District",
    "1820": "Mountainburg School District",
    "1830": "Mt. Vernon/Enola School District",
    "1840": "Mulberry-Pleasant View Bi-County School District",
    "1850": "Nashville School District",
    "1860": "Nemo Vista School District",
    "1870": "Nettleton School District",
    "1880": "Nevada School District",
    "1890": "Newport School District",
    "1900": "Norfork School District",
    "1910": "North Little Rock School District",
    "1920": "Northcentral Arkansas Education Service Coop",
    "1930": "Northeast Arkansas Education Cooperative",
    "1940": "Northwest Arkansas Education Service Cooperative",
    "1950": "Omaha School District",
    "1960": "Osceola School District",
    "1970": "Ouachita River School District",
    "1980": "Ouachita School District",
    "1990": "Ozark Mountain School District",
    "2000": "Ozark School District",
    "2010": "Ozarks Unlimited Resource Service Cooperative",
    "2020": "Palestine-Wheatley School District",
    "2030": "Pangburn School District",
    "2040": "Paragould School District",
    "2050": "Paris School District",
    "2060": "Parkers Chapel School District",
    "2070": "Pea Ridge School District",
    "2080": "Perryville School District",
    "2090": "Piggott School District",
    "2100": "Pine Bluff School District",
    "2110": "Pocahontas School District",
    "2120": "Pottsville School District",
    "2130": "Poyen School District",
    "2140": "Prairie Grove School District",
    "2150": "Premier High School of North Little Rock",
    "2160": "Premier High Schools of Arkansas",
    "2170": "Prescott School District",
    "2180": "Pulaski County Special SD",
    "2190": "Quitman School District",
    "2200": "Rector School District",
    "2210": "Responsive Ed Solutions Premier High School of Springdale",
    "2220": "Rivercrest School District 57",
    "2230": "Riverside School District",
    "2240": "Riverview School District",
    "2250": "Rogers School District",
    "2260": "Rose Bud School District",
    "2270": "Russellville School District",
    "2280": "Salem School District",
    "2290": "ScholarMade Achievement Place of Arkansas",
    "2300": "Scranton School District",
    "2310": "Searcy County School District",
    "2320": "Searcy School District",
    "2330": "Sheridan School District",
    "2340": "Shirley School District",
    "2350": "Siloam Springs School District",
    "2360": "Sloan-Hendrix School District",
    "2370": "Smackover-Norphlet School District",
    "2380": "So. Conway County School District",
    "2390": "South Central Education Service Cooperative",
    "2400": "South Pike County School District",
    "2410": "South Side(Bee Branch) School District",
    "2420": "Southeast Arkansas Community Based Education Ctr",
    "2430": "Southeast Arkansas Education Service Cooperative",
    "2440": "Southside School District",
    "2450": "Southwest Arkansas Education Cooperative",
    "2460": "Spring Hill School District",
    "2470": "Springdale School District",
    "2480": "Star City School District",
    "2490": "Strong-Huttig School District",
    "2500": "Stuttgart School District",
    "2510": "Success School District",
    "2520": "Texarkana School District",
    "2530": "The Excel Center",
    "2540": "Trumann School District",
    "2550": "Two Rivers School District",
    "2560": "Valley Springs School District",
    "2570": "Valley View School District",
    "2580": "Van Buren School District",
    "2590": "Vilonia School District",
    "2600": "Viola School District",
    "2610": "Waldron School District",
    "2620": "Warren School District",
    "2630": "Watson Chapel School District",
    "2640": "West Fork School District",
    "2650": "West Memphis School District",
    "2660": "West Side (Cleburne County) School District",
    "2670": "Western Yell County School District",
    "2680": "Westside Consolidated School District",
    "2690": "Westside(Johnson County) School District",
    "2700": "Westwind School for Performing Arts",
    "2710": "White County Central School District",
    "2720": "White Hall School District",
    "2730": "Wilbur D. Mills Education Service Cooperative",
    "2740": "Wonderview School District",
    "2750": "Woodlawn School District",
    "2760": "Wynne School District",
    "2770": "Yellville-Summit School District"
}

def get_school_name(school_id):
    try:
        school_name = data[school_id]
        return school_name
    except KeyError:
        return "School not found"

def getRequestSession(username, password, school_id):
    try:
        requestSession, school_name = None, None  # Initialize to None
        
        # Get the school name based on the school_id
        school_name = get_school_name(school_id)
        
        # Check if school_name is None
        if school_name is None:
            raise ValueError("Invalid school ID")

        # Create a requests session
        requestSession = requests.session()

        # Make the HTTP GET request to the login page
        loginScreenResponse = requestSession.get("https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f")

        # Check the HTTP status code
        loginScreenResponse.raise_for_status()

        # Access the response text after verifying the status code
        loginScreenResponseText = loginScreenResponse.text
        # Parse the HTML content
        parser = BeautifulSoup(loginScreenResponseText, 'html.parser')
        
        # Find the input element with the name '__RequestVerificationToken'
        requestVerificationTokenElement = parser.find('input', {'name': '__RequestVerificationToken'})
        
        if requestVerificationTokenElement is not None:
            requestVerificationToken = requestVerificationTokenElement['value']
        else:
            raise ValueError("RequestVerificationToken not found")

        requestHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'hac23.esp.k12.ar.us',
            'Origin': 'https://hac23.esp.k12.ar.us',
            'Referer': "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f",
            '__RequestVerificationToken': requestVerificationToken
        }

        requestPayload = {
            "__RequestVerificationToken": requestVerificationToken,
            "SCKTY00328510CustomEnabled": "False",
            "SCKTY00436568CustomEnabled": "False",
            "Database": school_id,
            "VerificationOption": "UsernamePassword",
            "LogOnDetails.UserName": username,
            "tempUN": "",
            "tempPW": "",
            "LogOnDetails.Password": password
        }

        # Make the POST request to log in
        pageDOM = requestSession.post(
            "https://hac23.esp.k12.ar.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f",
            data=requestPayload,
            headers=requestHeaders
        )

        # Check if the login was successful by inspecting the resulting pageDOM

        # You might want to add some conditions to check if the login was successful.
        # For example, check for specific elements in pageDOM that indicate a successful login.
        # If login failed, raise an exception or return an error message accordingly.

        return requestSession, school_name

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None, None

    except requests.exceptions.RequestException as re:
        print(f"RequestException: {re}")
        return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
