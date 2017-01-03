# -*- coding: utf-8 -*-
import pandas as pd
import unicodedata
import math
import os
import hashlib
import random

"""
	
"""
def clean_dataframe_last_update(df1,date_column,column_to_iterate):
	df2 = pd.DataFrame()
	for item in df1[column_to_iterate].unique():
		more_recent			=	max(df1[df1[column_to_iterate]==item][date_column])
		df2					=	df2.append(df1[(df1[column_to_iterate]==item)&(df1[date_column]==more_recent)][0:1])
	return df2

"""
dataset,column,new_column_name,custom_field

"""

def create_referal_code(seed):
	random.seed(seed)
	length			=	7
	allowed_chars 	=	'abcdefghijklmnopqrstuvwxyz1234567890'
	code 			=	''.join(random.choice(allowed_chars) for i in range(length))
	return code

"""
def create_referal_code(seed):
	#random_data		=	os.urandom(128)
	#referal_code		=	hashlib.md5(random_data).hexdigest()[:16]
	try:
		referal_code		=	hashlib.md5(seed+'hola').hexdigest()
	except:
		print "error: ",seed
	return referal_code
"""
def strip_accents(text_with_accents):
	 nfkd_form					= unicodedata.normalize('NFKD', text_with_accents)
	 text_whithout_accents		= 	nfkd_form.encode('ASCII', 'ignore')
	 return text_whithout_accents

def get_phone_characteristics(numero):
	"""
		Tomamos el Plan Nacional De Numeracion como Referencia
		Para validar si un numero es falso o no	
		y para obtener campos caracteristicos

	"""
	try:
		response = {'type':'',
					'carrier':'',
					'geo_state':'',
					'geo_department':'',
					'geo_town':''
					}
		numero					=	int(numero)
		archivo					=	"Plan_Nacional_Numeracion.csv"
		Referencia				=	pd.DataFrame.from_csv(archivo,header=0)
		Referencia.columns		=	['poblacion','municipio','estado','inicio','fin','tipo','modalidad','proveedor','fecha_asignacion','fecha_consolidacion','fecha_migracion','nir']
		Referencia 				= 	Referencia.reset_index()
		
		match					=	Referencia[(Referencia.inicio<numero) & (Referencia.fin>numero)]
			
		if not match.empty:
			response = {'type':match['tipo'].values[0],
						'carrier':match['proveedor'].values[0],
						'geo_state':match['estado'].values[0],
						'geo_department':match['municipio'].values[0],
						'geo_town':match['poblacion'].values[0]
						}
	except:
		#print "error in get_phone_characteristics: number = ",numero
		response = {'type':'',
					'carrier':'',
					'geo_state':'',
					'geo_department':'',
					'geo_town':''
					}
	finally:	
		return response

