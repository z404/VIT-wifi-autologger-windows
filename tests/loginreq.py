import requests
from requests.structures import CaseInsensitiveDict

url = "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://www.msftconnecttest.com/redirect"

headers = CaseInsensitiveDict()
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9"
headers["Accept-Language"] = "en-US,en;q=0.9"
headers["Cache-Control"] = "max-age=0"
headers["Connection"] = "keep-alive"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Origin"] = "http://phc.prontonetworks.com"
headers["Referer"] = "http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://google.com/"
headers["Sec-GPC"] = "1"
headers["Upgrade-Insecure-Requests"] = "1"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

data = "userId=20BDS0128&password=R8DBQY&serviceName=ProntoAuthentication&Submit22=Login"


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)