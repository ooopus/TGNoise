#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件示例
存储Telegram API凭据和消息设置
请基于此模板创建config.py文件并填入您的配置
"""

# Telegram API凭据
# 从 https://my.telegram.org/auth 获取
API_ID = ""  # 在此处填入您的API ID
API_HASH = ""  # 在此处填入您的API Hash
PHONE = ""  # 在此处填入您的电话号码（带国家代码，如+8613800138000）

# 消息设置
GROUP_ID = ""  # 目标群组ID或用户名（如 -1001234567890 或 @groupname）
INTERVAL_SECONDS = 60  # 发送间隔（秒），默认为1小时
MAX_MESSAGES = None  # 最大发送消息数量，None表示无限制

# 消息模板设置
MESSAGE_TEMPLATES = [
    "当前时间: {time}",
    "今天是 {date}",
    "这是一条自动生成的消息 - {datetime}",
]  # 消息模板列表，支持时间格式化：{time}, {date}, {datetime}

# 会话文件路径
SESSION_FILE_PATH = "~/.config/TGNoise/sessions/default.session"  # 在此处填入您的会话文件路径