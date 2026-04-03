# chatbot-app

基于streamlit编写的针对openai接口的各类模型对话web应用，目前支持基本对话、文生图、图片理解、语音转文、文转语言、智能公文编写、智能AI名片定制、融合通义千问文本图像生成。


## 0. 目标
- [yy] 支持Chat Completions API 的页面，进行文本对话
- [yy] 支持Vision的页面，进行图像理解
- [yy] 支持Image generation的页面，进行图片生成
- [yy] 支持语言转文本的页面
- [yy] 支持文本转语音的页面 
- [yy] 支持智能公文编写 
- [yy] 支持智能AI名片定制下载
- [yy] 支持通义千问文本图像生成

其他添加的小功能
- [yy] chat页面每次对话后显示耗时（配置文件中控制开关）
- [yy] chat页面每次对话后显示消耗的token数（配置文件中控制开关）
- [yy] 对whisper的输入添加违禁词过滤，包含违禁词则输出null
- [yy] 给chat页面增加了预设提示词，可以在配置文件中自定义
- [yy] 在draw页面添加了`revised_prompt`的显示，它保存了对你提示词的修改结果
- [yy] 在智能公文编写方面支持多种公文的编写，极大的扩展公文使用能力
- [yy] 在智能AI名片定制功能方面，使用了AI文生图的模式生成了名片背景图并压缩为名片所需尺寸，满足用户定制需求。
- [yy] 引入阿里云百炼的API_KEY，使用国产主流大模型生成文本及图像的生成功能，与openai形成对比

## 1 使用

### 直接运行

```bash
pip install -r requirements.txt
pip install --upgrade streamlit audio_recorder_streamlit
#命令行启动
streamlit run ./src/首页.py --server.port 8501
#PyCharm debug启动
script：D:/xx/xx/xx/.venv/Scripts/streamlit
script parameters：run ./src/首页.py --server.port 8501
Working directory：./chatbot-app
```

## 2. 配置文件
默认参数配置文件在`src/config/default.json`中，这里主要说明自定义的参数：
* models：chat页面上的下拉菜单显示的模型
* num_tokens：是否显示每次对话消耗的token数
* use_time：是否显示每次对话消耗的时间

@copyRight by yuyun（2026.3.4上传）有需要联系微信：wchatyuyun
