import os
import sys
import argparse
import warnings
from configparser import ConfigParser 
from time import gmtime, strftime
import json
import requests
import random
import string

from new_environment import *

def send_request(args):
	# AWS key 
	boto_default_session = boto3.setup_default_session()
	boto_session = boto3.Session(botocore_session=boto_default_session, region_name="ap-northeast-2")
	credentials = boto_session.get_credentials()

	# RESTful 
	project_name_updated = 'data/' + args.project_name + '-' + strftime("%Y-%m-%d-%H-%M-%S%z", gmtime())  # 'data/sklearn-pca-AMI-EC2-현재 연도 날짜 월 시간'
	output_data_dir =  project_name_updated + "/output_data" #'sklearn-pca-AMI-EC2/output_data'

	data = {}	  #dict 생성 해당하는 정보들을 담음
	data['aws_access_key_id'] = credentials.access_key 
	data['aws_secret_access_key'] = credentials.secret_key
	data['bucket_name'] = args.bucket_name
	data['region'] = boto_session.region_name
	data['output_data_dir'] = output_data_dir
	data['base_dir'] = args.base_dir


	
	headers = {'Content-Type': 'application/json',}
	url = 'http://' + args.host + ':' + args.port + '/receive'


	response = requests.post(url, headers=headers, data=json.dumps(data))
	
	
	if response.status_code == 200: #200뜨면 문제없
		print('DEAP successfully processed!')
	elif response.status_code == 404: # 요청에러
		print('Wrong Request Found.')
	
	# no longer store credentials  요청이 끝나서 id,secret_key 무작위 변경
	data['aws_access_key_id'] =  ''.join(random.choice(string.digits+string.ascii_letters) for i in range(24))
	data['aws_secret_access_key'] =  ''.join(random.choice(string.digits+string.ascii_letters) for i in range(24))

	# dump this for other processes
	with open(args.json_prefix + 'DEAP.json', 'w') as outfile:  #현재위치에 json 파일 저장
		json.dump(data, outfile)

	# flushing
	data.clear()

if __name__ == '__main__':
	warnings.filterwarnings("ignore", category=FutureWarning)

	parser = argparse.ArgumentParser()
	
	# usage
	# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
	parser.add_argument('--json_prefix', type=str, default="this_path")
	parser.add_argument('--bucket_name', type=str, default="datascience-gsitm-cjh")
	parser.add_argument('--project_name', type=str, default="DEAP")
	parser.add_argument('--base_dir', type=str, default="/usr/src/app/")
	parser.add_argument('--host', type=str, default='localhost')
	parser.add_argument('--port', type=str, default="54321")

	args, _ = parser.parse_known_args()

	send_request(args)	