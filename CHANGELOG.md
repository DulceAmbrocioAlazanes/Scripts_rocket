# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.0] - 2017-01-03
### Added
**Model_testing** this directory contains the following scripts:
- **MATRIX_GENERATOR/generator.py**: creates the test matrices in TEST_MATRIX
- **MATRIX_GENERATOR/TEST_MATRIX**: contains the test matrices for students, employees, housewifes, etc
- **pruebas_modelo.py**: this script runs the testing
- **module_request.py**: this script is called by pruebas_modelo.py to execute the testing to one of the available environments (local, prod,develop,stage).  

**reports** this directory contains the following scripts:
- **create_bd_bancomer.py**: this script contains the special filters to create bd for BBVA.
- **create_bd_gastos_diarios.py**: this script contains the bnecessary filters to create bd for gastos diarios.
- **create_complete_info_to_fill_new_bd.py**: this script create 3 groups of users to fill postgress bd with cassandra data.
- **create_smart_merge_santander.py**: this script merge the 3 reports from santander and creates a resume.
- **functions.py**: this script contains functions that are common to all scripts.
- **generate_report_for_Autopilot.py**: This script generates the input for autopilot acording to an special layout already defined.
- **load_data.py**:this script contains the functios to load data (V3 or V4)
	 