def set_user_subneed(subneed_code):
	if subneed_code == '22':
		return 'mas economica'
	elif subneed_code == '24':
		return 'no me gusta la que tengo'
	elif subneed_code == '25':
		return 'consolidar deudas'
	elif subneed_code == '21':
		return 'financiar mi negocio'
	elif subneed_code == '26':
		return 'financiar mi carrera universitaria'
	elif subneed_code == '27':
		return 'satisfacer una urgencia prox 20 dias'
	elif subneed_code == '28':
		return 'dinero para pagar mis creditos a tiempo'
	elif subneed_code == '29':
		return 'dinero para pagar un credito vencido'
	elif subneed_code == '30':
		return 'mejorar mediante tarjeta de bajo interes'
	elif subneed_code == '31':
		return 'mejorar mediante un prestamo'
	elif subneed_code == '32':
		return 'mejorar mediante una reparadora, estoy al cuello'
	elif subneed_code == '33':
		return 'en viajes'
	elif subneed_code == '34':
		return 'en promos'
	elif subneed_code == '45':
		return 'para incrementar mi linea de credito'
	elif subneed_code == '46':
		return 'para tener rewards y puntos'
	elif subneed_code == '47':
		return 'para viajar, soy viajero frecuente'
	elif subneed_code == '48':
		return 'sin anualidad'
	elif subneed_code == '49':
		return 'para domiciliar pago de servicios'
	elif subneed_code == '50':
		return 'con mayor linea de credito'
	elif subneed_code == '51':
		return 'que me de mas rewards'
	elif subneed_code == '52':
		return 'con beneficios para viajeros'
	elif subneed_code == '53':
		return 'sin anualidad'
	elif subneed_code == '54':
		return 'con menor tasa de interes'
	elif subneed_code == '55':
		return 'que me brinde mayor seguridad'
	elif subneed_code == '56':
		return 'con mejor servicio al cliente'
	elif subneed_code == '21':
		return 'financiar mi negocio'
	elif subneed_code == '58':
		return 'pagar deudas'
	elif subneed_code == '59':
		return 'remodelar mi casa'
	elif subneed_code == '60':
		return 'fiesta familiar'
	elif subneed_code == '61':
		return 'comprar un carro'
	elif subneed_code == '62':
		return 'tratamiento medico'
	#elif subneed_code == '29':
		#return 'pagar una deuda vencida'
	elif subneed_code == '1':
		return 'solventar un Acontecimiento inesperado'
	elif subneed_code == '6':
		return 'pagar un credito Actual'
	elif subneed_code == '64':
		return 'pagar un servicio publico'
	elif subneed_code == '37':
		return 'Mi primer tarjeta economica'
	elif subneed_code == '38':
		return 'Iniciarme en servicios financieros'
	elif subneed_code == '39':
		return 'Para uso de servicios en linea'
	elif subneed_code == '40':
		return 'Que me de rewards'
	elif subneed_code == '41':
		return 'Quiero comprar gadgets'
	elif subneed_code == '42':
		return 'con un credito para comprar algo'
	elif subneed_code == '43':
		return 'con una tarjeta de credito'
	elif subneed_code == '4':
		return ''
	elif subneed_code == '9':
		return ''
	elif subneed_code == '10':
		return ''
	elif subneed_code == '11':
		return ''
	elif subneed_code == '12':
		return ''
	elif subneed_code == '13':
		return ''
	elif subneed_code == '14':
		return ''
	elif subneed_code == '15':
		return ''
	elif subneed_code == '16':
		return ''
	elif subneed_code == '18':
		return ''
	elif subneed_code == '19':
		return ''
	elif subneed_code == '20':
		return ''
	elif subneed_code == '23':
		return ''
	elif subneed_code == 'Cambio de tarjeta y pagar menos':
		return 'Cambio de tarjeta y pagar menos'
	elif subneed_code == 'Corto Plazo':
		return 'Corto Plazo'
	elif subneed_code == 'Departamentales':
		return 'Departamentales'
	elif subneed_code == 'Descuentos en boletos':
		return 'Descuentos en boletos'
	elif subneed_code == 'Espectáculos':
		return 'Espectáculos'
	elif subneed_code == 'Gasolina':
		return 'Gasolina'
	elif subneed_code == 'Mantener la tarjeta pagando menos':
		return 'Mantener la tarjeta pagando menos'
	elif subneed_code == 'Menor CAT o intereses':
		return 'Menor CAT o intereses'
	elif subneed_code == 'Millas':
		return 'Millas'
	elif subneed_code == 'No pagar anualidad o barata':
		return 'No pagar anualidad o barata'
	elif subneed_code == 'Pago Fijo':
		return 'Pago Fijo'
	elif subneed_code == 'Pagos Fijos':
		return 'Pagos Fijos'
	elif subneed_code == 'Payback':
		return 'Payback'
	elif subneed_code == 'Privilegios':
		return 'Privilegios'
	elif subneed_code == 'Puntos':
		return 'Puntos'
	elif subneed_code == 'Restaurantes':
		return 'Restaurantes'
	elif subneed_code == 'Ropa':
		return 'Ropa'
	else:
		return "Unknown subneed"

def set_user_need(need_code):
	if need_code == '2':
		return 'tener mi primer tarjeta'
	elif need_code == '35':
		return 'iniciar historial'
	elif need_code == '8':
		return 'cambiar a una mejor tarjeta'
	elif need_code == '57':
		return 'un prestamo'
	elif need_code == '63':
		return 'pagar algo hoy mismo'
	elif need_code == '7':
		return 'comprar o financiar algo'
	elif need_code == '1':
		return 'una emergencia'
	#elif need_code == '8':
		#return 'cambiar de tarjeta'
	elif need_code == '3':
		return 'mejorar mi historial'
	elif need_code == '4':
		return 'promos'
	elif need_code == '36':
		return 'conciertos'
	elif need_code == 'Beneficios':
		return 'Beneficios'
	elif need_code == 'Consolidación de Deuda':
		return 'Consolidación de Deuda'
	elif need_code =='Crédito Pago Fijo':
		return 'Crédito Pago Fijo'
	elif need_code =='Crédito Corto Plazo':
		return 'Crédito Corto Plazo'
	elif need_code =='Crédito Personal':
		return 'Crédito Personal'
	elif need_code =='Descuentos':
		return 'Descuentos'
	elif need_code =='Tarjeta Económica':
		return 'Tarjeta Económica'
	elif need_code =='Viaje':
		return 'Viaje'
	elif need_code == '5':
		return ''
	elif need_code == '6':
		return ''
	elif need_code == '44':
		return 'tener una sig tarjeta'
	else:
		return "Unknown need"

