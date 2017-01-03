def fields_generator(employment_type,has_credit):
	try:
		fields 		= ["employment_type","need","sub_need","income","phone","has_credit"]

		#Basic data
		if has_credit	==	2:
			fields.extend(["credit_debt","when_you_got_credit","credit_type","cancelled_credit","is_delayed","delayed_payment","product_entity","credit_limit"])
		elif has_credit	==	3:
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
		return fields