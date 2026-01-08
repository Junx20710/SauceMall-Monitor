import requests
import os
import sys
from utils.logger import logger

def send_feishu_notification(webhook_url, title, text, success=True):
    """
    发送飞书 (Lark) 机器人通知
    """
    if not webhook_url:
        logger.warning("未配置 FEISHU_WEBHOOK 环境变量，跳过发送通知。")
        return

    # 构造颜色和卡片内容
    color = "green" if success else "red"
    status_text = "✅ 构建成功" if success else "❌ 构建失败"
    
    headers = {"Content-Type": "application/json"}
    
    # 飞书富文本卡片格式
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{title} - {status_text}"
                },
                "template": color
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": text
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "来自 GitHub Actions 自动构建"
                        }
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            logger.info("飞书通知发送成功")
        else:
            logger.error(f"飞书通知发送失败: {response.text}")
    except Exception as e:
        logger.error(f"发送通知时发生异常: {e}")

if __name__ == "__main__":
    # 从命令行参数获取状态 (可以在 CI yml 里传)
    # python utils/notification.py success "详细报告: http://xxx"
    
    webhook = os.getenv("FEISHU_WEBHOOK")
    
    if len(sys.argv) > 2:
        status_arg = sys.argv[1] # "success" or "failure"
        message_arg = sys.argv[2]
        
        is_success = (status_arg == "success")
        send_feishu_notification(
            webhook, 
            "SauceMall 监控系统", 
            message_arg, 
            success=is_success
        )
    else:
        # 本地测试用
        print("Usage: python utils/notification.py [success|failure] [message]")
