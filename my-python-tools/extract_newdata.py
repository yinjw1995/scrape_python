import json
import os
import requests
import re
import sent_info_to_feishu
def read_json_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"警告: {file_name} 是空的")
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"错误: 无法解析 {file_name}. 错误信息: {str(e)}")
        return {}
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_name}")
        return {}

# 读取 post_data.json 文件
post_data = read_json_file('post_data.json')

# 读取 config_info.json 文件
config_info = read_json_file('config_info.json')

if not post_data or not config_info:
    print("无法继续执行，请检查 JSON 文件")
    exit(1)

target_tweet_id = config_info['tweet_id']
new_tweet_id = post_data['timeline'][0]['tweet_id']  # 用于更新 config_info.json

for post in post_data['timeline']:
    current_tweet_id = post['tweet_id']
    
    if current_tweet_id == target_tweet_id:
        break
    
    # 提取 text
    text = post['text']
    text = re.sub(r'https?://t\.co/\S+', '', text).strip()
    print(f"Tweet ID: {current_tweet_id}")
    print(f"Text: {text}")
    
    image_paths = []
    # 检查是否有 media 和 photo
    if 'media' in post and 'photo' in post['media']:
        # 创建以 tweet_id 命名的文件夹
        folder_name = str(current_tweet_id)
        os.makedirs(folder_name, exist_ok=True)
        
        # 下载并保存所有图片
        for i, photo_url in enumerate(post['media']['photo']):
            response = requests.get(photo_url["media_url_https"])
            if response.status_code == 200:
                file_name = f"{folder_name}/photo_{i+1}.jpg"
                with open(file_name, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Saved: {file_name}")
                image_paths.append(file_name)
                print(image_paths)
    
    sent_info_to_feishu.send_message_to_feishu(text,image_paths)
    print("---")

# 更新 config_info.json
config_info['tweet_id'] = new_tweet_id
with open('config_info.json', 'w', encoding='utf-8') as f:
    json.dump(config_info, f, ensure_ascii=False, indent=2)

print("Updated config_info.json with new tweet_id")