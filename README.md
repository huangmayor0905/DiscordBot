# Mayor Bot

My Discord Bot with Python.

## 運行版本

Python `3.12.4`

| Package    | Version |
| ---------- | ------- |
| discord.py | 2.4.0   |
| requests   | 2.32.3  |

## 使用方法

### 請先確保電腦擁有 Python 環境

### 安裝必要套件

```shell
pip install -r requirements.txt
```

### 配置 config.json

- `botToken` 你的機器人 Token
- `CWA_API_KEY` 你的中央氣象署 API_KEY
- `roles` 身分組頻道設定
  - `adminID` 管理員身分組 ID
- `guilds` 伺服器頻道設定
  - `welcomeChannelID` 歡迎頻道ID
  - `leaveChannelID` 離開頻道ID
  - `dynamicChannelID` 動態語音頻道ID
- `valorants` 有關 valorant 的設定
  - `attackerChannelID` 進攻方語音頻道ID
  - `defenderChannelID` 守備方語音頻道ID
  - `maps` 地圖
  - `agents` 角色
- `teacherSays` 我高中老師的語錄：）
