import sys
import os
from copy import deepcopy
from io import StringIO

import streamlit as st
import pandas as pd

__chat_pandas_path = (
    "/".join(
        os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[:-2]
    )
)
sys.path.append(__chat_pandas_path)

from ChatPandas.config import *
from ChatPandas.logger import configure_logger
from ChatPandas.cp import *
from ChatPandas.prompt import *


logger = configure_logger(__name__)


# 模拟用户登录
def login(username, password):
    return username == "admin" and password == "123456"

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

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


if st.session_state.get("logged_in", False):
    st.title("分析界面")

    st.markdown("### 上传 CSV 文件")
    # 处理文件上传
    uploaded_file = st.file_uploader("选择文件", type=["csv"], key="file_uploader")

    # 检查文件是否为新上传的文件
    if uploaded_file is not None:
        if "uploaded_filename" not in st.session_state or st.session_state["uploaded_filename"] != uploaded_file.name:
            # 记录新的文件名
            st.session_state["uploaded_filename"] = uploaded_file.name

            # 读取 CSV 文件并存储到指定路径
            df = pd.read_csv(uploaded_file)
            os.makedirs(f"./user_data/{st.session_state['username']}", exist_ok=True)
            df.to_csv(f"./user_data/{st.session_state['username']}/df.csv")

            # 初始化或重置存储的 DataFrame 历史记录
            st.session_state["df"] = [deepcopy(df)]
            # st.success("文件已上传并处理完成！")
        else:
            pass
            # st.info("文件已上传，无需重复处理。")

        # 用户输入与代码调整
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["adjust"] = False
            user_input = st.text_area("输入信息", height=150)
            _col1, _col2 = st.columns([0.03, 0.2])
            with _col1:
                if st.button("发送", key="send_button"):
                    # 初始化 ChatPandas
                    prompt_config = PromptConfig(**st.session_state["config"]["prompt_config"])
                    agent_config = OpenaiConfig(**st.session_state["config"]["openai_config"])
                    history_config = HistoryConfig(file_folder=f"./user_data/{st.session_state['username']}")
                    if 'cp' not in st.session_state:
                        cp = ChatPandas(agent_config=agent_config, history_config=history_config, prompt_config=prompt_config)
                        st.session_state["cp"] = cp
                    st.session_state["response"] = st.session_state["cp"].chat(user_input, st.session_state["df"][-1], st.session_state["config"]["use_key"])

                    # 解析代码
                    parsed_code = st.session_state["response"]["code"].strip("`")
                    parsed_code = parsed_code.lstrip("python").replace("\\n", "\n")
                    st.session_state["parsed_code"] = parsed_code
                    st.session_state["user_query"] = user_input

                # if st.button("调整代码", key="adjust_code"):
                #     st.session_state["adjust"] = True

            with _col2:
                if st.button("撤销", key="undo_button"):
                    if len(st.session_state["df"]) > 1:
                        st.session_state["df"].pop()
                        df = deepcopy(st.session_state["df"][-1])
                        st.session_state["cp"].history.pop_history()
                        if len(st.session_state["df"]) == 2:
                            st.warning("最多只能保留5步数据，再撤销一次将回到数据最初状态失去所有修改！")
                    else:
                        st.warning("无法撤销，数据已是最初状态！")

        with col2:
            st.markdown("API-response预览")
            if "user_query" in st.session_state:
                st.json(st.session_state["response"])

        # 调整代码与运行逻辑
        if "user_query" in st.session_state:
            code_col1, code_col2 = st.columns(2)
            with code_col1:
                if st.session_state["adjust"]:
                    st.session_state["__adjusted_code"] = st.text_area("调整代码", 
                                                                       value=st.session_state.get("__adjusted_code", 
                                                                                                  st.session_state["parsed_code"]), 
                                                                       height=150)
                else:
                    st.code(st.session_state["parsed_code"], language="python")
                    st.session_state["final_code"] = st.session_state["parsed_code"]

            with code_col2:
                confirm_button = False
                if st.session_state["adjust"]:
                    confirm_button = st.button("确认", key="confirm_adjust")
                    # if st.button("确定", key="confirm_button"):
                if st.button("运行代码", key="run_code_button"):
                    try:
                        df = deepcopy(st.session_state["df"][-1])
                        exec(st.session_state["final_code"])
                        st.session_state["cp"].history.add_history(st.session_state["final_code"])
                        st.session_state["df"].append(deepcopy(df))
                        if len(st.session_state["df"]) > 5:
                            del st.session_state["df"][1]
                        st.success("代码运行成功！")
                    except Exception as e:
                        st.error(f"代码运行失败：{str(e)}")
                if confirm_button:
                    print(st.session_state["__adjusted_code"])
                    st.session_state["final_code"] = st.session_state["__adjusted_code"]
                    st.session_state["adjust"] = False
                    print(st.session_state["final_code"])
                    st.info("代码已确认，请点击运行以执行代码。")

        # 显示表格
        st.markdown("### 数据表预览")
        if st.session_state["df"]:
            st.dataframe(st.session_state["df"][-1].head(10), width=800, height=400)
        else:
            st.warning("当前没有可显示的数据！")
            
        csv_buffer = StringIO()
        current_df = st.session_state["df"][-1]
        current_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="下载当前数据表为CSV文件",
            data=csv_data,
            file_name=f"{st.session_state['username']}_data.csv",
            mime="text/csv"
        )
        
else:
    st.warning("请先在左侧栏登录以访问此页面！")