def extract_custom_field(dataset,column,new_column_name,custom_field,n=1):
	dataset[new_column_name] = [string.split(custom_field,1)[n]  if custom_field in string else '' for string in dataset[column]]
	return dataset
	
def set_product_id():
	return 
	
def set_image_url(row,column):
	try:
		if row[column]== '':
			return image_url
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		elif row[column]== '':
			return image_url 
		else:
			return "No identified Product "
	except Exception,e:
		print "something is wrong in set_image_url function: ",str(e)
		#import code; code.interact(local=locals())

		
	
def set_product_url():
	try:
		if row[column]== '':
			return product_url
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		elif row[column]== '':
			return product_url 
		else:
			return "No identified Product "
	except Exception,e:
		print "something is wrong in set_image_url function: ",str(e)
		#import code; code.interact(local=locals())
	
	
def set_status(row,column):
	try:
		if row[column] == 'No hizo nada' or row[column] =='cNo hizo nada':
			return 'Registro'
		elif row[column] == 'Solo solicito' or row[column] == 'bSolo solicito':
			return 'Solicito'
		elif row[column] == 'Agendo llamada' or row[column] =='aAgendo llamada':
			return 'Agendo'
		else:
			return "NO Identified Estatus"
	except Exception,e:
		print "something is wrong in set_status function: ",str(e)
		#import code; code.interact(local=locals())
def set_selected_columns_for_group__santander_no_identified():
	cols	= [	
				#leads
				'phone',
				'email',
				'birthdate',
				'santander_base_Nombre',
				'santander_base_Paterno',
				'santander_base_Materno',
				'santander_seg_RFC',
				'country'
				'phone_type',
				'phone_carrier',
				'phone_geo_state',
				'phone_geo_department',
				'phone_geo_town',
				#forms
				#'base_rocket_ID':'id',
				'profile_id',
				'santander_sel_Fecha Captura',
				#'base_rocket_Ocupacion':'job_occupation',
				#'base_rocket_Para que la quieres':'primary_need',
				#'base_rocket_Subcategoria':'secondary_need',
				'Status',
				'university_id',
				'university_name',
				#'base_rocket_Ingresos':'income',
				#'base_rocket_Gasto Financiero':'monthly_debt_payment',
				#'debt_ratio':'debt_ratio',#to do
				'found_recommended_credit_product',
				#product
				'products_shown',
				#
				'product_name',
				'product_id',
				'product_entity',
				'product_order',
				'product_is_requested',
				'product_requested_on',
				'product_is_call_scheduled',
				'product_call_scheduled_on',
				'product_is_approved',
				'product_approved_on',
				'product_status_bank',
				'product_status_bank_detail',
				'product_status_bank_updated_on',
				'product_is_formalized',
				'product_formalized_on',
				#pending
				#'product_status_bank':'Status Bank',
				#'product_status_bank_detail':'Status Detail',
				'santander_seg_TokenEfl',
				'santander_base_Semaforo',
				#'santander_seg_Formalizadas',
				'santander_seg_CodigoCliente',
				'Referal_Code'
				]
	return cols
