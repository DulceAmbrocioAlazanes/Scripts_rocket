# -*- coding: utf-8 -*-
import pandas as pd
import json
import functions

"""
			Products
"""

def load_universities():
	path 					=	'/home/dulce/Downloads/UNIVERSITIES/universities.json'
	
	#set as dataframe
	df			 			=	pd.read_json(path)
	df['name']				= 	[item['name']  for item in df['fields']]
	df['id']				=	[item['legacy_code']  for item in df['fields']]
	df['pk']				=	df['pk'].map(lambda short_name: str(short_name).lower())
	return	df
	

def get_products_info_path():
	#path					=	'/home/dulce/Downloads/PRODUCTS/data.json'
	path					=	'/home/dulce/Downloads/PRODUCTS/products.csv'
	return path
	
	
def load_products_info():
	products_path 			=	get_products_info_path()
	
	#json_data				=	open(products_path).read()
	#products_info			= 	json.loads(json_data)
	
	#set as dataframe
	#products_info 			=	pd.read_json(products_path)
	
	products_info 			=	pd.read_csv(products_path,encoding='utf-8')
	
	return products_info

"""
			BASE ROCKET
"""
def get_base_rocket_path():
	path					=	'/home/dulce/Downloads/DATOS_PARA_SANTANDER_CALL_CENTER/'
	#path					=	"/Users/dulceambrocio/Documents/OneDrive/Documentos/ROCKET/DATOS PARA SANTANDER CALL CENTER/"
	return path
	
def load_Rocket_test():
	base_rocket             =	pd.DataFrame()
	data_path				=	get_base_rocket_path()


	"""
	    V4
	"""
	#noviembre
	noviembre_v4           =    pd.read_excel(data_path+"V4/NOVIEMBRE_2016_V4/noviembre_2016_V4.xlsx")
	base_rocket            =    base_rocket.append(noviembre_v4)
	
	#base_rocket.reset_index()
	cols 				   =	[col for col in base_rocket.columns if 'Unnamed' not in col]
	df1 				   =	pd.DataFrame(base_rocket, columns=cols)
	cols2	               =	['base_rocket_'+col for col in cols]
	df1.columns 		   =	cols2
	return df1
		

