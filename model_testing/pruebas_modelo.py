import module_request
import module_input
import pandas as pd
import numpy as np
import glob
import os
from fnmatch import fnmatch
import time
import math

import sys

#	sys.argv[0] ---- this field defines the environment ['local','develop','stage','production']

#postdata 	= {"delayed_payment": 0,"has_credit": 1,"credit_debt": 0,"is_delayed": 1,"employment_type": 2,"credit_type": 1,"income": 4000,"need": 2,"sub_need":2,"cancelled_credit": 0,"age": 24,"when_you_got_credit": 0,"product_entity":10}
#postdata 	= {"need": 3,"sub_need":22,"employment_type": 2,"employment_time":3,"age": 19,"income": 7000,"credit_debt": 2100,"has_credit": 2,"when_you_got_credit": 8,"credit_type": 2,"cancelled_credit": 0,"is_delayed": 1,"delayed_payment": 1,"product_entity":10,"credit_limit":100,"phone":4422220823}
#print "postdata: ",postdata, type(postdata)
#ids,status 	= module_request.model_request(postdata)
#print "resultados: ", ids
#import code; code.interact(local=locals())

#change data type of all list items to int
def ch_dtype_list(my_list, dtype=int):
    return map(dtype,my_list)


def evaluation(filename):
	"""
	I csv to list of jsons
	"""
	if sys.argv[1] in ['local','develop','stage','prod','lambda']:
		environment 				=	sys.argv[1]
		mode 						=	sys.argv[2]
		print 'environment: ',environment
		try:
			matrix_inputs_file 		=	filename
			temp_file				= "temp_file_input.csv"
			data					=	pd.DataFrame.from_csv(matrix_inputs_file,header=0)
			print "hey"
			data['Expected_result'].fillna(0.0,inplace=True)
			data['Expected_list'].fillna('[0]',inplace=True)

			print "most be 0: ",len(data[data['Expected_result'].isnull()])

			if mode  != '' and mode  == 'basic':
				print "executing basic analysis, initial len data:",len(data)
				data 				=	data[(data.Expected_result.notnull()) & (data.Expected_list.notnull())]
				data 				=	data[data['Expected_result'] != 0.0]
				print "final len data:",len(data)
			elif mode  != '' and mode  == 'sample':
				print "initial lenght:", len(data)
				data 				=	data.sample(frac=0.01,replace=False,random_state=1986)
				print "final lenght:",len(data)
			elif mode  != '' and mode  == 'sample_pos':
				#evaluate sample of positives cases
				print "initial lenght:", len(data)
				data 				=	data[data['Expected_result'] != 0.0]
				print "only positives:", len(data)
				data 				=	data.sample(frac=0.01,replace=False,random_state=1986)
				print "final lenght:",len(data)
				print "runnig mode sample of positives cases"
			else:
				print "runnig mode FULL"
			if ("credit_debt" in data.columns):
				data["credit_debt"]		=	data["credit_debt"].astype(int,raise_on_error=False)
			if ("credit_limit" in data.columns ):
				data["credit_limit"]	=	data["credit_limit"].astype(int,raise_on_error=False)
			if ("credit_type") in data.columns:
				credit_types 		= []
				nulls 				= data["credit_type"].isnull()
				for isnull,credit_type in zip(nulls,data["credit_type"]):
					if isnull 		== True:
						credit_types.append(" ")
					else:
						credit_types.append(int(credit_type))
				data["credit_type"]	= credit_types
			if ("product_entity" in data.columns):
				#unfortunately not working:
				try:
					entities 			= []
					nulls 				= data["product_entity"].isnull()
					for isnull,entity in zip(nulls,data["product_entity"]):
						if isnull == True:
							entities.append(" ")
						else:
							entities.append(int(entity))
					data["product_entity"]	= entities
				except:
					data["product_entity"]	=	data["product_entity"].astype(int,raise_on_error=False)
					

				#csv file to list of jsons, each row a json to make model request
				#data.to_csv(temp_file,columns=["need","sub_need","employment_type","employment_time","age","income","credit_debt","has_credit","when_you_got_credit","credit_type","cancelled_credit","is_delayed","delayed_payment","product_entity","credit_limit","phone"])
			data.to_csv(temp_file)
			inputs 					= module_input.csv_to_jsons(temp_file)
		except Exception,e:
			print "error en modulo I: ", str(e)
			import code; code.interact(local=locals())
		"""
		I modelo request
		"""
		try:
			print "1"
			#iterate over rows, now jsons
			results 		= 	[]
			bcc 			=	[]
			ids 			=	[]
			duplicata 		=	{}
			n 				=	0
			for item in inputs:
				#print "item: ",item
				n 			=	n+1
				print "index: ",n
				if math.fmod(n,200)==0.0:
					print "wait 1 minute"
					time.sleep(60)#delay in seconds
				#remove empty fields in dict
				for key in item:
					if not(item[key]=='' or str(item[key]).isspace() or len(str(item[key]))==0):
						duplicata[key]=item[key]
				#import code; code.interact(local=locals())
				print "duplicata: ",duplicata['Expected_result']
				ids,status 	= module_request.model_request(duplicata,environment)
				print "results: ",ids
				#import code; code.interact(local=locals())
				if status != 1:
					print "error en input:",item
				#import code; code.interact(local=locals())
				if len(ids)== 0:
					#"results" has the best_credit_card" for each scenario in "item"
					#if there is no best_credit card, save zero
					results.append([0])
					bcc.append(0)
				else:
					results.append(ids)
					bcc.append(ids[0])
		except Exception,e:
			print "error en modulo II", str(e)
			import code; code.interact(local=locals())
		"""
		II append real results to dataframe
		"""
		try:
			data["Results"] 		= 	results
			data["BCC"]				=	bcc
			#lists are read as srings, convert to lists
			list_b 					=	[]
			for my_list in data["Expected_list"]:
				list_b.append(ch_dtype_list(my_list.replace('[','').replace(']','').split('-')))
			data["Expected_list_b"] = list_b
			#import code; code.interact(local=locals())
		except Exception,e:
			print "error en modulo III", str(e)
			import code; code.interact(local=locals())
		"""
		III compare to expected result
		"""
		try:
			#Level 1: Best_credit_card == expected_result?
			data["Test_L1"] 		=	data["Expected_result"]-data["BCC"]
			
			#Level 2: List of suggested cards == expected list?
			#data["Test_L2"]			=	[set(set2).difference(set(set1)) for set1,set2 in zip(data["Expected_list_b"],data["Results"])]
			l 					=		[]
			for expected,real in zip(data["Expected_list_b"],data["Results"]):
				s1 				=	set(expected)
				s2 				=	set(ch_dtype_list(real))
				if len(expected)>len(real):
					l.append(list(s1.difference(s2)))
				else:
					l.append(list(s2.difference(s1)))
			#import code; code.interact(local=locals())
			data["Test_L2"]		= 		[str(lista).replace(',','-') for lista in l]
			#Level 3: Does the order matches?
			data["Test_L3"]			=	[(np.array(set1) - np.array(set2)) if len(set1)==len(set2) else "no match" for set1,set2 in zip(data["Expected_list_b"],data["Results"])]
			data["Test_L3"]			=	[str(item).replace(',','-') for item in data["Test_L3"]]
			#save to file
			try:
				#import code; code.interact(local=locals())
				path 	= "MATRIX_GENERATOR/TEST_MATRIX/"+filename.split('/')[2]+"/output/Data_output_"+filename.split('/')[3]+'_'+filename.split('/')[4]+'_'+filename.split('/')[5]+'_'+environment+'_'+mode
				print "saving to: ",path
				data.to_csv(path+".csv",sep=",")
				#import code; code.interact(local=locals())
			except:
				print "cannot save output"
				import code; code.interact(local=locals())

		except Exception,e:
			print "error en modulo III", str(e)
			import code; code.interact(local=locals())
		return
	else:
		print "unknown environment"
		print "envorinments: ['local','develop','stage','prod']"	
		return

"""
for filename in glob.iglob("MATRIX_GENERATOR/TEST_MATRIX/students/*.csv"):
	print "filename",filename
	#import code; code.interact(local=locals())
	evaluation(filename)
"""
"""
root = 'MATRIX_GENERATOR/TEST_MATRIX/students_work/'
pattern = "*.csv"

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
        	print "start evaluation at: ",time.strftime("%H:%M:%S")
        	print "filename: ",name
        	print os.path.join(path,name)
        	evaluation(name)


"""
evaluation('MATRIX_GENERATOR/TEST_MATRIX/employees/57/21/1/matrix_old.csv')

"""
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/38/2/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/39/2/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/40/2/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/41/2/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/35/43/2/matrix_old.csv')

evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/38/3/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/39/3/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/40/3/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/41/3/matrix_old.csv')
evaluation('MATRIX_GENERATOR/TEST_MATRIX/students_work/35/43/3/matrix_old.csv')
"""
print "end"
import code; code.interact(local=locals())
