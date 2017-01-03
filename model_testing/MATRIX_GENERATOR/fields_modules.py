import numpy as np
import pandas as pd
import time 

def fields_generator(employment_type,has_credit):
	try:
		#print 'begin: ',time.strftime("%H:%M:%S")
		fields 			= ["employment_type","need","sub_need","income","phone","has_credit"]

		#Basic data
		if has_credit	!=	1:
			fields.extend(["credit_debt","when_you_got_credit","credit_type","cancelled_credit","is_delayed","delayed_payment","product_entity","credit_limit"])

		#Extra data
		if employment_type		==	1:
			fields.extend(["age","university"])
		elif employment_type	==	2:
			fields.extend(["age","university","employment_time"])
		elif employment_type 	 in [6,8]:
			fields.extend(["employment_time"])
		#elif employment_type 	==	5:
			#fields.extend()
		#elif employment_type 	==	7:
			#fields.extend()

	except Exception,e:
		print "error in collector: ",str(e)
		fields = []
	finally:
		#print 'end: ',time.strftime("%H:%M:%S")
		return fields

"""
			Parameters
"""
#mandatory fields
employment_type_options 		=	[1,2,5,6,7,8]
has_credit_options				=	[1,2,3]

#need_subneed_options			=	{"2":[2],"8":[22,24],"4":[33,34],"7":[21,25,26],"1":[27,28,29],"3":[30,31,32]}
phone_options					=	['5522208235']
#optional fields
age_pars						=	[18,25,6]
employment_time_options			=	[1,3,5,6,8,10,12]

#only if has_credit!=1:
credit_debt_ratio_pars			=	[0.2,1.0,0.2]
credit_exp_options				=	[2, 6, 12, 15]
credit_type_options				=	[1, 2, 3, 4]
is_delayed_options				=	[1, 2, 3]
delayed_payment_options			=	[1, 2, 3]
product_entity_options			=	[10,4,19,3,27,11,24,6,16,9,23,20,26,18,30,8,7,25,2,15,13,17,12,31,22,14,21,5]
credit_limit_pars				=	[0,15000,1500]

#only if has_credit==3
cancelled_credit_options		=	[1, 2]

#university_options	    		=

#arrays
age_array				=	np.arange(age_pars[0],age_pars[1],age_pars[2])
credit_type_options		=	[1, 2, 3, 4]
#product_entity_options	=	[10,4,19,3,27,11,24,6,16,9,23,20,26,18,30,8,7,25,2,15,13,17,12,31,22,14,21,5]
product_entity_options	=	[10,8]
credit_exp_options		=	[2, 6, 12, 15]
credit_debt_ratio_pars	=	[0.2,1.0,0.2]
credit_debt_ratio_array =	np.arange(credit_debt_ratio_pars[0],credit_debt_ratio_pars[1],credit_debt_ratio_pars[2])
credit_limit_pars		=	[0,10000,3000]
credit_limit_array		=	np.arange(credit_limit_pars[0],credit_limit_pars[1],credit_limit_pars[2])

