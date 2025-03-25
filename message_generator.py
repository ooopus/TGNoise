#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
消息生成器模块
支持多种消息生成方式，包括随机文本、时间相关内容和自定义函数等
"""

import random
from datetime import datetime
from typing import Callable, List, Optional, Union

class MessageGenerator:
    def __init__(self):
        self.templates: List[str] = []
        self.custom_generators: List[Callable[[], str]] = []
        
    def add_template(self, template: Union[str, List[str]]) -> None:
        """添加消息模板
        :param template: 单个模板字符串或模板列表
        """
        if isinstance(template, str):
            self.templates.append(template)
        else:
            self.templates.extend(template)
    
    def add_custom_generator(self, generator: Callable[[], str]) -> None:
        """添加自定义消息生成器函数
        :param generator: 返回字符串的生成器函数
        """
        self.custom_generators.append(generator)
    
    def generate_from_template(self) -> Optional[str]:
        """从模板中随机生成消息"""
        if not self.templates:
            return None
        template = random.choice(self.templates)
        # 支持基本的时间格式化
        now = datetime.now()
        return template.format(
            time=now.strftime('%H:%M:%S'),
            date=now.strftime('%Y-%m-%d'),
            datetime=now.strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def generate_from_custom(self) -> Optional[str]:
        """使用自定义生成器函数生成消息"""
        if not self.custom_generators:
            return None
        generator = random.choice(self.custom_generators)
        return generator()
    
    def generate(self) -> str:
        """生成消息
        优先使用模板生成，如果没有模板则尝试使用自定义生成器
        """
        message = self.generate_from_template()
        if message is None:
            message = self.generate_from_custom()
        if message is None:
            message = "No message template or generator available"
        return message