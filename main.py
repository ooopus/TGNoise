#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram消息定时发送脚本
使用Telethon库在特定Telegram群组中定期发送自定义消息
"""

import os
import time
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputPeerChannel
from telethon.errors import SessionPasswordNeededError, FloodWaitError
import config
from message_generator import MessageGenerator

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramMessageSender:
    def __init__(self, api_id, api_hash, phone, username=None):
        """
        初始化Telegram客户端
        :param api_id: Telegram API ID
        :param api_hash: Telegram API Hash
        :param phone: 电话号码（带国家代码，如+8613800138000）
        :param username: 用户名（可选）
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.username = username
        self.client = None
        
    async def connect(self):
        """
        连接到Telegram
        """
        # 创建会话文件名
        session_file = config.SESSION_FILE_PATH or self.username or self.phone
        
        # 创建客户端实例，不接收历史消息
        self.client = TelegramClient(session_file, self.api_id, self.api_hash, receive_updates=False)
        
        # 连接到Telegram服务器
        await self.client.connect()
        
        # 检查是否已经授权
        if not await self.client.is_user_authorized():
            logger.info("未授权，开始登录流程...")
            await self.client.send_code_request(self.phone)
            try:
                # 请求用户输入验证码
                verification_code = input("请输入Telegram发送的验证码: ")
                await self.client.sign_in(self.phone, verification_code)
            except SessionPasswordNeededError:
                # 如果启用了两步验证，则需要输入密码
                password = input("请输入两步验证密码: ")
                await self.client.sign_in(password=password)
        
        logger.info("成功登录Telegram")
        return self.client
    
    async def send_message_to_group(self, group_id, message):
        """
        向指定群组发送消息
        :param group_id: 群组ID或用户名
        :param message: 要发送的消息内容
        """
        try:
            # 发送消息
            await self.client.send_message(group_id, message)
            logger.info(f"消息已发送到 {group_id}")
            return True
        except FloodWaitError as e:
            # 处理频率限制错误
            wait_time = e.seconds
            logger.warning(f"发送频率过高，需要等待 {wait_time} 秒")
            await asyncio.sleep(wait_time)
            return False
        except Exception as e:
            logger.error(f"发送消息时出错: {e}")
            return False
    
    async def send_periodic_messages(self, group_id, message_generator, interval_seconds, max_messages=None):
        """
        定期向指定群组发送消息
        :param group_id: 群组ID或用户名
        :param message_generator: 消息生成器实例
        :param interval_seconds: 发送间隔（秒）
        :param max_messages: 最大发送消息数量（None表示无限制）
        """
        count = 0
        try:
            while max_messages is None or count < max_messages:
                # 生成并发送消息
                message = message_generator.generate()
                success = await self.send_message_to_group(group_id, message)
                
                if success:
                    count += 1
                    logger.info(f"已发送 {count} 条消息到 {group_id}" + 
                              (f"，共 {max_messages} 条" if max_messages else ""))
                
                # 等待指定的时间间隔
                logger.info(f"等待 {interval_seconds} 秒后发送下一条消息到 {group_id}...")
                await asyncio.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info(f"用户中断，停止向 {group_id} 发送消息")
        except Exception as e:
            logger.error(f"向 {group_id} 发送周期性消息时出错: {e}")
        finally:
            logger.info(f"总共向 {group_id} 发送了 {count} 条消息")

    async def send_messages_to_multiple_targets(self, targets, message_generator):
        """
        向多个目标发送消息
        :param targets: 目标配置字典，包含每个目标的interval_seconds和max_messages
        :param message_generator: 消息生成器实例
        """
        tasks = []
        for group_id, config in targets.items():
            task = asyncio.create_task(
                self.send_periodic_messages(
                    group_id,
                    message_generator,
                    config['interval_seconds'],
                    config.get('max_messages')
                )
            )
            tasks.append(task)
        
        try:
            # 等待所有任务完成或被中断
            await asyncio.gather(*tasks, return_exceptions=True)
        except KeyboardInterrupt:
            # 取消所有正在运行的任务
            for task in tasks:
                if not task.done():
                    task.cancel()
            # 等待所有任务完成取消操作
            await asyncio.gather(*tasks, return_exceptions=True)
            logger.info("已停止所有消息发送任务")
        except Exception as e:
            logger.error(f"多目标消息发送时出错: {e}")
            # 取消所有任务
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def close(self):
        """
        关闭客户端连接
        """
        if self.client:
            await self.client.disconnect()
            logger.info("已断开与Telegram的连接")

async def main():
    try:
        # 尝试从配置文件导入设置
        # 尝试从配置文件导入设置
        try:
            import config
            api_id = config.API_ID or os.environ.get('TELEGRAM_API_ID') or input("请输入Telegram API ID: ")
            api_hash = config.API_HASH or os.environ.get('TELEGRAM_API_HASH') or input("请输入Telegram API Hash: ")
            phone = config.PHONE or os.environ.get('TELEGRAM_PHONE') or input("请输入电话号码（带国家代码，如+8613800138000）: ")
            message_generator = MessageGenerator()
            message_generator.add_template(config.MESSAGE_TEMPLATES)
            targets = config.TARGETS
        except (ImportError, AttributeError):
            # 如果配置文件不存在或不完整，则从用户输入获取
            logger.info("未找到完整的配置文件，将从用户输入获取配置")
            api_id = os.environ.get('TELEGRAM_API_ID') or input("请输入Telegram API ID: ")
            api_hash = os.environ.get('TELEGRAM_API_HASH') or input("请输入Telegram API Hash: ")
            phone = os.environ.get('TELEGRAM_PHONE') or input("请输入电话号码（带国家代码，如+8613800138000）: ")
            
            # 获取多目标配置
            targets = {}
            while True:
                group_id = input("\n请输入目标群组ID或用户名（如 -1001234567890 或 @groupname），直接回车结束输入: ")
                if not group_id:
                    break
                    
                interval_seconds = float(input("请输入发送间隔（秒）: "))
                set_max = input("是否设置最大发送数量？(y/n): ").lower() == 'y'
                max_messages = int(input("请输入最大发送数量: ")) if set_max else None
                
                targets[group_id] = {
                    "interval_seconds": interval_seconds,
                    "max_messages": max_messages
                }
                
                if input("\n是否继续添加目标？(y/n): ").lower() != 'y':
                    break
            
            # 创建消息生成器实例并添加默认模板
            message_generator = MessageGenerator()
            message_generator.add_template(["当前时间: {time}", "今天是 {date}"])
        
        if not targets:
            logger.error("未配置任何目标，程序退出")
            return
        
        # 创建消息发送器实例
        sender = TelegramMessageSender(api_id, api_hash, phone)
        
        # 连接到Telegram
        await sender.connect()
        
        # 开始定期发送消息
        print("\n开始向多个目标发送消息...")
        print("按 Ctrl+C 停止发送\n")
        
        await sender.send_messages_to_multiple_targets(targets, message_generator)
    
    finally:
        # 关闭连接
        await sender.close()

if __name__ == "__main__":
    asyncio.run(main())