def set_column_order_name_for_group_santander_no_identified():
	#dict like array to set order and new name of columns 
	#columns	= {old_column_name:new_column_name}
	columns		= {	
				#leads
				'phone':'current_phone_number',
				'email':'current_email',
				'birthdate':'dob',#to do
				'santander_base_Nombre':'first_name',
				'santander_base_Paterno':'last_name',
				'santander_base_Materno':'last_name_2',
				'santander_seg_RFC':'rfc',
				'country':'country',#to do
				'phone_type':'phone_type',
				'phone_carrier':'phone_carrier',
				'phone_geo_state':'phone_geo_state',
				'phone_geo_department':'phone_geo_department',
				'phone_geo_town':'phone_geo_town',
				#forms
				#'base_rocket_ID':'id',
				'profile_id':'profile_id',#to do
				'santander_sel_Fecha Captura':'created_on',#to do
				#'base_rocket_Ocupacion':'job_occupation',
				#'base_rocket_Para que la quieres':'primary_need',
				#'base_rocket_Subcategoria':'secondary_need',
				'Status':'status',
				'university_id':'college_id',#to do -----------------------------special
				'university_name':'college_name',#to do
				#'base_rocket_Ingresos':'income',
				#'base_rocket_Gasto Financiero':'monthly_debt_payment',
				#'debt_ratio':'debt_ratio',#to do
				'found_recommended_credit_product':'found_recommended_credit_product',#to do ---default value
				#product
				'products_shown':'products_shown',#Numero de productos ofrecidos    to do ---default value
				#
				'product_name':'product_name', #to do -----------------------------special
				'product_id':'product_id',#to do -----------------------------special
				'product_entity':'product_entity',#to do -----------------------------special
				'product_order':'product_order', #to do -----------------------------default value
				'product_is_requested':'product_is_requested',#to do default value
				'product_requested_on':'product_requested_on',#to do ----------------special
				'product_is_call_scheduled':'product_is_call_scheduled',#to do defaul value
				'product_call_scheduled_on':'product_call_scheduled_on',#to do default value
				'product_is_approved':'product_is_approved',#to do 
				'product_approved_on':'product_approved_on',#to do
				'product_status_bank':'product_status_bank',
				'product_status_bank_detail':'product_status_bank_detail',
				'product_status_bank_updated_on':'product_status_bank_updated_on',
				'product_is_formalized':'product_is_formalized',
				'product_formalized_on':'product_formalized_on',
				#pending
				#'product_status_bank':'Status Bank',
				#'product_status_bank_detail':'Status Detail',
				'santander_seg_TokenEfl':'Token',
				'santander_base_Semaforo':'Light',
				#'santander_seg_Formalizadas':'Product Formalization',
				'santander_seg_CodigoCliente':'Client Code',
				'Referal_Code':'Referal_Code'
					}
	return columns

def set_selected_columns_for_group_no_santander():
	cols = [	
				#leads
				'phone',
				'email',
				'birthdate',
				'base_rocket_Nombre',
				#'santander_base_Nombre':'first_name',
				#'santander_base_Paterno':'last_name',
				#'santander_seg_RFC':'rfc',
				'country',
				'base_rocket_Tipo de telefono',
				'base_rocket_Proveedor de telefono',
				'base_rocket_Estado telefono',
				'base_rocket_Municipo de telefono',
				'base_rocket_Ciudad de telefono',
				#forms
				'base_rocket_ID',
				'profile_id',
				'date',
				'base_rocket_Ocupacion',
				'base_rocket_Para que la quieres',
				'base_rocket_Subcategoria',
				'Status',
				'university_id',
				'university_name',
				'base_rocket_Ingresos',
				'base_rocket_Gasto Financiero',
				'debt_ratio',
				'Credit_entity',
				'base_rocket_Limite de credito',
				'delayed_payments',
				'found_recommended_credit_product',
				#product
				'products_shown',  
				#
				'recommended_product_name',
				'recommended_product_id',
				'recommended_product_entity',
				'recommended_product_order',
				'recommended_product_is_requested',
				'recommended_product_requested_on',
				'recommended_product_is_scheduled',
				'recommended_product_scheduled_on',
				'recommended_product_is_approved',
				'recommended_product_approved_on',
				#
				'second_recommended_product_name',
				'second_recommended_product_id',
				'second_recommended_product_entity',
				'second_recommended_product_order',
				'second_recommended_product_is_requested',
				'second_recommended_product_requested_on',
				'second_recommended_product_is_scheduled',
				'second_recommended_product_scheduled_on',
				'second_recommended_product_is_approved',
				'second_recommended_product_approved_on',
				#
				'third_recommended_product_name',
				'third_recommended_product_id',
				'third_recommended_product_entity',
				'third_recommended_product_order',
				'third_recommended_product_is_requested',
				'third_recommended_product_requested_on',
				'third_recommended_product_is_scheduled',
				'third_recommended_product_scheduled_on',
				'third_recommended_product_is_approved',
				'third_recommended_product_approved_on',
				#
				'additional_recommended_product_name',
				'additional_recommended_product_id',
				'additional_recommended_product_entity',
				'additional_recommended_product_order',
				'additional_recommended_product_is_requested',
				'additional_recommended_product_requested_on',
				'additional_recommended_product_scheduled',
				'additional_recommended_product_scheduled_on',
				'additional_recommended_product_is_approved',
				'additional_recommended_product_approved_on',
				#
				'base_rocket_Best Credit Card',
				'base_rocket_Request credit card',
				'base_rocket_ESTATUS',
				'base_rocket_Antiguedad Laboral',
				'base_rocket_Experiencia Crediticia',
				'base_rocket_Pagos atrasados',
				'santander_seg_TokenEfl',
				'santander_base_Semaforo',
				'santander_seg_Formalizadas',
				'santander_seg_CodigoCliente',
				'base_rocket_Dispositivo',
				'base_rocket_Navegador',
				'base_rocket_Sistema Operativo',
				'base_rocket_Fuente',
				'base_rocket_Medio',
				'base_rocket_Termino',
				'base_rocket_UTM Cont',
				'base_rocket_Campana'
				]
	return cols
