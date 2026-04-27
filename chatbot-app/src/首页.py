import os
import streamlit as st
import sys

# Author: yuyun
# Email: yuyunsunboy@163.com
# wx: wchatyuyn
# Last Modified: 2026-04-01

def home():
    st.markdown("""
    <style>
    .css-12w0qz-container {
        font-size: 24px !important;
    }
    """, unsafe_allow_html=True)
    # 从 sessionStorage 中读取 user_name
    user_name = st.session_state.get('user_name')
    if not user_name:
        user_name = st.session_state.get('user_name', '')

    if user_name:
        st.title(f"🏠欢迎 {user_name}进入🏠AI应用多模态智能体")
    else:
        st.title("欢迎进入🏠AI应用多模态智能体")

    if "base_url" not in st.session_state:
        st.session_state['base_url'] = os.getenv('OPENAI_BASE_URL')

    if "api_key" not in st.session_state:
        st.session_state['api_key'] = os.getenv('OPENAI_API_KEY')

    ## 输入方式
    st.session_state.base_url = st.sidebar.text_input('Base URL', st.session_state.base_url)
    st.session_state.api_key = st.sidebar.text_input('API Key', st.session_state.api_key, type='password')

    st.markdown(
        """
        **体验OpenAI多模态功能**
        * 使用说明
        * 使用请在侧边栏填写`BASE_URL`&`API Key`。
        """
    )
    st.markdown(
        """
        功能描述：\r\n
        #1 💬 文本对话  \n
        该页面用于文本对话，选择模型，输入问题，得到回答。对应openai文档：[text-generation](https://platform.openai.com/docs/guides/text-generation)\n

        # 2 🖼️ 文生图 \n
        该页面用于图像生成，使用DALL·E模型，输入提示词，输出图片。对应openai文档：[image-generation](https://platform.openai.com/docs/guides/images?context=node)\n

        # 3 🗣️ 语音转文本 \n
        该页面用于语音转文本，使用whisper模型。对应openai文档：[speech-to-text](https://platform.openai.com/docs/guides/speech-to-text)\n

        # 4 📢 文本转语音 \n
        该页面用于文本转语音，使用tts模型。对应openai文档：[text-to-speech](https://platform.openai.com/docs/guides/text-to-speech)\n

        # 5 🎞️ 图像理解 \n
        该页面用于图像理解，使用gpt-4o模型，输入图片和问题，得到回答。对应openai文档：[vision](https://platform.openai.com/docs/guides/vision)\n

        # 6 💻 国产千问 \n
        该页面用于千问交互 你自己去查吧 \n
        
        # 7 🍎 智能定制 \n
        智能公文编写、智能AI名片定制  去用着试试吧  \n\r
        
        """
    )

    st.markdown(
        """
        ---------------------------------------------------------
        * 使用体验上有疑问联系 wx：wchatyuyun 
        * Copyright 2026 by yuyun。
        ---------------------------------------------------------
        """
    )




    # # 添加退出登录按钮
    # if st.button("\r退出登录", key="logout_button"):
    #     # 清除会话状态
    #     for key in st.session_state.keys():
    #         del st.session_state[key]
    #     # 重定向到登录页面
    #     command = f"streamlit run 登录.py"
    #     os.system(command)  # 或者使用 subprocess.run(command, shell=True)
    #     sys.exit()

if __name__ == "__main__":
    home()