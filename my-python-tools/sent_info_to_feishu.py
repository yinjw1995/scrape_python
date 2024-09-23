#https://open.feishu.cn/open-apis/bot/v2/hook/f93875c1-9739-4e24-b677-cf56e83c6f3a
#"Authorization": "Bearer t-g1049ndfL7MK5XPGXZOKUUH7R3QUPVCZEDPIMGVW",  # 替换为您的访问令牌
#t-g1049nfo6WKRG3CZDC4RNU6VI5IVNARRSK3ZK7A5
import requests
import json
from datetime import datetime
from requests_toolbelt import MultipartEncoder

def get_token_frome_feishu():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    app_id = "cli_a67a44c2a23d500b"
    app_secret = "8Uz2F2izhk20Zk3R5LPhsMFMcpwmZMTz"
    headers = {
        
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url=url, data=json.dumps(payload), headers=headers).json()
    response_token = response['tenant_access_token']
    print('get token from feishu:',response_token)   
    return response_token


def upload_image_to_feishu(picturePath,token):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    #token = get_token_frome_feishu()
    #token = "t-g1049nfo6WKRG3CZDC4RNU6VI5IVNARRSK3ZK7A5"
    print(token)
    headers = {
        "Authorization": "Bearer "+token,  # 替换为您的访问令牌
        "Content-Type": "application/json"
    }
    form = {
        "image_type": "message",
        "image": (open(picturePath.replace('/', '\\'), 'rb'))
    }
    multi_form = MultipartEncoder(form)
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST",url=url, data=multi_form, headers=headers).json()
    print(response)
    image_key = response['data']['image_key']
    print(image_key)
    return image_key



def send_message_to_feishu(text, image_paths=None):
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/f93875c1-9739-4e24-b677-cf56e83c6f3a"
    token = get_token_frome_feishu()
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": text
                            }
                        ]
                    ]
                }
            }
        }
    }
    
    if image_paths:
        for image_path in image_paths:
            image_key = upload_image_to_feishu(image_path,token)
            payload['content']['post']['zh_cn']['content'][0].append(
                {
                    "tag": "img",
                    "image_key": image_key
                })
            
            
            #requests.post(url=webhook_url, data=json.dumps(payload1), headers=headers)
    
    print(payload)

    
    
    response = requests.post(url=webhook_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        print("消息发送成功!")
    else:
        print(f"消息发送失败。状态码: {response.status_code}, 响应: {response.text}")

# 使用示例
if __name__ == "__main__":
    message = "这是一条来自Python脚本的测试消息!"
    send_message_to_feishu(message,['1837018838568976559/screenshot-20240923-155930.png','1837018838568976559/screenshot-20240923-155939.png'])