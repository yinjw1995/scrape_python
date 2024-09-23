import http.client
import json  # 添加json模块

conn = http.client.HTTPSConnection("twitter-api45.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2d6315cc78msh3876fba1a7f15ffp1e2400jsn406c1b4caeb3",
    'x-rapidapi-host': "twitter-api45.p.rapidapi.com"
}

conn.request("GET", "/timeline.php?screenname=myfxtrader", headers=headers)

res = conn.getresponse()
data = res.read()

#print(data.decode("utf-8"))
# 解析JSON数据并格式化打印
parsed_data = json.loads(data.decode("utf-8"))

#print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
# 将数据保存为JSON文件
with open('post_data.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)

print("数据已保存到 post_data.json 文件中")