def set_column_order_name_for_group_no_santander():
	#dict like array to set order and name of columns 
	#columns = {old_column_name:new_column_name}
	columns = {	
				#leads
				'phone':'current_phone_number',
				'email':'current_email',
				'birthdate':'dob',
				'base_rocket_Nombre':'first_name',
				#'santander_base_Nombre':'first_name',
				#'santander_base_Paterno':'last_name',
				#'santander_seg_RFC':'rfc',
				'country':'country',
				'base_rocket_Tipo de telefono':'phone_type',
				'base_rocket_Proveedor de telefono':'phone_carrier',
				'base_rocket_Estado telefono':'phone_geo_state',
				'base_rocket_Municipo de telefono':'phone_geo_department',
				'base_rocket_Ciudad de telefono':'phone_geo_town',
				#forms
				'base_rocket_ID':'id',
				'profile_id':'profile_id',#to do
				'date':'created_on',
				'base_rocket_Ocupacion':'job_occupation',
				'base_rocket_Para que la quieres':'primary_need',
				'base_rocket_Subcategoria':'secondary_need',
				'Status':'status',
				'university_id':'college_id',#to do
				'university_name':'college_name',#to do
				'base_rocket_Ingresos':'income',
				'base_rocket_Gasto Financiero':'monthly_debt_payment',
				'debt_ratio':'debt_ratio',#to do
				'Credit_entity':'credit_entity',
				'base_rocket_Limite de credito':'credit_limit',
				'delayed_payments':'delayed_payments',
				'found_recommended_credit_product':'found_recommended_credit_product',
				#product
				'products_shown':'products_shown',#Numero de productos ofrecidos    
				#
				'recommended_product_name':'first_product_name',
				'recommended_product_id':'first_product_id',
				'recommended_product_entity':'first_product_entity',
				'recommended_product_order':'first_product_order',
				'recommended_product_is_requested':'first_product_is_requested',
				'recommended_product_requested_on':'first_product_requested_on',
				'recommended_product_is_scheduled':'first_product_is_scheduled',
				'recommended_product_scheduled_on':'first_product_scheduled_on',
				'recommended_product_is_approved':'first_product_is_approved',
				'recommended_product_approved_on':'first_product_approved_on',
				#
				'second_recommended_product_name':'second_product_name',
				'second_recommended_product_id':'second_product_id',
				'second_recommended_product_entity':'second_product_entity',
				'second_recommended_product_order':'second_product_order',
				'second_recommended_product_is_requested':'second_product_is_requested',
				'second_recommended_product_requested_on':'second_product_requested_on',
				'second_recommended_product_is_scheduled':'second_product_is_scheduled',
				'second_recommended_product_scheduled_on':'second_product_scheduled_on',
				'second_recommended_product_is_approved':'second_product_is_approved',
				'second_recommended_product_approved_on':'second_product_approved_on',
				#
				'third_recommended_product_name':'third_product_name',
				'third_recommended_product_id':'third_product_id',
				'third_recommended_product_entity':'third_product_entity',
				'third_recommended_product_order':'third_product_order',
				'third_recommended_product_is_requested':'third_product_is_requested',
				'third_recommended_product_requested_on':'third_product_requested_on',
				'third_recommended_product_is_scheduled':'third_product_is_scheduled',
				'third_recommended_product_scheduled_on':'third_product_scheduled_on',
				'third_recommended_product_is_approved':'third_product_is_approved',
				'third_recommended_product_approved_on':'third_product_approved_on',
				#
				'additional_recommended_product_id':'additional_product_id',
				'additional_recommended_product_name':'additional_product_name',
				'additional_recommended_product_entity':'additional_product_entity',
				'additional_recommended_product_order':'additional_product_order',
				'additional_recommended_product_is_requested':'additional_product_is_requested',
				'additional_recommended_product_requested_on':'additional_product_requested_on',
				'additional_recommended_product_is_scheduled':'additional_product_scheduled',
				'additional_recommended_product_scheduled_on':'additional_product_scheduled_on',
				'additional_recommended_product_is_approved':'additional_product_is_approved',
				'additional_recommended_product_approved_on':'additional_product_approved_on',
				#testing
				'base_rocket_Best Credit Card':'base_rocket_Best Credit Card',
				'base_rocket_Request credit card':'base_rocket_Request credit card',
				'base_rocket_ESTATUS':'base_rocket_ESTATUS',
				#pending
				'base_rocket_Antiguedad Laboral':'Employment Time',
				'base_rocket_Experiencia Crediticia':'Credit Time',
				'base_rocket_Pagos atrasados':'Delayed Payments',
				'santander_seg_TokenEfl':'Token',
				'santander_base_Semaforo':'Light',
				'santander_seg_Formalizadas':'Product Formalization',
				'santander_seg_CodigoCliente':'Client Code',
				'base_rocket_Dispositivo':'tech_device',
				'base_rocket_Navegador':'tech_browser',
				'base_rocket_Sistema Operativo':'tech_operating_system',
				'base_rocket_Fuente':'utm_source',
				'base_rocket_Medio':'utm_medium',
				'base_rocket_Termino':'utm_term',
				'base_rocket_UTM Cont':'utm_content',
				'base_rocket_Campana':'utm_campaign'
				}
	return columns	

