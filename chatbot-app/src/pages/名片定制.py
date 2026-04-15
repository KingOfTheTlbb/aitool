import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
from openai import OpenAI
import requests
from io import BytesIO

def ensure_chinese_font():
    """确保中文字体存在，如果不存在则自动下载"""
    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    font_path = os.path.join(font_dir, "SourceHanSansSC-Regular.ttf")

    if not os.path.exists(font_path):
        try:
            os.makedirs(font_dir, exist_ok=True)
            st.info("正在下载中文字体文件，请稍候...")

            # 下载思源黑体简体中文
            font_url = "https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf"
            response = requests.get(font_url, timeout=30)
            response.raise_for_status()

            with open(font_path, 'wb') as f:
                f.write(response.content)

            st.success("✅ 中文字体下载完成！")
        except Exception as e:
            st.error(f"字体下载失败: {e}")
            return False
    return True

@st.cache_resource
def get_openai_client(url, api_key):
    '''
    使用了缓存，当参数不变时，不会重复创建client
    '''
    client = OpenAI(base_url=url, api_key=api_key)
    return client

def generate_namecard(name, company, position, phone, email, image_size, bg_name, avatar=None):
    width, height = 1050, 600
    try:
        base_dir = os.path.dirname(__file__) if "__file__" in locals() else "."
        img = Image.open(os.path.join(base_dir, f"resources/images/{bg_name}")).convert("RGB")
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    except:
        api_key = st.session_state.get("api_key", "")
        base_url = st.session_state.get("base_url", "https://api.openai-hk.com/v1")

        if not api_key:
            st.error("请先在侧边栏配置您的API密钥")
            return None
        # 创建客户端
        client = get_openai_client(base_url, api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=bg_name,
            size=image_size,
            quality="standard",
            n=1
        )
        image = response.data[0]
        image_url = image.url

        # 下载图片
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()  # 检查请求是否成功

        # 打开图片并转换为RGB模式（兼容性处理）
        img = Image.open(BytesIO(img_response.content)).convert("RGB")

        # 保持图片比例缩放，避免拉伸变形
        img.thumbnail((width, height), Image.Resampling.LANCZOS)

        # 计算居中位置
        x_offset = (width - img.width) // 2
        y_offset = (height - img.height) // 2
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)
    # 智能文字颜色适配
    text_color = (255, 255, 255) if sum(img.convert("L").getdata()) / (width * height) < 128 else (0, 0, 0)
    # 修复中文显示：多层级字体兼容方案
    def get_chinese_font(size):
        """获取中文字体，支持多平台"""
        # 字体优先级列表（从高到低）
        font_paths = [
            # 1. 项目本地字体（推荐）
            os.path.join(os.path.dirname(__file__), "fonts", "SourceHanSansSC-Regular.ttf"),
            os.path.join(os.path.dirname(__file__), "fonts", "simhei.ttf"),
            os.path.join(os.path.dirname(__file__), "fonts", "NotoSansCJK-Regular.ttc"),

            # 2. 系统字体路径
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",

            # 3. Windows系统字体
            "C:/Windows/Fonts/simhei.ttf",  # Windows黑体
            "C:/Windows/Fonts/msyh.ttc",  # Windows微软雅黑
            "C:/Windows/Fonts/simsun.ttc",  # Windows宋体

            # 4. macOS系统字体
            "/System/Library/Fonts/PingFang.ttc",  # macOS苹方
            "/System/Library/Fonts/STHeiti Light.ttc",  # macOS黑体
            "/System/Library/Fonts/STHeiti Medium.ttc",
        ]

        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, size)
                    # 测试字体是否支持中文
                    test_text = "测试"
                    bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test_text, font=font)
                    if bbox[2] > bbox[0]:  # 如果有宽度，说明字体支持中文
                        return font
            except:
                continue

        # 如果所有中文字体都找不到，使用默认字体并警告
        st.warning("⚠️ 未找到中文字体，中文可能显示为方框。已自动下载思源黑体字体，如仍有问题请手动安装中文字体。")
        return ImageFont.load_default()

    # 使用中文字体加载函数
    name_font = get_chinese_font(60)
    position_font = get_chinese_font(36)
    info_font = get_chinese_font(32)
    company_font = get_chinese_font(38)
    # 头像绘制优化
    avatar_size = 140
    avatar_x, avatar_y = 80, 80
    if avatar:
        avatar = avatar.resize((avatar_size, avatar_size))
        mask = Image.new('L', (avatar_size, avatar_size), 0)
        ImageDraw.Draw(mask).ellipse([(0, 0), (avatar_size, avatar_size)], fill=255)
        img.paste(avatar, (avatar_x, avatar_y), mask)
    else:
        draw.ellipse([avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size],
                     fill=(100, 180, 255) if text_color == (0, 0, 0) else (50, 50, 100),
                     outline=text_color, width=3)
        if name:
            bbox = draw.textbbox((0, 0), name[0].upper(), font=name_font)
            draw.text((avatar_x + avatar_size // 2 - (bbox[2] - bbox[0]) // 2,
                       avatar_y + avatar_size // 2 - (bbox[3] - bbox[1]) // 2),
                      name[0].upper(), font=name_font, fill=text_color)

    # 信息区域绘制（确保所有字段正确填充）
    info_start_x = avatar_x + avatar_size + 50
    info_start_y = avatar_y + 10

    # 姓名
    draw.text((info_start_x, info_start_y), name, font=name_font, fill=text_color)
    # 职务
    draw.text((info_start_x, info_start_y + 75), position, font=position_font, fill=text_color)
    # 分隔线
    draw.line([(info_start_x, info_start_y + 135), (info_start_x + 500, info_start_y + 135)],
              fill=(100, 180, 255) if text_color == (0, 0, 0) else (50, 50, 100), width=2)
    # 公司名称
    draw.text((info_start_x, info_start_y + 190), company, font=company_font, fill=text_color)
    # 电话
    phone_y = info_start_y + 245
    draw.ellipse([info_start_x - 5, phone_y + 15, info_start_x + 25, phone_y + 45],
                 fill=(100, 180, 255) if text_color == (0, 0, 0) else (50, 50, 100))
    draw.text((info_start_x + 7, phone_y + 10), "T", font=info_font, fill=text_color)
    draw.text((info_start_x + 40, phone_y), phone, font=info_font, fill=text_color)
    # 邮箱
    email_y = phone_y + 55
    draw.ellipse([info_start_x - 5, email_y + 15, info_start_x + 25, email_y + 45],
                 fill=(100, 180, 255) if text_color == (0, 0, 0) else (50, 50, 100))
    draw.text((info_start_x + 5, email_y + 10), "@", font=info_font, fill=text_color)
    draw.text((info_start_x + 40, email_y), email, font=info_font, fill=text_color)

    # 底部文字
    footer_text = "AI Designed Business Card"
    if "card2" in bg_name:
        footer_text = "典雅 · 匠心"
    bbox = draw.textbbox((0, 0), footer_text, ImageFont.load_default())
    draw.text((width - (bbox[2] - bbox[0]) - 50, height - 50),
              footer_text, font=ImageFont.load_default(), fill=(150, 150, 150))

    # 转字节流
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# Streamlit界面
st.set_page_config(page_title="智能名片生成器", layout="wide")

# 确保中文字体存在
ensure_chinese_font()

st.title("🎨 智能名片定制")
st.markdown("上传个人照片，填写信息，选择背景，一键生成专属名片。")

col1, col2 = st.columns([1, 2])
with col1:
    st.header("第一步：上传与填写")
    uploaded_file = st.file_uploader("上传1寸个人证件照", type=['png', 'jpg', 'jpeg'])
    avatar_image = Image.open(uploaded_file).convert("RGB") if uploaded_file else None
    if uploaded_file:
        st.image(Image.open(uploaded_file).resize((295, 413)), caption="您的1寸照片预览", use_column_width=True)

    with st.form("user_info_form"):
        name = st.text_input("姓名*", placeholder="请输入您的姓名")
        company = st.text_input("公司名称*", placeholder="请输入公司全称")
        position = st.text_input("职务*", placeholder="例如：高级产品经理")
        phone = st.text_input("电话*", placeholder="请输入手机号码")
        email = st.text_input("邮箱*", placeholder="请输入工作邮箱")

        image_size = st.selectbox('图像尺寸', ["1024x1024", "1024x1792", "1792x1024"], key='image_size')
        bg_name = st.text_area("请输入您对名片风格的要求:", height=150)
        submitted = st.form_submit_button("生成名片")

with col2:
    st.header("第二步：预览与生成")
    if submitted:
        # 严格校验必填项，过滤空格
        if all([name.strip(), company.strip(), position.strip(), phone.strip(), email.strip()]):
            with st.spinner("正在智能生成您的名片，请稍候..."):
                try:
                    # 生成名片
                    namecard = generate_namecard(name, company, position, phone, email, image_size, bg_name, avatar_image)

                    st.success("名片生成成功！")
                    st.subheader("📄 名片预览")
                    st.image(namecard, caption="您的名片预览", width=600)

                    st.subheader("📥 下载名片")
                    st.download_button(
                        label="下载PNG格式名片",
                        data=namecard,
                        file_name=f"{name}_名片.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")
        else:
            st.warning("⚠️ 请填写所有带*的必填信息，且内容不能仅为纯空格！")


# 侧边栏：使用说明
with st.sidebar:
    st.header("使用说明")
    st.markdown("""
    **📌 使用步骤：**
    1. 上传1寸个人证件照
    2. 填写所有个人信息
    3. 选择喜欢的背景风格
    4. 点击"生成名片"按钮
    5. 预览并下载名片

    **⚙️ 技术配置：**
    - 确保已安装Streamlit
    - 需要有效的OpenAI API密钥
    - 支持PNG/JPG格式图片

    **🔧 安装依赖：**
    ```bash
    pip install streamlit openai pillow requests
    ```
    """)

    # 背景模板管理
    st.header("背景模板管理")
    if st.button("查看更多模板"):
        st.info("更多模板功能开发中...")

# 页脚
st.markdown("---")
st.markdown("**智能名片生成器 v1.0** | 基于Streamlit + OpenAI | 专为AI定制设计")