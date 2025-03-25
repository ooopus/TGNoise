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

# 多目标消息设置
# 格式：{
#     "目标ID或用户名": {"interval_seconds": 发送间隔（秒）, "max_messages": 最大发送数量（可选）}
# }
TARGETS = {
    "@group1": {"interval_seconds": 60, "max_messages": 100},  # 每60秒发送一次，最多发送100条
    "-1001234567890": {"interval_seconds": 300},  # 每300秒发送一次，无限制发送
    "@channel1": {"interval_seconds": 3600, "max_messages": 10}  # 每小时发送一次，最多发送10条
}

# 消息模板设置
MESSAGE_TEMPLATES = [
    "当前时间: {time}",
    "今天是 {date}",
    "这是一条自动生成的消息 - {datetime}",
]  # 消息模板列表，支持时间格式化：{time}, {date}, {datetime}

# 会话文件路径
SESSION_FILE_PATH = "~/.config/TGNoise/sessions/default.session"  # 在此处填入您的会话文件路径