def set_selected_columns_for_group_santander_identified():
	columns 	= [
				#leads
				'phone',
				'email',
				'birthdate',
				'santander_base_Nombre',
				'santander_base_Paterno',
				'santander_base_Materno',
				'santander_seg_RFC',
				'country',
				'base_rocket_Tipo de telefono',
				'base_rocket_Proveedor de telefono',
				'base_rocket_Estado telefono',
				'base_rocket_Municipo de telefono',
				'base_rocket_Ciudad de telefono',
				#forms
				'base_rocket_ID',
				'profile_id',
				'date',
				'base_rocket_Ocupacion',
				'base_rocket_Para que la quieres',
				'base_rocket_Subcategoria',
				'Status',
				'university_id',
				'university_name',
				'base_rocket_Ingresos',
				'base_rocket_Gasto Financiero',
				'debt_ratio',
				'Credit_entity',
				'base_rocket_Limite de credito',
				'found_recommended_credit_product',
				#product
				'products_shown',
				#
				'recommended_product_name',
				'recommended_product_id',
				'recommended_product_entity',
				'recommended_product_order',
				'recommended_product_is_requested',
				'recommended_product_requested_on',
				'recommended_product_is_scheduled',
				'recommended_product_scheduled_on',
				'recommended_product_is_approved',
				'recommended_product_approved_on',
				'recommended_product_status_bank',
				'recommended_product_status_bank_detail',
				'recommended_product_status_bank_updated_on',
				'recommended_product_is_formalized',
				'recommended_product_formalized_on',
				#
				'second_recommended_product_name',
				'second_recommended_product_id',
				'second_recommended_product_entity',
				'second_recommended_product_order',
				'second_recommended_product_is_requested',
				'second_recommended_product_requested_on',
				'second_recommended_product_is_scheduled',
				'second_recommended_product_scheduled_on',
				'second_recommended_product_is_approved',
				'second_recommended_product_approved_on',
				'second_recommended_product_status_bank',
				'second_recommended_product_status_bank_detail',
				'second_recommended_product_status_bank_updated_on',
				'second_recommended_product_is_formalized',
				'second_recommended_product_formalized_on',
				#
				'third_recommended_product_name',
				'third_recommended_product_id',
				'third_recommended_product_entity',
				'third_recommended_product_order',
				'third_recommended_product_is_requested',
				'third_recommended_product_requested_on',#to do
				'third_recommended_product_is_scheduled',#to do
				'third_recommended_product_scheduled_on',#to do
				'third_recommended_product_is_approved',#to do
				'third_recommended_product_approved_on',#to do
				'third_recommended_product_status_bank',
				'third_recommended_product_status_bank_detail',
				'third_recommended_product_status_bank_updated_on',
				'third_recommended_product_is_formalized',
				'third_recommended_product_formalized_on',
				#
				'additional_recommended_product_id',
				'additional_recommended_product_name',
				'additional_recommended_product_entity',
				'additional_recommended_product_order',
				'additional_recommended_product_is_requested',
				'additional_recommended_product_requested_on',
				'additional_recommended_product_is_scheduled',
				'additional_recommended_product_scheduled_on',
				'additional_recommended_product_is_approved',
				'additional_recommended_product_approved_on',
				'additional_recommended_product_status_bank',
				'additional_recommended_product_status_bank_detail',
				'additional_recommended_product_status_bank_updated_on',
				'additional_recommended_product_is_formalized',
				'additional_recommended_product_formalized_on',
				#pending
				'base_rocket_Antiguedad Laboral',
				'base_rocket_Experiencia Crediticia',
				'base_rocket_Pagos atrasados',
				#'santander_sel_Estatus final',
				#'Dictamen',
				'santander_seg_TokenEfl',
				'santander_base_Semaforo',
				#'santander_seg_Formalizadas',
				'santander_seg_CodigoCliente',
				'base_rocket_Dispositivo',
				'base_rocket_Navegador',
				'base_rocket_Sistema Operativo',
				'base_rocket_Fuente',
				'base_rocket_Medio',
				'base_rocket_Termino',
				'base_rocket_UTM Cont',
				'base_rocket_Campana',
				'Referal_Code',
				#testing
				'base_rocket_Universidad',
				'santander_sel_Estatus final',
				'base_rocket_BCC2',
				'base_rocket_BCC3'
				]
	return columns
