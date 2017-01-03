# -*- coding: utf-8 -*-
import pandas as pd
import curp
import load_data
import time
import functions

#load santander reports
ppl_santander_seg      	= 	load_data.load_santander_seg()
ppl_santander_sel	   	=	load_data.load_santander_sel()						
ppl_santander_baserckt	=	load_data.load_santander_baserckt()

"""
				ppl from Santander reports with PROCESS in SANTANDER
"""

#mege Santander reports
ppl_santander 		=	pd.merge(ppl_santander_seg,ppl_santander_sel,left_on='santander_seg_Foliointeligente',right_on='santander_sel_Folio_inteligente') 
ppl_santander 		=	pd.merge(ppl_santander,ppl_santander_baserckt,left_on='santander_sel_Folio_inteligente',right_on='santander_base_Folio_inteligente')
ppl_santander['santander_sel_Correo_SEL'] = ppl_santander['santander_sel_Correo_SEL'].map(lambda x: str(x).lower())
ppl_santander['santander_base_Correo electronico'] = ppl_santander['santander_base_Correo electronico'].map(lambda x: str(x).lower())
#ID
ppl_santander		= functions.extract_custom_field(ppl_santander,"santander_sel_Query String","ID","utm_id=",1)
#extract ID from utm_campaign, (call center utm)
ppl_santander		= functions.extract_custom_field(ppl_santander,"santander_sel_Query String","dummy_ID","utm_campaign=",1)
ppl_santander		= functions.extract_custom_field(ppl_santander,"dummy_ID","dummy_ID_dummy","&",0)
ppl_santander['dummy_ID_dummy']= [item if item !="Sitio" and item!='EFL' else '' for item in ppl_santander['dummy_ID_dummy']]
ppl_santander['ID']	= [id_natural if len(id_natural)>=10 else id_artificial for id_natural,id_artificial in zip(ppl_santander['ID'],ppl_santander['dummy_ID_dummy'])]
#extract ID from utm_content, (call center utm)
ppl_santander		= functions.extract_custom_field(ppl_santander,"santander_sel_Query String","dummy_ID","utm_content=",1)
ppl_santander		= functions.extract_custom_field(ppl_santander,"dummy_ID","dummy_ID_su","utm_content=",1)
ppl_santander['ID']	= [id_natural if len(id_natural)>=10 else id_artificial for id_natural,id_artificial in zip(ppl_santander['ID'],ppl_santander['dummy_ID_su'])]
#Channel
ppl_santander 		= functions.extract_custom_field(ppl_santander,"santander_sel_Query String","channel_dummy","utm_channel=",1)
ppl_santander 		= functions.extract_custom_field(ppl_santander,"channel_dummy","channel","&",0)

ppl_santander['Estatus de Identificacion'] 		=	['Identificado por utm' if len(identif)>=1 else 'No  Identificado por utm' for identif in ppl_santander['ID']]
ppl_santander['Dictamen']						=	ppl_santander['santander_base_Dictamen solicitud'].fillna(ppl_santander['santander_seg_Dictamen'])

#standarize products names
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='VISA CLASICA SANTANDER ZERO',value='Santander Zero (Estudiantes Universitarios)')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='FIESTA REWARDS ORO',value='Fiesta Rewards Oro')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='UNIK',value='Tarjeta de crédito Santander Free')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='AEROMEXICO BLANCA',value='Santander Aeroméxico Blanca')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='AEROMEXICO PLATINUM',value='Santander Aeroméxico Platinum')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='BLACK UNLIMITED',value='Black Unlimited')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='LIGHT',value='Santander Light')
ppl_santander['santander_seg_Producto']			=	ppl_santander['santander_seg_Producto'].replace(to_replace='SANTANDER-AMEX',value='Santander American Express')

#Refered by
ppl_santander									=	functions.extract_custom_field(ppl_santander,"santander_sel_Query String","Refered_by","utm_ref=",0)
#Referal code
ppl_santander['Referal_Code']					=	[functions.create_referal_code(rfc) for rfc in ppl_santander['santander_seg_RFC']]
#quitar acentos en Estatus Final
ppl_santander['santander_sel_Estatus final']	=	ppl_santander['santander_sel_Estatus final'].fillna("N/A")
ppl_santander['santander_sel_Estatus final']	=	[functions.strip_accents(status) if item!="N/A" else "N/A" for status in ppl_santander['santander_sel_Estatus final']]

