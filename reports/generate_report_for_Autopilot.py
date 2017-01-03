# -*- coding: utf-8 -*-
import pandas as pd
import curp
import load_data
import time
import functions
from datetime import datetime
import subprocess
import math

#load santander data 
santander								= 		pd.read_csv('Santander_02_01_2017_with_referal_code_.csv',encoding='utf-8')

#load internal
internal 								=		load_data.load_dbRocket_V4(False)

#---------subset by time
internal['date']						=		pd.to_datetime(internal['base_rocket_Hora de finalizacion del formulario'])
date_min								= 		datetime.strptime('Oct 1 2014  12:00AM', '%b %d %Y %I:%M%p')
date_max								= 		datetime.strptime('Nov 30 2016  12:00AM', '%b %d %Y %I:%M%p')
internal 								=		internal[(internal['date']>date_min)&(internal['date']<date_max)]

#load products information
products 								=		load_data.load_products_info()																																																																																																																																																																																																																																																																																																																																																							

"""
			RFCs uniques in Santander report
"""

#RFCs

RfCs_uniques 								=	list(santander['santander_seg_RFC'].unique())

santander['santander_sel_Fecha Captura'] 	=	pd.to_datetime(santander['santander_sel_Fecha Captura'])

santander_rfcs_uniques 						=	pd.DataFrame()

print 4
for unique_rfc in RfCs_uniques:
	more_recent								=	max(santander[santander['santander_seg_RFC']==unique_rfc]['santander_sel_Fecha Captura'])
	santander_rfcs_uniques					=	santander_rfcs_uniques.append(santander[(santander['santander_seg_RFC']==unique_rfc)&(santander['santander_sel_Fecha Captura']==more_recent)][0:1])