def load_dbRocket():
	base_rocket             =	pd.DataFrame()
	data_path				=	get_base_rocket_path()
	print "starting loading internal"
	"""
		V2
	"""
	
	"""
	    V3
	"""
	
	#abril_2015
	abril_2015           	=    pd.read_excel(data_path+"V3/ABRIL_2015_V3/data_April_15.xlsx",encoding='utf-8')
	base_rocket            	=    base_rocket.append(abril_2015)
	print "V3 2015 len(abril_2015): ",len(abril_2015)
	#mayo_2015
	mayo_2015				=	pd.read_excel(data_path+"V3/MAYO_2015_V3/data_May_15.xlsx",encoding='utf-8')
	base_rocket            	= 	base_rocket.append(mayo_2015)
	print "V3 2015 len(mayo_2015): ",len(mayo_2015)
	#junio_2015
	junio_2015				=	pd.read_excel(data_path+"V3/JUNIO_2015_V3/data_June_15.xlsx",encoding='utf-8')
	base_rocket            	=	base_rocket.append(junio_2015)	
	print "V3 2015 len(junio_2015): ",len(junio_2015)
	#julio_2015
	julio_2015				=	pd.read_excel(data_path+"V3/JULIO_2015_V3/data_July_15.xlsx",encoding='utf-8')
	base_rocket            	=	base_rocket.append(julio_2015)
	print "V3 2015 len(julio_2015): ",len(julio_2015)
	#agosto_2015
	agosto_2015				=	pd.read_excel(data_path+"V3/AGOSTO_2015_V3/data_August_15.xlsx",encoding='utf-8')
	base_rocket            	=	base_rocket.append(agosto_2015)
	print "V3 2015 len(agosto_2015): ",len(agosto_2015)
	#septiembre_2015
	septiembre_2015			=	pd.read_excel(data_path+"V3/SEPTIEMBRE_2015_V3/data_September_15.xlsx",encoding='utf-8')
	base_rocket            	=	base_rocket.append(septiembre_2015)
	print "V3 2015 len(septiembre_2015): ",len(septiembre_2015)
	#octubre_2015
	octubre_2015			=	pd.read_excel(data_path+"V3/OCTUBRE 2015 V3/OCTUBRE_2015_V3.xlsx",sheetname='Hoja1',encoding='utf-8')
	base_rocket            	=	base_rocket.append(octubre_2015)
	print "V3 2015 len(octubre_2015): ",len(octubre_2015)
	#noviembre 2015
	noviembre_v3           =    pd.read_excel(data_path+"V3/NOVIEMBRE_2015_V3/NOVIEMBRE_2015_V3.xlsx",sheetname='Hoja1',encoding='utf-8')
	base_rocket            =    base_rocket.append(noviembre_v3)
	print "V3 2015 len(noviembre_v3): ",len(noviembre_v3)
	#diciembre 
	diciembre_v3           =    pd.read_excel(data_path+"V3/DICIEMBRE_2015_V3/DICIEMBRE_2015_V3.xlsx",sheetname='Hoja1',encoding='utf-8')
	base_rocket            =    base_rocket.append(diciembre_v3)
	print "V3 2015 len(diciembre_v3): ",len(diciembre_v3)
	#enero
	enero_v3               =    pd.read_excel(data_path+"V3/ENERO_2016_V3/ENERO_2016_V3.xlsx",sheetname='Hoja1',encoding='utf-8')
	base_rocket            =    base_rocket.append(enero_v3)
	print "V3 2016 len(enero_v3): ",len(enero_v3)
	#febrero
	febrero_v3             =    pd.read_excel(data_path+"V3/FEBRERO_2016_V3/FEBRERO_2016_V3.xlsx",sheetname='Hoja1',encoding='utf-8')
	base_rocket            =    base_rocket.append(febrero_v3)
	print "V3 2016 len(febrero_v3): ",len(febrero_v3)
	#marzo
	marzo_v3               =    pd.read_excel(data_path+"V3/MARZO_2016_V3/MARZO_2016_V3.xlsx",sheetname='Hoja1',encoding='utf-8')
	base_rocket            =    base_rocket.append(marzo_v3)
	print "V3 2016 len(marzo_v3): ",len(marzo_v3)
	#abril
	abril_v3               =    pd.read_excel(data_path+"V3/ABRIL_2016_V3/ABRIL_2016_V3.xlsx",sheetname='Unicos',encoding='utf-8')
	base_rocket            =    base_rocket.append(abril_v3)
	print "V3 2016 len(abril_v3): ",len(abril_v3)
	
	"""
	    V4
	"""
	"""
	#diciembre
	diciembre_v4           =    pd.read_excel(data_path+"V4/DICIEMBRE_2016_V4/diciembre_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(diciembre_v4)
	print " 2016 len(diciembre_v4):",len(diciembre_v4)
	#noviembre
	noviembre_v4           =    pd.read_excel(data_path+"V4/NOVIEMBRE_2016_V4/NOVIEMBRE_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(noviembre_v4)
	print " 2016 len(noviembre_v4):",len(noviembre_v4)
	#octubre
	octubre_v4             =    pd.read_excel(data_path+"V4/OCTUBRE_2016_V4/OCTUBRE_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(octubre_v4)
	print " 2016 len(octubre_v4):",len(octubre_v4)
	#septiembre
	septiembre_v4          =    pd.read_excel(data_path+"V4/SEPTIEMBRE_2016_V4/SEPTIEMBRE_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(septiembre_v4)
	print " 2016 len(septiembre_v4):",len(septiembre_v4)
	#agosto
	agosto_v4              =    pd.read_excel(data_path+"V4/AGOSTO_2016_V4/AGOSTO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(agosto_v4)
	print " 2016 len(agosto_v4):",len(agosto_v4)
	#julio
	julio_v4               =    pd.read_excel(data_path+"V4/JULIO_2016_V4/JULIO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(julio_v4)
	print " 2016 len(julio_v4):",len(julio_v4)
	#junio
	junio_v4               =    pd.read_excel(data_path+"V4/JUNIO_2016_V4/JUNIO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(junio_v4)
	print " 2016 len(junio_v4):",len(junio_v4)
	#mayo
	mayo_v4                =    pd.read_excel(data_path+"V4/MAYO_2016_V4/MAYO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(mayo_v4)
	print " 2016 len(mayo_v4):",len(mayo_v4)
	#abril
	abril_v4               =    pd.read_excel(data_path+"V4/ABRIL_2016_V4/ABRIL_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(abril_v4)
	print " 2016 len(abril_v4):",len(abril_v4)
	#marzo
	marzo_v4               =    pd.read_excel(data_path+"V4/MARZO_2016_V4/MARZO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(marzo_v4)
	print " 2016 len(marzo_v4):",len(marzo_v4)
	#febrero
	febrero_v4             =    pd.read_excel(data_path+"V4/FEBRERO_2016_V4/FEBRERO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(febrero_v4)
	print " 2016 len(febrero_v4):",len(febrero_v4)
	#enero
	enero_v4               =    pd.read_excel(data_path+"V4/ENERO_2016_V4/ENERO_2016_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(enero_v4)
	print " 2016 len(enero_v4):",len(enero_v4)
	#diciembre 
	diciembre_v4           =    pd.read_excel(data_path+"V4/DICIEMBRE_2015_V4/DICIEMBRE_2015_V4.xlsx",encoding='utf-8')
	base_rocket            =    base_rocket.append(diciembre_v4)
	print " 2015 len(diciembre_v4):",len(diciembre_v4)
	#noviembre 
	noviembre_v4           =    pd.read_excel(data_path+"V4/NOVIEMBRE_2015_V4/NOVIEMBRE_2015_V4.xlsx",encoding='utf-8')
	base_rocket 		   =    base_rocket.append(noviembre_v4)
	print " 2015 len(noviembre_v4):",len(noviembre_v4)
	"""
	base_rocket.reset_index()
	#codigo super necesario para cargar V3 data, bueno probar sin el
	#cols 				   =	[col.replace(' ','_') for col in base_rocket.columns if 'Unnamed' not in col]
	cols 				   =	[col for col in base_rocket.columns if 'Unnamed' not in col]
	df1 				   =	pd.DataFrame(base_rocket, columns=cols)
	cols2	               =	['base_rocket_'+functions.strip_accents(col) for col in cols]
	df1.columns 		   =	cols2
	
	print "len(df1): ",len(df1)
	print "columns: "
	for columna in df1.columns:
		print columna

	return df1

