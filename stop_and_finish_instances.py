import settings
import boto3
import argparse
import pickle

print('Start stopping and finishing instances.')

# コマンドライン引数を受け取る
parser  = argparse.ArgumentParser()
parser.add_argument('--INSTANCE_IDS_FILE_NAME', type=str, help='停止・終了するインスタンスが保存されたファイルの名前')
args = parser.parse_args()
INSTANCE_IDS_FILE_NAME = args.INSTANCE_IDS_FILE_NAME
filepath = 'created_instance_ids_files/{}'.format(INSTANCE_IDS_FILE_NAME)

ec2 = boto3.resource('ec2')

# コマンドライン引数で指定したファイルから、終了対象のidのリストを読み取り、インスタンスを取得する
with open(filepath, 'r') as f:
    instance_list = list(map(
        lambda instance_id: ec2.Instance(id=instance_id),
        f.read().split(',')
        )
    )

# インスタンスを停止する
for instance in instance_list:
    instance.terminate()

# 全てのインスタンスが終了するまで待機する
for instance in instance_list:
    instance.wait_until_terminated()
    print('Stopping instance:{} is complete!'.format(instance.id))
    
print('Stop and start instances is complete!')