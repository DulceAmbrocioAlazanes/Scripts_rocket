#!/usr/bin/python

import sys
import fields_modules
import time

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)


#	sys.argv[0] ---- this field defines the mode ['custom','full']
#	sys.argv[1]	---- if custom, define employment type in [1,2,5,6,7,8]
#	sys.argv[2]	---- if custom, define has credit in [1,2,3]

print '1st argument:  mode ["custom","full"]' 
print '2nd argument: if custom, define employment type in [1,2,5,6,7,8]'
print '3rd argument: if custom, define has credit in [1,2,3]'



"""
			Generator
"""
try:
	need_subneed_options						=	{"57":[21,58,59,60,61,62],"63":[1,29,6,64]}
	#need_subneed_options						=	{"2":[37,38,39,40,41],"35":[42,43],"44":[45,46,47,48,49],"8":[50,51,52,53,54,55,56],"57":[21,58,59,60,61,62],"63":[29,1,6,64,65]}
	if sys.argv[1] in ['custom','full']:
		if sys.argv[1] 	== 'full':
			#Generate full map of profiles
			#for employment_type in [1,2,5,6,7,8]:
			for employment_type in [6,7,8]:
				print "employment_type: ",employment_type, 'time: ',time.strftime("%H:%M:%S")
				for has_credit in [1,2,3]:
					#I 	Define fields to iterate
					#empty_fields		=	fields_modules.fields_generator(employment_type,has_credit)
					#II Fill each field acording to parameters definitions
					#fields_modules.fill_fields(employment_type,has_credit,empty_fields)
					#import code; code.interact(local=locals())
					fields_modules.save_matrix(employment_type,has_credit,need_subneed_options)
		else:
			print "no custom module yet"

	else:
		print "verify parametrers"
except Exception,e:
	print "error in generator: ",str(e)