def save_matrix(employment_type,has_credit,need_subneed_options):
	print "start:",time.strftime("%H:%M:%S"),"employment_type:",employment_type,"has_credit: ",has_credit
	
	#arrays
	income_pars						=	[3500,12000,2500]
	phone_options					=	['5522208235']

	age_pars						=	[18,25,6]
	employment_time_options			=	[1,6,12]

	#only if has_credit!=1:
	credit_debt_ratio_pars			=	[0.2,0.8,0.2]
	credit_exp_options				=	[6,12, 15]
	credit_type_options				=	[1, 2, 3, 4]
	is_delayed_options				=	[1, 2, 3]
	delayed_payment_options			=	[1, 2, 3]

	#only if has_credit==3
	cancelled_credit_options		=	[1, 2]

	#university_options	    		=

	income_array			=	np.arange(income_pars[0],income_pars[1],income_pars[2])
	#income_array			=	[4000,7000,7500,10000,15000,25000,40000,50000]
	#income_array			=	[2000.0,3000.0,4000.0,5000.0,7000.0,10000.0]
	
	age_array				=	np.arange(age_pars[0],age_pars[1],age_pars[2])
	print "age_array:",age_array
	#product_entity_options	=	[10,4,19,3,27,11,24,6,16,9,23,20,26,18,30,8,7,25,2,15,13,17,12,31,22,14,21,5]
	product_entity_options	=	[10,8]
	credit_debt_ratio_array =	np.arange(credit_debt_ratio_pars[0],credit_debt_ratio_pars[1],credit_debt_ratio_pars[2])
	#credit_limit_pars		=	[0,10000,3000]
	#credit_limit_array		=	np.arange(credit_limit_pars[0],credit_limit_pars[1],credit_limit_pars[2])
	credit_limit_array		=	[7000,7500,10000,15000]

	if has_credit == 2:
		l 		  = []
		for income in income_array:
			n = 0
			print "income:",income, n
			#time.sleep(5)
			for phone in phone_options:
				if employment_type in [2,6,8]:
					for employment_time in employment_time_options:
						for credit_type in credit_type_options:
							if credit_type == 1:
								for entity in product_entity_options:
									for credit_exp in credit_exp_options:
										for credit_limit in credit_limit_array:
											for credit_debt_ratio in credit_debt_ratio_array:
												for is_delayed in is_delayed_options:
													if is_delayed in [1,3]:
														if employment_type == 2:
															for age in age_array:
																n = n+1
																#print "n",n
																l.append({'income':income,'phone':phone,'age':age,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':0})
														else:
															l.append({'income':income,'phone':phone,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':0})
													else:
														if employment_type == 2:
															for age in age_array:
																n = n+1
																#print "n",n
																l.append({'income':income,'phone':phone,'age':age,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':1})
																l.append({'income':income,'phone':phone,'age':age,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':2})
																l.append({'income':income,'phone':phone,'age':age,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':3})
														else:
															l.append({'income':income,'phone':phone,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':1})
															l.append({'income':income,'phone':phone,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':2})
															l.append({'income':income,'phone':phone,
																		'employment_type':employment_type,'employment_time':employment_time,
																		'has_credit':has_credit,'credit_type':credit_type,
																		'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																		'when_you_got_credit':credit_exp,
																		'credit_limit':credit_limit,
																		'is_delayed':is_delayed,'delayed_payment':3})

							else:
								for credit_exp in credit_exp_options:
									for credit_debt_ratio in credit_debt_ratio_array:
										for is_delayed in is_delayed_options:
											if is_delayed in [1,3]:
												if employment_type == 2:
													for age in age_array:
														n = n+1
														#print "n",n
														l.append({'income':income,'phone':phone,'age':age,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,
																'is_delayed':is_delayed,'delayed_payment':0})
												else:
													l.append({'income':income,'phone':phone,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,
																'is_delayed':is_delayed,'delayed_payment':0})
											else:
												if employment_type == 2:
													for age in age_array:
														n = n+1
														#print "n",n
														l.append({'income':income,'phone':phone,'age':age,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,
																'is_delayed':is_delayed,'delayed_payment':1})
														l.append({'income':income,'phone':phone,'age':age,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,
																'is_delayed':is_delayed,'delayed_payment':2})
														l.append({'income':income,'phone':phone,'age':age,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,
																'is_delayed':is_delayed,'delayed_payment':3})
												else:
													l.append({'income':income,'phone':phone,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,
																'is_delayed':is_delayed,'delayed_payment':1})
													l.append({'income':income,'phone':phone,
															'employment_type':employment_type,'employment_time':employment_time,
															'has_credit':has_credit,'credit_type':credit_type,
															'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,
															'is_delayed':is_delayed,'delayed_payment':2})
													l.append({'income':income,'phone':phone,
															'employment_type':employment_type,'employment_time':employment_time,
															'has_credit':has_credit,'credit_type':credit_type,
															'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,
															'is_delayed':is_delayed,'delayed_payment':3})
				elif employment_type == 1:
					for age in age_array:
						for credit_type in credit_type_options:
							if credit_type == 1:
								for entity in product_entity_options:
									for credit_exp in credit_exp_options:
										for credit_limit in credit_limit_array:
											for credit_debt_ratio in credit_debt_ratio_array:
												for is_delayed in is_delayed_options:
													if is_delayed in [1,3]:
														l.append({'income':income,'phone':phone,'age':age,
															'employment_type':employment_type,
															'has_credit':has_credit,'credit_type':credit_type,
															'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,
															'credit_limit':credit_limit,
															'is_delayed':is_delayed,'delayed_payment':0})
													else:
														l.append({'income':income,'phone':phone,'age':age,
															'employment_type':employment_type,
															'has_credit':has_credit,'credit_type':credit_type,
															'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,
															'credit_limit':credit_limit,
															'is_delayed':is_delayed,'delayed_payment':1})
														l.append({'income':income,'phone':phone,'age':age,
															'employment_type':employment_type,
															'has_credit':has_credit,'credit_type':credit_type,
															'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,
															'credit_limit':credit_limit,
															'is_delayed':is_delayed,'delayed_payment':2})
														l.append({'income':income,'phone':phone,'age':age,
															'employment_type':employment_type,
															'has_credit':has_credit,'credit_type':credit_type,
															'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,
															'credit_limit':credit_limit,
															'is_delayed':is_delayed,'delayed_payment':3})

							else:
								for credit_exp in credit_exp_options:
									for credit_limit in credit_limit_array:
										for credit_debt_ratio in credit_debt_ratio_array:
											for is_delayed in is_delayed_options:
												if is_delayed in [1,3]:
													l.append({'income':income,'age':age,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':0})
												else:
													l.append({'income':income,'age':age,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':1})
													l.append({'income':income,'age':age,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':2})
													l.append({'income':income,'age':age,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':3})
				elif employment_type == 5:
					for credit_type in credit_type_options:
						if credit_type == 1:
							for entity in product_entity_options:
								for credit_exp in credit_exp_options:
									for credit_limit in credit_limit_array:
										for credit_debt_ratio in credit_debt_ratio_array:
											for is_delayed in is_delayed_options:
												if is_delayed in [1,3]:
													l.append({'income':income,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':0})
												else:
													l.append({'income':income,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':1})
													l.append({'income':income,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':2})
													l.append({'income':income,'phone':phone,
														'employment_type':employment_type,
														'has_credit':has_credit,'credit_type':credit_type,
														'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
														'when_you_got_credit':credit_exp,
														'credit_limit':credit_limit,
														'is_delayed':is_delayed,'delayed_payment':3})

						else:
							for credit_exp in credit_exp_options:
								for credit_limit in credit_limit_array:
									for credit_debt_ratio in credit_debt_ratio_array:
										for is_delayed in is_delayed_options:
											if is_delayed in [1,3]:
												l.append({'income':income,'phone':phone,
													'employment_type':employment_type,'employment_time':0,
													'has_credit':has_credit,'credit_type':credit_type,
													'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
													'when_you_got_credit':credit_exp,
													'credit_limit':credit_limit,
													'is_delayed':is_delayed,'delayed_payment':0})
											else:
												l.append({'income':income,'phone':phone,
													'employment_type':employment_type,'employment_time':0,
													'has_credit':has_credit,'credit_type':credit_type,
													'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
													'when_you_got_credit':credit_exp,
													'credit_limit':credit_limit,
													'is_delayed':is_delayed,'delayed_payment':1})
												l.append({'income':income,'phone':phone,
													'employment_type':employment_type,'employment_time':0,
													'has_credit':has_credit,'credit_type':credit_type,
													'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
													'when_you_got_credit':credit_exp,
													'credit_limit':credit_limit,
													'is_delayed':is_delayed,'delayed_payment':2})
												l.append({'income':income,'phone':phone,
													'employment_type':employment_type,'employment_time':0,
													'has_credit':has_credit,'credit_type':credit_type,
													'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
													'when_you_got_credit':credit_exp,
													'credit_limit':credit_limit,
													'is_delayed':is_delayed,'delayed_payment':3})

		for need in need_subneed_options.keys():
			for subneed in need_subneed_options[need]:
				data 					=	pd.DataFrame(l)
				data['need'] 			=	need
				data['sub_need']		=	subneed
				data['Expected_result']	=	np.nan
				data['Expected_list']	=	np.nan

				semipath			=	str(need)+'/'+str(subneed)+'/'+str(has_credit)+'/matrix'
				#import code; code.interact(local=locals())
				if employment_type == 1:
					data.to_csv('TEST_MATRIX/students/'+semipath+'.csv')
				elif employment_type == 2:
					data.to_csv('TEST_MATRIX/students_work/'+semipath+'.csv')
				elif employment_type == 5:
					data.to_csv('TEST_MATRIX/housewifes/'+semipath+'.csv')
				elif employment_type == 6:
					data.to_csv('TEST_MATRIX/employees/'+semipath+'.csv')
				elif employment_type == 7:
					data.to_csv('TEST_MATRIX/no_employees/'+semipath+'.csv')
				elif employment_type == 8:
					data.to_csv('TEST_MATRIX/freelancers/'+semipath+'.csv')
				else:
					print "unknown employment_type: ", employment_type
	elif has_credit == 3:
		l = []
		for income in income_array:
			for phone in phone_options:
				if employment_type in [2,6,8]:
					for employment_time in employment_time_options:
						for credit_type in credit_type_options:
							if credit_type == 1:
								for entity in product_entity_options:
									for credit_exp in credit_exp_options:
										for credit_limit in credit_limit_array:
											for credit_debt_ratio in credit_debt_ratio_array:
												for cancelled_credit in cancelled_credit_options:
													for is_delayed in is_delayed_options:
														if is_delayed in [1,3]:
															if employment_type == 2:
																for age in age_array:
																	l.append({'income':income,'phone':phone,'age':age,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,
																			'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																			'is_delayed':is_delayed,'delayed_payment':0})
															else:
																l.append({'income':income,'phone':phone,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,
																			'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																			'is_delayed':is_delayed,'delayed_payment':0})
														else:
															if employment_type == 2:
																for age in age_array:
																	l.append({'income':income,'phone':phone,'age':age,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,'cancelled_credit':cancelled_credit,
																			'credit_limit':credit_limit,
																			'is_delayed':is_delayed,'delayed_payment':1})
																	l.append({'income':income,'phone':phone,'age':age,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,'cancelled_credit':cancelled_credit,
																			'credit_limit':credit_limit,
																			'is_delayed':is_delayed,'delayed_payment':2})
																	l.append({'income':income,'phone':phone,'age':age,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,
																			'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																			'is_delayed':is_delayed,'delayed_payment':3})
															else:
																l.append({'income':income,'phone':phone,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,'cancelled_credit':cancelled_credit,
																			'credit_limit':credit_limit,
																			'is_delayed':is_delayed,'delayed_payment':1})
																l.append({'income':income,'phone':phone,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,'cancelled_credit':cancelled_credit,
																			'credit_limit':credit_limit,
																			'is_delayed':is_delayed,'delayed_payment':2})
																l.append({'income':income,'phone':phone,
																			'employment_type':employment_type,'employment_time':employment_time,
																			'has_credit':has_credit,'credit_type':credit_type,
																			'product_entity':entity,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																			'when_you_got_credit':credit_exp,
																			'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																			'is_delayed':is_delayed,'delayed_payment':3})
							else:
								for credit_exp in credit_exp_options:
									for credit_debt_ratio in credit_debt_ratio_array:
										for cancelled_credit in cancelled_credit_options:
											for is_delayed in is_delayed_options:
												if is_delayed in [1,3]:
													if employment_type == 2:
														for age in age_array:
															l.append({'income':income,'phone':phone,'age':age,
																'employment_type':employment_type,'employment_time':employment_time,
																'has_credit':has_credit,'credit_type':credit_type,
																'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																'when_you_got_credit':credit_exp,'cancelled_credit':cancelled_credit,
																'is_delayed':is_delayed,'delayed_payment':0})
													else:
														l.append({'income':income,'phone':phone,
															'employment_type':employment_type,'employment_time':employment_time,
															'has_credit':has_credit,'credit_type':credit_type,
															'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
															'when_you_got_credit':credit_exp,'cancelled_credit':cancelled_credit,
															'is_delayed':is_delayed,'delayed_payment':0})
												else:
													if employment_type == 2:
														for age in age_array:
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':employment_time,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'cancelled_credit':cancelled_credit,
																	'when_you_got_credit':credit_exp,
																	'is_delayed':is_delayed,'delayed_payment':1})
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':employment_time,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'cancelled_credit':cancelled_credit,
																	'when_you_got_credit':credit_exp,
																	'is_delayed':is_delayed,'delayed_payment':2})
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':employment_time,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'cancelled_credit':cancelled_credit,
																	'when_you_got_credit':credit_exp,
																	'is_delayed':is_delayed,'delayed_payment':3})
													else:
														l.append({'income':income,'phone':phone,
																	'employment_type':employment_type,'employment_time':employment_time,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'cancelled_credit':cancelled_credit,
																	'when_you_got_credit':credit_exp,
																	'is_delayed':is_delayed,'delayed_payment':1})
														l.append({'income':income,'phone':phone,
																	'employment_type':employment_type,'employment_time':employment_time,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'cancelled_credit':cancelled_credit,
																	'when_you_got_credit':credit_exp,
																	'is_delayed':is_delayed,'delayed_payment':2})
														l.append({'income':income,'phone':phone,
																	'employment_type':employment_type,'employment_time':employment_time,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'cancelled_credit':cancelled_credit,
																	'when_you_got_credit':credit_exp,
																	'is_delayed':is_delayed,'delayed_payment':3})
				else:
					for age in age_array:
						for credit_type in credit_type_options:
							if credit_type == 1:
								for entity in product_entity_options:
									for credit_exp in credit_exp_options:
										for credit_limit in credit_limit_array:
											for credit_debt_ratio in credit_debt_ratio_array:
												for cancelled_credit in cancelled_credit_options:
													for is_delayed in is_delayed_options:
														if is_delayed in [1,3]:
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':entity,'credit_debt':income*credit_debt_ratio,
																	'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':0})
														else:
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':entity,'credit_debt':income*credit_debt_ratio,
																	'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':1})
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':entity,'credit_debt':income*credit_debt_ratio,
																	'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':2})
															l.append({'income':income,'phone':phone,'age':age,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':entity,'credit_debt':income*credit_debt_ratio,
																	'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':3})

							else:
								for credit_exp in credit_exp_options:
										for credit_limit in credit_limit_array:
											for credit_debt_ratio in credit_debt_ratio_array:
												for cancelled_credit in cancelled_credit_options:
													for is_delayed in is_delayed_options:
														if is_delayed in [1,3]:
															l.append({'income':income,'age':age,'phone':phone,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':0})
														else:
															l.append({'income':income,'age':age,'phone':phone,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':1})
															l.append({'income':income,'age':age,'phone':phone,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':2})
															l.append({'income':income,'age':age,'phone':phone,
																	'employment_type':employment_type,'employment_time':0,
																	'has_credit':has_credit,'credit_type':credit_type,
																	'product_entity':0,'credit_debt':income*credit_debt_ratio,'credit_debt_ratio':credit_debt_ratio,
																	'when_you_got_credit':credit_exp,
																	'credit_limit':credit_limit,'cancelled_credit':cancelled_credit,
																	'is_delayed':is_delayed,'delayed_payment':3})

		for need in need_subneed_options.keys():
			for subneed in need_subneed_options[need]:
				data 					=	pd.DataFrame(l)
				data['need'] 			=	need
				data['sub_need']		=	subneed
				data['Expected_result']	=	np.nan
				data['Expected_list']	=	np.nan

				semipath			=	str(need)+'/'+str(subneed)+'/'+str(has_credit)+'/matrix'
				#import code; code.interact(local=locals())
				if employment_type == 1:
					data.to_csv('TEST_MATRIX/students/'+semipath+'.csv')
					#import code; code.interact(local=locals())
				elif employment_type == 2:
					data.to_csv('TEST_MATRIX/students_work/'+semipath+'.csv')
				elif employment_type == 5:
					data.to_csv('TEST_MATRIX/housewifes/'+semipath+'.csv')
				elif employment_type == 6:
					data.to_csv('TEST_MATRIX/employees/'+semipath+'.csv')
				elif employment_type == 7:
					data.to_csv('TEST_MATRIX/no_employees/'+semipath+'.csv')
				elif employment_type == 8:
					data.to_csv('TEST_MATRIX/freelancers/'+semipath+'.csv')
				else:
					print "unknown employment_type: ", employment_type
	elif has_credit==1:
		l = []
		for income in income_array:
			for phone in phone_options:
				if employment_type in [5,6,8]:
					for employment_time in employment_time_options:
						l.append({'income':income,
									'phone':phone,'employment_time':employment_time,
									'employment_type':employment_type,'has_credit':has_credit})
				else:
					for age in age_array:
						l.append({'income':income,'age':age,
								'phone':phone,'employment_type':employment_type,'employment_time':0,
								'has_credit':has_credit,})
		for need in need_subneed_options.keys():
			for subneed in need_subneed_options[need]:
				data 					=	pd.DataFrame(l)
				data['need'] 			=	need
				data['sub_need']		=	subneed
				data['Expected_result']	=	np.nan
				data['Expected_list']	=	np.nan
				semipath 	= str(need)+'/'+str(subneed)+'/'+str(has_credit)+'/matrix'
				#import code; code.interact(local=locals())
				if employment_type == 1:
					data.to_csv('TEST_MATRIX/students/'+semipath+'.csv')
				elif employment_type == 2:
					data.to_csv('TEST_MATRIX/students_work/'+semipath+'.csv')
				elif employment_type == 5:
					data.to_csv('TEST_MATRIX/housewifes/'+semipath+'.csv')
				elif employment_type == 6:
					data.to_csv('TEST_MATRIX/employees/'+semipath+'.csv')
				elif employment_type == 7:
					data.to_csv('TEST_MATRIX/no_employees/'+semipath+'.csv')
				elif employment_type == 8:
					data.to_csv('TEST_MATRIX/freelancers/'+semipath+'.csv')
				else:
					print "unknown employment_type: ", employment_type

	return
