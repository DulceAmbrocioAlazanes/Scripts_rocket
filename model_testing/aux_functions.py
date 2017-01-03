import pandas as pd

def fillna_with_zeros(csvfile):
	data 	=	pd.DataFrame.from_csv(csvfile,header=0)
	data['Expected_result'].fillna(0.0,inplace=True)
	data['Expected_list'].fillna('[0]',inplace=True)
	data.to_csv(csvfile,sep=",")
	return


fillna_with_zeros('MATRIX_GENERATOR/TEST_MATRIX/students_work/2/37/3/matrix_old.csv')
#fillna_with_zeros('MATRIX_GENERATOR/TEST_MATRIX/employees/8/56/2/matrix.csv')

