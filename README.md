# server_building_exercise_ec2_operarion

## 前提
- 複製元のインスタンスのイメージが作成済みで、イメージidがわかっている

## 設定
[.env](.env)にiamユーザーの認証情報を書く

## コマンド説明
### create_and_start_instances_from_image_id.py
- 個数と元イメージのidをコマンドライン引数で指定し、個数分EC2上にインスタンスを作成する
- フラグの説明
  - IMAGE_ID: 元となるイメージのid
  - COUNT: 作成するインスタンスの個数
  - INSTANCE_TYPE（任意）: 作成するインスタンスのタイプ（デフォルトは無料枠のt2.micro）
- 例
  ```
  python create_and_start_instances_from_image_id.py --IMAGE_ID ami-0ce727dd9e7ed7a47 --COUNT 10
  ```
- 完了時に```To stop and finish created instances, please run "python stop_and_finish_instances.py --INSTANCE_IDS_FILE_NAME=<timestamp>_created.txt"```が出力されるので、作成したインスタンスを停止する場合はこれを実行する

### stop_and_finish_instances.py
- インスタンス作成時に保存された、インスタンスidのテキストファイルのファイル名をコマンドライン引数で受け取り、該当するidのインスタンスを終了する
- フラグの説明
  - INSTANCE_IDS_FILE_NAME: インスタンス作成時に保存された、インスタンスidのテキストファイルのファイル名
  - 例
  ```
  python stop_and_finish_instances.py --INSTANCE_IDS_FILE_NAME=20210831_101227_created.txt
  ```