"""
		V3
"""	
def load_dbRocket_V3(with_duplicates):
	path				=	get_base_rocket_path()
	path 				=	path + 'V3/'
	if with_duplicates == False:
		return pd.read_csv(path+'V3_no_duplicates.csv',encoding='utf-8')
	else:
		return pd.read_csv(path+'V3_with_duplicates.csv',encoding='utf-8') 

"""
		V4
"""	
def load_dbRocket_V4(with_duplicates):
	path				=	get_base_rocket_path()
	path 				=	path + 'V4/'
	if with_duplicates == False:
		return pd.read_csv(path+'V4_no_duplicates.csv',encoding='utf-8')
	else:
		return pd.read_csv(path+'V4_with_duplicates.csv',encoding='utf-8')  

"""
			CALL CENTER
"""
def get_callcenter_path():
	path				=	'/Users/dulceambrocio/Documents/OneDrive/Documentos/ROCKET/ROCKET_programms/CONSOLIDACION_SANTANDER/'
	path 				=	 path + 'CCROCKET/Datos Solicitud Santander/'
	return path

def load_callcenter_data():
	try:
		#load data from cc_center rocket
		ccpath 				=	 get_callcenter_path()
		rocio 				=	 pd.read_excel(ccpath+"Datos solicitud Santander ROCIO.xlsx",header=3,sheetname="OCT 16")
		rocio   			=	 rocio.append(pd.read_excel(ccpath+"Datos solicitud Santander ROCIO.xlsx",header=3,sheetname="NOV 16"))
		jaque 				=	 pd.read_excel(ccpath+"Datos solicitud Santander JAQUELINE.xlsx",header=3,sheetname="OCT 16")
		jaque 				=	 jaque.append(pd.read_excel(ccpath+"Datos solicitud Santander JAQUELINE.xlsx",header=3,sheetname="NOV 16"))
		shar 				=	 pd.read_excel(ccpath+"Datos solicitud Santander SHARDEY.xlsx",header=3)
		dey 				=	 pd.read_excel(ccpath+"Datos solicitud Santander DEY.xlsx",header=3)
		paty 				=	 pd.read_excel(ccpath+"Datos solicitud Santander PATY.xlsx",header=3)
		paco 				=	 pd.read_excel(ccpath+"Datos solicitud Santander PACO.xlsx",header=3,sheetname="OCT 16")
		paco 				=	 paco.append(pd.read_excel(ccpath+"Datos solicitud Santander PACO.xlsx",header=3,sheetname="NOV 16"))
		#artur 				=	 pd.read_excel(ccpath+"Datos solicitud Santander Arturo.xlsx",sheetname='Hoja1')
		sam 				=	 pd.read_excel(ccpath+"Datos solicitud Santander SAMUEL.xlsx",header=3,sheetname='NOV 16')

		#integrate info from cc
		data 				= 	pd.DataFrame()
		data 				=	data.append(rocio)
		data 				=	data.append(jaque)
		data 				=	data.append(shar)
		data 				=	data.append(dey)
		data 				=	data.append(paty)
		data 				=	data.append(paco)
		data 				=	data.append(sam)



		name_columns 		=	['rocket_call_date','rocket_info_email','rocket_info_tel',
								'rocket_call_status','rocket_call_obs1','rocket_info_lastname1',
								'rocket_info_lastname2','rocket_info_firstname','rocket_info_secondname',
								'rocket_info_birthdate','rocket_info_RFC','rocket_home_street',
								'rocket_home_extnum','rocket_home_intnum','rocket_home_cp',
								'rocket_home_col','rocket_home_del','rocket_home_state',
								'rocket_info_nacionality','rocket_info_email2','rocket_home_lada',
								'rocket_home_tel','rocket_info_cellnum','rocket_info_telcompany',
								'rocket_info_jobtitle','rocket_work_income','rocket_credits_datosTDC',
								'rocket_credits_bank','rocket_credits_hipo','rocket_credits_car',
								'rocket_home_vivienda','rocket_home_ant','rocket_info_edocivil',
								'rocket_info_genre','rocket_info_jobtitle2','rocket_work_company',
								'rocket_work_street','rocket_work_numext','rocket_work_numint',
								'rocket_work_cp','rocket_work_col','rocket_work_del',
								'rocket_work_state','rocket_work_lada','rocket_work_tel',
								'rocket_work_telext','rocket_work_experience','rocket_work_totincome',
								'rocket_ref1_lastname1','rocket_ref1_lastname2','rocket_ref1_firstname',
								'rocket_ref1_secondname','rocket_ref1_lada','rocket_ref1_tel',
								'rocket_ref2_lastname1','rocket_ref2_lastname2','rocket_ref2_firstname',
								'rocket_ref2_secondname','rocket_ref2_lada','rocket_ref2_tel',
								'rocket_call_hour']

		data.columns 		=	name_columns
		#data.to_csv('dummy_data.csv',encoding='utf-8')
		#clean dates format from excel by saveing/loading csv file	
		#datos_res 			= 	pd.read_csv('dummy_data.csv')
	except Exception,e:
		print "something get wrong getting santander_base_rocket: ",str(e)
	return data

