# -*- coding: utf-8 -*-
import load_data
import pandas as pd
from datetime import datetime
import time
import functions

base_internal 							=		load_data.load_dbRocket_V4(False)
print "len(internal):",len(base_internal)

#filter by date
base_internal['date']					=	pd.to_datetime(base_internal['base_rocket_Hora de finalizacion del formulario'])

date_min								= 	datetime.strptime('Apr 01 2015  12:00AM', '%b %d %Y %I:%M%p')
date_max								= 	datetime.strptime('Dec 22 2016  12:00AM', '%b %d %Y %I:%M%p')
base_internal 							=	base_internal[(base_internal['date']>=date_min)&(base_internal['date']<=date_max)]

#filter by Employment type
employees								=	base_internal[(base_internal['base_rocket_Ocupacion']=='Estudiante y trabaja')|(base_internal['base_rocket_Ocupacion']=='Trabajo en una empresa')]	

#filter by income
employees								=	employees[(employees['base_rocket_Ingresos']>=15000)]

#filter by Credit Experience


#---recalculate Exp Cred
today									=	datetime.now()
employees['Recalculated_Credit_Exp']	=	[(credit_exp+int(((today-date).days)/30.)) for date,credit_exp in zip(employees['date'],employees['base_rocket_Experiencia Crediticia'])]

employees								=	employees[employees['Recalculated_Credit_Exp']>=18]

#filter by credit type
entidades_bancarias						=	['Bancomer']

employees								=	employees[~employees['base_rocket_Entidad donde tiene TC'].isin(entidades_bancarias)]

#filter by delayed payments
employees								=	employees[(employees['base_rocket_Pagos atrasados']!='2')&(employees['base_rocket_Pagos atrasados']!='3')&(employees['base_rocket_Pagos atrasados']!='4')&(employees['base_rocket_Pagos atrasados']!='5')&(employees['base_rocket_Pagos atrasados']!='Alguna vez')&(employees['base_rocket_Pagos atrasados']!='Aun estoy atrasado')]

#filter by need
employees								=	employees[employees['base_rocket_Para que la quieres']!='Pregunta Descontinuada']

#ramdom sample
data									=	pd.DataFrame()
#data 									=	data.append(employees.sample(n=4000,random_state=1986))
data									=	employees

#conditionning
data['base_rocket_Para que la quieres']	=	data['base_rocket_Para que la quieres'].fillna('no_data')

data									=	data[(data['base_rocket_Para que la quieres']!='no_data')&(data['base_rocket_Para que la quieres']!='ola ke ase')]
data['base_rocket_Para que la quieres']	=	[need if type(need)==int or type(need)==float else need.encode('utf-8') for need in data['base_rocket_Para que la quieres']]
data['base_rocket_Subcategoria']		=	data['base_rocket_Subcategoria'].fillna('no_data')
data['base_rocket_Subcategoria']		=	[subneed if type(subneed)==int or type(subneed)==float else subneed.encode('utf-8') for subneed in data['base_rocket_Subcategoria']]

#Need & Subneed from code to text
data['Necesidad']						=	data['base_rocket_Para que la quieres'].map(lambda need_code: functions.set_user_need(str(need_code)))
data['Subnecesidad']					=	data['base_rocket_Subcategoria'].map(lambda subneed_code: functions.set_user_subneed(str(subneed_code)))
										
#remove already send users
users_send								=	pd.read_csv('/home/dulce/Downloads/BBVA/data_BBVA_06_12_2016.csv')
users_send								=	users_send.append(pd.read_csv('/home/dulce/Downloads/BBVA/data_BBVA_15_12_2016.csv'))
users_send								=	users_send.append(pd.read_csv('/home/dulce/Downloads/BBVA/data_BBVA_27_12_2016.csv'))

ids_users_send							=	list(users_send['base_rocket_Correo electronico'].unique())

final_users								=	data[~data['base_rocket_Correo electronico'].isin(ids_users_send)]

#savedata
cols									=	['base_rocket_ID','base_rocket_Salida','base_rocket_Telefono',
											'base_rocket_Correo electronico','base_rocket_Fecha de visita',
											'base_rocket_Ocupacion','base_rocket_Ingresos',
											'base_rocket_Ingresos','base_rocket_Para que la quieres',
											'Necesidad','base_rocket_Subcategoria','Subnecesidad']

path = 'BBVA/data_BBVA_'+time.strftime("%d_%m_%Y")+'.csv'									
final_users.to_csv(path,columns=cols,encoding='utf-8')
import code; code.interact(local=locals())

