import settings
import boto3
import argparse
import pickle
import time
import json

start = time.time()

print('Start stopping and finishing instances.')

# コマンドライン引数を受け取る
parser  = argparse.ArgumentParser()
parser.add_argument('--INSTANCE_IDS_FILE_NAME', type=str, help='停止・終了するインスタンスが保存されたファイルの名前')
args = parser.parse_args()
INSTANCE_IDS_FILE_NAME = args.INSTANCE_IDS_FILE_NAME
filepath = 'created_instance_ids_files/{}'.format(INSTANCE_IDS_FILE_NAME)

ec2 = boto3.resource('ec2')

instance_info = json.load(open(filepath, 'r')) 
instances = [ec2.Instance(id=instance_id) for instance_id in instance_info.keys()]

# インスタンスを停止する
for instance in instances:
    instance.terminate()

# 全てのインスタンスが終了するまで待機する
for instance in instances:
    instance.wait_until_terminated()
    print('Stopping instance:{} is complete!'.format(instance.id))
    
print('Stop and start instances is complete!')
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")