def set_column_order_name_for_group_santander_identified():
	#dict like array to set order and name of columns 
	#columns	= {old_column_name:new_column_name}
	columns 	= {
				#leads
				'phone':'current_phone_number',
				'email':'current_email',
				'birthdate':'dob',#to do
				'santander_base_Nombre':'first_name',
				'santander_base_Paterno':'last_name',
				'santander_base_Materno':'last_name_2',
				'santander_seg_RFC':'rfc',
				'country':'country',
				'base_rocket_Tipo de telefono':'phone_type',
				'base_rocket_Proveedor de telefono':'phone_carrier',
				'base_rocket_Estado telefono':'phone_geo_state',
				'base_rocket_Municipo de telefono':'phone_geo_department',
				'base_rocket_Ciudad de telefono':'phone_geo_town',
				#forms
				'base_rocket_ID':'id',
				'profile_id':'profile_id',#to do
				'date':'created_on',
				'base_rocket_Ocupacion':'job_occupation',
				'base_rocket_Para que la quieres':'primary_need',
				'base_rocket_Subcategoria':'secondary_need',
				'Status':'status',
				'university_id':'college_id',#to do
				'university_name':'college_name',
				'base_rocket_Ingresos':'income',
				'base_rocket_Gasto Financiero':'monthly_debt_payment',
				'debt_ratio':'debt_ratio',#to do
				'Credit_entity':'credit_entity',
				'base_rocket_Limite de credito':'credit_limit',
				'found_recommended_credit_product':'found_recommended_credit_product',#to do
				#product
				'products_shown':'products_shown',#Numero de productos ofrecidos    to do
				#
				'recommended_product_name':'first_product_name',
				'recommended_product_id':'first_product_id',
				'recommended_product_entity':'first_product_entity',
				'recommended_product_order':'first_product_order',
				'recommended_product_is_requested':'first_product_is_requested',#to do
				'recommended_product_requested_on':'first_product_requested_on',#to do
				'recommended_product_is_scheduled':'first_product_is_scheduled',#to do
				'recommended_product_scheduled_on':'first_product_scheduled_on',#to do
				'recommended_product_is_approved':'first_product_is_approved',#to do
				'recommended_product_approved_on':'first_product_approved_on',#to do
				'recommended_product_status_bank':'first_product_status_bank',
				'recommended_product_status_bank_detail':'first_product_status_bank_detail',
				'recommended_product_status_bank_updated_on':'first_product_status_bank_updated_on',
				'recommended_product_is_formalized':'first_product_is_formalized',
				'recommended_product_formalized_on':'first_product_formalized_on',
				#
				'second_recommended_product_name':'second_product_name',
				'second_recommended_product_id':'second_product_id',
				'second_recommended_product_entity':'second_product_entity',
				'second_recommended_product_order':'second_product_order',
				'second_recommended_product_is_requested':'second_product_is_requested',#to do
				'second_recommended_product_requested_on':'second_product_requested_on',#to do
				'second_recommended_product_is_scheduled':'second_product_is_scheduled',#to do
				'second_recommended_product_scheduled_on':'second_product_scheduled_on',#to do
				'second_recommended_product_is_approved':'second_product_is_approved',#to do
				'second_recommended_product_approved_on':'second_product_approved_on',#to do
				'second_recommended_product_status_bank':'second_product_status_bank',
				'second_recommended_product_status_bank_detail':'second_product_status_bank_detail',
				'second_recommended_product_status_bank_updated_on':'second_product_status_bank_updated_on',
				'second_recommended_product_is_formalized':'second_product_is_formalized',
				'second_recommended_product_formalized_on':'second_product_formalized_on',
				#
				'third_recommended_product_name':'third_product_name',
				'third_recommended_product_id':'third_product_id',
				'third_recommended_product_entity':'third_product_entity',
				'third_recommended_product_order':'third_product_order',
				'third_recommended_product_is_requested':'third_product_is_requested',#to do
				'third_recommended_product_requested_on':'third_product_requested_on',#to do
				'third_recommended_product_is_scheduled':'third_product_is_scheduled',#to do
				'third_recommended_product_scheduled_on':'third_product_scheduled_on',#to do
				'third_recommended_product_is_approved':'third_product_is_approved',#to do
				'third_recommended_product_approved_on':'third_product_approved_on',#to do
				'third_recommended_product_status_bank':'third_product_status_bank',
				'third_recommended_product_status_bank_detail':'third_product_status_bank_detail',
				'third_recommended_product_status_bank_updated_on':'third_product_status_bank_updated_on',
				'third_recommended_product_is_formalized':'third_product_is_formalized',
				'third_recommended_product_formalized_on':'third_product_formalized_on',
				#
				'additional_recommended_product_id':'additional_product_id',
				'additional_recommended_product_name':'additional_product_name',
				'additional_recommended_product_entity':'additional_product_entity',
				'additional_recommended_product_order':'additional_product_order',
				'additional_recommended_product_is_requested':'additional_product_is_requested',
				'additional_recommended_product_requested_on':'additional_product_requested_on',
				'additional_recommended_product_is_scheduled':'additional_product_is_scheduled',
				'additional_recommended_product_scheduled_on':'additional_product_scheduled_on',
				'additional_recommended_product_is_approved':'additional_product_is_approved',
				'additional_recommended_product_approved_on':'additional_product_approved_on',
				'additional_recommended_product_status_bank':'additional_product_status_bank',
				'additional_recommended_product_status_bank_detail':'additional_product_status_bank_detail',
				'additional_recommended_product_status_bank_updated_on':'additional_product_status_bank_updated_on',
				'additional_recommended_product_is_formalized':'additional_product_is_formalized',
				'additional_recommended_product_formalized_on':'additional_product_formalized_on',
				#pending
				'base_rocket_Antiguedad Laboral':'Employment Time',
				'base_rocket_Experiencia Crediticia':'Credit Time',
				'base_rocket_Pagos atrasados':'Delayed Payments',
				#'santander_sel_Estatus final':'status_bank',
				#'Dictamen':'status_bank_detail',
				'santander_seg_TokenEfl':'Token',
				'santander_base_Semaforo':'Light',
				#'santander_seg_Formalizadas':'Product Formalization',
				'santander_seg_CodigoCliente':'Client Code',
				'base_rocket_Dispositivo':'tech_device',
				'base_rocket_Navegador':'tech_browser',
				'base_rocket_Sistema Operativo':'tech_operating_system',
				'base_rocket_Fuente':'utm_source',
				'base_rocket_Medio':'utm_medium',
				'base_rocket_Termino':'utm_term',
				'base_rocket_UTM Cont':'utm_content',
				'base_rocket_Campana':'utm_campaign',
				'Referal_Code':'Referal_Code',
				#testing
				'base_rocket_Universidad':'base_rocket_Universidad',
				'santander_sel_Estatus final':'santander_sel_Estatus final',
				'base_rocket_BCC2':'base_rocket_BCC2',
				'base_rocket_BCC3':'base_rocket_BCC3'
				}
	return columns
	