"""
			SANTANDER
"""
def get_santander_path():
	path				=	'Santander/'
	return path


#load santander reports
def load_santander_baserckt():
	try:
		path 				=	get_santander_path()
		baserckt 			=	pd.read_excel(path+"Base_Rocket.xlsx")
		baserckt.columns 	=	['santander_base_Folio_inteligente','santander_base_Agencia',
								  'santander_base_Afiliado','santander_base_Nombre',
								  'santander_base_Paterno','santander_base_Materno',
								  'santander_base_RFC','santander_base_Producto',
								  'santander_base_Usuario captura basica','santander_base_Fecha captura basica',
								  'santander_base_Usuario autenticacion','santander_base_Fecha autenticacion',
								  'santander_base_Resultado autenticacion','santander_base_Intentos Autenticacion',
								  'santander_base_Usuario evaluacion','santander_base_Fecha evaluacion',
								  'santander_base_Usuario cierre venta','santander_base_Fecha cierre venta',
								  'santander_base_Usuario carga de audio','santander_base_Fecha carga de audio',
								  'santander_base_Usuario revision audio','santander_base_Fecha revision audio',
								  'santander_base_Calificacion revisor','santander_base_Calificacion auditoria',
								  'santander_base_Motivo rechazo audio','santander_base_Situacion audio',
								  'santander_base_Usuario carga de documentos','santander_base_Fecha de carga de documentos',
								  'santander_base_Calificacion de documento','santander_base_Situacion Documento',
								  'santander_base_Sub estatus Documento','santander_base_Procesada',
								  'santander_base_Semaforo','santander_base_Dictamen solicitud',
								  'santander_base_Motivo','santander_base_Estatus cancelaciones pendientes',
								  'santander_base_Supervisor','santander_base_Numero de cliente',
								  'santander_base_Fecha de carga','santander_base_Fecha de ultimo proceso',
								  'santander_base_Telefono domicilio','santander_base_Telefono celular',
								  'santander_base_Correo electronico','santander_base_Fuente',
								  'santander_base_Numero empleado','santander_base_Punto de venta',
								  'santander_base_Folio SEL']
								
	except Exception,e:
		print "something get wrong getting santander_base_rocket: ",str(e)
	return baserckt
						

