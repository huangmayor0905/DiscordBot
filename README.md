# Mayor Bot

My Discord Bot with Python.

## 運行版本

Python `3.12.4`

| Package    | Version |
| ---------- | ------- |
| discord.py | 2.4.0   |
| requests   | 2.32.3  |

## 使用方法

- 請先確保電腦擁有 Python 環境

- 安裝必要套件
  ```shell
  pip install -r requirements.txt
  ```

- 配置 config.json

> [!NOTE]
> ID 找不到？
> 請至【Discord 設定】 -> 側邊欄【進階】 -> 打開【開發者模式】</br>
> 接著右鍵點擊語音或文字頻道，就可以看到【複製頻道 ID】

  - `botToken` 你的機器人 Token
  - `CWA_API_KEY` 你的中央氣象署 API_KEY
  - `roles` 身分組頻道設定
    - `adminID` 管理員身分組 ID
  - `guilds` 伺服器頻道設定
    - `welcomeChannelID` 歡迎頻道 ID
    - `leaveChannelID` 離開頻道 ID
    - `dynamicChannelID` 動態語音頻道 ID
  - `valorants` 有關 Valorant 的設定
    - `attackerChannelID` 進攻方語音頻道 ID
    - `defenderChannelID` 守備方語音頻道 ID
    - `maps` 地圖
    - `agents` 角色
  - `teacherSays` 我高中老師的語錄：）


- 若欲使用前綴指令，預設前綴字符為 `=`