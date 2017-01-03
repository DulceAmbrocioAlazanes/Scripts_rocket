# -*- coding: utf-8 -*-
import pandas as pd
import curp
import load_data
import time
import functions
from datetime import datetime
import subprocess
import math
import numpy as np

try:
	#load santander data 
	santander									= 		pd.read_csv('Santander_special_02_01_2017.csv',encoding='utf-8')
	#load internal
	#internal 									=		load_data.load_dbRocket()
	internal									=		load_data.load_dbRocket_V4(False)
	print "len(internal):",len(internal)
	#---------lower
	internal['base_rocket_Correo electronico']	=		internal['base_rocket_Correo electronico'].fillna('N/A')
	internal['base_rocket_Correo electronico']	=		internal['base_rocket_Correo electronico'].map(lambda x: x.lower())
	
	#---------remove ola ke ase
	if 'base_rocket_Para que la quieres' in internal.columns:
		internal['base_rocket_Para que la quieres']	=		['N/A' if item == 'ola ke ase' else item for item in internal['base_rocket_Para que la quieres']]
		internal['base_rocket_Para que la quieres']	=		['N/A' if item == 'Pregunta Descontinuada' else item for item in internal['base_rocket_Para que la quieres']]
	
	#---------subset by time
	internal['date']							=		pd.to_datetime(internal['base_rocket_Hora de finalizacion del formulario'])
	#date_min									= 		datetime.strptime('Nov 15 2013  12:00AM', '%b %d %Y %I:%M%p')
	#date_max									= 		datetime.strptime('Nov 30 2016  12:00AM', '%b %d %Y %I:%M%p')
	#internal 									=		internal[(internal['date']>date_min)&(internal['date']<date_max)]
	#print len(internal)
	
	#---------remove ids duplicated
	#print "len(internal) before duplicates: ",len(internal)
	#internal									=		functions.clean_dataframe_last_update(internal,'date','base_rocket_ID')
	#print "len(internal) after remove duplicates: ",len(internal)
	#import code; code.interact(local=locals())
	
	#load products information
	products 									=		load_data.load_products_info()
	#load universities
	universities								=		load_data.load_universities()

	#subprocess.call(['speech-dispatcher'])        #start speech dispatcher
	#subprocess.call(['spd-say', 'data loaded'])
	


	"""
				RFCs uniques in Santander report
	"""

	#RFCs

	RfCs_uniques 								=	list(santander['santander_seg_RFC'].unique())

	santander['santander_sel_Fecha Captura'] 	=	pd.to_datetime(santander['santander_sel_Fecha Captura'])
	santander['Fecha_ultima_modif']				=	pd.to_datetime(santander['Fecha_ultima_modif'])
	santander['santander_seg_CodigoCliente']	=	santander['santander_seg_CodigoCliente'].fillna('N/A')
	
	print "inicio len(santander): ",len(santander)
	#segmento de usuarios con mismo ID en la utm pero diferente identidad
	segmento_para_tratar_por_separado			=	pd.DataFrame()
	for i in santander['ID'].unique():
		correos									=	list(santander[santander['ID']==i]['santander_sel_Correo_SEL'].unique())
		if len(correos)>1:
			segmento_para_tratar_por_separado	=	segmento_para_tratar_por_separado.append(santander[santander['ID']==i])
	
	ids_para_tratar_por_separado				=	segmento_para_tratar_por_separado['ID'].unique()
	santander									=	santander[~santander['ID'].isin(ids_para_tratar_por_separado)]
	
	print "sin ids para tratar por separado len(santander): ",len(santander)	
	#santander_rfcs_uniques 					=	pd.DataFrame()
	#for unique_rfc in RfCs_uniques:
		#more_recent							=	max(santander[santander['santander_seg_RFC']==unique_rfc]['Fecha_ultima_modif'])
		#santander_rfcs_uniques					=	santander_rfcs_uniques.append(santander[(santander['santander_seg_RFC']==unique_rfc)&(santander['Fecha_ultima_modif']==more_recent)][0:1])
	#rfcs unicos
	
	santander_rfcs_uniques						=	functions.clean_dataframe_last_update(santander,'Fecha_ultima_modif','santander_seg_RFC')
	santander_rfcs_uniques['ID']				=	santander_rfcs_uniques['ID'].fillna("N/A")
	print "santander_rfcs_uniques['ID'].unique():",len(santander_rfcs_uniques['ID'].unique())
	
	
	#ids unicos (ids and phones as ids)
	#santander_rfcs_uniques_with_id				=	santander_rfcs_uniques[santander_rfcs_uniques['ID']!='N/A']
	#santander_rfcs_uniques_with_id				=	functions.clean_dataframe_last_update(santander_rfcs_uniques_with_id,'Fecha_ultima_modif','ID')
	
	#santander_rfcs_uniques_no_id				=	santander_rfcs_uniques[santander_rfcs_uniques['ID']=='N/A']
	#santander_rfcs_uniques						=	santander_rfcs_uniques_with_id.append(santander_rfcs_uniques_no_id)
	
	
	#telefonos unicos
	santander_rfcs_uniques['santander_base_Telefono celular']	=	santander_rfcs_uniques['santander_base_Telefono celular'].fillna('N/A')
	santander_rfcs_uniques_with_phone			=	santander_rfcs_uniques[santander_rfcs_uniques['santander_base_Telefono celular']!='N/A']
	santander_rfcs_uniques_with_phone			=	functions.clean_dataframe_last_update(santander_rfcs_uniques_with_phone,'Fecha_ultima_modif','santander_base_Telefono celular')
	santander_rfcs_uniques_no_phone				=	santander_rfcs_uniques[santander_rfcs_uniques['santander_base_Telefono celular']=='N/A']
	santander_rfcs_uniques						=	santander_rfcs_uniques_with_phone.append(santander_rfcs_uniques_no_phone)
	
	#emails unicos
	santander_rfcs_uniques['santander_sel_Correo_SEL']	= santander_rfcs_uniques['santander_sel_Correo_SEL'].fillna('N/A')
	santander_rfcs_uniques_with_mail			=	santander_rfcs_uniques[santander_rfcs_uniques['santander_sel_Correo_SEL']!='N/A']
	santander_rfcs_uniques_with_mail			=	functions.clean_dataframe_last_update(santander_rfcs_uniques_with_mail,'Fecha_ultima_modif','santander_sel_Correo_SEL')
	santander_rfcs_uniques_no_mail				=	santander_rfcs_uniques[santander_rfcs_uniques['santander_sel_Correo_SEL']=='N/A']
	santander_rfcs_uniques						=	santander_rfcs_uniques_with_mail.append(santander_rfcs_uniques_no_mail)	
	
	print "finalmente: len(santander_rfcs_uniques)",len(santander_rfcs_uniques)
	"""
				Definitions
	"""
	ids_santander 								=	list(santander_rfcs_uniques[(santander_rfcs_uniques['ID'].str.len()==36) & (santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]['ID'].unique())
	phones_as_ids_santander 					=	list(santander_rfcs_uniques[(santander_rfcs_uniques['ID'].str.len()==10) & (santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]['ID'].unique())
	ids_internal 								=	list(internal['base_rocket_ID'].unique())
	internal['base_rocket_Telefono']			=	internal['base_rocket_Telefono'].astype(str)#standarize datatype of phone numbers
	phones_internal								=	list(internal['base_rocket_Telefono'].unique())
	mails_internal 								=	list(internal['base_rocket_Correo electronico'].unique())
	
	"""
				Merge Internal / Entities reports
	"""
	print "len(santander): ",len(santander)
	print "len(RfCs_uniques): ",len(RfCs_uniques)
	
	#merge by ID for users with contextid in utm
	# a	) look for ids to merge
	ids_founded												=	list(filter(lambda x: x in ids_internal,ids_santander))
	print "I len(ids_santander):",len(ids_santander)," uniques: ",len(set(ids_santander))
	print "I len(ids_founded):",len(ids_founded)
	# b )
	santander_identified_by_id_id_founded					=	santander_rfcs_uniques[(santander_rfcs_uniques['ID'].isin(ids_founded))&(santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]
	santander_identified_by_id_id_founded					=	functions.clean_dataframe_last_update(santander_identified_by_id_id_founded,'Fecha_ultima_modif','ID')
	print "I len(santander_identified_by_id_id_founded): ",len(santander_identified_by_id_id_founded)
	# c	)
	data													=	pd.merge(internal,santander_identified_by_id_id_founded,left_on='base_rocket_ID',right_on='ID')
	print "len(data):",len(data)
	# d	)
	santander_rfcs_uniques									=	santander_rfcs_uniques[~(santander_rfcs_uniques['ID'].isin(ids_founded))]
	data_rfcs_founded										=	data['santander_seg_RFC'].unique()
	santander_rfcs_uniques									=	santander_rfcs_uniques.append(santander_identified_by_id_id_founded[~santander_identified_by_id_id_founded['santander_seg_RFC'].isin(data_rfcs_founded)])
	#merge by phone_number for users with phone in utm
	# a )
	phones_as_ids_founded									=	list(filter(lambda x: x in phones_internal,phones_as_ids_santander))
	print "II len(phones_as_ids_santander):",len(phones_as_ids_santander)," uniques: ",len(set(phones_as_ids_santander))
	print "II len(phones_as_ids_founded):",len(phones_as_ids_founded)
	# b )
	santander_identified_by_id_phone_founded				=	santander_rfcs_uniques[(santander_rfcs_uniques['ID'].isin(phones_as_ids_founded))&(santander_rfcs_uniques['ID'].str.len()<36) & (santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]
	santander_identified_by_id_phone_founded				=	functions.clean_dataframe_last_update(santander_identified_by_id_phone_founded,'Fecha_ultima_modif','ID')
	print "II len(santander_identified_by_id_phone_founded): ",len(santander_identified_by_id_phone_founded)
	# c )
	santander_identified_by_id_phone_founded['last_form']	=	[max(internal[internal['base_rocket_Telefono']==phone]['date']) for phone in santander_identified_by_id_phone_founded['ID']]
	santander_identified_by_id_phone_founded['last_ID']		=	[internal[(internal['base_rocket_Telefono']==phone)&(internal['date']==date)]['base_rocket_ID'].unique()[0] for date,phone in zip(santander_identified_by_id_phone_founded['last_form'],santander_identified_by_id_phone_founded['ID'])]

	data													=	data.append(pd.merge(internal,santander_identified_by_id_phone_founded,left_on='base_rocket_ID',right_on='last_ID'))
	print "II len(data):",len(data)
	# d )
	santander_rfcs_uniques									=	santander_rfcs_uniques[~(santander_rfcs_uniques['ID'].isin(phones_as_ids_founded))]

	#merge by phone number for users with phone not in utm
	santander_rfcs_uniques['santander_base_Telefono celular']=	santander_rfcs_uniques['santander_base_Telefono celular'].fillna('N/A')
	santander_rfcs_uniques['santander_base_Telefono celular']=	[str(tel).replace('.0','') for tel in santander_rfcs_uniques['santander_base_Telefono celular']]
	phones_santander										=	santander_rfcs_uniques['santander_base_Telefono celular'].unique()
	print "III len(phones_santander): ",len(phones_santander)," uniques: ",len(set(phones_santander))
	# a )
	phones_founded											=	list(filter(lambda x: x in phones_internal,phones_santander))
	print "III len(phones_founded): ",len(phones_founded)
	# b )
	santander_identified_by_phone							=	santander_rfcs_uniques[(santander_rfcs_uniques['santander_base_Telefono celular'].isin(phones_founded))]
	santander_identified_by_phone							=	functions.clean_dataframe_last_update(santander_identified_by_phone,'Fecha_ultima_modif','santander_base_Telefono celular')
	santander_identified_by_phone['last_form']				=	[max(internal[internal['base_rocket_Telefono']==phone]['date']) for phone in santander_identified_by_phone['santander_base_Telefono celular']]
	santander_identified_by_phone['last_ID']				=	[internal[(internal['base_rocket_Telefono']==phone)&(internal['date']==date)]['base_rocket_ID'].unique()[0] for date,phone in zip(santander_identified_by_phone['last_form'],santander_identified_by_phone['santander_base_Telefono celular'])]
	# c )
	data 													=	data.append(pd.merge(internal,santander_identified_by_phone,left_on='base_rocket_ID',right_on='last_ID'))
	print "III len(data):",len(data)
	# d )
	santander_rfcs_uniques									=	santander_rfcs_uniques[~(santander_rfcs_uniques['santander_base_Telefono celular'].isin(phones_founded))]

	#merge by mail for the rest
	mails_santander 										=	list(santander_rfcs_uniques['santander_sel_Correo_SEL'].unique())
	print "IV len(mails_santander): ",len(mails_santander)," uniques: ",len(set(mails_santander))
	# a )
	mails_founded 											=	list(filter(lambda x: x in mails_internal,mails_santander))
	print "IV len(mails_founded):",len(mails_founded)
	# b )
	santander_identified_by_mail 							=	santander_rfcs_uniques[(santander_rfcs_uniques['santander_sel_Correo_SEL'].isin(mails_founded))]
	santander_identified_by_mail							=	functions.clean_dataframe_last_update(santander_identified_by_mail,'Fecha_ultima_modif','santander_sel_Correo_SEL')
	print "IV len(santander_identified_by_mail):",len(santander_identified_by_mail)
	santander_identified_by_mail['last_form']				=	[max(internal[internal['base_rocket_Correo electronico']==email]['date']) for email in santander_identified_by_mail['santander_sel_Correo_SEL']]
	santander_identified_by_mail['last_ID']					=	[internal[(internal['base_rocket_Correo electronico']==email)&(internal['date']==date)]['base_rocket_ID'].unique()[0] for date,email in zip(santander_identified_by_mail['last_form'],santander_identified_by_mail['santander_sel_Correo_SEL'])]
	# c )
	data 													=	data.append(pd.merge(internal,santander_identified_by_mail,left_on='base_rocket_ID',right_on='last_ID'))
	print "len(data):",len(data)
	# d )
	santander_rfcs_uniques 									=	santander_rfcs_uniques[~(santander_rfcs_uniques['santander_sel_Correo_SEL'].isin(mails_founded))]

	#Merge---no santander
	data_mails												=	list(data['base_rocket_Correo electronico'].unique())
	data_phones												=	list(data['base_rocket_Telefono'].unique())
	data_ids												=	list(data['ID'].unique())

	ids_identified											=	[]
	ids_identified.extend(ids_founded)
	ids_identified.extend(list(santander_identified_by_id_phone_founded['last_ID']))
	ids_identified.extend(list(santander_identified_by_phone['last_ID']))
	ids_identified.extend(list(santander_identified_by_mail['last_ID']))

	print "internal inicial", len(internal)
	internal												=	internal[~(internal['base_rocket_ID'].isin(ids_identified))]
	print "len(data): ",len(data)
	print "len(internal) final: ",len(internal)
	print "len(no_identified): ",len(santander_rfcs_uniques)
	#import code; code.interact(local=locals())
	
except Exception,e:
	print "error in getting and setting datasets: ",str(e)
	import code; code.interact(local=locals())

"""
			SPECIAL TREATEMENT FOR multiple emails - single ID
"""
internal_emails			=	internal['base_rocket_Correo electronico'].unique()
for item in segmento_para_tratar_por_separado['ID'].unique():
	correos				=	list(segmento_para_tratar_por_separado[segmento_para_tratar_por_separado['ID']==item]['santander_sel_Correo_SEL'].unique())
	for correo in correos:
		correo 			=	correo.lower()
		individuo		=	segmento_para_tratar_por_separado[(segmento_para_tratar_por_separado['ID']==item)&(segmento_para_tratar_por_separado['santander_sel_Correo_SEL']==correo)]
		if correo in internal_emails:
			#append to identificados
			data 		=	data.append(individuo) 
		else:
			#append to no identificados
			santander_rfcs_uniques = santander_rfcs_uniques.append(individuo)
			
#import code; code.interact(local=locals())
"""
			Satander Identified 
"""

try:
	print "starting santander identified"
	data['santander_base_Telefono celular']				=	data['santander_base_Telefono celular'].fillna('N/A')
	data['phone']										=	[phone_number_internal if phone_numer_bank== "N/A" else phone_numer_bank for phone_numer_bank,phone_number_internal in zip(data['santander_base_Telefono celular'],data['base_rocket_Telefono'])]
	data['phone']										=	[str(phone) if phone !='N/A' else phone for phone in data['phone']]
	data['phone']										=	[phone.replace('.0','') if phone !='N/A' else phone for phone in data['phone']]
	#data['phone_other']								=	[ for phone_home,phone_internal in zip(data['phone'],data['santander_base_Telefono domicilio'],data['base_rocket_Telefono'])]	
	data['santander_sel_Correo_SEL']					=	data['santander_sel_Correo_SEL'].fillna('N/A')
	data['email']										=	[email_internal if email_bank=='N/A' else email_bank for email_bank,email_internal in zip(data['santander_sel_Correo_SEL'],data['base_rocket_Correo electronico'])]
	data['email']										=	data['email'].map(lambda email: str(email).lower())
	data['birthdate']									=	[str(rfc)[-2:]+'-'+str(rfc)[-4:-2]+'-'+'19'+str(rfc)[-6:-4] for rfc in data['santander_seg_RFC']]	
	data['country']										=	['Mexico' for rfc in data['santander_seg_RFC']]
	data['profile_id']									=	['' for rfc in data['santander_seg_RFC']]
	print "1"
	#overwrite original status
	data['Status']										=	['Solicito' for rfc in data['santander_seg_RFC']]
	data['santander_seg_Universidad']					=	data['santander_seg_Universidad'].fillna('N/A')
	data['base_rocket_Universidad']						=	data['base_rocket_Universidad'].fillna('N/A')
	data['university_name']								=	[name_from_internal if name_from_bank=='N/A' else name_from_bank for name_from_bank,name_from_internal in zip(data['santander_seg_Universidad'],data['base_rocket_Universidad'])]
	data['university_name']								=	data['university_name'].map(lambda name: name.lower())
	data['university_dummy_flag']						=	['find' if name!='otra' and name!='nan' and name!='n/a' else 'no find' for name in data['university_name']]
	data['university_id']								=	[universities[universities['name']==name]['id'].unique()[0] if flag =='find' and len(universities[universities['name']==name]['id'])>0 else 'no id' for name,flag in zip(data['university_name'],data['university_dummy_flag'])]
	data['university_id']								=	[0 if name=='otra' else uni_id for name,uni_id in zip(data['university_name'],data['university_id'])]
	data['university_id']								=	['n/a' if name=='n/a' else college_id for college_id,name in zip(data['university_id'],data['university_name'])]
	data['university_id']								=	[universities[universities['pk']==college_name]['id'].unique()[0] if college_id == 'no id' and len(universities[universities['pk']==college_name])>0 else college_id for college_id,college_name in zip(data['university_id'],data['university_name'])]
	print "2"
	#ingresos
	data['base_rocket_Ingresos']						=	['N/A' if income=='error' else income for income in data['base_rocket_Ingresos']]
	data['base_rocket_Ingresos']						= 	data['base_rocket_Ingresos'].fillna('N/A')
	#gasto financiero
	data['base_rocket_Gasto Financiero']				=	data['base_rocket_Gasto Financiero'].fillna(0)	
	data['debt_ratio']									=	[(1.*int(gasto_financiero))/(1.*int(ingresos)) if ingresos!='N/A' else 'N/A' for ingresos,gasto_financiero in zip(data['base_rocket_Ingresos'],data['base_rocket_Gasto Financiero'])]
	data['Credit_entity']								=	[entity if entity != "error" else "N/A" for entity in data['base_rocket_Entidad donde tiene TC']]
	if 'base_rocket_Limite de credito' in data.columns:
		data['base_rocket_Limite de credito']			=	data['base_rocket_Limite de credito'].fillna("N/A")
		data['base_rocket_Limite de credito']			=	[limite if limite !='|' else "N/A" for limite in data['base_rocket_Limite de credito']]
		data['base_rocket_Limite de credito']			=   [int(str(limit).replace('.0','')) if limit != "N/A" else "N/A" for limit in data['base_rocket_Limite de credito']]
	print "a"
	data['found_recommended_credit_product']			=	[1 for rfc in data['santander_seg_RFC']]
	data['Fecha_ultima_modif']							=	data['Fecha_ultima_modif'].fillna('N/A')
	data['selected_product_name']						=	data['santander_seg_Producto']
	data['selected_product_name']						=	data['selected_product_name'].replace(to_replace='',value='N/A')
	data['selected_product_id']							=	[int(products[products['name']==name]['id']) if len(products[products['name']==name]['id'])>0 else 'N/A' for name in data['selected_product_name']]
	#clean cases of BCCN1==BCCN2---------------------
	data['recommended_product_name']					=	data['base_rocket_Best Credit Card'].fillna("N/A")
	data['second_recommended_product_name']				=	data['base_rocket_BCC2'].fillna("N/A")
	data['third_recommended_product_name']				=	data['base_rocket_BCC3'].fillna("N/A")
	
	data['second_recommended_product_name']				=	['N/A' if bcc==bcc2 else bcc2 for bcc,bcc2 in zip(data['recommended_product_name'],data['second_recommended_product_name'])]
	data['third_recommended_product_name']				=	['N/A' if bcc2==bcc3 else bcc3 for bcc2,bcc3 in zip(data['second_recommended_product_name'],data['third_recommended_product_name'])]
	data['third_recommended_product_name']				=	['N/A' if bcc==bcc3 else bcc3  for bcc,bcc3 in zip(data['recommended_product_name'],data['third_recommended_product_name'])]
	#-----------------------------------------------
	data['recommended_product_name']					=	data['recommended_product_name'].replace(to_replace="error",value="N/A")
	data['recommended_product_id']						=	[int(products[products['name']==name]['id'].unique()[0]) if name!= "N/A" and len(products[products['name']==name]['id'])>0 else "N/A" for name in data['recommended_product_name']]
	data['recommended_product_entity']					=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in data['recommended_product_id']]
	data['recommended_product_order']					=	[1 if name!="N/A" else 'N/A' for name in data['recommended_product_name']]
	data['recommended_product_is_requested']			=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' and id_recommended_product!='N/A' else 0 for id_selected_product,id_recommended_product,status in zip(data['selected_product_id'],data['recommended_product_id'],data['Status'])]	
	data['recommended_product_requested_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(data['recommended_product_is_requested'],data['santander_sel_Fecha Captura'])]
	data['recommended_product_is_scheduled']			=	[0 for rfc in data['santander_seg_RFC']]
	data['recommended_product_scheduled_on']			=	["N/A" for rfc in data['santander_seg_RFC']]
	data['recommended_product_status_bank']				=	[status_bank if (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,status_bank in zip(data['recommended_product_is_requested'],data['recommended_product_is_scheduled'],data['santander_sel_Estatus final'])]
	data['recommended_product_status_bank_detail']		=	[status_bank_detail if (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,status_bank_detail in zip(data['recommended_product_is_requested'],data['recommended_product_is_scheduled'],data['Dictamen'])]
	data['recommended_product_status_bank_updated_on']	=	[last_update if  (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,last_update in zip(data['recommended_product_is_requested'],data['recommended_product_is_scheduled'],data['Fecha_ultima_modif'])]
	data['recommended_product_is_approved']				=	['pending' if product_requested==1 else "N/A" for product_requested in data['recommended_product_is_requested']]
	data['recommended_product_is_approved']				=	[1 if product_requested==1 and 'aprobado' in status_bank.lower() else is_aproved for is_aproved,status_bank,product_requested in zip(data['recommended_product_is_approved'],data['recommended_product_status_bank'],data['recommended_product_is_requested'])]
	data['recommended_product_is_approved']				=	[0 if product_requested==1  and ('declinado' in status_bank.lower() or 'rechazo' in status_bank.lower()) else is_aproved for is_aproved,status_bank,product_requested in zip(data['recommended_product_is_approved'],data['recommended_product_status_bank'],data['recommended_product_is_requested'])]
	data['recommended_product_approved_on']				=	[date if status ==1 else 'N/A' for status,date in zip(data['recommended_product_is_approved'],data['Fecha_ultima_modif'])]
	data['recommended_product_is_formalized']			=	[1 if (is_formalized=='SI' and is_this_product_scheduled==1) or (is_formalized=='SI' and is_this_product_requested==1) else 0 for is_formalized,is_this_product_requested,is_this_product_scheduled in zip(data['santander_seg_Formalizadas'],data['recommended_product_is_requested'],data['recommended_product_is_scheduled'])]
	data['recommended_product_formalized_on']			=	[formalized_date if is_formalized==1 else 'N/A' for is_formalized,formalized_date in zip(data['recommended_product_is_formalized'],data['santander_seg_FechaFormalizacion'])]
	print "b"
	data['second_recommended_product_name']					=	data['second_recommended_product_name'].replace(to_replace="error",value="N/A")
	data['second_recommended_product_id']					=	[int(products[products['name']==name]['id'].unique()[0]) if len(products[products['name']==name]['id'])>0 else "N/A" for name in data['second_recommended_product_name']]
	data['second_recommended_product_entity']				=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in data['second_recommended_product_id']]
	data['second_recommended_product_order']				=	[2  if name!="N/A" else 'N/A' for name in data['second_recommended_product_name']]
	data['second_recommended_product_is_requested']			=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' and id_recommended_product!='N/A'  else 0 for id_selected_product,id_recommended_product,status in zip(data['selected_product_id'],data['second_recommended_product_id'],data['Status'])]	
	data['second_recommended_product_requested_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(data['second_recommended_product_is_requested'],data['santander_sel_Fecha Captura'])]
	data['second_recommended_product_is_scheduled']			=	[0 for rfc in data['santander_seg_RFC']]
	data['second_recommended_product_scheduled_on']			=	["N/A" for rfc in data['santander_seg_RFC']]
	data['second_recommended_product_status_bank']			=	[status_bank if (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,status_bank in zip(data['second_recommended_product_is_requested'],data['second_recommended_product_is_scheduled'],data['santander_sel_Estatus final'])]
	data['second_recommended_product_status_bank_detail']	=	[status_bank_detail if  (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,status_bank_detail in zip(data['second_recommended_product_is_requested'],data['second_recommended_product_is_scheduled'],data['Dictamen'])]
	data['second_recommended_product_status_bank_updated_on']=	[last_update if  (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,last_update in zip(data['second_recommended_product_is_requested'],data['second_recommended_product_is_scheduled'],data['Fecha_ultima_modif'])]
	data['second_recommended_product_is_approved']			=	['pending' if product_requested==1 else "N/A" for product_requested in data['second_recommended_product_is_requested']]
	data['second_recommended_product_is_approved']			=	[1 if product_requested==1 and 'aprobado' in status_bank.lower() else is_aproved for is_aproved,status_bank,product_requested in zip(data['second_recommended_product_is_approved'],data['second_recommended_product_status_bank'],data['second_recommended_product_is_requested'])]
	data['second_recommended_product_is_approved']			=	[0 if product_requested==1  and ('declinado' in status_bank.lower() or 'rechazo' in status_bank.lower()) else is_aproved for is_aproved,status_bank,product_requested in zip(data['second_recommended_product_is_approved'],data['second_recommended_product_status_bank'],data['second_recommended_product_is_requested'])]
	data['second_recommended_product_approved_on']			=	[date if status ==1 else "N/A" for status,date in zip(data['second_recommended_product_is_approved'],data['Fecha_ultima_modif'])]
	data['second_recommended_product_is_formalized']		=	[1 if (is_formalized=='SI' and is_this_product_scheduled==1) or (is_formalized=='SI' and is_this_product_requested==1) else 0 for is_formalized,is_this_product_requested,is_this_product_scheduled in zip(data['santander_seg_Formalizadas'],data['second_recommended_product_is_requested'],data['second_recommended_product_is_scheduled'])]
	data['second_recommended_product_formalized_on']		=	[formalized_date if is_formalized==1 else 'N/A' for is_formalized,formalized_date in zip(data['second_recommended_product_is_formalized'],data['santander_seg_FechaFormalizacion'])]
	print "c"
	data['third_recommended_product_name']					=	data['third_recommended_product_name'].replace(to_replace="error",value="N/A")
	data['third_recommended_product_id']					=	[int(products[products['name']==name]['id'].unique()[0]) if len(products[products['name']==name]['id'])>0 else "N/A" for name in data['third_recommended_product_name']]
	data['third_recommended_product_entity']				=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in data['third_recommended_product_id']]
	data['third_recommended_product_order']					=	[3 if name!="N/A" else 'N/A' for name in data['third_recommended_product_name']]
	data['third_recommended_product_is_requested']			=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' and id_recommended_product!='N/A'  else 0 for id_selected_product,id_recommended_product,status in zip(data['selected_product_id'],data['third_recommended_product_id'],data['Status'])]	
	data['third_recommended_product_requested_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(data['third_recommended_product_is_requested'],data['santander_sel_Fecha Captura'])]
	data['third_recommended_product_is_scheduled']			=	[0 for rfc in data['santander_seg_RFC']]
	data['third_recommended_product_scheduled_on']			=	["N/A" for rfc in data['santander_seg_RFC']]
	data['third_recommended_product_status_bank']			=	[status_bank if (is_requested==1 or is_scheduled == 1)  else 'N/A' for is_requested,is_scheduled,status_bank in zip(data['third_recommended_product_is_requested'],data['third_recommended_product_is_scheduled'],data['santander_sel_Estatus final'])]
	data['third_recommended_product_status_bank_detail']	=	[status_bank_detail if (is_requested==1 or is_scheduled == 1)  else 'N/A' for is_requested,is_scheduled,status_bank_detail in zip(data['third_recommended_product_is_requested'],data['third_recommended_product_is_scheduled'],data['Dictamen'])]
	data['third_recommended_product_status_bank_updated_on']=	[last_update if  (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,last_update in zip(data['third_recommended_product_is_requested'],data['third_recommended_product_is_scheduled'],data['Fecha_ultima_modif'])]
	data['third_recommended_product_is_approved']			=	['pending' if product_requested==1 else "N/A" for product_requested in data['third_recommended_product_is_requested']]
	data['third_recommended_product_is_approved']			=	[1 if product_requested==1 and 'aprobado' in status_bank.lower() else is_aproved for is_aproved,status_bank,product_requested in zip(data['third_recommended_product_is_approved'],data['third_recommended_product_status_bank'],data['third_recommended_product_is_requested'])]
	data['third_recommended_product_is_approved']			=	[0 if product_requested==1  and ('declinado' in status_bank.lower() or 'rechazo' in status_bank.lower()) else is_aproved for is_aproved,status_bank,product_requested in zip(data['third_recommended_product_is_approved'],data['third_recommended_product_status_bank'],data['third_recommended_product_is_requested'])]
	data['third_recommended_product_approved_on']			=	[date if status ==1 else "N/A" for status,date in zip(data['third_recommended_product_is_approved'],data['Fecha_ultima_modif'])]
	data['third_recommended_product_is_formalized']			=	[1 if (is_formalized=='SI' and is_this_product_scheduled==1) or (is_formalized=='SI' and is_this_product_requested==1) else 0 for is_formalized,is_this_product_requested,is_this_product_scheduled in zip(data['santander_seg_Formalizadas'],data['third_recommended_product_is_requested'],data['third_recommended_product_is_scheduled'])]
	data['third_recommended_product_formalized_on']			=	[formalized_date if is_formalized==1 else 'N/A' for is_formalized,formalized_date in zip(data['third_recommended_product_is_formalized'],data['santander_seg_FechaFormalizacion'])]
	print "d"
	data['additional_recommended_product_id']				=	[selected_product_id if selected_product_id not in [first_product_id,second_product_id,third_product_id] else 'N/A' for selected_product_id,first_product_id,second_product_id,third_product_id in zip(data['selected_product_id'],data['recommended_product_id'],data['second_recommended_product_id'],data['third_recommended_product_id'])]
	data['additional_recommended_product_name']				=	[products[products['id']==identificador]['name'].unique()[0] if identificador != 'N/A' else 'N/A' for identificador in data['additional_recommended_product_id']]
	data['additional_recommended_product_entity']			=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in data['additional_recommended_product_id']]
	data['additional_recommended_product_order']			=	[4 if name!="N/A" else 'N/A' for name in data['additional_recommended_product_name']]
	data['additional_recommended_product_is_requested']		=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' and id_recommended_product!='N/A' else 0 for id_selected_product,id_recommended_product,status in zip(data['selected_product_id'],data['additional_recommended_product_id'],data['Status'])]	
	data['additional_recommended_product_requested_on']		=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(data['third_recommended_product_is_requested'],data['santander_sel_Fecha Captura'])]
	data['additional_recommended_product_is_scheduled']		=	[0 for rfc in data['santander_seg_RFC']]
	data['additional_recommended_product_scheduled_on']		=	["N/A" for rfc in data['santander_seg_RFC']]
	data['additional_recommended_product_status_bank']		=	[status_bank if (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,status_bank in zip(data['additional_recommended_product_is_requested'],data['additional_recommended_product_is_scheduled'],data['santander_sel_Estatus final'])]
	data['additional_recommended_product_status_bank_detail']=	[status_bank_detail if (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,status_bank_detail in zip(data['additional_recommended_product_is_requested'],data['additional_recommended_product_is_scheduled'],data['Dictamen'])]
	data['additional_recommended_product_status_bank_updated_on']=	[last_update if  (is_requested==1 or is_scheduled == 1) else 'N/A' for is_requested,is_scheduled,last_update in zip(data['additional_recommended_product_is_requested'],data['additional_recommended_product_is_scheduled'],data['Fecha_ultima_modif'])]
	data['additional_recommended_product_is_approved']		=	['pending' if product_requested==1 else "N/A" for product_requested in data['additional_recommended_product_is_requested']]
	data['additional_recommended_product_is_approved']		=	[1 if product_requested==1 and 'aprobado' in status_bank.lower() else is_aproved for is_aproved,status_bank,product_requested in zip(data['additional_recommended_product_is_approved'],data['additional_recommended_product_status_bank'],data['additional_recommended_product_is_requested'])]
	data['additional_recommended_product_is_approved']		=	[0 if product_requested==1  and ('declinado' in status_bank.lower() or 'rechazo' in status_bank.lower()) else is_aproved for is_aproved,status_bank,product_requested in zip(data['additional_recommended_product_is_approved'],data['additional_recommended_product_status_bank'],data['additional_recommended_product_is_requested'])]
	data['additional_recommended_product_approved_on']		=	[date if status ==1 else "N/A" for status,date in zip(data['additional_recommended_product_is_approved'],data['Fecha_ultima_modif'])]
	data['additional_recommended_product_is_formalized']	=	[1 if (is_formalized=='SI' and is_this_product_scheduled==1) or (is_formalized=='SI' and is_this_product_requested==1) else 0 for is_formalized,is_this_product_requested,is_this_product_scheduled in zip(data['santander_seg_Formalizadas'],data['additional_recommended_product_is_requested'],data['additional_recommended_product_is_scheduled'])]
	data['additional_recommended_product_formalized_on']	=	[formalized_date if is_formalized==1 else 'N/A' for is_formalized,formalized_date in zip(data['additional_recommended_product_is_formalized'],data['santander_seg_FechaFormalizacion'])]

	
	data.to_csv('data_to review_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8')
	#pasa que algunos usuarios tienen 2 solicitudes con la misma liga, mismo id de internal
	#esto provoca que tenga varios registros con mismo id de internal, los voy a limpiar
	#data													=		functions.clean_dataframe_last_update(data,'Fecha_ultima_modif','base_rocket_ID')	
	print "len final de data: ", len(data)
	
	data['products_shown']									=		[sum(np.array(list(set([str(id_1),str(id_2),str(id_3),str(id_4)])))!='N/A') for id_1,id_2,id_3,id_4 in zip(data['recommended_product_id'],data['second_recommended_product_id'],data['third_recommended_product_id'],data['additional_recommended_product_id'])]#Numero de productos ofrecidos
	#data
	data_cols												=		functions.set_selected_columns_for_group_santander_identified()
	data													=		pd.DataFrame(data, columns= data_cols)		
	
	data.rename(index=str,columns =	functions.set_column_order_name_for_group_santander_identified(),inplace=True)	
	data.to_csv('Grupo_A_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8')
	#import code; code.interact(local=locals())
except Exception,e:
	print "error setting santander people data: ",str(e)
	import code; code.interact(local=locals())



"""
			Santander No Identified
"""

try:
	print "starting no identified"
	print "a"
	no_identified										=	santander_rfcs_uniques
	no_identified['phone']								=	no_identified['santander_base_Telefono celular'].fillna('N/A')
	no_identified['phone']								=	[str(phone) if phone !='N/A' else phone for phone in no_identified['phone']]
	no_identified['phone']								=	[phone.replace('.0','') if phone !='N/A' else phone for phone in no_identified['phone']]
	no_identified['email']								=	no_identified['santander_sel_Correo_SEL'].fillna('N/A')
	no_identified['birthdate']							=	[str(rfc)[-2:]+'-'+str(rfc)[-4:-2]+'-'+'19'+str(rfc)[-6:-4] for rfc in no_identified['santander_seg_RFC']]	
	no_identified['country']							=	['Mexico' for rfc in no_identified['santander_seg_RFC']]
	no_identified['phone_characteristics']				=	no_identified['phone'].map(lambda phone: functions.get_phone_characteristics(phone))
	no_identified['phone_type']							=	[phone_data['type'] for phone_data in no_identified['phone_characteristics']]
	no_identified['phone_carrier']						=	[phone_data['carrier'] for phone_data in no_identified['phone_characteristics']]
	no_identified['phone_geo_state']					=	[phone_data['geo_state'] for phone_data in no_identified['phone_characteristics']]
	no_identified['phone_geo_department']				=	[phone_data['geo_department'] for phone_data in no_identified['phone_characteristics']]
	no_identified['phone_geo_town']						=	[phone_data['geo_town'] for phone_data in no_identified['phone_characteristics']]
	no_identified['profile_id']							=	['' for rfc in no_identified['santander_seg_RFC']]
	print "b"
	#date
	no_identified['Status']								=	['Solicito' for rfc in no_identified['santander_seg_RFC']]
	no_identified['college_name']						=	no_identified['santander_seg_Universidad'].fillna('N/A')
	no_identified['college_name']						=	[functions.strip_accents(name) if name != 'N/A' else 'N/A' for name in no_identified['college_name']]
	no_identified['college_name']						= 	no_identified['college_name'].map(lambda name: str(name).lower())
	no_identified['college_id']							=	[universities[universities['name']==name]['id'].unique()[0] if name !='n/a' and len(universities[universities['name']==name]['id'].unique())>0  else 'no_id' for name in no_identified['college_name']]
	no_identified['found_recommended_credit_product']	=	[1 for user in no_identified['santander_sel_Folio_inteligente']]
	no_identified['products_shown']						=	[1 for user in no_identified['santander_sel_Folio_inteligente']]
	no_identified['product_name']						=	no_identified['santander_seg_Producto']
	no_identified['product_id']							=	[int(products[products['name']==name]['id'].unique()[0]) if len(products[products['name']==name]['id'])>0 else "N/A" for name in no_identified['product_name']]
	no_identified['product_entity']						=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in no_identified['product_id']]
	no_identified['product_order']						=	[1 for product_id in no_identified['product_id']]
	no_identified['product_is_requested']				=	[1 for product_id in no_identified['product_id']]
	no_identified['product_requested_on']				=	no_identified['santander_sel_Fecha Captura']
	no_identified['product_is_scheduled']				=	[0 for product_id in no_identified['product_id']]
	no_identified['product_scheduled_on']				=	['N/A' for product_id in no_identified['product_id']]
	no_identified['product_is_approved']				=	[1 if client_code !='N/A' else 'pending' for client_code in no_identified['santander_seg_CodigoCliente']]
	no_identified['product_approved_on']				=	[no_identified['Fecha_ultima_modif'] if flag ==1 else 'N/A' for flag in no_identified['product_is_approved']]	
	no_identified['product_status_bank']				=	no_identified['santander_sel_Estatus final']
	no_identified['product_status_bank_detail']			=	no_identified['Dictamen']
	no_identified['product_status_bank_updated_on']		=	[updated_on if (is_requested == 1 or is_scheduled==1) else 'N/A' for is_requested,is_scheduled,updated_on in zip(no_identified['product_is_requested'],no_identified['product_is_scheduled'],no_identified['Fecha_ultima_modif'])]
	no_identified['product_is_formalized']				=	[1 if (is_formalized=='SI' and is_this_product_scheduled==1) or (is_formalized=='SI' and is_this_product_requested==1) else 0 for is_formalized,is_this_product_requested,is_this_product_scheduled in zip(no_identified['santander_seg_Formalizadas'],no_identified['product_is_requested'],no_identified['product_is_scheduled'])]
	no_identified['product_formalized_on']				=	[formalized_date if is_formalized==1 else 'N/A' for is_formalized,formalized_date in zip(no_identified['product_is_formalized'],no_identified['santander_seg_FechaFormalizacion'])]
	
	#define order and new names of columns
	no_identified_cols								=		functions.set_selected_columns_for_group__santander_no_identified()

	no_identified									=		pd.DataFrame(no_identified, columns=no_identified_cols)		
	
	no_identified.rename(index=str,columns 			=		functions.set_column_order_name_for_group_santander_no_identified(),inplace=True)
	
	no_identified.to_csv('Grupo_B_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8')
except Exception,e:
	print "error setting santander (no identified) people data: ",str(e)
	import code; code.interact(local=locals())


"""
			Internal data (No santander people)
"""

try:
	print "starting internal"
	internal['phone']									=	internal['base_rocket_Telefono']
	internal['email']									=	internal['base_rocket_Correo electronico']
	internal['base_rocket_Nombre']						=	[name if name!='N/D' else 'N/A' for name in internal['base_rocket_Nombre']]
	internal['birthdate']								=	[dob if dob !='error' else 'N/A' for dob in internal['base_rocket_Edad']]
	internal['country']									=	['Mexico' for id in internal['base_rocket_ID']]
	internal['profile_id']								=	['' for id in internal['base_rocket_ID']]
	#date
	#base_rocket_Ocupacion
	#need
	#subneed
	internal['Status']									=	internal.apply(lambda row: functions.set_status(row,'base_rocket_ESTATUS'),axis=1)
	internal['base_rocket_Universidad']					=	internal['base_rocket_Universidad'].fillna('N/A')
	internal['base_rocket_Universidad']					=	[functions.strip_accents(uni_name) if uni_name !='N/A' else 'N/A' for uni_name in internal['base_rocket_Universidad']]
	internal['university_name']							=	internal['base_rocket_Universidad'].map(lambda x: str(x).lower())
	internal['university_dummy_flag']					=	['find' if name!='otra' and name!='nan' and name!='n/a' else 'no find' for name in internal['university_name']]
	internal['university_id']							=	[universities[universities['name']==name]['id'].unique()[0] if flag =='find' and len(universities[universities['name']==name]['id'])>0 else 'no id' for name,flag in zip(internal['university_name'],internal['university_dummy_flag'])]
	internal['university_id']							=	[0 if name=='otra' else uni_id for name,uni_id in zip(internal['university_name'],internal['university_id'])]
	internal['university_id']							=	['n/a' if name=='n/a' else college_id for college_id,name in zip(internal['university_id'],internal['university_name'])]
	#internal['university_id']							=	[61 if name=='universidad autonoma del estado de morelos' else uni_id for name,uni_id in zip(internal['university_name'],internal['university_id'])]
	internal['university_id']							=	[universities[universities['pk']==college_name]['id'].unique()[0] if college_id == 'no id' and len(universities[universities['pk']==college_name])>0 else college_id for college_id,college_name in zip(internal['university_id'],internal['university_name'])]
	
	#ingresos
	internal['base_rocket_Ingresos']					=	['N/A' if income=='error' else income for income in internal['base_rocket_Ingresos']]
	internal['base_rocket_Ingresos']					=	internal['base_rocket_Ingresos'].fillna('N/A')	
	#gasto financiero
	internal['base_rocket_Gasto Financiero']			=	internal['base_rocket_Gasto Financiero'].fillna(0)	
	internal['debt_ratio']								=	[(1.*int(gasto_financiero))/(1.*int(ingresos)) if ingresos!='N/A' else 'N/A' for ingresos,gasto_financiero in zip(internal['base_rocket_Ingresos'],internal['base_rocket_Gasto Financiero'])]
	#internal['debt_ratio']								=	[gasto_fianciero/ingresos if gasto_financiero!='' else 'N/A' for gasto_financiero in internal['debt_ratio'])]

	internal['Credit_entity']							=	[entity if entity != "error" else "N/A" for entity in internal['base_rocket_Entidad donde tiene TC']]
	internal['base_rocket_Limite de credito']			=	internal['base_rocket_Limite de credito'].fillna("N/A")#mirar el formato y quitar "error" si es el caso
	internal['delayed_payments']						=	[item if item != "Invalid" else "N/A" for item in internal['base_rocket_Pagos atrasados']]

	internal['selected_product_name']					=	[name if name != 'N/S' else 'N/A' for name in internal['base_rocket_Request credit card']]
	internal['selected_product_name']					=	internal['selected_product_name'].replace(to_replace='',value='N/A')
	internal['selected_product_id']						=	[int(products[products['name']==name]['id']) if len(products[products['name']==name]['id'])>0 else 'N/A' for name in internal['selected_product_name']]
	
	internal['scheduled_product_name']					=	[name if status == 'Agendo' else 'N/A' for name,status in zip(internal['base_rocket_Tarjeta agendada'],internal['Status'])]
	internal['scheduled_product_name']					=	internal['scheduled_product_name'].replace(to_replace='',value='N/A')
	internal['scheduled_product_id']					=	[int(products[products['name']==name]['id']) if len(products[products['name']==name]['id'])>0 else 'N/A' for name in internal['scheduled_product_name']]

	internal['recommended_product_name']				=	internal['base_rocket_Best Credit Card'].fillna("N/A")
	internal['recommended_product_name']				=	internal['recommended_product_name'].replace(to_replace="error",value="N/A")
	internal['recommended_product_id']					=	[int(products[products['name']==name]['id'].unique()[0]) if name!= "N/A" and len(products[products['name']==name]['id'])>0 else "N/A" for name in internal['recommended_product_name']]
	internal['recommended_product_entity']				=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in internal['recommended_product_id']]
	internal['recommended_product_order']				=	[1 if name!="N/A" else 'N/A' for name in internal['recommended_product_name']]
	internal['recommended_product_is_requested']		=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' else 0 for id_selected_product,id_recommended_product,status in zip(internal['selected_product_id'],internal['recommended_product_id'],internal['Status'])]	
	internal['recommended_product_requested_on']		=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['recommended_product_is_requested'],internal['date'])]
	internal['recommended_product_is_scheduled']		=	[1 if id_selected_product==id_recommended_product and status == 'Agendo' else 0 for id_selected_product,id_recommended_product,status in zip(internal['scheduled_product_id'],internal['recommended_product_id'],internal['Status'])]
	internal['recommended_product_scheduled_on']		=	[date if is_requested is 1 else 'N/A' for is_requested,date in zip(internal['recommended_product_is_scheduled'],internal['date'])]
	internal['recommended_product_is_approved']			=	['pending' if (status == 'Solicito' and recommended_product_is_requested==1) or (status == 'Agendo' and recommended_product_is_call_scheduled==1) else 'N/A' for status,recommended_product_is_requested,recommended_product_is_call_scheduled in zip(internal['Status'],internal['recommended_product_is_requested'],internal['recommended_product_is_scheduled'])]
	internal['recommended_product_approved_on']			=	['N/A' for name in internal['recommended_product_name']]

	internal['second_recommended_product_name']					=	internal['base_rocket_BCC2'].fillna("N/A")
	internal['second_recommended_product_name']					=	[name_second if name_first!=name_second else 'N/A' for name_first,name_second in zip(internal['recommended_product_name'],internal['second_recommended_product_name'])]
	internal['second_recommended_product_name']					=	internal['second_recommended_product_name'].replace(to_replace="error",value="N/A")
	internal['second_recommended_product_id']					=	[int(products[products['name']==name]['id'].unique()[0]) if len(products[products['name']==name]['id'])>0 else "N/A" for name in internal['second_recommended_product_name']]
	internal['second_recommended_product_entity']				=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in internal['second_recommended_product_id']]
	internal['second_recommended_product_order']				=	[2  if name!="N/A" else 'N/A' for name in internal['second_recommended_product_name']]
	internal['second_recommended_product_is_requested']			=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' else 0 for id_selected_product,id_recommended_product,status in zip(internal['selected_product_id'],internal['second_recommended_product_id'],internal['Status'])]	
	internal['second_recommended_product_requested_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['second_recommended_product_is_requested'],internal['date'])]
	internal['second_recommended_product_is_scheduled']			=	[1 if id_selected_product==id_recommended_product and status == 'Agendo' else 0 for id_selected_product,id_recommended_product,status in zip(internal['scheduled_product_id'],internal['second_recommended_product_id'],internal['Status'])]
	internal['second_recommended_product_scheduled_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['second_recommended_product_is_scheduled'],internal['date'])]
	internal['second_recommended_product_is_approved']			=	['pending' if (status == 'Solicito' and recommended_product_is_requested==1) or (status == 'Agendo' and recommended_product_is_call_scheduled==1) else 'N/A' for status,recommended_product_is_requested,recommended_product_is_call_scheduled in zip(internal['Status'],internal['second_recommended_product_is_requested'],internal['second_recommended_product_is_scheduled'])]
	internal['second_recommended_product_approved_on']			=	['N/A' for name in internal['second_recommended_product_name']]

	internal['third_recommended_product_name']					=	internal['base_rocket_BCC3'].fillna("N/A")
	internal['third_recommended_product_name']					=	[name_3 if name_3 not in [name_1,name_2] else 'N/A' for name_1,name_2,name_3 in zip(internal['recommended_product_name'],internal['second_recommended_product_name'],internal['third_recommended_product_name'])]
	internal['third_recommended_product_name']					=	internal['third_recommended_product_name'].replace(to_replace="error",value="N/A")
	internal['third_recommended_product_id']					=	[int(products[products['name']==name]['id'].unique()[0]) if len(products[products['name']==name]['id'])>0 else "N/A" for name in internal['third_recommended_product_name']]
	internal['third_recommended_product_entity']				=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in internal['third_recommended_product_id']]
	internal['third_recommended_product_order']					=	[3 if name!="N/A" else 'N/A' for name in internal['third_recommended_product_name']]
	internal['third_recommended_product_is_requested']			=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' else 0 for id_selected_product,id_recommended_product,status in zip(internal['selected_product_id'],internal['third_recommended_product_id'],internal['Status'])]	
	internal['third_recommended_product_requested_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['third_recommended_product_is_requested'],internal['date'])]
	internal['third_recommended_product_is_scheduled']			=	[1 if id_selected_product==id_recommended_product and status == 'Agendo' else 0 for id_selected_product,id_recommended_product,status in zip(internal['scheduled_product_id'],internal['third_recommended_product_id'],internal['Status'])]
	internal['third_recommended_product_scheduled_on']			=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['third_recommended_product_is_scheduled'],internal['date'])]
	internal['third_recommended_product_is_approved']			=	['pending' if (status == 'Solicito' and recommended_product_is_requested==1) or (status == 'Agendo' and recommended_product_is_call_scheduled==1) else 'N/A' for status,recommended_product_is_requested,recommended_product_is_call_scheduled in zip(internal['Status'],internal['third_recommended_product_is_requested'],internal['third_recommended_product_is_scheduled'])]
	internal['third_recommended_product_approved_on']			=	['N/A' for name in internal['third_recommended_product_name']]
	
	internal['dummy_additional_product_id']						=	[scheduled_product_id if selected_product_id=='N/A' else selected_product_id for scheduled_product_id,selected_product_id in zip(internal['scheduled_product_id'],internal['selected_product_id'])]
	internal['additional_recommended_product_id']				=	[selected_product_id if selected_product_id not in [first_product_id,second_product_id,third_product_id] else "N/A" for selected_product_id,first_product_id,second_product_id,third_product_id in zip(internal['dummy_additional_product_id'],internal['recommended_product_id'],internal['second_recommended_product_id'],internal['third_recommended_product_id'])]
	internal['additional_recommended_product_name']				=	[products[products['id']==identificador]['name'].unique()[0] if identificador != 'N/A' else 'N/A' for identificador in internal['additional_recommended_product_id']]
	internal['additional_recommended_product_entity']			=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != "N/A" else 'N/A' for identificador in internal['additional_recommended_product_id']]
	internal['additional_recommended_product_order']				=	[4 if name!="N/A" else 'N/A' for name in internal['additional_recommended_product_name']]
	internal['additional_recommended_product_is_requested']		=	[1 if id_selected_product==id_recommended_product and status == 'Solicito' else 0 for id_selected_product,id_recommended_product,status in zip(internal['selected_product_id'],internal['additional_recommended_product_id'],internal['Status'])]	
	internal['additional_recommended_product_is_scheduled']		=	[1 if id_selected_product==id_recommended_product and status == 'Agendo' else 0 for id_selected_product,id_recommended_product,status in zip(internal['scheduled_product_id'],internal['additional_recommended_product_id'],internal['Status'])]
	internal['additional_recommended_product_scheduled_on']		=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['additional_recommended_product_is_scheduled'],internal['date'])]
	internal['additional_recommended_product_is_approved']		=	['pending' if (status == 'Solicito' and recommended_product_is_requested==1) or (status == 'Agendo' and recommended_product_is_call_scheduled==1) else 'N/A' for status,recommended_product_is_requested,recommended_product_is_call_scheduled in zip(internal['Status'],internal['additional_recommended_product_is_requested'],internal['additional_recommended_product_is_scheduled'])]
	internal['additional_recommended_product_approved_on']		=	['N/A' for name in internal['additional_recommended_product_name']]
	internal['additional_recommended_product_requested_on']		=	[date if is_requested == 1 else 'N/A' for is_requested,date in zip(internal['additional_recommended_product_is_requested'],internal['date'])]

	internal['products_shown']									=	[sum(np.array(list(set([str(id_1),str(id_2),str(id_3),str(id_4)])))!='N/A') for id_1,id_2,id_3,id_4 in zip(internal['recommended_product_id'],internal['second_recommended_product_id'],internal['third_recommended_product_id'],internal['additional_recommended_product_id'])]#Numero de productos ofrecidos
	internal['found_recommended_credit_product']				=	[1 if n_products>=1 else 0 for n_products in internal['products_shown']]

	#import code; code.interact(local=locals())

	#define and rename columns

	internal_cols						=		functions.set_selected_columns_for_group_no_santander()

	internal							=		pd.DataFrame(internal, columns=internal_cols)		
	
	internal.rename(index=str,columns 	=		functions.set_column_order_name_for_group_no_santander(),inplace=True)
	
	internal.to_csv('Grupo_C_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8')
	
	print "Internal: DONE!"
except Exception,e:
	print "error setting internal data: ",str(e)
	import code; code.interact(local=locals())

print "The End woooho!"
import code; code.interact(local=locals())

