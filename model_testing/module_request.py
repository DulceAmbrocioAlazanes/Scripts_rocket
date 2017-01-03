import json
import urllib2
import requests	

def order_cards(messy_id_set):
	try:
		orders 				=	[]
		ids 				=	[]
		for item in messy_id_set["credit_cards"]:
			orders.append(int(item["order"]))
			ids.append(int(item["id"]))

		processed 			= 	[]
		organized_ids		=	[]
		for i in ids:
			minimum			=	min(set(orders).difference(set(processed)))
			#print "minimum: ",minimum
			organized_ids.append(ids[orders.index(minimum)])
			processed.append(minimum)
		#import code; code.interact(local=locals())
	except Exception,e:
		print "error: ",str(e)
		import code; code.interact(local=locals())
	return organized_ids

def select_environment(environment):
	if environment == 'local':
		url 		= 	'http://localhost:8000/api/v1.0/benefits_results/predict_test/'
	elif environment == 'develop':
		url 		=	'https://model-delta.rocket.la/api/v1.0/benefits_results/predict_test/'
	elif environment == 'stage':
		url 		=	'https://model-omega.rocket.la/api/v1.0/benefits_results/predict_test/'
	elif environment == 'prod':
		url 		=	'https://model.rocket.la/api/v1.0/benefits_results/predict_test/'
	elif environment == 'lambda':
		url 		=	'https://h7bvrcelud.execute-api.us-east-1.amazonaws.com/prod/'
	else:
		url 		=	'https://model.rocket.la/api/v1.0/benefits_results/predict_test/'
	return url


def model_request(user_data,environment):
	try :
		credit_card_ids	= 	[]
		status			= 	1
		url 			=	select_environment(environment)
		if environment != 	"lambda":
			r 			= 	requests.post(url,user_data)
		else:
			r 			=	requests.post(url,json.dumps(user_data))
		data 			= 	json.loads(r.content)
		credit_card_ids	= 	[]
		if "credit_cards" in data:
			try:
				#for item in data["credit_cards"]:
					#credit_card_ids.append(item["id"])
				credit_card_ids	= order_cards(data)
				status 			= 	1
			except Exception,e:
				print "error: ",str(e)
				status 			= 	2
	except Exception, e:
	    print "HTTP Post error:", str(e)
	    #import code; code.interact(local=locals())
	    status 			= 	2
	    credit_card_ids	= [-1]
	finally:
		return credit_card_ids,status

