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
     - `TARGETS`: 多目标配置字典，格式如下：
       ```python
       TARGETS = {
           "@group1": {"interval_seconds": 60, "max_messages": 100},
           "-1001234567890": {"interval_seconds": 300},
           "@channel1": {"interval_seconds": 3600, "max_messages": 10}
       }
       ```
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

首次运行时，Telegram会发送验证码到您的账户，您需要输入该验证码完成登录。

### 多目标消息发送

通过配置`TARGETS`字典，您可以同时向多个目标发送消息，每个目标可以设置不同的发送间隔和最大消息数量：

- `interval_seconds`: 发送间隔（秒）
- `max_messages`: 最大发送消息数量（可选，不设置表示无限制）

脚本会自动为每个目标创建独立的发送任务，并同时运行这些任务。您可以通过按 Ctrl+C 随时停止所有发送任务。

## 注意事项

- 请勿频繁发送消息，以免触发Telegram的限制
- 脚本会自动处理频率限制错误，并在必要时等待
- 可以通过按 Ctrl+C 随时停止发送消息

## 许可证

MIT