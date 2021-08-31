import settings
import boto3
import argparse
import datetime
import time
import json

start = time.time()
print('Start creating and starting instances.')

# コマンドライン引数を受け取る
parser  = argparse.ArgumentParser()
parser.add_argument('--IMAGE_ID', type=str, help='コピー元のインスタンスのイメージID')
parser.add_argument('--COUNT', type=int, help='作成するインスタンスの数')
parser.add_argument('--INSTANCE_TYPE', type=str, default='t2.micro', help='インスタンスの種類（デフォルトは無料枠のt2.micro）')
args = parser.parse_args()
IMAGE_ID = args.IMAGE_ID
COUNT = args.COUNT
INSTANCE_TYPE = args.INSTANCE_TYPE

ec2 = boto3.resource('ec2')

# コマンドライン引数で受け取った条件でインスタンスを作成・スタートする
instances = ec2.create_instances(
    ImageId=IMAGE_ID,
    InstanceType=INSTANCE_TYPE,
    MaxCount=COUNT,
    MinCount=COUNT
)

# インスタンスを停止させるためにidとipアドレスなどの情報を保持する
instance_info_dic = {}

# idを保持しながら、全てのインスタンスの起動が終わるまで待機する
for instance in instances:
    instance_id = instance.id
    instance.wait_until_running()
    instance_info = ec2.Instance(instance_id)
    instance_info_dic[instance_id] = {'public_ip_address': instance_info.public_ip_address}
    print('Starting instance:{} is complete!'.format(instance_id))

# インスタンスの情報を、created_instance_ids_files/<timestamp>_created.jsonに保存する
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = '{}_created.json'.format(timestamp)
filepath = 'created_instance_ids_files/{}'.format(filename)
json.dump(instance_info_dic, open(filepath, 'w'), indent=4)
    
print(
'''
Create and start instances is complete!
To stop and finish created instances,
please run "python stop_and_finish_instances.py --INSTANCE_IDS_FILE_NAME={}"
'''.format(filename)
)

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")