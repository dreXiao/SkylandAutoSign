import logging
import os
import token
from datetime import date

import requests


def push_napcat(all_logs: list[str]):
    """
    Napcat
    """
    napcat_token = os.environ.get("NAPCAT_TOKEN", "").strip()
    group_id = os.environ.get("GROUP_ID", "").strip()
    # if not napcat_token:
    #     return

    title = f"运行结果 - {date.today().strftime('%Y-%m-%d')}"
    desp = "\n".join(all_logs) if all_logs else "无输出，请检查日志文件。"
    message = f"{title}\n{desp}"
    api = "https://api.napcat.noyoru.top/send_msg"
    if napcat_token:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {napcat_token}",
        }
    else:
        headers = {
            "Content-Type": "application/json",
        }
    try:
        payload = {
            "message_type": "group",
            "group_id": group_id,
            "message":  message,
        }
        print(headers, payload)
        r = requests.post(api, headers=headers, json=payload)
        if r.status_code != 200:
            logging.error(f"Napcat 消息发送失败，HTTP {r.status_code} {r.text}")
    except Exception as e:
        logging.error("Napcat 消息发送异常", exc_info=e)
