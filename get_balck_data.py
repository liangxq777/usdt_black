import requests
import time
import json
from tronpy.keys import to_base58check_address
import os
import datetime

api_key = "UW4YVBF3QQ14RWE1679V9CJ9XJ2759HUPX"
usdt_contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"


for i in range(2):
    print(i)
    if i == 0:
        topic = "0x42e160154868087d6bfdc0ca23d96a1c1cfa32f1b72ba9ba27b69b98a0d819dc"
        on_off = "black"
    else:
        topic = "0xd7e9ec6e6ecd65492dce6bf513cd6867560d49544421d0783ddf06e76c24470c"
        on_off = "remove"
    page = 1
    all_data = []
    while True:
        url = f"https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=0&toBlock=latest&address={usdt_contract_address}&topic0={topic}&page={page}&offset=1000&apikey={api_key}"

        response = requests.get(url)
        data = response.json()

        if data["status"] == "1":
            # 处理返回的事件信息
            events = data["result"]
            for event in events:

                transactionHash = event["transactionHash"]
                data_address = "0x" + event["data"][2:][-40:]
                timeStamp = int(event["timeStamp"][2:], 16)
                all_data += [
                    {
                    "hash": transactionHash,
                    "black_address": data_address,
                    "black_time": timeStamp
                    }
                ]
        else:
            print("API 请求失败：", data["message"])
            break
        page += 1


    with open(f'eth_{on_off}.json', 'w') as json_file:
        json.dump(all_data, json_file, indent=4)



usdt_contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
api_key = "1e46cdaf-24a8-4803-8d5d-33fde29e40e3"


for i in range(2):
    if i == 0:
        event_name = "AddedBlackList"
        on_off = "black"
    else:
        event_name = "RemovedBlackList"
        on_off = "remove"
    min_block_timestamp = 1555400628000
    max_block_timestamp = int(time.time() * 1000)
    all_data = []
    while True:
        url = (f"https://api.trongrid.io/v1/contracts/{usdt_contract_address}/events?min_block_timestamp={min_block_timestamp}&max_block_timestamp={max_block_timestamp}&event_name={event_name}&limit=200")

        headers = {
            'Content-Type': "application/json",
            'TRON-PRO-API-KEY': api_key
           }

        response = requests.get(url, headers=headers)
        data = response.json()
        events = data["data"]
        if events:
            for event in events:
                transaction_id = event["transaction_id"]
                hex_address = event["result"]["_user"]
                address = to_base58check_address(hex_address)
                block_timestamp = event["block_timestamp"]
                all_data += [
                    {
                    "hash": transaction_id,
                    "black_address": address,
                    "black_time": block_timestamp / 1000
                    }
                ]

        else:
            break
        max_block_timestamp = block_timestamp - 1
    with open(f'tron_{on_off}.json', 'w') as json_file:
            json.dump(all_data, json_file, indent=4)






repo_url = 'https://github.com/liangxq777/usdt_black.git'  # 替换为你的GitHub仓库URL
local_path = '.'  # 替换为你想要克隆仓库的本地路径

if not os.path.exists(local_path):
    os.makedirs(local_path)
    os.system(f'git clone {repo_url} {local_path}')

now = datetime.datetime.now().strftime('%Y-%m-%d')
os.chdir(local_path)  # 进入本地仓库目录
os.system('git add .')  # 添加所有更改的文件
os.system(f'git commit -m {now}')# 提交更改

os.system('git push')  # 推送更改到GitHub