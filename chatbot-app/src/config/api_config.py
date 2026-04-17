import streamlit as st
import os

def check_api_config():
    """统一的API配置检查函数

    返回:
        tuple: (base_url, api_key) 如果配置有效
        否则显示错误并停止执行
    """
    # 初始化参数
    if "base_url" not in st.session_state:
        st.session_state['base_url'] = os.getenv('OPENAI_BASE_URL', 'https://api.openai-hk.com/v1')
    if "api_key" not in st.session_state:
        st.session_state['api_key'] = os.getenv('OPENAI_API_KEY')

    base_url = st.session_state.get('base_url', '')
    api_key = st.session_state.get('api_key', '')

    # 检查配置是否存在
    if not base_url or not api_key:
        st.error("请先在首页设置 Base URL 和 API Key")
        st.info("在侧边栏输入您的 OpenAI API 配置后，刷新页面即可使用。")
        st.stop()

    return base_url, api_key

def display_config_sidebar():
    """在侧边栏显示当前配置信息（只读）"""
    if "base_url" in st.session_state and "api_key" in st.session_state:
        st.sidebar.markdown("**当前配置：**")
        st.sidebar.text(f"Base URL: {st.session_state.base_url}")
        st.sidebar.text(f"API Key: {'*' * len(st.session_state.api_key) if st.session_state.api_key else '未设置'}")