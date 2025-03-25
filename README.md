# Telegram消息定时发送脚本

这是一个使用Telethon库在特定Telegram群组中定期发送自定义消息的Python脚本。

## 功能特点

- 自动登录Telegram账户
- 支持两步验证
- 定期向指定群组发送消息
- 可设置发送间隔时间
- 可设置最大发送消息数量
- 异常处理和日志记录

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用前准备

1. 获取Telegram API凭据：
   - 访问 https://my.telegram.org/auth
   - 登录您的Telegram账户
   - 点击 "API development tools"
   - 创建一个新应用，填写必要信息
   - 获取 API ID 和 API Hash

2. 配置文件设置：
   - 复制 `config.example.py` 为 `config.py`
   - 在 `config.py` 中填入您的配置信息：
     - `API_ID`: 从Telegram获取的API ID
     - `API_HASH`: 从Telegram获取的API Hash
     - `PHONE`: 您的电话号码（带国家代码，如+8613800138000）
     - `GROUP_ID`: 目标群组ID或用户名（如 -1001234567890 或 @groupname）
     - `INTERVAL_SECONDS`: 发送间隔（秒），默认60秒（1分钟）
     - `MAX_MESSAGES`: 最大发送消息数量，None表示无限制
     - `MESSAGE_TEMPLATES`: 消息模板列表，支持时间格式化：{time}, {date}, {datetime}
     - `SESSION_FILE_PATH`: 会话文件保存路径

3. 配置环境变量（可选）：
   ```bash
   export TELEGRAM_API_ID="您的API ID"
   export TELEGRAM_API_HASH="您的API Hash"
   export TELEGRAM_PHONE="您的电话号码（带国家代码，如+8613800138000）"
   ```

## 使用方法

```bash
python main.py
```

如果没有设置环境变量，脚本会提示您输入必要的信息：

1. Telegram API ID
2. Telegram API Hash
3. 电话号码（带国家代码，如+8613800138000）
4. 目标群组ID或用户名（如 -1001234567890 或 @groupname）
5. 要发送的消息内容
6. 发送间隔（秒）
7. 是否设置最大发送数量

首次运行时，Telegram会发送验证码到您的账户，您需要输入该验证码完成登录。

## 注意事项

- 请勿频繁发送消息，以免触发Telegram的限制
- 脚本会自动处理频率限制错误，并在必要时等待
- 可以通过按 Ctrl+C 随时停止发送消息

## 许可证

MIT