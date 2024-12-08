import sys
import os
from dataclasses import asdict
__chat_pandas_path = (
    "/".join(
        os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[:-2]
    )
)
sys.path.append(__chat_pandas_path)

import streamlit as st

from ChatPandas.config import *

# 定义模型选项
MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "Custom"]

# 模拟用户登录
def login(username, password):
    return username == "admin" and password == "123456"

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# 左侧登录栏
# 左侧登录栏
if "logged_in" not in st.session_state:
    st.sidebar.title("登录")
    username = st.sidebar.text_input("用户名")
    password = st.sidebar.text_input("密码", type="password")
    if st.sidebar.button("登录"):
        if login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.sidebar.success("登录成功！")
        else:
            st.session_state["logged_in"] = False
            st.sidebar.error("用户名或密码错误！")
else:
    if st.sidebar.button("登出"):
        logout()


# 判断登录状态
if st.session_state.get("logged_in", False):
    # 初始化 session_state 中的 config
    if 'config' not in st.session_state:
        st.session_state['config'] = {
            "openai_config": asdict(OpenaiConfig(api_key="", model="gpt-3.5-turbo", base_url="https://api.openai.com/v1", max_retrys=5)),
            
            "prompt_config": asdict(PromptConfig()),
            "use_key": False
        }
    st.title("配置设置")
    
    st.header("OpenAI Config")
    # 读取 OpenAI 配置
    api_key = st.text_input(
        "API Key",
        value=st.session_state['config']['openai_config']['api_key'],
        type="password",
        help="Your OpenAI API key"
    )
    model = st.selectbox(
        "Model",
        options=MODEL_OPTIONS,
        index=MODEL_OPTIONS.index(st.session_state['config']['openai_config']['model'])
        if st.session_state['config']['openai_config']['model'] in MODEL_OPTIONS
        else MODEL_OPTIONS.index("Custom"),
        help="Select a model or choose 'Custom' to enter your own."
    )
    # 如果选择 Custom，允许用户输入自定义模型
    if model == "Custom":
        model = st.text_input(
            "Custom Model",
            value=st.session_state['config']['openai_config']['model'],
            help="Enter your custom model name"
        )
    
    base_url = st.text_input(
        "Base URL",
        value=st.session_state['config']['openai_config']['base_url'],
        help="The base URL for OpenAI API requests"
    )
    max_retrys = st.number_input(
        "Max Retries",
        min_value=1,
        max_value=10,
        value=st.session_state['config']['openai_config']['max_retrys'],
        step=1,
        help="Maximum number of retry attempts for API requests"
    )
    
    st.header("Use Key")
    use_key = st.checkbox(
        "Use Key",
        value=st.session_state['config']['use_key'],
        help="If to use your own key or use our test codes"
    )
    
    st.header("Prompt Config")
    # 读取 Prompt 配置
    use_rationale = st.checkbox(
        "Use Rationale",
        value=st.session_state['config']['prompt_config']['use_rationale'],
        help="Enable or disable rationale usage in prompts"
    )
    need_df_header = st.checkbox(
        "Need DataFrame Header",
        value=st.session_state['config']['prompt_config']['need_df_header'],
        help="Include DataFrame headers in prompt generation"
    )
    
    # 更新 session_state 中的 config
    st.session_state['config']['openai_config'] = asdict(OpenaiConfig(
        api_key=api_key,
        model=model,
        base_url=base_url,
        max_retrys=max_retrys
    ))
    st.session_state['config']['prompt_config'] = asdict(PromptConfig(
        use_rationale=use_rationale,
        need_df_header=need_df_header
    ))
    st.session_state["config"]["use_key"] = use_key

    # 显示配置数据
    st.subheader("Current Configuration")
    st.write("**OpenAI Config:**")
    st.json(st.session_state['config']['openai_config'])
    st.write(f"**Use key: {st.session_state['config']['use_key']}**")
    st.write("**Prompt Config:**")
    st.json(st.session_state['config']['prompt_config'])

    # 保存功能
    if st.button("Save Configuration"):
        st.success("Configuration saved to session state!")

else:
    st.warning("请先在左侧栏登录以访问此页面！")