#quitar acentos en Causa de rechazo
ppl_santander['santander_seg_CausaRechazo']		=	ppl_santander['santander_seg_CausaRechazo'].fillna('N/A')
ppl_santander['santander_seg_CausaRechazo']		=	[functions.strip_accents(causa) if causa!="N/A" else "N/A" for causa in ppl_santander['santander_seg_CausaRechazo']]
ppl_santander['santander_seg_CausaRechazo'] 	=	[causa.replace('A3','o') for causa in ppl_santander['santander_seg_CausaRechazo']]

#quitar acentos en Situacion
ppl_santander['santander_sel_Situacion']		=	ppl_santander['santander_sel_Situacion'].fillna('N/A')
ppl_santander['santander_sel_Situacion']		=	[functions.strip_accents(situacion) if situacion!="N/A" else "N/A" for situacion in ppl_santander['santander_sel_Situacion']]

#ppl_santander = ppl_santander.reset_index()
#ppl_santander= ppl_santander.drop_duplicates(subset=columns)

ppl_santander.to_csv('Santander_'+time.strftime("%d_%m_%Y")+'_with_referal_code_'+'.csv',encoding='utf-8',header=True,
							columns=['santander_sel_Folio_inteligente','santander_sel_Fecha Captura','santander_seg_Producto',
							'Estatus de Identificacion','santander_sel_Query String','channel','ID','santander_base_Nombre','santander_base_Paterno',
							'santander_base_Materno','santander_seg_RFC','santander_sel_Correo_SEL','santander_base_Telefono domicilio',
							'santander_base_Telefono celular','santander_seg_Universidad','santander_seg_Formalizadas',
							'santander_seg_CodigoCliente','santander_seg_TokenEfl','santander_seg_FechaEnvioToken',
							'santander_sel_Estatus final','santander_sel_Situacion','Dictamen','santander_seg_CausaRechazo',
							'santander_base_Resultado autenticacion','santander_base_Semaforo','Referal_Code'])

ppl_santander['santander_base_Fecha captura basica']		=	pd.to_datetime(ppl_santander['santander_base_Fecha captura basica'])
ppl_santander['santander_base_Fecha autenticacion']			=	pd.to_datetime(ppl_santander['santander_base_Fecha autenticacion'])
ppl_santander['santander_base_Fecha evaluacion']			=	pd.to_datetime(ppl_santander['santander_base_Fecha evaluacion'])
ppl_santander['santander_base_Fecha cierre venta']			=	pd.to_datetime(ppl_santander['santander_base_Fecha cierre venta'])

ppl_santander['Fecha_ultima_modif']							=	[max([datea,dateb,datec,dated]) for datea,dateb,datec,dated in zip(ppl_santander['santander_base_Fecha captura basica'],ppl_santander['santander_base_Fecha autenticacion'],ppl_santander['santander_base_Fecha evaluacion'],ppl_santander['santander_base_Fecha cierre venta'])]

ppl_santander.to_csv('Santander_special_'+time.strftime("%d_%m_%Y")+'.csv',encoding='utf-8',header=True,
							columns=['santander_sel_Folio_inteligente','santander_sel_Fecha Captura','santander_seg_Producto',
							'Estatus de Identificacion','santander_sel_Query String','channel','ID','santander_base_Nombre','santander_base_Paterno',
							'santander_base_Materno','santander_seg_RFC','santander_sel_Correo_SEL','santander_base_Telefono domicilio',
							'santander_base_Telefono celular','santander_seg_Universidad','santander_seg_Formalizadas',
							'santander_seg_CodigoCliente','santander_seg_TokenEfl','santander_seg_FechaEnvioToken',
							'santander_sel_Estatus final','santander_sel_Situacion','Dictamen','santander_seg_CausaRechazo',
							'santander_base_Resultado autenticacion','santander_base_Semaforo','Referal_Code','santander_seg_FechaFormalizacion','Fecha_ultima_modif'])



import code; code.interact(local=locals())

