from openai import OpenAI
import streamlit as st


@st.cache_resource
def get_openai_client(url, api_key):
    '''
    使用了缓存，当参数不变时，不会重复创建client
    '''
    client = OpenAI(base_url=url, api_key=api_key)
    return client


# 定义了drawing_page函数，设置页面标题和说明文字。
def drawing_page():
    st.title("文生图")
    st.caption("使用 DALL·E 3 绘图")

    # 初始化参数
    api_key = (
        st.session_state.api_key
        if "api_key" in st.session_state and st.session_state.api_key != ""
        else None
    )
    if api_key is None:
        st.error("请在主页中输入您的API密钥.")
        st.stop()

    if "base_url" in st.session_state:
        base_url = st.session_state.base_url
    else:
        base_url = "https://api.openai-hk.com/v1"

    # 使用Streamlit的selectbox组件创建下拉菜单，让用户选择图像尺寸、质量和生成图像的数量。
    image_size = st.selectbox('图像尺寸', ["1024x1024", "1024x1792", "1792x1024"], key='image_size')
    quality = st.selectbox('图像质量', ["standard", "hd"], key='quality')
    num_images = st.selectbox('数量 （dall-e-3 only n=1）', [1], key='num_images')

    if prompt := st.chat_input("prompt"):
        st.chat_message("user").write(prompt)
        with st.chat_message('助手'):
            with st.spinner('思考中...'):
                try:
                    client = get_openai_client(base_url, api_key)
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size=image_size,
                        quality=quality,
                        n=num_images,
                    )

                    # print(response)
                    for image in response.data:
                        image_url = image.url
                        revised_prompt = image.revised_prompt
                        st.image(image_url, caption=prompt, width=200)

                        # 添加下载链接
                        download_link = f'<a href="{image_url}" download>Download</a>'
                        st.markdown(download_link, unsafe_allow_html=True)
                        # 显示提示词
                        st.write("revised_prompt : " + revised_prompt)
                except Exception as e:
                    st.error(e)
                    st.stop()


if __name__ == "__main__":
    drawing_page()