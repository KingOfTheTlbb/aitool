import streamlit as st
from openai import OpenAI
import json
from typing import Dict, List
import time

# Author: yuyun
# Email: yuyunsunboy@163.com
# wx: wchatyuyn
# Last Modified: 2026-04-11

@st.cache_resource
def get_openai_client(url, api_key):
    # 使用了缓存，当参数不变时，不会重复创建client
    client = OpenAI(base_url=url, api_key=api_key)
    return client

# 页面配置
st.set_page_config(
    page_title="AI简历优化助手",
    page_icon="📝",
    layout="wide"
)

# 初始化session state
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False
if 'optimization_results' not in st.session_state:
    st.session_state.optimization_results = None


def validate_api_key(api_key: str) -> bool:
    """验证OpenAI API密钥"""
    try:
        base_url = st.session_state.get("base_url", "https://api.openai-hk.com/v1")

        if not api_key:
            st.error("请先在侧边栏配置您的API密钥")
            return False  # 返回False而不是None

        # 创建客户端
        client = get_openai_client(base_url, api_key)
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return True
    except:
        return False


def diagnose_resume(resume_text: str) -> Dict:
    """诊断简历问题"""
    prompt = f'''
    请作为专业的HR专家，仔细分析以下简历并指出存在的问题。从以下几个维度进行评估：
    1. 结构组织（是否有清晰的层次结构）
    2. 内容完整性（关键信息是否齐全）
    3. 表达方式（语言是否精炼有力）
    4. 关键词匹配（是否符合目标岗位要求）
    5. 成果量化（是否有具体的数据支撑）

    简历内容：
    {resume_text}

    请按以下JSON格式返回诊断结果：
    {{
        "overall_score": 0-100的评分,
        "issues": [
            {{
                "category": "问题类别",
                "description": "具体问题描述",
                "severity": "严重程度（high/medium/low）"
            }}
        ]
    }}
    '''

    try:
        api_key = st.session_state.get("api_key", "")
        base_url = st.session_state.get("base_url", "https://api.openai-hk.com/v1")

        if not api_key:
            st.error("请先在侧边栏配置您的API密钥")
            return None
        # 创建客户端
        client = get_openai_client(base_url, api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1800,
            temperature=0.3
        )

        diagnosis_json = response.choices[0].message.content
        # 清理可能的markdown包装
        if diagnosis_json.startswith("```json"):
            diagnosis_json = diagnosis_json[7:-3]
        elif diagnosis_json.startswith("```"):
            diagnosis_json = diagnosis_json[3:-3]

        return json.loads(diagnosis_json)
    except Exception as e:
        st.error(f"诊断过程中出错: {str(e)}")
        return {"overall_score": 0, "issues": []}


def optimize_resume(resume_text: str, options: Dict) -> Dict:
    """根据选定选项优化简历"""
    optimizations = []
    if options.get("structure"):
        optimizations.append("- 重新组织简历结构，使其更加清晰易读")
    if options.get("keywords"):
        optimizations.append("- 优化关键词匹配，更好地契合目标职位")
    if options.get("action_verbs"):
        optimizations.append("- 替换弱动词，使用更有力量的行为动词")
    if options.get("quantification"):
        optimizations.append("- 量化工作成果，加入具体的数字指标")
    if options.get("grammar"):
        optimizations.append("- 修正语法和拼写错误")
    if options.get("conciseness"):
        optimizations.append("- 精简冗余表述，使语言更加简洁有力")

    optimization_list = "\n".join(optimizations)

    prompt = f'''
        你是顶尖的职业规划师和简历写作专家。请根据以下要求优化这份简历：

        优化重点：
        {optimization_list}

        原始简历：
        {resume_text}

        输出要求：
        1. 先提供优化后的完整简历文本
        2. 然后列出具体的修改建议

        请严格按照以下JSON格式返回：
        {{
            "optimized_resume": "优化后的简历全文",
            "suggestions": [
                {{
                    "type": "修改类型",
                    "original": "原文内容",
                    "improved": "修改后内容",
                    "reason": "修改原因说明"
                }}
            ]
        }}
        '''

    try:
        api_key = st.session_state.get("api_key", "")
        base_url = st.session_state.get("base_url", "https://api.openai-hk.com/v1")

        if not api_key:
            st.error("请先在侧边栏配置您的API密钥")
            return None
        # 创建客户端
        client = get_openai_client(base_url, api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3200,
            temperature=0.5,
            top_p=0.9,
            n=1
        )
        # 更安全的访问方式
        if response.choices and len(response.choices) > 0:
            result_json = response.choices[0].message.content
        else:
            raise ValueError("API未返回有效响应")
        # 清理可能的markdown包装
        if result_json.startswith("```json"):
            result_json = result_json[7:-3]
        elif result_json.startswith("```"):
            result_json = result_json[3:-3]

        return json.loads(result_json)
    except Exception as e:
        st.error(f"优化过程中出错: {str(e)}")
        return {"optimized_resume": "", "suggestions": []}


