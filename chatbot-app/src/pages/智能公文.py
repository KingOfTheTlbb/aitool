import streamlit as st
from openai import OpenAI
import time

# Author: yuyun
# Email: yuyunsunboy@163.com
# wx: wchatyuyn
# Last Modified: 2026-04-10

# 设置页面配置
st.set_page_config(
    page_title="AI智能公文生成器",
    page_icon="📄",
    layout="wide"
)

# 初始化OpenAI客户端（带缓存）
@st.cache_resource
def get_openai_client(url, api_key):
    '''
    使用了缓存，当参数不变时，不会重复创建client
    '''
    client = OpenAI(base_url=url, api_key=api_key)
    return client

def generate_official_document(prompt, document_type, tone_style, length):
    """
    生成公文的核心函数
    """
    # 获取API配置
    api_key = st.session_state.get("api_key", "")
    base_url = st.session_state.get("base_url", "https://api.openai-hk.com/v1")

    if not api_key:
        st.error("请先在侧边栏配置您的API密钥")
        return None

    try:
        # 创建客户端
        client = get_openai_client(base_url, api_key)

        # 构建系统提示词，优化公文生成
        system_prompt = f"""你是一位专业的公文写作助手，请根据以下要求生成{length}字的{document_type}：
        1. 使用正式、规范的公文语言
        2. 遵循{document_type}的标准格式和结构
        3. 语言风格：{tone_style}
        4. 内容要严谨、准确、完整
        5. 包含必要的公文要素（如标题、正文、落款等）
        6. 避免口语化表达"""

        # 构建用户消息
        user_content = f"请根据以下主题和要求生成公文：\n主题：{prompt}"

        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 使用更适合对话的模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            max_tokens=length * 2,  # 根据字数需求调整token数
            temperature=0.7,
            top_p=0.9,
            n=1
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"生成公文时出错：{str(e)}")
        return None

def main():
    # 侧边栏配置
    with st.sidebar:
        # 初始化参数
        # 强制使用 openai-hk 地址
        base_url = "https://api.openai-hk.com/v1"

        api_key = (
            st.session_state.api_key
            if "api_key" in st.session_state and st.session_state.api_key != ""
            else None
        )
        if api_key is None:
            st.error("请在主页中输入您的API密钥.")
            st.stop()
        st.divider()
        # 公文参数设置
        st.header("📋 公文参数")

        document_type = st.selectbox(
            "公文类型",
            ["通知","短评","报告", "请示", "函", "纪要", "决定", "公告", "通报", "意见", "编者按"],
            help="选择要生成的公文类型"
        )

        tone_style = st.selectbox(
            "语言风格",
            ["正式严谨", "简洁明了", "温和委婉", "坚决有力"],
            help="选择公文的语言风格"
        )

        length = st.slider(
            "生成字数",
            min_value=100,
            max_value=1500,
            value=100,
            step=100,
            help="控制生成公文的长度"
        )

        st.divider()

        # 使用说明
        with st.expander("📖 使用说明"):
            st.markdown("""
            1. 在侧边栏配置API密钥和参数
            2. 在主界面输入公文主题和要求
            3. 点击"生成公文"按钮
            4. 生成的公文会自动格式化显示
            5. 可以复制或下载生成的公文
            """)

    # 主界面
    st.title("📄 AI智能公文生成器")
    st.markdown("---")

    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    with col1:
        # 输入区域
        st.subheader("📝 公文主题和要求")
        prompt = st.text_area(
            "请输入公文的主题、要点或具体要求：",
            height=150,
            placeholder="例如：关于召开2024年度工作总结会议的通知\n要求：包含会议时间、地点、议程、参会人员等",
            help="请详细描述您需要生成的公文内容"
        )

        # 生成按钮
        if st.button("🚀 生成公文", type="primary", use_container_width=True):
            if not prompt:
                st.warning("请输入公文主题和要求")
            elif not st.session_state.get("api_key"):
                st.error("请先在侧边栏配置API密钥")
            else:
                with st.spinner('正在生成公文，请稍候...'):
                    # 显示进度条
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    # 生成公文
                    generated_text = generate_official_document(
                        prompt, document_type, tone_style, length
                    )
                    if generated_text:
                        st.success('✅ 公文生成完成！')
    with col2:
        # 公文模板示例
        st.subheader("📋 公文结构示例")
        with st.expander("查看通知模板"):
            st.markdown("""
            &zwnj;**关于[事由]的通知**&zwnj;

            各[相关部门/单位]：

            一、[背景和目的]

            二、[具体事项]
                1. [事项一]
                2. [事项二]
                3. [事项三]

            三、[工作要求]

            四、[其他说明]

            [发文单位]
            [日期]
            """)

    # 显示生成的公文
    if 'generated_text' in locals() and generated_text:
        st.markdown("---")
        st.subheader("📄 生成的公文")

        # 公文显示区域
        with st.container():
            st.markdown("### " + document_type)
            st.markdown("---")

            # 格式化显示公文内容
            st.markdown(generated_text)

            st.markdown("---")

            # 操作按钮
            col_btn1, col_btn2, col_btn3 = st.columns(3)

            with col_btn1:
                if st.button("📋 复制内容", use_container_width=True):
                    st.code(generated_text, language=None)
                    st.success("已复制到剪贴板（请手动复制）")

            with col_btn2:
                if st.button("🔄 重新生成", use_container_width=True):
                    st.rerun()

            with col_btn3:
                if st.button("💾 下载文件", use_container_width=True):
                    # 创建下载链接
                    import base64
                    b64 = base64.b64encode(generated_text.encode()).decode()
                    href = f'<a href="data:text/plain;base64,{b64}" download="{document_type}_{time.strftime("%Y%m%d_%H%M%S")}.txt">点击下载'
                    st.markdown(href, unsafe_allow_html=True)

    # 底部信息
    st.markdown("---")
    st.caption("💡 提示：生成的公文仅供参考，请根据实际情况进行修改和完善")

if __name__ == "__main__":
    main()
