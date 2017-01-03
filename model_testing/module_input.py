import csv
#import json

"""
def csv_to_jsons(file_inputs):
	csvfile = open(file_inputs, 'r')

	fieldnames = ("index","need","sub_need","employment_type","employment_time","age","income","credit_debt","has_credit","when_you_got_credit","credit_type","cancelled_credit","is_delayed","delayed_payment","Expected_result")
	reader = csv.DictReader( csvfile, fieldnames)

	inputs = []
	for row in reader:
	    inputs.append(json.dumps(row))
	csvfile.close()
	return inputs
"""
def csv_to_jsons(file_inputs):
	with open(file_inputs) as csvfile:
	    reader = csv.DictReader(csvfile)
	    inputs = [row for row in reader]
	return inputs