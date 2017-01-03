import load_data
import pandas as pd
from datetime import datetime

base_internal 							=	load_data.load_dbRocket()

#filter by device/operating system
base_internal 							=	base_internal[(base_internal['base_rocket_Sistema Operativo']!='mac') & (base_internal['base_rocket_Sistema Operativo']!='ios')]

#filter by date
base_internal['date']					=	pd.to_datetime(base_internal['base_rocket_Hora de finalizacion del formulario'])
date_min								= 	datetime.strptime('Jan 1 2016  12:00AM', '%b %d %Y %I:%M%p')
date_max								= 	datetime.strptime('Mar 31 2016  12:00AM', '%b %d %Y %I:%M%p')
base_internal 							=	base_internal[(base_internal['date']>date_min)&(base_internal['date']<date_max)]

#filter by Employment type
employees 								=	base_internal[base_internal['base_rocket_Ocupacion']=='Trabajo en una empresa']	
students								=	base_internal[(base_internal['base_rocket_Ocupacion']=='Estudiante y trabaja')|(base_internal['base_rocket_Ocupacion']=='Estudiante')]

segunda									=	base_internal[(base_internal['base_rocket_Ocupacion']=='Independiente')|(base_internal['base_rocket_Ocupacion']=='Trabajo en una empresa')]
#---recalculate Exp Cred
today									=	datetime.now()
segunda['Recalculated_Credit_Exp']		=	[(credit_exp+int(((today-date).days)/30.)) for date,credit_exp in zip(segunda['date'],segunda['base_rocket_Experiencia Crediticia'])]
segunda									=	segunda[segunda['Recalculated_Credit_Exp']>=12]

#filter by credit type
#entidades_bancarias					=	['Liverpool','Bancoppel','Banco Azteca','Suburbia','']
#segunda								=	segunda[~segunda['base_rocket_Entidad donde tiene TC'].isin(entidades_bancarias)]

#filter by delayed payments
segunda									=	segunda[(segunda['base_rocket_Pagos atrasados']!='2')&(segunda['base_rocket_Pagos atrasados']!='3')&(segunda['base_rocket_Pagos atrasados']!='4')&(segunda['base_rocket_Pagos atrasados']!='5')&(segunda['base_rocket_Pagos atrasados']!='Alguna vez')&(segunda['base_rocket_Pagos atrasados']!='Aun estoy atrasado')]


import code; code.interact(local=locals())

"""
#filter by Request_product/No request porduct

"""


#ramdom sample
data									=	pd.DataFrame()
data									= 	data.append(students.sample(n=5000,random_state=2017))
#data 									=	data.append(employees_request_product.sample(n=1000,random_state=1986))
#data 									=	data.append(employees_no_request_product.sample(n=1000,random_state=1986))
#data 									=	data.append(students_request_product.sample(n=1000,random_state=1986))
#data 									=	data.append(students_no_request_product.sample(n=1000,random_state=1986))

#savedata
cols									=	['base_rocket_ID','base_rocket_Salida','base_rocket_Telefono',
											'base_rocket_Correo electronico','base_rocket_Fecha de visita',
											'base_rocket_Ocupacion']
data.to_csv('data_gastos_diarios_Q1_universitarios.csv',columns=cols,encoding='utf-8')
import code; code.interact(local=locals())
