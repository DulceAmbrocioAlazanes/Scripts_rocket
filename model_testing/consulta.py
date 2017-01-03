import json
import urllib2
import requests

try :
    url 		= 'http://rocketmodelmx.us-east-1.elasticbeanstalk.com/api/v1.0/benefits_results/predict_test/'
    postdata 	= {"delayed_payment": 0,"has_credit": 1,"credit_debt": 0,"is_delayed": 1,"employment_type": 6,"credit_type": 1,"income": 4000,"need": 8,"sub_need":22,"cancelled_credit": 0,"age": 24,"when_you_got_credit": 0}
    r 			= requests.post(url,postdata)
    print "leggo"
    data 		= json.loads(r.content)
    print json.loads(r.content)

    if "credit_cards" in data:
    	print "si"
    	for item in data["credit_cards"]:
    		print "cosa: ",item["name"],item["id"]
except:
    print "HTTP Post error:"