def load_santander_seg():
	path 				=	get_santander_path()
	seg_apr             =   pd.read_excel(path+"Seguimiento.xlsx")
	seg_apr.columns 	=	['santander_seg_Agencia','santander_seg_FechaCaptura',
								'santander_seg_SemanaIngreso','santander_seg_Foliointeligente',
								'santander_seg_Afiliado','santander_seg_NombreCliente',
								'santander_seg_RFC','santander_seg_Producto',
								'santander_seg_Dictamen','santander_seg_Estatus',
								'santander_seg_EstatusFinal','santander_seg_CausaRechazo',
								'santander_seg_FechaRecepcionBanco','santander_seg_SemanaRecepcionBanco',
								'santander_seg_FechaCargaJupiter','santander_seg_CausaRechazoJupiter',
								'santander_seg_FechaVigenciaOferta','santander_seg_Formalizadas',
								'santander_seg_ClaveProducto','santander_seg_ClaveSubProducto',
								'santander_seg_FechaFormalizacion','santander_seg_ID_CUESTIONARIO',
								'santander_seg_CodigoCliente','santander_seg_TokenEfl',
								'santander_seg_FechaEnvioToken','santander_seg_TokenGranData',
								'santander_seg_Universidad','santander_seg_Campania',
								'santander_seg_Producto_Formalizado','santander_seg_SubProducto_Formalizado']
	return seg_apr

def load_santander_sel():
	try:
		path 				=	get_santander_path()
		sel_rocket 			=	pd.read_excel(path+"SEL.xlsx")
		sel_rocket.columns 	=	['santander_sel_Agencia','santander_sel_Folio',
								'santander_sel_Folio_inteligente','santander_sel_Correo_SEL',
								'santander_sel_Fecha Captura','santander_sel_Fecha_Autenticacion',
								'santander_sel_Fecha_Evaluacion','santander_sel_Fecha Cierre de Venta',
								'santander_sel_Estatus final','santander_sel_Situacion',
								'santander_sel_Query String','santander_sel_Afiliado']
	except Exception,e:
		print "something get wrong getting santander_sel: ",str(e)
	return sel_rocket
