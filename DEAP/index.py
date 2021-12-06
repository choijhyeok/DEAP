import os
import sys
import numpy as np

from flask import Flask, jsonify, request, Response, abort

import deap
import time
import warnings

import joblib
import pandas as pd
from io import StringIO
import json
import boto3
from boto3.session import Session
import botocore

import glob

# --- custom package -------#
from . import new_environment
from . import package_all
# --- custom package -------#

import sys
import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)


aws_credential_info = {"aws_access_key_id" : None, "aws_secret_access_key" : None, "bucket_name" : None, "region" : None} # aws 정보 담을 dict 생성
additional_info  =  {"output_data_dir" : None, "base_dir" : None} #경로 담을 dict 생성

def check_Nones(dict_file):
	value = 0
	for key in dict_file:
		if dict_file[key] == None:
			value = -1

	return value

def upload_files_from_RESTful_to_S3(local_file, s3_file):
	session = Session(aws_access_key_id=aws_credential_info['aws_access_key_id'], aws_secret_access_key=aws_credential_info['aws_secret_access_key'])

	try:
		session.resource('s3').Bucket(aws_credential_info['bucket_name']).upload_file(local_file, s3_file)
		print("Upload Successful")
		return True
	except FileNotFoundError:
		print("The local file was not found")
		return False
	except NoCredentialsError:
		print("Credentials not available")
		return False



# import sys

# f=open('t.txt','w')

# stdout=sys.stdout # 표준출력 저장(백업 개념)

# sys.stdout=f



# print('테스트 메시지1')

# print('테스트 메시지2')

# print('테스트 메시지3')



# f.close()

# sys.stdout=stdout


@app.route('/receive', methods=['POST']) #localhost:50000/receive  post 방법 사용
def process_data():
	data = json.loads(request.data) # json 데이터 읽어와서

	aws_credential_info['aws_access_key_id'] = data.get("aws_access_key_id", None)
	aws_credential_info['aws_secret_access_key'] = data.get("aws_secret_access_key", None)
	aws_credential_info['bucket_name'] = data.get("bucket_name", None)
	aws_credential_info['region'] = data.get("region", None)

	additional_info['output_data_dir'] = data.get("output_data_dir", None)
	additional_info['base_dir'] = data.get("base_dir", None)

	check_stop_1 = check_Nones(aws_credential_info) #비어있으면 -1 아니면 0
	check_stop_2 = check_Nones(additional_info) #비어있으면 -1 아니면 0

	if check_stop_1 < 0 or check_stop_2 < 0: #둘중 어느거라도 -1이면 404
		return abort(404)
	else:
		env = new_environment.Env()
		real_data = env.data.copy()
		real_data.to_csv('{}'.format(additional_info['base_dir'])+'data_csv/원본데이터.csv',index=False)

		log_data = open('{}'.format(additional_info['base_dir'])+'data_log/mapping_process_log.txt', 'w')
		stdout=sys.stdout
		sys.stdout=log_data

		def_list = [package_all.region_mapping,package_all.logistics_mapping,package_all.nearest_logistics_mapping]

		for d,i in enumerate(['region_mapping','logistics_mapping','nearest_logistics_mapping']):
			print()
			print('-'*150)
			print('\n지역 우선 맵핑\n') if d == 0 else print('\n물류비 절감 우선 맵핑\n') if d == 1 else print('\n근접 물류비 절감 우선 맵핑\n')
			
			globals()['choice_{}'.format(d)] = def_list[d](real_data,env)
			globals()['choice_{}'.format(d)].to_csv('{}'.format(additional_info['base_dir'])+'data_csv/{}.csv'.format(i),index=False)
			

			if len(globals()['choice_{}'.format(d)]):
				
				print('-'*150)
				print('\n 유전 알고리즘을 수행합니다.')		

				package_all.mapping(globals()['choice_{}'.format(d)],d)

				png_list = glob.glob('{}'.format(additional_info['base_dir'])+'data_image/'+i+'/*.png')
			
				if len(png_list):
					for j in range(len(png_list)):
						upload_files_from_RESTful_to_S3('{}'.format(png_list[j]),'{}/'.format(additional_info['output_data_dir'])+i+'/{}'.format(png_list[j].split(i+'/')[1]))
				else:
					pass
			
			else:
				print('매칭결과가 없습니다.')

		log_data.close()
		sys.stdout=stdout

		csv_list = glob.glob('{}'.format(additional_info['base_dir'])+'data_csv/*.csv')
		for i in csv_list:
			upload_files_from_RESTful_to_S3('{}'.format(i),'{}/'.format(additional_info['output_data_dir'])+'csv/{}'.format(i.split('data_csv/')[1]))


		upload_files_from_RESTful_to_S3('{}'.format(additional_info['base_dir'])+'data_log/mapping_process_log.txt','{}/log/mapping_process_log.txt'.format(additional_info['output_data_dir']))

	aws_credential_info.clear()
	additional_info.clear()

	return jsonify("Process completed")

	

if __name__ == "__main__":
	app.run()
