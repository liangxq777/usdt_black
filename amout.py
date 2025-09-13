import json

file_name = "/home/ubuntu/black/usdt_black/tron_black.json"

with open(file_name, "r", encoding="utf-8") as f:
    data = json.load(f)

# print(len(data))

for line in data:
    tx = line.get("hash")
    print(tx)