"""
			Definitions
"""
ids_santander 								=	list(santander_rfcs_uniques[(santander_rfcs_uniques['ID'].str.len()==36) & (santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]['ID'].unique())
phones_as_ids_santander 					=	list(santander_rfcs_uniques[(santander_rfcs_uniques['ID'].str.len()==10) & (santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]['ID'].unique())
ids_internal 								=	list(internal['base_rocket_ID'].unique())
internal['base_rocket_Telefono']			=	internal['base_rocket_Telefono'].astype(str)#standarize datatype of phone numbers
phones_internal								=	list(internal['base_rocket_Telefono'].unique())
mails_internal 								=	list(internal['base_rocket_Correo electronico'].unique())


print 5
"""
			Merge Internal / Entities reports
"""
#merge by ID for users with contextid in utm
# a	) look for ids to merge
ids_founded									=	list(filter(lambda x: x in ids_internal,ids_santander))
# b )
santander_identified_by_id_id_founded		=	santander_rfcs_uniques[(santander_rfcs_uniques['ID'].isin(ids_founded))&(santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]

# c	)
data										=	pd.merge(internal,santander_identified_by_id_id_founded,left_on='base_rocket_ID',right_on='ID')
# d	)
santander_rfcs_uniques						=	santander_rfcs_uniques[~(santander_rfcs_uniques['ID'].isin(ids_founded))]

#merge by phone_number for users with phone in utm
# a )
phones_as_ids_founded						=	list(filter(lambda x: x in phones_internal,phones_as_ids_santander))
# b )
santander_identified_by_id_phone_founded	=	santander_rfcs_uniques[(santander_rfcs_uniques['ID'].isin(phones_as_ids_founded))&(santander_rfcs_uniques['ID'].str.len()<36) & (santander_rfcs_uniques['Estatus de Identificacion']=='Identificado por utm')]
# c )
data										=	data.append(pd.merge(internal,santander_identified_by_id_phone_founded,left_on='base_rocket_Telefono',right_on='ID'))
# d )
santander_rfcs_uniques						=	santander_rfcs_uniques[~(santander_rfcs_uniques['ID'].isin(phones_as_ids_founded))]

#merge by phone number for users with phone not in utm
phones_santander 										=	list(santander_rfcs_uniques['santander_base_Telefono celular'].unique())
phones_santander										=	[str(tel) for tel in phones_santander if tel !='nan' and not math.isnan(tel)]
phones_santander										=	[phone.replace('.0','') for phone in phones_santander]
# a )
phones_founded											=	list(filter(lambda x: x in phones_internal,phones_santander))
# b )
santander_identified_by_phone				=	santander_rfcs_uniques[(santander_rfcs_uniques['santander_base_Telefono celular'].isin(phones_founded))]
# c )
data 										=	data.append(pd.merge(internal,santander_identified_by_phone,left_on='base_rocket_Telefono',right_on='santander_base_Telefono celular'))
# d )
santander_rfcs_uniques						=	santander_rfcs_uniques[~(santander_rfcs_uniques['santander_base_Telefono celular'].isin(phones_founded))]

#merge by mail for the rest
mails_santander 							=	list(santander_rfcs_uniques['santander_sel_Correo_SEL'].unique())
# a )
mails_founded 								=	list(filter(lambda x: x in mails_internal,mails_santander))
# b )
santander_identified_by_mail 				=	santander_rfcs_uniques[(santander_rfcs_uniques['santander_sel_Correo_SEL'].isin(mails_founded))]
# c )
data 										=	data.append(pd.merge(internal,santander_identified_by_mail,left_on='base_rocket_Correo electronico',right_on='santander_sel_Correo_SEL'))
# d )
santander_rfcs_uniques 						=	santander_rfcs_uniques[~(santander_rfcs_uniques['santander_sel_Correo_SEL'].isin(mails_founded))]

#No identified
santander_rfcs_uniques.to_csv('No_Identificados_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8')

#

#Merge
data_mails									=	list(data['base_rocket_Correo electronico'].unique())
data_phones									=	list(data['base_rocket_Telefono'].unique())
data_ids									=	list(data['ID'].unique())

internal									=	internal[~(internal['base_rocket_Correo electronico'].isin(data_mails))&(~(internal['base_rocket_Telefono'].isin(data_phones))&(~(internal['base_rocket_ID'].isin(data_ids))))]


super_merge 								=	internal.append(data)

"""
		Custom functions
"""
super_merge['Status']							=	super_merge.apply (lambda row: functions.set_status(row,'base_rocket_ESTATUS'),axis=1)

super_merge['recommended_product_name']			=	super_merge['base_rocket_Best Credit Card']
super_merge['recommended_product_name']			=	super_merge['recommended_product_name'].replace(to_replace="error",value="N/A")
super_merge['recommended_product_id']			=	[int(products[products['name']==name]['id'].unique()[0]) if len(products[products['name']==name]['id'])>0 else 'N/A' for name in super_merge['base_rocket_Best Credit Card']]
super_merge['recommended_product_url'] 			= 	[str(products[products['id']==identificador]['url'].unique()[0]) if identificador != 'N/A' else '' for identificador in super_merge['recommended_product_id']]
super_merge['recommended_product_image']		=	[str(products[products['id']==identificador]['card_image'].unique()[0]) if identificador != 'N/A' else '' for identificador in super_merge['recommended_product_id']]
super_merge['recommended_product_entity']		=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != 'N/A' else '' for identificador in super_merge['recommended_product_id']]

super_merge['scheduled_product_name']			=	[name if status == 'Schedule' else 'N/A' for name,status in zip(super_merge['base_rocket_Tarjeta agendada'],super_merge['Status'])]
super_merge['scheduled_product_name']			=	super_merge['scheduled_product_name'].fillna('N/A')
super_merge['scheduled_product_id']				=	[int(products[products['name']==name]['id'].unique()[0]) if name!='N/A' and len(products[products['name']==name]['id'])>0 else '' for name in super_merge['scheduled_product_name']]
super_merge['scheduled_product_url']			=	[str(products[products['id']==identificador]['url'].unique()[0]) if identificador != '' else '' for identificador in super_merge['scheduled_product_id']]
super_merge['scheduled_product_image']			=	[str(products[products['id']==identificador]['card_image'].unique()[0]) if identificador != '' else '' for identificador in super_merge['scheduled_product_id']]
super_merge['scheduled_product_image']			=	[str(products[products['id']==identificador]['entity']) if identificador != '' else '' for identificador in super_merge['scheduled_product_id']]


#Product selected&status correction
super_merge['dummy_RFC']						=	super_merge['santander_seg_RFC'].fillna('N/A')
super_merge['Status']							=	['Solicito' if user_rfc!='N/A' else status for user_rfc,status in zip(super_merge['dummy_RFC'],super_merge['Status'])]

super_merge['selected_product_name']			=	[name if status == 'Solicito' else 'N/A' for name,status in zip(super_merge['base_rocket_Request credit card'],super_merge['Status'])]
super_merge['selected_product_name']			=	[new_product if user_rfc!='N/A' else old_product for user_rfc,new_product,old_product in zip(super_merge['dummy_RFC'],super_merge['santander_seg_Producto'],super_merge['selected_product_name'])]
super_merge['selected_product_name']			=	super_merge['selected_product_name'].replace(to_replace='',value="N/A")

super_merge['selected_product_id']				=	[int(products[products['name']==name]['id']) if len(products[products['name']==name]['id'])>0 else 'N/A' for name in super_merge['selected_product_name']]
super_merge['selected_product_url']				=	[str(products[products['id']==identificador]['url'].unique()[0]) if identificador != 'N/A' else '' for identificador in super_merge['selected_product_id']]
super_merge['selected_product_image']			=	[str(products[products['id']==identificador]['card_image'].unique()[0]) if identificador != 'N/A' else '' for identificador in super_merge['selected_product_id']]
super_merge['selected_product_entity']			=	[str(products[products['id']==identificador]['entity'].unique()[0]) if identificador != 'N/A' else '' for identificador in super_merge['selected_product_id']]

super_merge['base_rocket_Antiguedad Laboral']	=	super_merge['base_rocket_Antiguedad Laboral'].replace(to_replace='error',value='N/A')

super_merge['dummy_rocket_email']				=	super_merge['base_rocket_Correo electronico'].fillna('N/A')
super_merge['dummy_entity_mail']				=	super_merge['santander_sel_Correo_SEL'].fillna('N/A')
super_merge['Email_final']						=	[mail_entity if mail_entity != 'N/A' and mail_entity!=mail_rocket else mail_rocket for mail_entity,mail_rocket in zip(super_merge['dummy_entity_mail'],super_merge['dummy_rocket_email'])]

super_merge['Credit_entity']					=	[entity if entity != "error" else "" for entity in super_merge['base_rocket_Entidad donde tiene TC']]

super_merge['base_rocket_Pagos atrasados']		=	[entity if entity != "Invalid" else "" for entity in super_merge['base_rocket_Pagos atrasados']]

subprocess.call(['speech-dispatcher'])        #start speech dispatcher
subprocess.call(['spd-say', 'done'])


"""
		Final Report
"""

#define columns

#from internal: contxid, Result (Salida), Phone, Email, Registered at, User Type, Income, Employment Time, Credit Institution, Credit Time, Status (Rocket: apply/register/schedule), 
				#Recommended Product Name, Scheduled Product Name, Selected Product Name
				
#from Santander: Token, First Name, Last Name, Light, Status Bank, Status Detail,


#change name of columns and set order
columns 									=	['base_rocket_ID','santander_base_Nombre',
												'santander_base_Paterno','santander_seg_RFC',
												'santander_base_Telefono domicilio','base_rocket_Telefono',
												'base_rocket_Correo electronico','base_rocket_Ocupacion',
												'base_rocket_Ingresos','base_rocket_Antiguedad Laboral',
												'base_rocket_Experiencia Crediticia',
												'Credit_entity','base_rocket_Pagos atrasados',
												'base_rocket_Fecha de visita','base_rocket_Salida',
												'selected_product_name','selected_product_id',
												'selected_product_url','selected_product_image',
												'recommended_product_name','recommended_product_id',
												'recommended_product_url','recommended_product_image',
												'scheduled_product_name','scheduled_product_id','scheduled_product_url','scheduled_product_image',
												'Status','santander_sel_Estatus final','Dictamen','santander_seg_TokenEfl','santander_base_Semaforo',
												'santander_seg_Formalizadas','santander_seg_CodigoCliente','Referal_Code']


super_merge = pd.DataFrame(super_merge, columns=columns)

super_merge.rename(index=str,columns 	=		{'base_rocket_ID':'Contxid', 
												'santander_base_Nombre':'First Name',
												'santander_base_Paterno':'Last Name',
												'santander_seg_RFC':'RFC',
												'santander_base_Telefono domicilio':'Phone',
												'base_rocket_Telefono':'Mobile',
												'base_rocket_Correo electronico':'Email',
												'base_rocket_Ocupacion':'User Type',
												'base_rocket_Ingresos':'Income',
												'base_rocket_Antiguedad Laboral':'Employment Time',
												'base_rocket_Experiencia Crediticia':'Credit Time',
												'Credit_entity':'Credit Entity',
												'base_rocket_Pagos atrasados':'Delayed Payments',
												'base_rocket_Fecha de visita':'Registered at',
												'base_rocket_Salida':'Result',
												'recommended_product_name':'Recommended Product Name',
												'recommended_product_id':'Recommend Product Id',
												'recommended_product_url':'Recommended Product URL',
												'recommended_product_image':'Recommended Product Image',
												'selected_product_name':'Selected Product Name',
												'selected_product_id':'Selected Product ID',
												'selected_product_url':'Selected Product URL',
												'selected_product_image':'Selected Product Image',
												'scheduled_product_name':'Scheduled Product Name',
												'scheduled_product_id':'Scheduled Product ID',
												'scheduled_product_url':'Scheduled Product URL',
												'scheduled_product_image':'Scheduled Product Image',
												'Status':'Status',
												'santander_sel_Estatus final':'Status Bank',
												'Dictamen':'Status Detail',
												'santander_seg_TokenEfl':'Token',
												'santander_base_Semaforo':'Light',
												'santander_seg_Formalizadas':'Product Formalization',
												'santander_seg_CodigoCliente':'Client Code',
												'Referal_Code':'Referal_Code',
													},inplace=True)

super_merge.to_csv('report_Autopilot_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8')



import code; code.interact(local=locals())

