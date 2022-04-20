import json
import os
import requests
import datetime

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("sessionInfo")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    print("debug log")
    print(city)
    dateReq = parameters.get("date")
    print(dateReq)
    dateReq = datetime.date(int(dateReq.get("year")),int(dateReq.get("month")),int(dateReq.get("day")));
    print(dateReq)
    print("debug log")
    if city is None:
        return None
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=3f0387334624d977b626208dde397bcd')
    json_object = r.json()
    weather=json_object['list']
    condition= "?"
    for i in range(len(weather)):
        if dateReq in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']
            print(condition)
            break
    if condition == "?" and len(weather) != 0:
        condition = weather[0]['weather'][0]['description']
    speech = "The forecast for "+city+ " for "+date+" is "+condition
    print(speech)
    return {
    "text": speech
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
