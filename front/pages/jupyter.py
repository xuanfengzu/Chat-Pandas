import streamlit as st
import subprocess
import os
import time

# 初始化服务器信息
if "jupyter_process" not in st.session_state:
    st.session_state["jupyter_process"] = None
if "jupyter_url" not in st.session_state:
    st.session_state["jupyter_url"] = None

# 用户输入动态设置
st.title("Dynamic Jupyter Notebook Server")
jupyter_port = st.number_input("Enter the port for Jupyter Notebook server:", value=8888, step=1)
# notebook_path = st.text_input("Enter the path to the .ipynb file:", value="./example.ipynb")
notebook_path = f"user_data/{st.session_state['username']}/default_notebook.ipynb"

# 启动 Jupyter Notebook 服务器
def start_jupyter_server(port):
    """
    启动 Jupyter Notebook 服务器并返回访问 URL。
    """
    command = [
        "jupyter", "notebook", "--no-browser", "--port", str(port), "--NotebookApp.token=''",
        "--NotebookApp.password=''", "--allow-root", "--ip=0.0.0.0", '--NotebookApp.allow_origin="*"', """--NotebookApp.tornado_settings=\"{'headers': {'Content-Security-Policy': ''}}\""""
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 等待服务器启动
    time.sleep(3)
    return process

# 停止 Jupyter Notebook 服务器
def stop_jupyter_server():
    if st.session_state["jupyter_process"]:
        st.session_state["jupyter_process"].terminate()
        st.session_state["jupyter_process"] = None
        st.session_state["jupyter_url"] = None

# 启动按钮
if st.button("Start Jupyter Server"):
    if st.session_state["jupyter_process"] is not None:
        st.warning("Jupyter server is already running.")
    else:
        # 启动服务器
        process = start_jupyter_server(jupyter_port)
        st.session_state["jupyter_process"] = process
        st.session_state["jupyter_url"] = f"https://127.0.0.1:{jupyter_port}/notebooks/{notebook_path}"
        st.success(f"Jupyter server started! URL: {st.session_state['jupyter_url']}")

# 停止按钮
if st.button("Stop Jupyter Server"):
    stop_jupyter_server()
    st.success("Jupyter server stopped.")

# 嵌入 Notebook 页面
if st.session_state["jupyter_url"]:
    st.markdown(
        f"""
        <iframe src="{st.session_state['jupyter_url']}" width="100%" height="800" sandbox="allow-scripts allow-same-origin allow-forms" frameborder="0"></iframe>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Jupyter server is not running. Please start the server.")

# 保存 Notebook 配置
if st.button("Save Notebook Path"):
    st.success(f"Notebook path saved: {notebook_path}")
