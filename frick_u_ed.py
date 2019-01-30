import http.client, urllib

car_on = True
temp = 30
while car_on == True:
	if temp >= 30:
		conn = http.client.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
  			urllib.parse.urlencode({
    			"token": "APP_TOKEN",
    			"user": "USER_KEY",
    			"message": "Your baby died",
  			}), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()