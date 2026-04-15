import streamlit as st
from openai import OpenAI
import os
import requests

# 定义一个函数，用于获取OpenAI客户端
@st.cache_resource
def get_openai_client(url, api_key):
    client = OpenAI(base_url=url, api_key=api_key)
    return client

# 列出模型页面
def list_models_page():
    st.title("列出可用模型")

    # 初始化参数
    if "base_url" not in st.session_state:
        st.session_state['base_url'] = os.getenv('OPENAI_BASE_URL', 'https://api.openai-hk.com/v1')
    if "api_key" not in st.session_state:
        st.session_state['api_key'] = os.getenv('OPENAI_API_KEY')

    # 检查配置是否存在
    if not st.session_state.get('base_url') or not st.session_state.get('api_key'):
        st.error("请先在首页设置 Base URL 和 API Key")
        st.stop()

    # 显示当前配置（只读）
    st.sidebar.markdown("**当前配置：**")
    st.sidebar.text(f"Base URL: {st.session_state.base_url}")
    st.sidebar.text(f"API Key: {'*' * len(st.session_state.api_key) if st.session_state.api_key else '未设置'}")

    # 获取OpenAI客户端
    client = get_openai_client(st.session_state.base_url, st.session_state.api_key)

    # 调用接口
    if st.button("获取模型列表"):
        with st.spinner('正在加载...'):
            try:
                response = requests.get(f"{st.session_state.base_url}/models", headers={"Authorization": f"Bearer {st.session_state.api_key}"})
                response.raise_for_status()
                models = response.json()['data']

                # 显示结果
                for model in models:
                    st.write(f"Model ID: {model['id']}, Owned By: {model['owned_by']}")
            except Exception as e:
                st.error(f"请求失败: {e}")

if __name__ == "__main__":
    list_models_page()