def main():
    st.title("🚀 AI简历优化助手")
    st.markdown("---")

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

    # 主界面布局
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📄 输入简历内容")
        resume_text = st.text_area("粘贴您的简历内容:", height=400,
                                   placeholder="请在此处粘贴您的简历文本...")

        # 诊断按钮
        if st.button("🔍 诊断简历", use_container_width=True):
            if not resume_text.strip():
                st.warning("请先输入简历内容")
                return

            with st.spinner("正在进行简历诊断..."):
                diagnosis_result = diagnose_resume(resume_text)
                st.session_state.diagnosis_result = diagnosis_result

    with col2:
        st.header("⚙️ 优化选项")

        # 优化选项复选框
        opt_structure = st.checkbox("优化结构布局", value=True)
        opt_keywords = st.checkbox("强化关键词匹配", value=True)
        opt_action_verbs = st.checkbox("使用强力动词", value=True)
        opt_quantification = st.checkbox("量化工作成果", value=True)
        opt_grammar = st.checkbox("修正语法错误", value=True)
        opt_conciseness = st.checkbox("提升表达简洁性", value=True)

        options = {
            "structure": opt_structure,
            "keywords": opt_keywords,
            "action_verbs": opt_action_verbs,
            "quantification": opt_quantification,
            "grammar": opt_grammar,
            "conciseness": opt_conciseness
        }

        # 优化按钮
        if st.button("✨ 开始优化", type="primary", use_container_width=True):
            if not resume_text.strip():
                st.warning("请先输入简历内容")
                return

            with st.spinner("正在优化简历...这可能需要几秒钟"):
                optimization_result = optimize_resume(resume_text, options)
                st.session_state.optimization_results = optimization_result

    # 显示诊断结果
    if 'diagnosis_result' in st.session_state:
        st.markdown("---")
        st.header("📋 诊断报告")

        diagnosis = st.session_state.diagnosis_result

        # 总体评分
        score_col1, score_col2 = st.columns([1, 3])
        with score_col1:
            st.metric("总体评分", f"{diagnosis['overall_score']}/100")
        with score_col2:
            # 进度条颜色根据分数变化
            color = "red" if diagnosis['overall_score'] < 60 else "orange" if diagnosis[
                                                                                  'overall_score'] < 80 else "green"
            st.progress(diagnosis['overall_score'] / 100)

        # 问题列表
        if diagnosis['issues']:
            st.subheader("发现问题:")
            for i, issue in enumerate(diagnosis['issues'], 1):
                severity_color = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(issue['severity'], "⚪")

                with st.expander(f"{severity_color} [{issue['category']}] {issue['description']}"):
                    st.write(f"**严重程度:** {issue['severity'].upper()}")
                    st.write(f"**问题描述:** {issue['description']}")

        # 显示优化结果
        if st.session_state.optimization_results:
            st.markdown("---")
            st.header("🎯 优化结果")

            tab1, tab2 = st.tabs(["📝 优化后简历", "💡 修改建议"])

            with tab1:
                st.subheader("优化后的简历内容")
                # 修复：为text_area提供非空标签
                st.text_area("优化后的简历内容：",
                             value=st.session_state.optimization_results["optimized_resume"],
                             height=450,
                             key="optimized_resume_display",
                             label_visibility="visible")

                # 下载按钮
                st.download_button(
                    label="📥 下载优化后简历",
                    data=st.session_state.optimization_results["optimized_resume"],
                    file_name="optimized_resume.txt",
                    mime="text/plain"
                )

            with tab2:
                st.subheader("详细修改建议")
                suggestions = st.session_state.optimization_results["suggestions"]

                if suggestions:
                    for i, suggestion in enumerate(suggestions, 1):
                        with st.expander(f"{i}. {suggestion['type']}"):
                            st.markdown("&zwnj;**原文:**&zwnj;")
                            st.info(suggestion['original'])
                            st.markdown("&zwnj;**修改后:**&zwnj;")
                            st.success(suggestion['improved'])
                            st.markdown("&zwnj;**修改理由:**&zwnj;")
                            st.write(suggestion['reason'])
                else:
                    st.info("暂无具体修改建议")


if __name__ == "__main__":
    main()
