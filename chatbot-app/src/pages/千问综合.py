import streamlit as st
from dashscope import Generation, ImageSynthesis
import dashscope
import os
import base64
from io import BytesIO

# 初始化DashScope
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', 'sk-56c2dff09b054decb4014c93230587b0')


def generate_text(prompt, model="qwen-plus"):
    """使用通义千问生成文本"""
    try:
        response = Generation.call(
            model=model,
            prompt=prompt,
            max_tokens=1000
        )
        return response.output.text if response.output else "生成失败"
    except Exception as e:
        return f"文本生成错误: {str(e)}"


def generate_image(prompt, n=1, size="1024*1024"):
    """使用通义千问生成图像"""
    try:
        response = ImageSynthesis.call(
            model=ImageSynthesis.Models.wanx_v1,
            prompt=prompt,
            n=n,
            size=size
        )
        if response.output and response.output.results:
            return [result.url for result in response.output.results]
        return []
    except Exception as e:
        st.error(f"图像生成错误: {str(e)}")
        return []


def main():
    st.set_page_config(page_title="通义千问多功能应用", layout="wide")

    # 侧边栏配置
    st.sidebar.title("功能选择")
    app_mode = st.sidebar.selectbox(
        "选择应用模式",
        ["文本生成", "图像生成", "综合应用"]
    )

    st.title("通义千问API集成演示")

    if app_mode == "文本生成":
        st.header("智能文本生成")
        prompt = st.text_area("输入您的问题或提示:", height=150)
        model_choice = st.selectbox(
            "选择模型",
            ["qwen-plus", "qwen-max", "qwen-turbo"]
        )

        if st.button("生成文本"):
            if prompt:
                with st.spinner("正在生成文本..."):
                    result = generate_text(prompt, model_choice)
                    st.subheader("生成结果:")
                    st.write(result)
            else:
                st.warning("请输入提示内容")

    elif app_mode == "图像生成":
        st.header("AI图像生成")
        image_prompt = st.text_input("描述您想要生成的图像:")
        image_size = st.selectbox(
            "选择图像尺寸",
            ["1024*1024", "768*768", "512*512"]
        )
        num_images = st.slider("生成数量", 1, 4, 1)

        if st.button("生成图像"):
            if image_prompt:
                with st.spinner("正在生成图像..."):
                    image_urls = generate_image(image_prompt, num_images, image_size)
                    if image_urls:
                        cols = st.columns(len(image_urls))
                        for i, url in enumerate(image_urls):
                            cols[i].image(url, caption=f"生成图像 {i + 1}")
                    else:
                        st.error("图像生成失败，请重试")
            else:
                st.warning("请输入图像描述")

    elif app_mode == "综合应用":
        st.header("文本与图像综合应用")
        prompt = st.text_area("输入您的创意提示:", height=100)

        if st.button("综合生成"):
            if prompt:
                with st.spinner("正在处理您的请求..."):
                    # 生成文本内容
                    text_result = generate_text(f"基于以下提示创作详细内容: {prompt}")
                    st.subheader("文本内容:")
                    st.write(text_result)

                    # 基于文本生成图像
                    st.subheader("相关图像:")
                    image_urls = generate_image(prompt, 2, "1024*1024")
                    if image_urls:
                        cols = st.columns(2)
                        for i, url in enumerate(image_urls):
                            cols[i].image(url, caption=f"相关图像 {i + 1}")
                    else:
                        st.info("暂无相关图像生成")
            else:
                st.warning("请输入提示内容")


if __name__ == "__main__":
    main()
